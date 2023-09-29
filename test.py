import unittest
from server import app

class Test(unittest.TestCase):
    """
    Unit testing class using Python unittest module
    """
    def setUp(self):
        # Configure the app for testing
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_add(self):
        # Test /add endpoint with 5 requests
        add_transactions = [
            {"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"},
            {"payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z"},
            {"payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z"},
            {"payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z"},
            {"payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z"}
        ]
        for transaction_data in add_transactions:
            print(f"Sending /add POST request: {transaction_data}")
            response = self.client.post("/add", json=transaction_data)
            self.assertEqual(response.status_code, 200)


    def test_spend(self):
        # Test /spend endpoint with 5000 points in a single request
        print(f"Sending /spend POST request: {{'points':5000}}")
        response = self.client.post("/spend", json={"points":5000})
        self.assertEqual(response.status_code, 200)
        expected_data = [
            { "payer": "DANNON", "points": -100 },
            { "payer": "UNILEVER", "points": -200 },
            { "payer": "MILLER COORS", "points": -4700}
        ]
        for data in expected_data:
            self.assertIn(data, response.get_json())

    def test_balance(self):
        # Test /balance endpoint with a single request
        print("Sending /balance GET request")
        response = self.client.get("/balance")
        self.assertEqual(response.status_code, 200)
        expected_data = {
            "DANNON": 1000,
            "UNILEVER" : 0,
            "MILLER COORS": 5300
        }
        for data in expected_data:
            self.assertIn(data, response.get_json())

if __name__ == '__main__':
    unittest.main()
