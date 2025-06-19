from Block import Block
from Blockchain import Blockchain
import time

def main():
    # создание объекта blockchain и первого блока
    my_blockchain = Blockchain()
    my_blockchain.add_genesis_block()

    # сгенерируем n количество блоков и добавляем в цепь
    for i in range(1, 5):
        block = Block(i, time.time(), f"block {i}")
        my_blockchain.add_block(block)

    # выводим всю цепь блоков
    for block in my_blockchain.chain:
        print("---")
        print(f"index: {block.index}, timestamp: {block.timestamp}, data: {block.data}, previous_hash: {block.previous_hash}, hash: {block.hash}")

if __name__ == "__main__":
    main()