class LegacyTransaction:
    def __init__(self, from_address, to, nonce, gas_price, gas_limit, value, data, v=None, r=None, s=None):
        self.from_address = from_address
        self.to = to
        self.nonce = int(nonce, 16)
        self.gas_price = int(gas_price, 16)
        self.gas_limit = int(gas_limit, 16)
        self.value = int(value, 16)
        self.data = data
        self.v = v
        self.r = r
        self.s = s

    def __str__(self):
        return f"{self.from_address}->{self.to}: value={self.value}, nonce={hex(self.nonce)}"
