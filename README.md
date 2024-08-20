# IntelX Trading Bot

This repository contains a Python-based Twitter bot designed to listen for specific commands on Twitter and execute token purchases on Uniswap using the Web3 library. The bot interacts with the Ethereum blockchain to facilitate automated trading based on user commands.

## Features
- **Twitter Command Listening**: Monitors mentions on Twitter and executes commands like token purchases.
- **Uniswap Trading**: Integrates with Uniswap to buy tokens using ETH based on commands received.
- **Customizable**: Easily extend or modify the bot to suit your trading needs.

## Installation

To get started with the IntelX Trading Bot, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Intel-X/intelxbot.git
   cd intelxbot
2. **Install the Required Dependencies**
   Ensure you have python installed, then run:
   ```bash
   pip install -r requirements.txt
3. **Configure Your Environment**
   Rename 'config_example.py' to 'config.py'
   Open 'config.py' and fill in your API keys, Ethereum node URl, and other necessary credentials

## Usage

To run the bot, use the following command:
```bash
python src/intelbot.py
```
## How It Works

1. **Twitter Integration**: The bot uses Tweepy to connect to the Twitter API and listen for specific mentions of your Twitter handle.
2. **Command Parsing**: When the bot is mentioned with a command (e.g., ```@intelxtradingbot buy [contract_address] [ETH_amount]```), it parses the command and initiates a token purchase on Uniswap.
3. **Transaction Execution**: The bot interacts with the Uniswap smart contract via Web3.py to execute the token purchase.

## License

This project is licensed under the [MIT License](LICENSE) - see the License filed for details.

## Acknowledgements
- **Tweepy**: For the twitter API integration.
- **Web3.py**: For interacting with the Ethereum blockchain.
- **Uniswap**: For providing the decentralized trading platform.
