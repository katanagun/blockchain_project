from LegacyTransaction import LegacyTransaction

class Interpreter:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.sender = "0x53f71e9815eebb203a35e07c2c5933a853dcad55"

    def create_transaction(self, to_addr, value, nonce, gas_price=1, gas_limit=21000, v="0x0", r="0x0", s="0x0"):
        tx = LegacyTransaction(
            from_address=self.sender,
            to=to_addr,
            nonce=hex(nonce),
            gas_price=hex(gas_price),
            gas_limit=hex(gas_limit),
            value=hex(value),
            data="0x00",
            v=v,
            r=r,
            s=s
        )
        tx.set_hash()
        return tx

    def execute(self):
        recipients = ["0x1111111111111111111111111111111111111111", "0x2222222222222222222222222222222222222222", "0x3333333333333333333333333333333333333333"]
        total_value = 3000
        portion = total_value // len(recipients)
        nonce = self.blockchain.nonces.get(self.sender.lower(), 0)

        transactions = []

        for i, recipient in enumerate(recipients):
            tx = self.create_transaction(recipient, portion, nonce + i)
            transactions.append(tx)

        success = self.blockchain.add_block(transactions)

        if success:
            print(f"Блок добавлен с {len(transactions)} транзакциями.")
        else:
            print("Ошибка: транзакции не прошли проверку.")

        print("\nБалансы адресов:")
        for addr in [self.sender] + recipients:
            balance = self.blockchain.balances.get(addr.lower(), 0)
            print(f"{addr}: {balance}")

        print("\nЦепочка блоков:")
        for i, block in enumerate(self.blockchain.chain):
            print(f"Блок {i} — хэш: {block.hash}, транзакций: {len(block.transactions)}")
