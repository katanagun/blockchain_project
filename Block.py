import hashlib

class Block:
    def __init__(self, index, timestamp, data, previous_hash=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = 0

    def calculate_hash(self):
        return hashlib.sha256(f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode()).hexdigest()