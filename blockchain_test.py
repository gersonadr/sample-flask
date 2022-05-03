import unittest
import blockchain

class TestBlockchain(unittest.TestCase):
    def test_swap_binance_testnet(self):

        address1 = "0x71E0C6DD765b990C8F53DaF753AB36064C481670"
        address2 = "0xC94B3ba0dD04726CF294CdC5f7BE973742eF989C"

        result = blockchain.get_swap(97, address1, address2)

        self.assertIsNotNone(result)
        self.assertGreater(result, 0);

    def test_swap_binance_testnet2(self):

        address2 = "0x1651d5a7d1C02b890ba203EBBCb15498511A0604"
        address1 = "0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd"

        result = blockchain.get_swap(97, address1, address2)

        self.assertIsNotNone(result)
        self.assertGreater(result, 0);