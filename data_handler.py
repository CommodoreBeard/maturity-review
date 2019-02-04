import csv
import copy

class DataHandler:

    def __init__(self, csv_path):
        self.parsed_csv = self.parse(csv_path)
        
    def process_data(self):
        parsed = self.remove_nulls(self.parsed_csv)
        parsed = self.gen_weighted_score(parsed)
        parsed = self.gen_max_weighted_score(parsed)
        parsed = self.gen_total_max_weighted_score_per_topic(parsed)
        parsed = self.gen_maturity(parsed)
        return self.gen_avg_maturity(parsed)

    def parse(self, path):
        with open(path) as f:
            return [{k: v for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]

    def remove_nulls(self, parsed_csv):
        transform = copy.deepcopy(parsed_csv)
        return list(filter(lambda row: row["Notes"].lower() != 'n/a', transform))

    def gen_weighted_score(self, parsed_csv):
        # Weighted Score = Score * Impact * (1+1/level)
        transform = copy.deepcopy(parsed_csv)
        for row in transform:
            if (row["Score"] == '' or row["Impact"] == '' or row["Level"] == ''):
                continue
            row["WeightedScore"] = int(row["Score"]) * int(row["Impact"]) * ( 1 + 1 / int(row["Level"]) )
        return transform

    def gen_max_weighted_score(self, parsed_csv):
        # Max Weighted Score = MaxLevel (2) * Impact * (1+1/Level)
        transform = copy.deepcopy(parsed_csv)
        for row in transform:
            if (row["Impact"] == '' or row["Level"] == ''):
                continue
            row["MaxWeightedScore"] = 2 * int(row["Impact"]) * ( 1 + 1 / int(row["Level"]) )
        return transform

    def get_unique(self, qualifier, rows):
        unique = []
        for row in rows:
            if row[qualifier] not in unique:
                unique.append(row[qualifier])
        return list(filter(lambda t: t != '', unique))

    def gen_total_max_weighted_score_per_topic(self, parsed_csv_with_max_weighted_score):
        # sum of max weighted score for each topic
        transform = copy.deepcopy(parsed_csv_with_max_weighted_score)
        unique_topics = self.get_unique("Topic", transform)

        for topic in unique_topics:
            topic_score = 0
            topic_rows = list(filter(lambda row: row["Topic"] == topic, transform))
            for t in topic_rows:
                topic_score += int(t.get("MaxWeightedScore"))
            for row in transform:
                if row["Topic"] == topic:
                    row["TotalMaxWeightedScoreForTopic"] = topic_score

        return transform

    def gen_maturity(self, parsed_csv_with_total_max):
        # maturity = weighted score /total max weighted score
        transform = copy.deepcopy(parsed_csv_with_total_max)
        for row in transform:
            if (not 'WeightedScore' in row or not 'TotalMaxWeightedScoreForTopic' in row):
                continue
            row["Maturity"] = int(row["WeightedScore"]) / int(row["TotalMaxWeightedScoreForTopic"])
        return transform

    def gen_avg_maturity(self, parsed_csv_with_maturity):
        # Avg Maturity = (Category Maturity Total/number of topics in category )*100"
        transform = copy.deepcopy(parsed_csv_with_maturity)

        unique_categories = self.get_unique("Category", transform)

        for category in unique_categories:
            total_maturity = 0
            category_rows = list(filter(lambda row: row["Category"] == category, transform))
            unique_topics = self.get_unique("Topic", category_rows)
            for row in category_rows:
                row["NumberOfTopicsInCategory"] = len(unique_topics)
                if ("Maturity" not in row):
                    continue
                total_maturity += float(row["Maturity"])
            for row in category_rows:
                    row["CategoryMaturityTotal"] = total_maturity

        for row in transform:
            if (not 'CategoryMaturityTotal' in row or not 'NumberOfTopicsInCategory' in row):
                continue
            row["AverageMaturity"] = (row["CategoryMaturityTotal"] / row["NumberOfTopicsInCategory"]) * 100
        
        return transform

    def format_for_chart(self, processed_csv):
        transform = copy.deepcopy(processed_csv)
        unique_categories = self.get_unique("Category", transform)
        populated_list = {}
        for category in unique_categories:
            category_rows = list(filter(lambda row: row["Category"] == category, transform))
            final_average_maturity = category_rows[0]["AverageMaturity"]
            # populated_list.append({category: final_average_maturity})
            populated_list[category] = final_average_maturity
        return [populated_list] 