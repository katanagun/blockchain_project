from Block import Block
from Transaction import Transaction
from Token import Token
import time

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.balances = {}
        self.add_genesis_block()

    def add_genesis_block(self):
        genesis_transaction = Transaction("genesis", "Viktor", Token("temp", 100))
        block = Block(0, time.time(), [genesis_transaction], difficulty=self.difficulty)
        block.hash = block.calculate_hash()
        self.apply_transactions([genesis_transaction])
        self.chain.append(block)

    def add_block(self, transactions):
        index = len(self.chain)
        previous_hash = self.chain[-1].hash

        block = Block(index, time.time(), transactions, previous_hash, self.difficulty)

        if self.validate_transactions(transactions):
            self.apply_transactions(transactions)
            self.chain.append(block)
        else:
            print("Transactions failed verification.")

    def validate_transactions(self, transactions):
        for tx in transactions:
            if tx.sender == "genesis":
                continue
            if self.balances.get(tx.sender, 0) < tx.token.value:
                return False
        return True


    def apply_transactions(self, transactions):
        for tx in transactions:
            sender, receiver, token = tx.sender, tx.receiver, tx.token
            if sender != "genesis":
                self.balances[sender] = self.balances.get(sender, 0) - token.value
            self.balances[receiver] = self.balances.get(receiver, 0) + token.value
