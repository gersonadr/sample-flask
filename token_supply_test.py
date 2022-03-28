import unittest
import token_supply

class TestToken(unittest.TestCase):
    def test_token(self):

        token_address = "0x7EC1EdCB89343A8DF4329Ad94C174458225105aE"

        result = token_supply.get_max_supply(56, token_address)

        self.assertIsNotNone(result)
        self.assertEqual(result, 100000000000000000000000)

    def test_token_wrong_address(self):

        token_address = "0x9991EdCB89343A8DF4329Ad94C174458225105aE"

        result = token_supply.get_max_supply(56, token_address)

        self.assertIsNotNone(result)
        self.assertTrue('type' in result and result['type'] == 'error')

    def test_token_wrong_chain(self):

        token_address = "0x7EC1EdCB89343A8DF4329Ad94C174458225105aE"

        result = token_supply.get_max_supply(1, token_address)

        self.assertIsNotNone(result)
        self.assertTrue('type' in result and result['type'] == 'error')