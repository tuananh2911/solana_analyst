import json

from solana.rpc.api import Client
from web3 import Web3, HTTPProvider


class SolanaAnalyst:
    def __init__(self, rpc_url="https://api.mainnet-beta.solana.com"):
        self.client = Client(rpc_url)
        self.signer1 = 'Gm16UVXwhB8oaipRTa52qJ36zWeBK4k3CurkT8JGE5VE'
        self.signer2 = 'Djdsf1rrGG6mijFJeVwpVCtoaWiMZGpqRzdZusv7hZMq'

    def get_transactions(self, block_id):
        response = self.client.get_block(slot=block_id,max_supported_transaction_version=0).to_json()
        response_dict = json.loads(response)  # Convert the JSON string to a dictionary
        if 'transactions' in response_dict['result']:
            return response_dict['result']['transactions']
        return []

    def get_info_signer(self, transaction):
        num_required_signatures = transaction['transaction']['message']['header']['numRequiredSignatures']
        signers = transaction['transaction']['message']['accountKeys'][:num_required_signatures]
        return signers

    def filter_signers(self, transactions, signer1, signer2):
        filtered_transactions = []
        for transaction in transactions:
            signers = self.get_info_signer(transaction)
            # print('signer', signers)
            if signer1 in signers or signer2 in signers:

                filtered_transactions.append(transaction)
        return filtered_transactions



# Example usage:
analyst = SolanaAnalyst()
block_id = 285907174 # Replace with the actual block ID
for block in range(block_id, block_id+3):
    transactions = analyst.get_transactions(block_id)
    filtered_transactions = analyst.filter_signers(transactions, analyst.signer1, analyst.signer2)

    for tx in filtered_transactions:
        tx = json.dumps(tx,indent=4)
        with open("../data/transaction_of_signer.json", "w") as outfile:
            outfile.write(tx)
