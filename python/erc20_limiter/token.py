# standard imports
import logging
import os
import enum

# external imports
from chainlib.eth.constant import ZERO_ADDRESS
from chainlib.eth.constant import ZERO_CONTENT
from chainlib.eth.contract import (
    ABIContractEncoder,
    ABIContractDecoder,
    ABIContractType,
    abi_decode_single,
)
from chainlib.eth.jsonrpc import to_blockheight_param
from chainlib.eth.error import RequestMismatchException
from chainlib.eth.tx import (
    TxFactory,
    TxFormat,
)
from chainlib.jsonrpc import JSONRPCRequest
from chainlib.block import BlockSpec
from hexathon import (
    add_0x,
    strip_0x,
)
from chainlib.eth.cli.encode import CLIEncoder

# local imports
from erc20_limiter.data import data_dir

logg = logging.getLogger()


class LimiterTokenRegistry(TxFactory):

    __abi = None
    __bytecode = None

    def constructor(self, sender_address, holder_address, limiter_address, tx_format=TxFormat.JSONRPC, version=None):
        code = self.cargs(holder_address, limiter_address, version=version)
        tx = self.template(sender_address, None, use_nonce=True)
        tx = self.set_code(tx, code)
        return self.finalize(tx, tx_format)


    @staticmethod
    def cargs(holder_address, limiter_address, version=None):
        code = LimiterTokenRegistry.bytecode(version=version)
        enc = ABIContractEncoder()
        enc.address(holder_address)
        enc.address(limiter_address)
        args = enc.get()
        code += args
        logg.debug('constructor code: ' + args)
        return code


    @staticmethod
    def gas(code=None):
        return 4000000


    @staticmethod
    def abi():
        if LimiterTokenRegistry.__abi == None:
            f = open(os.path.join(data_dir, 'LimiterTokenRegistry.json'), 'r')
            LimiterTokenRegistry.__abi = json.load(f)
            f.close()
        return LimiterTokenRegistry.__abi


    @staticmethod
    def bytecode(version=None):
        if LimiterTokenRegistry.__bytecode == None:
            f = open(os.path.join(data_dir, 'LimiterTokenRegistry.bin'))
            LimiterTokenRegistry.__bytecode = f.read()
            f.close()
        return LimiterTokenRegistry.__bytecode


    def have(self, contract_address, token_address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('have')
        enc.typ(ABIContractType.ADDRESS)
        enc.address(token_address)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o['params'].append('latest')
        o = j.finalize(o)
        return o
