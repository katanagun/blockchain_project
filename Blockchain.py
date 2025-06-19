from Block import Block
import time

class Blockchain:
    def __init__(self):
        self.chain = []

    def add_genesis_block(self):
        block = Block(0, time.time(), "Genesis block")
        block.hash = block.calculate_hash()
        self.chain.append(block)

    def add_block(self, block):
        block.previous_hash = self.chain[-1].hash
        block.hash = block.calculate_hash()
        self.chain.append(block)
