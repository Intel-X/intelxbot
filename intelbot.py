import tweepy
import time
from web3 import Web3

# Twitter API credentials
API_KEY = 'enter'
API_SECRET_KEY = 'enter'
ACCESS_TOKEN = 'enter'
ACCESS_TOKEN_SECRET = 'enter'
BEARER_TOKEN = 'enter'

# Web3 Ethereum node setup
INFURA_URL = 'enter'
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Contract addresses (Example: Uniswap)
UNISWAP_ROUTER_ADDRESS = '0x...'
UNISWAP_ROUTER_ABI = [...]  # Add Uniswap Router ABI

# Tweepy authentication using the API key and secret
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Define the function to buy tokens
def buy_token(contract_address, eth_amount):
    router = web3.eth.contract(address=UNISWAP_ROUTER_ADDRESS, abi=UNISWAP_ROUTER_ABI)
    path = [web3.toChecksumAddress(web3.eth.default_account), web3.toChecksumAddress(contract_address)]
    
    tx = router.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
        0,  # Minimum amount of tokens to accept
        path,
        web3.eth.default_account,
        int(time.time()) + 1000  # Deadline timestamp
    ).buildTransaction({
        'from': web3.eth.default_account,
        'value': web3.toWei(eth_amount, 'ether'),
        'gas': 200000,
        'gasPrice': web3.toWei('5', 'gwei'),
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key='your_private_key')
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return web3.toHex(tx_hash)

# Define the stream listener
class MyStream(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        text = tweet.text.lower()
        if "@intelxtradingbot" in text and "buy" in text:
            try:
                parts = text.split(" ")
                action = parts[1]
                contract_address = parts[2]
                eth_amount = float(parts[3])

                if action == "buy":
                    tx_hash = buy_token(contract_address, eth_amount)
                    reply_text = (f"@{tweet.user.screen_name} Purchase of {eth_amount} ETH worth of tokens at "
                                  f"contract address {contract_address} initiated. "
                                  f"Transaction Hash: {tx_hash}")
                    api.update_status(reply_text, in_reply_to_status_id=tweet.id)
            except Exception as e:
                api.update_status(f"@{tweet.user.screen_name} Error processing your request: {e}", in_reply_to_status_id=tweet.id)

    def on_error(self, status_code):
        if status_code == 420:
            return False  # Disconnects the stream

# Start the stream
my_stream = MyStream(bearer_token=BEARER_TOKEN)
my_stream.filter(track=["@intelxtradingbot"])
