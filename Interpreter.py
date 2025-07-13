from LegacyTransaction import LegacyTransaction
import json

class Interpreter:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.sender = "0x53f71e9815eebb203a35e07c2c5933a853dcad55"

    import json

    def create_multi_transaction(self, recipients, values, nonce, gas_price=1, gas_limit=21000, v="0x0", r="0x0", s="0x0"):
        payload = {
            "recipients": recipients,
            "values": values
        }
        data = "0x" + json.dumps(payload).encode().hex()
        tx = LegacyTransaction(
            from_address=self.sender,
            to="0x0000000000000000000000000000000000000000",
            nonce=hex(nonce),
            gas_price=hex(gas_price),
            gas_limit=hex(gas_limit),
            value="0x0",
            data=data,
            v=v,
            r=r,
            s=s
        )
        tx.set_hash()
        return tx

    def execute(self):
        recipients = [
            "0x1111111111111111111111111111111111111111",
            "0x2222222222222222222222222222222222222222",
            "0x3333333333333333333333333333333333333333"
        ]
        total_value = 3000
        portion = total_value // len(recipients)
        values = [portion] * len(recipients)
        nonce = self.blockchain.nonces.get(self.sender.lower(), 0)

        tx = self.create_multi_transaction(recipients, values, nonce)
        success = self.blockchain.add_block([tx])

        if success:
            print(f"Блок добавлен с 1 мульти-транзакцией.")
        else:
            print("Ошибка: транзакция не прошла проверку.")

        # Вывод балансов
        print("\nБалансы адресов:")
        all_addresses = [self.sender] + recipients
        for addr in all_addresses:
            balance = self.blockchain.balances.get(addr.lower(), 0)
            print(f"{addr}: {balance}")

        # Вывод цепочки блоков
        print("\nЦепочка блоков:")
        for i, block in enumerate(self.blockchain.chain):
            print(f"Блок {i} — хэш: {block.hash}, транзакций: {len(block.transactions)}")

