import unittest
import balance

class TestBalance(unittest.TestCase):
    def test_balance(self):

        result = balance.get_holder_balance(56, '0x7EC1EdCB89343A8DF4329Ad94C174458225105aE', '0x68E596b8122Ac6F4Ddc2C897CFf816C31E309eB3')

        self.assertIsNotNone(result)
        self.assertEqual(result['status'], "1")
        self.assertEqual(result['message'], "OK")
        self.assertGreater(int(result['result']), 0)

    def test_balance_negation(self):

        result = balance.get_holder_balance(1, '0x7EC1EdCB89343A8DF4329Ad94C174458225105aE', '0x68E596b8122Ac6F4Ddc2C897CFf816C31E309eB3')

        self.assertIsNotNone(result)
        self.assertEqual(result['status'], "1")
        self.assertEqual(result['message'], "OK")
        self.assertEqual(int(result['result']), 0)

    
    def test_balance_invalid_chain(self):

        result = balance.get_holder_balance(9999, '0x7EC1EdCB89343A8DF4329Ad94C174458225105aE', '0x68E596b8122Ac6F4Ddc2C897CFf816C31E309eB3')
        self.assertIsNotNone(result)
        self.assertTrue('type' in result and result['type'] == 'error')