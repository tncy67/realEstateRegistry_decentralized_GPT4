from flask import Flask, render_template, request, redirect, url_for
from web3 import Web3
from abi import ABI
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Replace with your contract's ABI and address
contract_abi = ABI
contract_address = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB_PROVIDER_URI")))
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "register" in request.form:
            price = float(request.form["price"])
            details = request.form["details"]
            register_property(price, details)
        elif "buy" in request.form:
            property_id = int(request.form["property_id"])
            purchase_price = float(request.form["purchase_price"])
            buy_property(property_id, purchase_price)
        return redirect(url_for("index"))

    return render_template("./index.html")


def register_property(price, details):
    # Replace with the appropriate account and private key
    account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
    price_wei = w3.toWei(price, "ether")

    nonce = w3.eth.getTransactionCount(account.address)
    txn = contract.functions.registerProperty(price_wei, details).buildTransaction({
        "from": account.address,
        "gas": 1000000,
        "gasPrice": w3.eth.gasPrice,
        "nonce": nonce,
    })
    signed_txn = account.sign_transaction(txn)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)


def buy_property(property_id, purchase_price):
    # Replace with the appropriate account and private key
    account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
    purchase_price_wei = w3.toWei(purchase_price, "ether")

    nonce = w3.eth.getTransactionCount(account.address)
    txn = contract.functions.buyProperty(property_id).buildTransaction({
        "from": account.address,
        "value": purchase_price_wei,
        "gas": 1000000,
        "gasPrice": w3.eth.gasPrice,
        "nonce": nonce,
    })
    signed_txn = account.sign_transaction(txn)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)


if __name__ == "__main__":
    app.run(debug=True)
