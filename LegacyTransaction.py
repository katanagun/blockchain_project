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

    def __str__(self):
        return f"{self.from_address}->{self.to}: value={self.value}, nonce={hex(self.nonce)}"

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
