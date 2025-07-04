from web3 import Web3
import rlp
from eth_account._utils.legacy_transactions import Transaction as EthLegacyTransaction

class LegacyTransaction:
    def __init__(self, from_address, to, nonce, gas_price, gas_limit, value, data, v, r, s):
        self.from_address = from_address
        self.to = self._normalize_address(to)
        self.nonce = self._hex_to_int(nonce)
        self.gas_price = self._hex_to_int(gas_price)
        self.gas_limit = self._hex_to_int(gas_limit)
        self.value = self._hex_to_int(value)
        self.data = data
        self.v = self._hex_to_int(v)
        self.r = self._hex_to_int(r)
        self.s = self._hex_to_int(s)

        self.tx_hash = None

    def set_hash(self):
        # Создаём RLP-транзакцию в формате legacy
        rlp_tx = EthLegacyTransaction(
            nonce=self.nonce,
            gasPrice=self.gas_price,
            gas=self.gas_limit,
            to=bytes.fromhex(self.to[2:]) if self.to and self.to != "0x0000000000000000000000000000000000000000" else b"",
            value=self.value,
            data=bytes.fromhex(self.data[2:]) if self.data.startswith("0x") else self.data,
            v=self.v,
            r=self.r,
            s=self.s
        )
        self.tx_hash = Web3.keccak(rlp.encode(rlp_tx)).hex()

    def __str__(self):
        return self.tx_hash if self.tx_hash else f"{self.from_address}->{self.to}: value={self.value}, nonce={hex(self.nonce)}"

    def __repr__(self):
        return f"<LegacyTransaction from={self.from_address} to={self.to} value={self.value} nonce={self.nonce} hash={self.tx_hash}>"

    @staticmethod
    def _hex_to_int(val):
        if isinstance(val, int):
            return val
        if isinstance(val, str):
            return int(val, 16) if val.startswith("0x") else int(val)
        return 0

    @staticmethod
    def _normalize_address(addr):
        if isinstance(addr, str) and not addr.startswith("0x"):
            return "0x" + addr.lower()
        return addr.lower() if isinstance(addr, str) else None
