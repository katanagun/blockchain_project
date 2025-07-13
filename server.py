import web3
import requests
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import rlp
from web3 import Web3
from eth_account._utils.legacy_transactions import (
    Transaction as EthLegacyTransaction
)

from Blockchain import Blockchain
from LegacyTransaction import LegacyTransaction
from Block import Block


PEERS = os.getenv("PEERS", "").split(",")
NODE_NAME = os.getenv("NODE_NAME", "unnamed")

print(f"Стартует нода: {NODE_NAME}")
print(f"Подключенные PEERS: {PEERS}")

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
blockchain = Blockchain()

app = Flask(__name__)
CORS(app)

CHAIN_ID = 1111

def broadcast_block(block):
    for peer in PEERS:
        try:
            requests.post(f"{peer}/receive-block", json=block.serialize())
        except Exception as e:
            print(f"Не удалось отправить блок на {peer}: {e}")

@app.route("/receive-block", methods=["POST"])
def receive_block():
    try:
        block_data = request.get_json(force=True)
        block = Block.deserialize(block_data)

        # Проверка: не дублируй, если блок уже есть
        if any(b.hash == block.hash for b in blockchain.chain):
            return "Блок уже есть", 200

        success = blockchain.append_block(block)
        if success:
            return "Блок принят", 200
        else:
            return "Ошибка верификации", 400
    except Exception as e:
        return f"Ошибка приема блока: {str(e)}", 500

@app.route("/chain")
def chain():
    return jsonify([b.serialize() for b in blockchain.chain])


