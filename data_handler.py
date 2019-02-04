""" Really messy module for manipulating the data from airtable. """

import csv

def parse(path):
    """ returns a list of dictionaries """
    with open(path) as file:
        return [{k: v for k, v in row.items()}
                for row in csv.DictReader(file, skipinitialspace=True)]

def remove_nulls(data):
    """ abstracted way to remove incomplete rows, not perfect """
    return list(filter(lambda row: row["Notes"].lower() != 'n/a', data))

def get_unique(qualifier, rows):
    """ returns a list of unique items """
    unique = []
    for row in rows:
        if row[qualifier] not in unique:
            unique.append(row[qualifier])
    return list(filter(lambda t: t != '', unique))

def gen_weighted_score(data):
    """ Weighted Score = Score * Impact * (1+1/level) """
    for row in data:
        if (row["Score"] == '' or row["Impact"] == '' or row["Level"] == ''):
            continue
        row["WeightedScore"] = int(row["Score"]) * int(row["Impact"]) \
                * (1 + 1 / int(row["Level"]))
    return data

def gen_max_weighted_score(data):
    """ Max Weighted Score = MaxLevel (2) * Impact * (1+1/Level) """
    for row in data:
        if (row["Impact"] == '' or row["Level"] == ''):
            continue
        row["MaxWeightedScore"] = 2 * int(row["Impact"]) * (1 + 1 / int(row["Level"]))
    return data

def gen_total_max_weighted_score_per_topic(data):
    """ sum of max weighted score for each topic """
    unique_topics = get_unique("Topic", data)

    for topic in unique_topics:
        # pylint: disable=cell-var-from-loop
        topic_rows = list(filter(lambda row: row["Topic"] == topic, data))
        topic_score = sum(int(row["MaxWeightedScore"]) for row in topic_rows)
        for row in data:
            if row["Topic"] == topic:
                row["TotalMaxWeightedScoreForTopic"] = topic_score
    return data

def gen_maturity(data):
    """ maturity = weighted score /total max weighted score """
    for row in data:
        if (not 'WeightedScore' in row or not 'TotalMaxWeightedScoreForTopic' in row):
            continue
        row["Maturity"] = int(row["WeightedScore"]) / int(row["TotalMaxWeightedScoreForTopic"])
    return data

def gen_avg_maturity(data):
    """ Avg Maturity = (Category Maturity Total/number of topics in category )*100 """
    unique_categories = get_unique("Category", data)

    for category in unique_categories:

        # pylint: disable=cell-var-from-loop
        category_rows = list(filter(
            lambda row: row["Category"] == category and row.get("Maturity") is not None, data))
        unique_topics = get_unique("Topic", category_rows)
        total_maturity = sum(float(row.get("Maturity")) for row in category_rows)

        for row in data:
            if row["Category"] == category:
                row["NumberOfTopicsInCategory"] = len(unique_topics)
                row["CategoryMaturityTotal"] = total_maturity

    for row in data:
        if not 'CategoryMaturityTotal' in row or not 'NumberOfTopicsInCategory' in row:
            continue
        row["AverageMaturity"] = (row["CategoryMaturityTotal"] \
            / row["NumberOfTopicsInCategory"]) * 100
    return data

def format_for_chart(data):
    """ build a dict with the first average maturity for every catagory """
    unique_categories = get_unique("Category", data)
    populated_list = {}
    for category in unique_categories:
        # pylint: disable=cell-var-from-loop
        category_rows = list(filter(lambda row: row["Category"] == category, data))
        final_average_maturity = category_rows[0]["AverageMaturity"]
        populated_list[category] = final_average_maturity
    return [populated_list]

# pylint: disable=too-few-public-methods
class DataHandler:
    """ Simple class for generating data """

    def __init__(self, csv_path):
        self.parsed_csv = parse(csv_path)

    def process_data(self):
        """ This is bad boy that does all the work """
        parsed = remove_nulls(self.parsed_csv)
        parsed = gen_weighted_score(parsed)
        parsed = gen_max_weighted_score(parsed)
        parsed = gen_total_max_weighted_score_per_topic(parsed)
        parsed = gen_maturity(parsed)
        return gen_avg_maturity(parsed)
