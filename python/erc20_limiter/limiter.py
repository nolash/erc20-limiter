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


class Limiter(TxFactory):

    __abi = None
    __bytecode = None

    def constructor(self, sender_address, tx_format=TxFormat.JSONRPC, version=None):
        code = self.cargs(version=version)
        tx = self.template(sender_address, None, use_nonce=True)
        tx = self.set_code(tx, code)
        return self.finalize(tx, tx_format)


    @staticmethod
    def cargs(version=None):
        code = Limiter.bytecode(version=version)
        enc = ABIContractEncoder()
        args = enc.get()
        code += args
        logg.debug('constructor code: ' + args)
        return code


    @staticmethod
    def gas(code=None):
        return 4000000


    @staticmethod
    def abi():
        if Limiter.__abi == None:
            f = open(os.path.join(data_dir, 'Limiter.json'), 'r')
            Limiter.__abi = json.load(f)
            f.close()
        return Limiter.__abi


    @staticmethod
    def bytecode(version=None):
        if Limiter.__bytecode == None:
            f = open(os.path.join(data_dir, 'Limiter.bin'))
            Limiter.__bytecode = f.read()
            f.close()
        return Limiter.__bytecode


    def set_limit(self, contract_address, sender_address, token_address, limit, holder_address=None, tx_format=TxFormat.JSONRPC, id_generator=None):
        enc = ABIContractEncoder()
        if holder_address != None:
            enc.method('setLimitFor')
        enc.typ(ABIContractType.ADDRESS)
        if holder_address != None:
            enc.typ(ABIContractType.ADDRESS)
        enc.typ(ABIContractType.UINT256)
        enc.address(token_address)
        if holder_address != None:
            enc.address(holder_address)
        enc.uint256(limit)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format, id_generator=id_generator)
        return tx


    def limit_of(self, contract_address, token_address, holder_address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('limitOf')
        enc.typ(ABIContractType.ADDRESS)
        enc.typ(ABIContractType.ADDRESS)
        enc.address(token_address)
        enc.address(holder_address)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o['params'].append('latest')
        o = j.finalize(o)
        return o


