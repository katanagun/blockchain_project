from Block import Block
from LegacyTransaction import LegacyTransaction
import time
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

    def validate_transactions(self, transactions):
        for tx in transactions:
            expected_nonce = self.nonces.get(tx.from_address.lower(), 0)
            required_balance = tx.value + tx.gas_price * tx.gas_limit
            if self.balances.get(tx.from_address.lower(), 0) < required_balance:
                print(f"{tx.from_address} does not have enough funds")
                return False
            if tx.nonce != expected_nonce:
                print(f"Invalid nonce for {tx.from_address}: expected {expected_nonce}, received {tx.nonce}")
                return False
            # if not self.verify_signature(tx):
            #     print(f"Неверная подпись от {tx.from_address}")
            #     return False

            self.apply_transactions([tx])
        return True

    # этот метод нигде не используется
    # def verify_signature(self, tx):
    #     try:
    #         if not tx.v or not tx.r or not tx.s:
    #             print("Подпись отсутствует")
    #             return False
    #
    #         v = int(tx.v, 16) if isinstance(tx.v, str) else tx.v
    #         r = int(tx.r, 16) if isinstance(tx.r, str) else tx.r
    #         s = int(tx.s, 16) if isinstance(tx.s, str) else tx.s
    #
    #         CHAIN_ID = 1111
    #
    #         to_field = tx.to
    #         if isinstance(to_field, bytes):
    #             to_field = "0x" + to_field.hex()
    #         elif isinstance(to_field, str):
    #             to_field = to_field.lower()
    #             if not to_field.startswith("0x"):
    #                 to_field = "0x" + to_field
    #         else:
    #             to_field = None
    #
    #         # Собираем словарь неподписанной транзакции
    #         unsigned_dict = {
    #             "nonce": tx.nonce,
    #             "gasPrice": tx.gas_price,
    #             "gas": tx.gas_limit,
    #             "to": tx.to,
    #             "value": tx.value,
    #             "data": decode_hex(tx.data),
    #             "chainId": CHAIN_ID,
    #         }
    #
    #         unsigned_tx = serializable_unsigned_transaction_from_dict(unsigned_dict)
    #         message_hash = unsigned_tx.hash()
    #
    #         # Вычисляем "v"
    #         v_standard = v - (CHAIN_ID * 2 + 35)
    #         if v_standard not in (0, 1):
    #             print("Неверный recovery id:", v_standard)
    #             return False
    #
    #         # Собираем подпись и восстанавливаем публичный ключ
    #         signature = r.to_bytes(32, "big") + s.to_bytes(32, "big") + bytes([v_standard])
    #         public_key = keys.ecdsa_recover(message_hash, signature)
    #         recovered_address = public_key.to_checksum_address()
    #
    #         return recovered_address.lower() == tx.from_address.lower()
    #
    #     except Exception as e:
    #         print("Ошибка подписи:", e)
    #         return False

    def apply_transactions(self, transactions):
        for tx in transactions:
            fee = tx.gas_price * tx.gas_limit
            self.balances[tx.from_address.lower()] = abs(self.balances.get(tx.from_address.lower(), 0) - (tx.value + fee))
            self.balances[tx.to.lower()] = self.balances.get(tx.to.lower(), 0) + tx.value
            self.nonces[tx.from_address.lower()] = self.nonces.get(tx.from_address.lower(), 0) + 1


