from flask import Flask, request, jsonify
from flask_cors import CORS
from Blockchain import Blockchain
from LegacyTransaction import LegacyTransaction

app = Flask(__name__)
CORS(app)

blockchain = Blockchain()

@app.route("/balance/<address>", methods=["GET"])
def get_balance(address):
    balance = blockchain.balances.get(address, 0)
    return jsonify({"address": address, "balance": balance})

@app.route("/submit_tx", methods=["POST"])
def submit_tx():
    try:
        data = request.json

        print("Пришёл JSON:", data) # для проверки

        tx = LegacyTransaction(
            from_address=data["from"],
            to=data["to"],
            nonce=data["nonce"],
            gas_price=data["gasPrice"],
            gas_limit=data["gasLimit"],
            value=data["value"],
            data=data.get("data", "0x0"),
            v=data.get("v"),
            r=data.get("r"),
            s=data.get("s")
        )
        blockchain.add_block([tx])
        # просмотр блоков (для проверки)
        for block in blockchain.chain:
            print(
                f"index: {block.index}, time: {block.timestamp}, previous_hash: {block.previous_hash}, difficulty: {block.difficulty}, nonce: {block.nonce}, hash: {block.hash}")
            for transaction in block.transactions:
                print(f"{transaction}")
            print("---")

        return jsonify({"status": "success", "message": "Transaction added to block"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
