# frontend/app.py
import streamlit as st
import sys
import os

# --- Add backend path ---
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
from client import BinanceBotClient

# --- Page Config ---
st.set_page_config(
    page_title="Cryptrizx_Binance_Bot",
    page_icon="💹",  # <-- You can replace this with your custom icon link: st.set_page_config(page_icon="path_to_icon.png")
    layout="centered",
)

# --- Custom CSS for background and styling ---
st.markdown(
    """
    <style>
    /* Background image */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1605902711622-cfb43c4436f7?auto=format&fit=crop&w=1470&q=80");  /* <-- Replace with your background image link */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Customize container */
    .css-18e3th9 {
        background-color: rgba(0,0,0,0.6);  /* semi-transparent overlay */
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.5);
    }

    /* Headings */
    .stTitle, .stHeader {
        color: #FFD700;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
    }

    /* Sidebar */
    .sidebar .css-1d391kg {
        background-color: rgba(0,0,0,0.7);
        color: #fff;
        padding: 1rem;
        border-radius: 10px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #FFA500;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #FF8C00;
    }

    /* Inputs */
    input[type="text"], input[type="password"], input[type="number"] {
        border-radius: 10px;
        padding: 0.3rem;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("💿Cryptrizx Binance <+=> Bot")

# --- API Credentials ---
st.sidebar.header("🔑 API Credentials")
api_key = st.sidebar.text_input("Binance API Key", type="password", placeholder="Enter your Binance API Key")
api_secret = st.sidebar.text_input("Binance API Secret", type="password", placeholder="Enter your Binance API Secret")

# --- Press Enter to trigger submission ---
def submit_api():
    if not api_key or not api_secret:
        st.warning("Please enter your API credentials to continue.")
        return None
    try:
        bot = BinanceBotClient(api_key=api_key, api_secret=api_secret, testnet=True)
        return bot
    except Exception as e:
        st.error(f"API Initialization Failed: {e}")
        return None

# Press Enter key detection
api_submit = st.sidebar.button("Connect", on_click=submit_api)
bot = None
if api_key and api_secret:
    bot = submit_api()
if not bot:
    st.stop()

# --- Order Selection ---
order_type = st.selectbox(
    "Choose Order Type",
    ["Market Order", "Limit Order", "Stop-Limit Order", "OCO Order", "TWAP Order", "Grid Order"]
)

# --- Input Forms per Order ---
order_details = None

# Function to handle order response
def show_response(resp):
    if resp:
        st.success(
            f"✅ Order Placed Successfully!\n"
            f"- Symbol: {resp['symbol']}\n"
            f"- Order ID: {resp['orderId']}\n"
            f"- Type: {resp['type']}\n"
            f"- Side: {resp['side']}\n"
            f"- Quantity: {resp['origQty']}\n"
            f"- Status: {resp['status']}"
        )
    else:
        st.error("❌ Failed to place order. Check logs.")

if order_type == "Market Order":
    st.subheader("Market Order")
    symbol = st.text_input("Symbol (e.g., BTCUSDT)")
    side = st.radio("Side", ["BUY", "SELL"])
    quantity = st.number_input("Quantity", min_value=0.0, format="%.3f")
    if st.button("Place Market Order"):
        order_details = {'symbol': symbol, 'side': side, 'type': 'MARKET', 'quantity': quantity}
        resp = bot.place_order(order_details)
        if resp:
            st.success(
                f"✅ Order Placed Successfully!\n"
                f"- Symbol: {resp['symbol']}\n"
                f"- Order ID: {resp['orderId']}\n"
                f"- Type: {resp['type']}\n"
                f"- Side: {resp['side']}\n"
                f"- Quantity: {resp['origQty']}\n"
                f"- Status: {resp['status']}"
            )
        else:
            st.error("❌ Failed to place order. Check logs.")

elif order_type == "Limit Order":
    st.subheader("Limit Order")
    symbol = st.text_input("Symbol (e.g., ETHUSDT)")
    side = st.radio("Side", ["BUY", "SELL"])
    quantity = st.number_input("Quantity", min_value=0.0, format="%.3f")
    price = st.number_input("Limit Price", min_value=0.0, format="%.2f")
    if st.button("Place Limit Order"):
        order_details = {'symbol': symbol, 'side': side, 'type': 'LIMIT',
                         'timeInForce': 'GTC', 'quantity': quantity, 'price': price}
        resp = bot.place_order(order_details)
        show_response(resp)

elif order_type == "Stop-Limit Order":
    st.subheader("Stop-Limit Order")
    symbol = st.text_input("Symbol")
    side = st.radio("Side", ["BUY", "SELL"])
    quantity = st.number_input("Quantity", min_value=0.0, format="%.3f")
    stop_price = st.number_input("Stop Price", min_value=0.0, format="%.2f")
    limit_price = st.number_input("Limit Price", min_value=0.0, format="%.2f")
    if st.button("Place Stop-Limit Order"):
        order_details = {'symbol': symbol, 'side': side, 'type': 'STOP',
                         'timeInForce': 'GTC', 'quantity': quantity,
                         'price': limit_price, 'stopPrice': stop_price}
        resp = bot.place_order(order_details)
        show_response(resp)

elif order_type == "OCO Order":
    st.subheader("OCO Order")
    symbol = st.text_input("Symbol")
    side = st.radio("Side", ["BUY", "SELL"])
    quantity = st.number_input("Quantity", min_value=0.0, format="%.3f")
    take_profit = st.number_input("Take Profit Price", min_value=0.0, format="%.2f")
    stop_loss = st.number_input("Stop Loss Price", min_value=0.0, format="%.2f")
    if st.button("Place OCO Order"):
        batch_orders = [
            {'symbol': symbol, 'side': side, 'type': 'TAKE_PROFIT_MARKET',
             'quantity': str(quantity), 'stopPrice': str(take_profit), 'reduceOnly': 'true'},
            {'symbol': symbol, 'side': side, 'type': 'STOP_MARKET',
             'quantity': str(quantity), 'stopPrice': str(stop_loss), 'reduceOnly': 'true'}
        ]
        resp = bot.place_batch_order(batch_orders)
        show_response(resp)

elif order_type == "TWAP Order":
    st.subheader("TWAP Order")
    symbol = st.text_input("Symbol")
    side = st.radio("Side", ["BUY", "SELL"])
    total_quantity = st.number_input("Total Quantity", min_value=0.0, format="%.3f")
    duration_minutes = st.number_input("Duration (minutes)", min_value=1, step=1)
    num_orders = st.number_input("Number of Sub-Orders", min_value=1, step=1)
    if st.button("Start TWAP Execution"):
        qty_per_order = total_quantity / num_orders
        interval_sec = (duration_minutes * 60) / num_orders
        st.info(f"Plan: {num_orders} orders, {qty_per_order:.6f} each, every {interval_sec:.2f}s")
        for i in range(num_orders):
            order_details = {'symbol': symbol, 'side': side, 'type': 'MARKET', 'quantity': qty_per_order}
            resp = bot.place_order(order_details)
            show_response(resp)

elif order_type == "Grid Order":
    st.subheader("Grid Order")
    symbol = st.text_input("Symbol")
    lower_price = st.number_input("Lower Price", min_value=0.0, format="%.2f")
    upper_price = st.number_input("Upper Price", min_value=0.0, format="%.2f")
    num_grids = st.number_input("Number of Grid Lines", min_value=2, max_value=11, step=1)
    qty_per_grid = st.number_input("Quantity per Grid", min_value=0.0, format="%.3f")
    if st.button("Place Grid Orders"):
        current_price = bot.get_current_price(symbol)
        price_step = (upper_price - lower_price) / (num_grids - 1)
        grid_prices = [lower_price + i * price_step for i in range(num_grids)]
        batch_orders = []
        for price in grid_prices:
            side = "BUY" if price < current_price else "SELL"
            batch_orders.append({'symbol': symbol, 'side': side, 'type': 'LIMIT',
                                 'timeInForce': 'GTC', 'quantity': str(qty_per_grid),
                                 'price': f"{price:.2f}"})
        resp = bot.place_batch_order(batch_orders)
        show_response(resp)
