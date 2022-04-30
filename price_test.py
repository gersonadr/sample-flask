import unittest
import price

class TestPrice(unittest.TestCase):
    # def test_price(self):

    #     # Make sample call to BNB token
    #     result = price.get_price(56, '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', '0x7EC1EdCB89343A8DF4329Ad94C174458225105aE')

    #     self.assertIsNotNone(result)
    #     self.assertGreater(float(result), 0)

    def test_ETH_price(self):

        result = price.get_ETH_price()

        self.assertIsNotNone(result)
        self.assertGreater(float(result), 0)

    def test_BNB_price(self):

        result = price.get_BNB_price()

        self.assertIsNotNone(result)
        self.assertGreater(float(result), 0)