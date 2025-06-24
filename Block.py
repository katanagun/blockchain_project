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