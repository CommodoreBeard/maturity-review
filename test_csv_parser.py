import unittest
from csv_parser import parse, remove_nulls, gen_weighted_score, gen_max_weighted_score, gen_total_max_weighted_score_per_topic, gen_maturity, gen_avg_maturity, format_for_chart
from write_csv import write

class CsvParseSpec(unittest.TestCase):

    wellformatted_csv_path = "test/fixtures/RawSheet.csv"

    def test_wellformatted(self):
        actual = parse(self.wellformatted_csv_path)
        self.assertEqual(99, len(actual))

    def test_remove_nulls(self):
        parsed = parse(self.wellformatted_csv_path)
        actual = remove_nulls(parsed)
        self.assertEqual(len(actual), 92)

    def test_gen_weighted_score(self):
        parsed = parse(self.wellformatted_csv_path)
        parsed = remove_nulls(parsed)
        actual = gen_weighted_score(parsed)
        self.assertEqual(actual[0]["WeightedScore"], 12)
        self.assertEqual(actual[40]["WeightedScore"], 4)
        self.assertEqual(actual[48]["WeightedScore"], 4)

    def test_gen_weighted_score(self):
        parsed = parse(self.wellformatted_csv_path)
        parsed = remove_nulls(parsed)
        actual = gen_max_weighted_score(parsed)
        self.assertEqual(actual[0]["MaxWeightedScore"], 12)
        self.assertEqual(actual[40]["MaxWeightedScore"], 8)
        self.assertEqual(actual[48]["MaxWeightedScore"], 4)
    
    def test_gen_total_max_weighted_score_per_topic(self):
        parsed = parse(self.wellformatted_csv_path)
        parsed = remove_nulls(parsed)
        parsed = gen_max_weighted_score(parsed)
        actual = gen_total_max_weighted_score_per_topic(parsed)
        self.assertEqual(actual[0]["TotalMaxWeightedScoreForTopic"], 48)
        self.assertEqual(actual[40]["TotalMaxWeightedScoreForTopic"], 8)
        self.assertEqual(actual[48]["TotalMaxWeightedScoreForTopic"], 4)
    
    def test_gen_maturity(self):
        parsed = parse(self.wellformatted_csv_path)
        parsed = remove_nulls(parsed)
        parsed = gen_weighted_score(parsed)
        parsed = gen_max_weighted_score(parsed)
        parsed = gen_total_max_weighted_score_per_topic(parsed)
        actual = gen_maturity(parsed)
        self.assertEqual(actual[0]["Maturity"], 0.25)
        self.assertEqual(actual[40]["Maturity"], 0.5)
        self.assertEqual(actual[48]["Maturity"], 1)

    def test_gen_avg_maturity(self):
        parsed = parse(self.wellformatted_csv_path)
        parsed = remove_nulls(parsed)
        parsed = gen_weighted_score(parsed)
        parsed = gen_max_weighted_score(parsed)
        parsed = gen_total_max_weighted_score_per_topic(parsed)
        parsed = gen_maturity(parsed)
        actual = gen_avg_maturity(parsed)
        self.assertEqual(actual[0]["AverageMaturity"], 100)
        self.assertEqual(actual[40]["AverageMaturity"], 80.86834733893559)
        self.assertEqual(actual[48]["AverageMaturity"], 83.33333333333333)

    def test_gen_avg_maturity(self):
        parsed = parse(self.wellformatted_csv_path)
        parsed = remove_nulls(parsed)
        parsed = gen_weighted_score(parsed)
        parsed = gen_max_weighted_score(parsed)
        parsed = gen_total_max_weighted_score_per_topic(parsed)
        parsed = gen_maturity(parsed)
        actual = gen_avg_maturity(parsed)
        self.assertEqual(actual[0]["AverageMaturity"], 100)
        self.assertEqual(actual[40]["AverageMaturity"], 80.86834733893559)
        self.assertEqual(actual[48]["AverageMaturity"], 83.33333333333333)

    def test_final(self):
        parsed = parse(self.wellformatted_csv_path)
        parsed = remove_nulls(parsed)
        parsed = gen_weighted_score(parsed)
        parsed = gen_max_weighted_score(parsed)
        parsed = gen_total_max_weighted_score_per_topic(parsed)
        parsed = gen_maturity(parsed)
        parsed = gen_avg_maturity(parsed)
        actual = format_for_chart(parsed)
        write(actual, "output.csv")
        self.assertEqual(actual[0]["AverageMaturity"], 100)
        self.assertEqual(actual[40]["AverageMaturity"], 80.86834733893559)
        self.assertEqual(actual[48]["AverageMaturity"], 83.33333333333333)

if __name__ == '__main__':
    unittest.main()