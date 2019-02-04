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

    def remove_nulls(self, data):
        return list(filter(lambda row: row["Notes"].lower() != 'n/a', data))

    def get_unique(self, qualifier, rows):
        unique = []
        for row in rows:
            if row[qualifier] not in unique:
                unique.append(row[qualifier])
        return list(filter(lambda t: t != '', unique))

    def gen_weighted_score(self, parsed_csv):
        # Weighted Score = Score * Impact * (1+1/level)
        for row in parsed_csv:
            if (row["Score"] == '' or row["Impact"] == '' or row["Level"] == ''):
                continue
            row["WeightedScore"] = int(row["Score"]) * int(row["Impact"]) * ( 1 + 1 / int(row["Level"]) )
        return parsed_csv

    def gen_max_weighted_score(self, parsed_csv):
        # Max Weighted Score = MaxLevel (2) * Impact * (1+1/Level)
        for row in parsed_csv:
            if (row["Impact"] == '' or row["Level"] == ''):
                continue
            row["MaxWeightedScore"] = 2 * int(row["Impact"]) * ( 1 + 1 / int(row["Level"]) )
        return parsed_csv

    def gen_total_max_weighted_score_per_topic(self, data):
        # sum of max weighted score for each topic
        unique_topics = self.get_unique("Topic", data)

        for topic in unique_topics:
            topic_rows = list(filter(lambda row: row["Topic"] == topic, data))
            topic_score = sum(int(row["MaxWeightedScore"]) for row in topic_rows)
            for row in data:
                if row["Topic"] == topic:
                    row["TotalMaxWeightedScoreForTopic"] = topic_score
        return data

    def gen_maturity(self, data):
        # maturity = weighted score /total max weighted score
        for row in data:
            if (not 'WeightedScore' in row or not 'TotalMaxWeightedScoreForTopic' in row):
                continue
            row["Maturity"] = int(row["WeightedScore"]) / int(row["TotalMaxWeightedScoreForTopic"])
        return data

    def gen_avg_maturity(self, data):
        # Avg Maturity = (Category Maturity Total/number of topics in category )*100"
        unique_categories = self.get_unique("Category", data)

        for category in unique_categories:

            category_rows = list(filter(lambda row: row["Category"] == category and row.get("Maturity") != None, data))
            unique_topics = self.get_unique("Topic", category_rows)
            total_maturity = sum(float(row.get("Maturity")) for row in category_rows)
        
            for row in data:
                if row["Category"] == category:
                    row["NumberOfTopicsInCategory"] = len(unique_topics)
                    row["CategoryMaturityTotal"] = total_maturity

        for row in data:
            if not 'CategoryMaturityTotal' in row or not 'NumberOfTopicsInCategory' in row:
                continue
            row["AverageMaturity"] = (row["CategoryMaturityTotal"] / row["NumberOfTopicsInCategory"]) * 100
        return data

    def format_for_chart(self, data):
        unique_categories = self.get_unique("Category", data)
        populated_list = {}
        for category in unique_categories:
            category_rows = list(filter(lambda row: row["Category"] == category, data))
            final_average_maturity = category_rows[0]["AverageMaturity"]
            populated_list[category] = final_average_maturity
        return [populated_list] 