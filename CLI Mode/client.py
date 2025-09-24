import os
import logging
from dotenv import load_dotenv
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

# Load environment variables from .env file
load_dotenv()

def setup_logging():
    """Configures structured logging to both console and file."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

class BinanceBotClient:
    """A wrapper for the Binance client to handle authentication, logging, and requests."""
    
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        self.logger = setup_logging()
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        
        if not self.api_key or not self.api_secret:
            self.logger.error("FATAL: API key and/or secret not found in .env file.")
            raise ValueError("Please set BINANCE_API_KEY and BINANCE_API_SECRET in a .env file.")
            
        try:
            self.client = Client(self.api_key, self.api_secret, testnet=testnet)
            # Use the testnet URL for futures
            if testnet:
                self.client.FUTURES_URL = 'https://testnet.binancefuture.com'
            self.client.ping()
            self.logger.info("Successfully connected to Binance API.")
        except (BinanceAPIException, BinanceRequestException) as e:
            self.logger.error(f"API Connection Error: {e}")
            raise

    def place_order(self, order_details):
        """Places a single order and handles API responses."""
        try:
            self.logger.info(f"Placing order with details: {order_details}")
            order = self.client.futures_create_order(**order_details)
            self.logger.info("Successfully placed order.")
            self.logger.info(f"API Response: {order}")
            print("\n✅ Order Placed Successfully!")
            print(f"   - Symbol: {order['symbol']}")
            print(f"   - Order ID: {order['orderId']}")
            print(f"   - Type: {order['type']}")
            print(f"   - Side: {order['side']}")
            print(f"   - Quantity: {order['origQty']}")
            print(f"   - Status: {order['status']}")
            return order, None
        except BinanceAPIException as e:
            self.logger.error(f"API Error placing order: {e.status_code} - {e.message}")
            print(f"\n❌ Error placing order: {e.message}")
            return None, f"❌ Error placing order: {e.message}"
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            print(f"\n❌ An unexpected error occurred: {e}")
            return None, f"❌ An unexpected error occurred: {e}"

    def place_batch_order(self, batch_orders):
        """Places a batch of orders (e.g., for OCO) and handles API responses."""
        try:
            self.logger.info(f"Placing batch order with details: {batch_orders}")
            order_responses = self.client.futures_place_batch_order(batchOrders=batch_orders)
            self.logger.info("Successfully placed batch order.")
            self.logger.info(f"API Response: {order_responses}")
            print("\n✅ Batch Order Placed Successfully!")
            for i, order in enumerate(order_responses):
                if 'orderId' in order: # Successful order
                    print(f"\n--- Sub-Order {i+1} ---")
                    print(f"   - Symbol: {order['symbol']}")
                    print(f"   - Order ID: {order['orderId']}")
                    print(f"   - Type: {order['type']}")
                    print(f"   - Status: {order['status']}")
                else: # Failed order in batch
                    print(f"\n--- Sub-Order {i+1} Failed ---")
                    print(f"   - Code: {order.get('code')}")
                    print(f"   - Message: {order.get('msg')}")
            return order_responses, None
        except BinanceAPIException as e:
            self.logger.error(f"API Error placing batch order: {e.status_code} - {e.message}")
            print(f"\n❌ Error placing batch order: {e.message}")
            return None, f"❌ Error placing order: {e.message}"
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during batch order: {e}")
            print(f"\n❌ An unexpected error occurred: {e}")
            return None, f"❌ An unexpected error occurred: {e}"

    def get_current_price(self, symbol):
        """Fetches the last traded price for a given symbol."""
        try:
            ticker = self.client.futures_ticker(symbol=symbol)
            price = float(ticker['lastPrice'])
            self.logger.info(f"Current price for {symbol} is {price}")
            return price
        except Exception as e:
            self.logger.error(f"Could not fetch price for {symbol}: {e}")
            return None