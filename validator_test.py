import unittest
import validator

class TestValidator(unittest.TestCase):

    def test_address_validation(self):
        result = validator.is_eth_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE')
        self.assertTrue(result)

    def test_address_validation_negative(self):
        result = validator.is_eth_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeeeeEEeE')
        self.assertFalse(result)

    def test_address_validation_blank(self):
        result = validator.is_eth_address('')
        self.assertFalse(result)

    def test_address_validation_None(self):
        result = validator.is_eth_address(None)
        self.assertFalse(result)
    
    def test_chain_valid(self):
        result = validator.is_chain_valid("56")
        self.assertTrue(result)
    
    def test_chain_doesnt_exist(self):
        result = validator.is_chain_valid("48")
        self.assertFalse(result)

    def test_chain_blank(self):
        result = validator.is_chain_valid("")
        self.assertFalse(result)
    
    def test_chain_none(self):
        result = validator.is_chain_valid(None)
        self.assertFalse(result)