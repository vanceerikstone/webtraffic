from webtraffic import UserPageTimeAggregator
import os
import unittest


class AggregatorTestCase(unittest.TestCase):

    def test_add_csv(self):
        agg = UserPageTimeAggregator()
        dir = os.path.dirname(__file__)
        with open(os.path.join(dir, "sample_data.csv")) as f:
            agg.add_csv(f)

        self.assertEqual(agg.data["378"]["/"], 16)

    def test_dump_csv(self):
        agg = UserPageTimeAggregator()
        dir = os.path.dirname(__file__)
        with open(os.path.join(dir, "sample_data.csv")) as f:
            agg.add_csv(f)

        csv = agg.dump_csv().split()
        self.assertEqual(len(csv), 7)
        header = csv[0]
        self.assertIn("/signup", header)
        self.assertIn("user_id", header)


if __name__ == "__main__":
    unittest.main()
