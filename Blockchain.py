from Block import Block
from LegacyTransaction import LegacyTransaction
import time
import json

from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict
from eth_utils import decode_hex
from eth_keys import keys

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.balances = {}
        self.nonces = {}
        self.add_genesis_block()

    def add_genesis_block(self):
        genesis_transaction = LegacyTransaction("genesis", "0x53f71e9815eebb203a35e07c2c5933a853dcad55", "0x0", "0x0", "0x0", hex(10**18), "0x0", "0x0", "0x0", "0x0")
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
            return True
        else:
            print("Transactions failed verification.")
            return False

    import json

    def validate_transactions(self, transactions):
        for tx in transactions:
            expected_nonce = self.nonces.get(tx.from_address.lower(), 0)
            fee = tx.gas_price * tx.gas_limit

            total_value = tx.value

            # Обработка мульти-транзакции
            if tx.to == "0x0000000000000000000000000000000000000000" and tx.data != "0x00":
                try:
                    payload = json.loads(bytes.fromhex(tx.data[2:]).decode())
                    total_value = sum(payload["values"])
                except Exception as e:
                    print("Ошибка чтения данных мульти-транзакции:", e)
                    return False

            required_balance = total_value + fee

            if self.balances.get(tx.from_address.lower(), 0) < required_balance:
                print(f"{tx.from_address} недостаточно средств.")
                return False

            if tx.nonce != expected_nonce:
                print(f"Неправильный nonce для {tx.from_address}: ожидается: {expected_nonce}, получено: {tx.nonce}")
                return False

            self.apply_transactions([tx])
        return True

    def apply_transactions(self, transactions):
        for tx in transactions:
            fee = tx.gas_price * tx.gas_limit
            sender = tx.from_address.lower()

            # Обработка мульти-транзакции
            if tx.to == "0x0000000000000000000000000000000000000000" and tx.data != "0x00":
                try:
                    payload = json.loads(bytes.fromhex(tx.data[2:]).decode())
                    recipients = payload["recipients"]
                    values = payload["values"]

                    total_sent = sum(values)
                    total_cost = total_sent + fee

                    self.balances[sender] = self.balances.get(sender, 0) - total_cost
                    self.nonces[sender] = self.nonces.get(sender, 0) + 1

                    for addr, value in zip(recipients, values):
                        receiver = addr.lower()
                        self.balances[receiver] = self.balances.get(receiver, 0) + value
                except Exception as e:
                    print("Ошибка применения мульти-транзакции:", e)
                    continue
            else:
                # Стандартная транзакция
                value = tx.value
                receiver = tx.to.lower()

                self.balances[sender] = self.balances.get(sender, 0) - (value + fee)
                self.balances[receiver] = self.balances.get(receiver, 0) + value
                self.nonces[sender] = self.nonces.get(sender, 0) + 1



