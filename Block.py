import hashlib

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash=None, difficulty=2):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.mine_block()

    def serialize(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "transactions": [self._tx_to_dict(tx) for tx in self.transactions]
        }

    @classmethod
    def deserialize(cls, data):
        transactions = [cls._tx_from_dict(tx_data) for tx_data in data.get("transactions", [])]
        return cls(
            index=data["index"],
            timestamp=data["timestamp"],
            transactions=transactions,
            nonce=data["nonce"],
            previous_hash=data["previous_hash"],
            hash=data["hash"]
        )

    def calculate_hash(self):
        tx_str = "".join(str(tx) for tx in self.transactions)
        data = f"{self.index}{self.timestamp}{tx_str}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()

    def mine_block(self):
        prefix = "0" * self.difficulty
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith(prefix):
                return self.hash
            self.nonce += 1

    @staticmethod
    def _tx_to_dict(tx):
        return {
            "from_address": tx.from_address,
            "to": tx.to,
            "nonce": tx.nonce,
            "gas_price": tx.gas_price,
            "gas_limit": tx.gas_limit,
            "value": tx.value,
            "data": tx.data,
            "v": tx.v,
            "r": tx.r,
            "s": tx.s,
            "tx_hash": tx.tx_hash
        }

    @staticmethod
    def _tx_from_dict(tx_data):
        from LegacyTransaction import LegacyTransaction
        tx = LegacyTransaction(
            from_address=tx_data["from_address"],
            to=tx_data["to"],
            nonce=tx_data["nonce"],
            gas_price=tx_data["gas_price"],
            gas_limit=tx_data["gas_limit"],
            value=tx_data["value"],
            data=tx_data["data"],
            v=tx_data.get("v", 0),
            r=tx_data.get("r", 0),
            s=tx_data.get("s", 0)
        )
        tx.tx_hash = tx_data.get("tx_hash")
        return tx