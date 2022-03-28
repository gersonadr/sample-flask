import unittest
import holder

class TestHolder(unittest.TestCase):
    def test_holder(self):

        lp_address = "0xffaac354BF590257CdDfAF46049555c8f5457430"
        contract_address = "0x7ec1edcb89343a8df4329ad94c174458225105ae"

        result = holder.get_all_holders_from_block(56, lp_address, contract_address)

        self.assertIsNotNone(result)
        self.assertTrue('type' not in result)
        self.assertGreaterEqual(len(result), 3)
        for item in result:
            self.assertEqual(item['holder'], '0x68e596b8122ac6f4ddc2c897cff816c31e309eb3')
            self.assertEqual(item['contract_address'], contract_address)
            self.assertIsNotNone(item['txn_hash'])
            self.assertGreater(item['block'], 0)
            self.assertTrue(item['from'] == lp_address.lower() or item['to'] == lp_address.lower())
            self.assertTrue(item['from'] == '0x68e596b8122ac6f4ddc2c897cff816c31e309eb3' or item['to'] == '0x68e596b8122ac6f4ddc2c897cff816c31e309eb3')
            self.assertEqual(item['holder'], '0x68e596b8122ac6f4ddc2c897cff816c31e309eb3')

    def test_holder_non_existing_lp(self):

        lp_address = "0xffaac354BF590257AAAAAF46049555c8f5457430"
        contract_address = "0x7ec1edcb89343a8df4329ad94c174458225105ae"

        result = holder.get_all_holders_from_block(56, lp_address, contract_address)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)

    def test_holder_non_existing_token(self):

        lp_address = "0xffaac354BF590257CdDfAF46049555c8f5457430"
        contract_address = "0x7ec1edcb89343a8df4329ad94c17445822510aaa"

        result = holder.get_all_holders_from_block(56, lp_address, contract_address)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)

    def test_holder_invalid_params(self):

        lp_address = "0xffaac354BF590257CdDfAF46049555c8f545"
        contract_address = "0x7ec1edcb89343a8df4329ad94c1744582251"

        result = holder.get_all_holders_from_block(56, lp_address, contract_address)

        self.assertIsNotNone(result)
        self.assertTrue('type' in result and result['type'] == 'error')

    def test_holder_wrong_chain(self):

        lp_address = "0xffaac354BF590257AAAAAF46049555c8f5457430"
        contract_address = "0x7ec1edcb89343a8df4329ad94c174458225105ae"

        result = holder.get_all_holders_from_block(1, lp_address, contract_address)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)

    def test_holder_start_block_too_high(self):

        lp_address = "0xffaac354BF590257CdDfAF46049555c8f5457430"
        contract_address = "0x7ec1edcb89343a8df4329ad94c174458225105ae"

        result = holder.get_all_holders_from_block(56, lp_address, contract_address, 16000000)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)