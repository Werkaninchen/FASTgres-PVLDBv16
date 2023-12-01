import unittest

from speedup import getSpeedupFactor


class TestSpeedup(unittest.TestCase):

    def test_speedup_positive(self):
        base = {
            "21.sql": 8192,
            "9.sql": 100,
            "22.sql": 16383,
            "18.sql": 8192,
            "4.sql": 16383,
            "6.sql": 512,
            "2.sql": 16383,
            "15.sql": 16383,
            "17.sql": 16383,
            "16.sql": 16383,
            "12.sql": 16383,
            "11.sql": None
        }
        query = "21.sql"
        val = 10.717789888381958
        expected_result = 764.3366855773219
        self.assertEqual(getSpeedupFactor(base, query, val), expected_result)
        query = "22.sql"
        val = 15
        expected_result = 1092.2
        self.assertEqual(getSpeedupFactor(base, query, val), expected_result)
        query = "9.sql"
        val = 25
        expected_result = 4
        self.assertEqual(getSpeedupFactor(base, query, val), expected_result)


if __name__ == '__main__':
    unittest.main()
