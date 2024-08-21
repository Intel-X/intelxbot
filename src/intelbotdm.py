import tweepy
from web3 import Web3
import json
import time

# Twitter API credentials
API_KEY = 'enter'
API_SECRET_KEY = 'enter'
ACCESS_TOKEN = 'enter'
ACCESS_TOKEN_SECRET = 'enter'

# Ethereum and Uniswap settings
INFURA_URL = 'https://mainnet.infura.io/v3/your_infura_project_id'
PRIVATE_KEY = 'your_private_key'
WALLET_ADDRESS = 'your_wallet_address'
UNISWAP_ROUTER_ADDRESS = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Load Uniswap Router ABI
with open('uniswap_router_abi.json', 'r') as f:
    uniswap_router_abi = json.load(f)

uniswap_router = web3.eth.contract(address=UNISWAP_ROUTER_ADDRESS, abi=uniswap_router_abi)

# Initialize Tweepy API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Function to swap ETH for tokens
def swap_eth_for_tokens(token_address, eth_amount, user_address):
    deadline = int(time.time()) + 600
    tx = uniswap_router.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
        0,  # amountOutMin
        [web3.toChecksumAddress(web3.eth.defaultAccount), token_address],
        user_address,
        deadline
    ).buildTransaction({
        'from': WALLET_ADDRESS,
        'value': web3.toWei(eth_amount, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': web3.eth.getTransactionCount(WALLET_ADDRESS)
    })
    return send_transaction(tx)

# Function to swap tokens for ETH
def swap_tokens_for_eth(token_address, token_amount, user_address):
    deadline = int(time.time()) + 600
    tx = uniswap_router.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
        web3.toWei(token_amount, 'ether'),
        0,  # amountOutMin
        [token_address, web3.toChecksumAddress(web3.eth.defaultAccount)],
        user_address,
        deadline
    ).buildTransaction({
        'from': WALLET_ADDRESS,
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': web3.eth.getTransactionCount(WALLET_ADDRESS)
    })
    return send_transaction(tx)

# Helper function to send transactions
def send_transaction(tx):
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return web3.toHex(tx_hash)

# Function to handle direct messages
def handle_dm(dm):
    sender_id = dm.message_create['sender_id']
    text = dm.message_create['message_data']['text']

    if sender_id != api.me().id:
        try:
            action, token_address, amount = text.split()
            amount = float(amount)

            if action.lower() == 'buy':
                tx_hash = swap_eth_for_tokens(token_address, amount, sender_id)
                api.send_direct_message(sender_id, f"Buy order placed. Transaction Hash: {tx_hash}")
            elif action.lower() == 'sell':
                tx_hash = swap_tokens_for_eth(token_address, amount, sender_id)
                api.send_direct_message(sender_id, f"Sell order placed. Transaction Hash: {tx_hash}")
            else:
                api.send_direct_message(sender_id, "Invalid action. Use 'buy' or 'sell'.")
        except Exception as e:
            api.send_direct_message(sender_id, f"Error: {str(e)}")

# Main bot loop
def run_bot():
    last_seen_id = None

    while True:
        dms = api.list_direct_messages()
        for dm in reversed(dms):
            if last_seen_id is None or dm.id > last_seen_id:
                handle_dm(dm)
                last_seen_id = dm.id
        time.sleep(10)

if __name__ == '__main__':
    run_bot()