@app.route("/", methods=["POST"])
def rpc():
    try:
        payload = request.get_json(force=True)
        if not payload:
            return jsonify({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Invalid JSON"}}), 400

        method = payload.get("method")
        params = payload.get("params", [])
        rpc_id = payload.get("id", 1)

        print("Метод:", method)

        if method == "eth_chainId":
            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": hex(CHAIN_ID)
            })

        elif method == "net_version":
            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": str(CHAIN_ID)
            })

        elif method == "eth_blockNumber":
            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": hex(len(blockchain.chain) - 1)
            })


        elif method == "eth_getBlockByNumber":
            block_param = params[0] if len(params) > 0 else "latest"
            full_tx = params[1] if len(params) > 1 else False

            if block_param == "latest":
                block_index = len(blockchain.chain) - 1

            elif isinstance(block_param, str) and block_param.startswith("0x"):
                block_index = int(block_param, 16)

            else:
                block_index = int(block_param)

            if block_index < 0 or block_index >= len(blockchain.chain):
                return jsonify({"jsonrpc": "2.0", "id": rpc_id, "result": None})

            block_obj = blockchain.chain[block_index]

            # Генерируем список транзакций
            if full_tx:
                transactions = []
                for tx in block_obj.transactions:
                    transactions.append({
                        "from": tx.from_address,
                        "to": tx.to,
                        "value": hex(tx.value),
                        "nonce": hex(tx.nonce),
                        "gas": hex(tx.gas_limit),
                        "gasPrice": hex(tx.gas_price),
                        "input": tx.data,
                        "v": hex(int(tx.v, 16) if isinstance(tx.v, str) else tx.v) if tx.v else "0x0",
                        "r": hex(int(tx.r, 16) if isinstance(tx.r, str) else tx.r) if tx.r else "0x0",
                        "s": hex(int(tx.s, 16) if isinstance(tx.s, str) else tx.s) if tx.s else "0x0",
                    })
            else:
                transactions = [f"0x{str(tx)}" for tx in block_obj.transactions]
            block_response = {
                "number": hex(block_obj.index),
                "hash": "0x" + block_obj.hash,
                "parentHash": "0x" + (block_obj.previous_hash or "0" * 64),
                "nonce": hex(block_obj.nonce),
                "sha3Uncles": "0x" + "0" * 64,
                "logsBloom": "0x" + "0" * 512,
                "transactionsRoot": "0x" + "0" * 64,
                "stateRoot": "0x" + "0" * 64,
                "receiptsRoot": "0x" + "0" * 64,
                "miner": "0x0000000000000000000000000000000000000000",
                "difficulty": "0x1",
                "totalDifficulty": "0x1",
                "extraData": "0x",
                "size": hex(1000),
                "gasLimit": hex(30000000),
                "gasUsed": hex(0),
                "timestamp": hex(int(block_obj.timestamp)),
                "transactions": transactions,
                "uncles": []
            }

            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": block_response
            })

        elif method == "eth_getBlockByHash":
            if len(params) < 1:
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "result": None
                })

            requested_hash = params[0].replace("0x", "").lower()
            full_tx = params[1] if len(params) > 1 else False
            block_obj = None

            for block in blockchain.chain:
                if block.hash.lower() == requested_hash:
                    block_obj = block
                    break

            if not block_obj:
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "result": None
                })

            if full_tx:
                transactions = []
                for tx in block_obj.transactions:
                    transactions.append({
                        "from": tx.from_address,
                        "to": tx.to,
                        "value": hex(tx.value),
                        "nonce": hex(tx.nonce),
                        "gas": hex(tx.gas_limit),
                        "gasPrice": hex(tx.gas_price),
                        "input": tx.data,
                        "v": hex(int(tx.v, 16) if isinstance(tx.v, str) else tx.v) if tx.v else "0x0",
                        "r": hex(int(tx.r, 16) if isinstance(tx.r, str) else tx.r) if tx.r else "0x0",
                        "s": hex(int(tx.s, 16) if isinstance(tx.s, str) else tx.s) if tx.s else "0x0",
                    })
            else:
                transactions = ["0x" + tx.tx_hash for tx in block_obj.transactions]

            block_response = {
                "number": hex(block_obj.index),
                "hash": "0x" + block_obj.hash,
                "parentHash": "0x" + (block_obj.previous_hash or "0" * 64),
                "nonce": hex(block_obj.nonce),
                "sha3Uncles": "0x" + "0" * 64,
                "logsBloom": "0x" + "0" * 512,
                "transactionsRoot": "0x" + "0" * 64,
                "stateRoot": "0x" + "0" * 64,
                "receiptsRoot": "0x" + "0" * 64,
                "miner": "0x0000000000000000000000000000000000000000",
                "difficulty": "0x1",
                "totalDifficulty": "0x1",
                "extraData": "0x",
                "size": hex(1000),
                "gasLimit": hex(30000000),
                "gasUsed": hex(0),
                "timestamp": hex(int(block_obj.timestamp)),
                "transactions": transactions,
                "uncles": []
            }

            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": block_response
            })

        elif method == "eth_getBalance":
            if len(params) < 1:
                raise ValueError("Missing address")
            address = params[0].lower()
            balance = blockchain.balances.get(address, 0)
            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": hex(balance)
            })

        elif method == "eth_getTransactionCount":
            if len(params) < 1:
                raise ValueError("Missing address")
            address = params[0].lower()
            nonce = blockchain.nonces.get(address, 0)
            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": hex(nonce)
            })

        elif method == "eth_getCode":
            if len(params) < 1:
                raise ValueError("Missing address parameter")
            address = params[0].lower()

            # Предположим, у нас нет контрактов — возвращаем пустой код
            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": "0x"  # адрес не содержит кода (обычный кошелёк)
            })

        elif method == "eth_call":
            # Просто всегда возвращаем "0x"
            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": "0x"
            })


        elif method == "eth_sendRawTransaction":
            raw_tx_hex = params[0]
            raw_bytes = bytes.fromhex(raw_tx_hex[2:] if raw_tx_hex.startswith("0x") else raw_tx_hex)
            try:
                # RLP-декод
                eth_tx = rlp.decode(raw_bytes, EthLegacyTransaction)
                # Генерация настоящего хэша транзакции
                tx_rlp = rlp.encode(eth_tx)
                tx_hash = Web3.keccak(tx_rlp).hex()
                # Нормализуем адрес назначения
                if isinstance(eth_tx.to, bytes):
                    to_address = "0x" + eth_tx.to.hex()
                elif isinstance(eth_tx.to, str):
                    to_address = eth_tx.to
                else:
                    to_address = "0x" + "0" * 40
                # Создаём объект LegacyTransaction
                tx = LegacyTransaction(
                    from_address=web3.eth.account.recover_transaction(raw_tx_hex),
                    to=to_address,
                    nonce=hex(eth_tx.nonce),
                    gas_price=hex(eth_tx.gasPrice),
                    gas_limit=hex(eth_tx.gas),
                    value=hex(eth_tx.value),
                    data="0x" + eth_tx.data.hex(),
                    v=hex(eth_tx.v),
                    r=hex(eth_tx.r),
                    s=hex(eth_tx.s),
                )
                tx.set_hash()

                print(f"Принята транзакция: {tx}")

                # добавление в блокчейн
                success = blockchain.add_block([tx])
                if success:
                    broadcast_block(blockchain.chain[-1])
                    return jsonify({
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "result": "0x" + tx.tx_hash
                    })
                else:
                    return jsonify({
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "error": {"code": -32000, "message": "Transaction rejected"}
                    })



            except Exception as e:
                print("Ошибка обработки rawTransaction:", e)
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "error": {"code": -32602, "message": f"Failed to decode raw transaction: {str(e)}"}
                })

        elif method == "eth_getTransactionReceipt":
            print("Параметры запроса:", params)

            if len(params) < 1:
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "result": None
                })
            tx_hash = params[0].replace("0x", "").lower()
            receipt = None

            for idx, block in enumerate(blockchain.chain):
                for tx in block.transactions:
                    if tx.tx_hash is not None:
                        if tx.tx_hash.lower() == tx_hash:
                            receipt = {
                                "transactionHash": "0x" + tx_hash,
                                "transactionIndex": "0x0",
                                "blockHash": "0x" + block.hash,
                                "blockNumber": hex(idx),
                                "from": tx.from_address.lower(),
                                "to": tx.to.lower(),
                                "cumulativeGasUsed": hex(tx.gas_limit),
                                "gasUsed": hex(tx.gas_limit),
                                "effectiveGasPrice": hex(tx.gas_price),
                                "contractAddress": None,
                                "type": "0x0",
                                "logs": [],
                                "logsBloom": "0x" + "0" * 512,
                                "status": "0x1"
                            }
                    else:
                        continue

            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": receipt
            })

        elif method == "eth_gasPrice":
            # Возвращаем фиксированное значение
            gas_price = 2 * 10 ** 9  # 2 Gwei в wei
            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": hex(gas_price)
            })

        elif method == "eth_estimateGas":
            if len(params) < 1:
                raise ValueError("Missing transaction object")

            tx = params[0]
            gas_estimate = 21000

            if tx.get("data") and tx["data"] != "0x":
                gas_estimate += 50000

            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": hex(gas_estimate)
            })

        else:
            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {
                    "code": -32601,
                    "message": f"Method '{method}' not implemented"
                }
            })

    except Exception as e:
        print("Ошибка обработки запроса:", e)
        return jsonify({
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8545)
