# standard imports
import unittest
import logging

# external imports
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt

# local imports
from erc20_limiter import Limiter
from erc20_limiter.unittest import TestLimiter

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestLimiterBase(TestLimiter):

    def test_limit(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], conn=self.conn)
        c = Limiter(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.set_limit(self.address, self.accounts[0], '2c26b46b68ffc68ff99b453c1d30413413422d70', 256)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)


if __name__ == '__main__':
    unittest.main()
