import unittest
import utils

class TestMyUtils(unittest.TestCase):
    def test_get_explorer_endpoint(self):
        result = utils.get_explorer_endpoint(56)
        self.assertEqual(result, "https://api.bscscan.com/api")

    def test_explorer_endpoint_string(self):
        result = utils.get_explorer_endpoint("56")
        self.assertEqual(result, "https://api.bscscan.com/api")

    def test_get_mainnet_key(self):
        result = utils.get_random_key(1)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 34)

    def test_get_testnet_key(self):
        result = utils.get_random_key(4)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 34)

    def test_get_mainnet_key_negative(self):
        result = utils.get_random_key(999999)
        self.assertTrue('type' in result and result['type'] == 'error')