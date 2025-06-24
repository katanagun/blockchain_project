from Blockchain import Blockchain
from Transaction import Transaction
from Token import Token

def main():
    # создание объекта blockchain (вместе с созданием объекта создается первый блок и пополняется баланс получателя)
    my_blockchain = Blockchain()

    # создание транзакций и добавление их в блоки
    transaction1 = Transaction("Viktor", "Alice", Token("temp", 10))
    transaction2 = Transaction("Viktor", "John", Token("temp", 15))
    transaction3 = Transaction("Viktor", "Alex", Token("temp", 30))
    transaction4 = Transaction("Alex", "Alice", Token("temp", 5))
    transaction5 = Transaction("Viktor", "Alice", Token("temp", 5))
    transaction6 = Transaction("Alice", "Alex", Token("temp", 3))
    transaction7 = Transaction("John", "Viktor", Token("temp", 4))

    transaction_block1 = [transaction1, transaction2, transaction3]
    transaction_block2 = [transaction4, transaction5, transaction6, transaction7]

    my_blockchain.add_block(transaction_block1)
    my_blockchain.add_block(transaction_block2)

    # выводим всю цепь блоков
    for block in my_blockchain.chain:
        print(f"index: {block.index}, time: {block.timestamp}, previous_hash: {block.previous_hash}, difficulty: {block.difficulty}, nonce: {block.nonce}, hash: {block.hash}")
        for transaction in block.transactions:
            print(f"{transaction}")
        print("---")

if __name__ == "__main__":
    main()