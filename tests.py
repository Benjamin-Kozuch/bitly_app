import unittest
from app.bitly_api import create_avg_click_list

class AvgClicksCase(unittest.TestCase):

    def test_avg_clicks(self):
        countries = {
            "CA": [
                1,
                5
            ],
            "GB": [
                10
            ],
            "US": [
                4,
                8
            ]}
        expected_result = [
            {
            "average_clicks": 6,
            "value": "US"
            },
            {
            "average_clicks": 10,
            "value": "GB"
            },
            {
            "average_clicks": 3,
            "value": "CA"
            }
        ]
        print(create_avg_click_list(countries))
        print(expected_result)
        self.assertCountEqual(create_avg_click_list(countries), expected_result)

if __name__ == '__main__':
    unittest.main()