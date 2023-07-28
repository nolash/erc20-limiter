# standard imports
import unittest
import logging

# external imports
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt

# local imports
from erc20_limiter import Limiter
from erc20_limiter.token import LimiterTokenRegistry
from erc20_limiter.unittest import TestLimiterTokenRegistry

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestLimiterBase(TestLimiterTokenRegistry):

    def setUp(self):
        super(TestLimiterBase, self).setUp()
        self.publish_limiter()
        self.token_registry = self.publish_token_registry(self.accounts[0], self.address)
        logg.debug('tokenreg {}'.format(self.token_registry))


    def test_limit(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], conn=self.conn)

        foo_token = '2c26b46b68ffc68ff99b453c1d30413413422d70'
        c = LimiterTokenRegistry(self.chain_spec)
        o = c.have(self.token_registry, foo_token, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(int(r, 16), 0)

        c = Limiter(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.set_limit(self.address, self.accounts[0], foo_token, 42)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        c = LimiterTokenRegistry(self.chain_spec)
        o = c.have(self.token_registry, foo_token, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(int(r, 16), 1)


if __name__ == '__main__':
    unittest.main()

