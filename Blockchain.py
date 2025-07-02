from Block import Block
from LegacyTransaction import LegacyTransaction
import time

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.balances = {}
        self.nonces = {}
        self.add_genesis_block()

    def add_genesis_block(self):
        genesis_transaction = LegacyTransaction("genesis", "0x53f71e9815eebb203a35e07c2c5933a853dcad55", "0x0", "0x0", "0x0", hex(10**18), "0x0")
        block = Block(0, time.time(), [genesis_transaction], difficulty=self.difficulty)
        block.hash = block.calculate_hash()
        self.apply_transactions([genesis_transaction])
        self.chain.append(block)

    def add_block(self, transactions):
        index = len(self.chain)
        previous_hash = self.chain[-1].hash

        block = Block(index, time.time(), transactions, previous_hash, self.difficulty)

        if self.validate_transactions(transactions):
            self.chain.append(block)
        else:
            print("Transactions failed verification.")

    def validate_transactions(self, transactions):
        for tx in transactions:
            expected_nonce = self.nonces.get(tx.from_address, 0)
            required_balance = tx.value + tx.gas_price * tx.gas_limit
            if self.balances.get(tx.from_address, 0) < required_balance:
                print(f"{tx.from_address} does not have enough funds")
                return False
            if tx.nonce != expected_nonce:
                print(f"Invalid nonce for {tx.from_address}: expected {expected_nonce}, received {tx.nonce}")
                return False
            self.apply_transactions([tx])
        return True

    def apply_transactions(self, transactions):
        for tx in transactions:
            fee = tx.gas_price * tx.gas_limit
            self.balances[tx.from_address] = self.balances.get(tx.from_address, 0) - (tx.value + fee)
            self.balances[tx.to] = self.balances.get(tx.to, 0) + tx.value
            self.nonces[tx.from_address] = self.nonces.get(tx.from_address, 0) + 1
