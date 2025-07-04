# from Blockchain import Blockchain
# from LegacyTransaction import LegacyTransaction
#
# def main():
#     # создание объекта blockchain (вместе с созданием объекта создается первый блок и пополняется баланс получателя)
#     my_blockchain = Blockchain()
#
#     # создание транзакций и добавление их в блоки
#     transaction1 = LegacyTransaction("0x53f71e9815eebB203a35E07C2c5933A853DcAd55", "Alex", "0x0", "0x3b9aca00", "0x5208", hex(1_000_000_000), "0x0")
#
#     my_blockchain.add_block([transaction1])
#
#     # выводим всю цепь блоков
#     for block in my_blockchain.chain:
#         print(f"index: {block.index}, time: {block.timestamp}, previous_hash: {block.previous_hash}, difficulty: {block.difficulty}, nonce: {block.nonce}, hash: {block.hash}")
#         for transaction in block.transactions:
#             print(f"{transaction}")
#         print("---")
#
# if __name__ == "__main__":
#      main()