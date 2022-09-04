from tabnanny import check
from algosdk.v2client import algod
from algosdk import constants
from algosdk.future import transaction
import json
import base64

def client():
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    return algod.AlgodClient(algod_token, algod_address)

def submit_txn(signed_txn, params, amount, client, my_address):
    
    #submit transaction
    txid = client.send_transaction(signed_txn)
    account_info = client.account_info(my_address)
    print("Successfully sent transaction with txID: {}".format(txid))
    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(client, txid, 4)  
    except Exception as err:
        print(err)
        return
    
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))
    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee)) 
    account_info = client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")



def checkbalance(client, pubaddress):
    account_info = client.account_info(pubaddress)
    return account_info.get('amount')

def first_transaction_example(private_key, sender_addy ,reciever_addy, amount):

    algod_client = client()
    amount = amount * 1000000
    params = algod_client.suggested_params()
    if checkbalance(algod_client, sender_addy) < amount:
        print("Insufficient balance")
        return False

    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE 
    
    note = "Hello World".encode()
    unsigned_txn = transaction.PaymentTxn(sender_addy, params, reciever_addy, amount, None, note)
    signed_txn = unsigned_txn.sign(private_key)
    submit_txn(signed_txn, params, amount, algod_client, sender_addy)




