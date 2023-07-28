# standard imports
import logging
import time

# external imports
from chainlib.eth.unittest.ethtester import EthTesterCase
from chainlib.connection import RPCConnection
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt
from chainlib.eth.address import to_checksum_address
from chainlib.eth.block import block_latest

# local imports
from erc20_limiter import Limiter
from erc20_limiter.token import LimiterTokenRegistry

logg = logging.getLogger(__name__)

class TestLimiter(EthTesterCase):

    def setUp(self):
        super(TestLimiter, self).setUp()
        self.conn = RPCConnection.connect(self.chain_spec, 'default')
        self.address = self.publish_limiter()


    def publish_limiter(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], conn=self.conn)
        c = Limiter(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.constructor(self.accounts[0])
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)
        address = to_checksum_address(r['contract_address'])
        logg.debug('published limiter on address {} with hash {}'.format(address, tx_hash))
        return address


class TestLimiterTokenRegistry(TestLimiter):

    def publish_token_registry(self, holder_address, limiter_address):
        nonce_oracle = RPCNonceOracle(self.accounts[0], conn=self.conn)
        c = LimiterTokenRegistry(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.constructor(self.accounts[0], holder_address, limiter_address)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)
        address = to_checksum_address(r['contract_address'])
        logg.debug('published limiter token registry proxy on address {} with hash {}'.format(address, tx_hash))
        return address
