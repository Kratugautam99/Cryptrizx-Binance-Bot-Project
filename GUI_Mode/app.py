# frontend/app.py
import streamlit as st
import sys
import os

# --- Add backend path ---
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "CLI_Mode"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
from client import BinanceBotClient

# --- Page Config ---
st.set_page_config(
    page_title="Cryptrizx_Binance_Bot",
    page_icon="https://raw.githubusercontent.com/Kratugautam99/Cryptrizx-Binance-Bot-Project/main/images/icon.png",
    layout="centered",
)

# --- Custom CSS for background and styling ---
st.markdown(
    """
    <style>
    /* Background image */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/Kratugautam99/Cryptrizx-Binance-Bot-Project/main/images/bg.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Card container for forms */
    .form-card {
        background: rgba(0,0,0,0.7);
        border-radius: 15px;
    }

    /* Sidebar */
    .sidebar .css-1d391kg {
        background-color: rgba(0,0,0,0.8);
        color: #fff;
        padding: 1rem;
        border-radius: 10px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #ff8c00, #ffa500);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease-in-out;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ffa500, #ff4500);
        transform: scale(1.05);
    }

    /* Inputs + Select + Radio */
    input[type="text"], input[type="password"], input[type="number"], select, textarea {
        border-radius: 10px;
        padding: 0.4rem;
        border: 1px solid cyan;
        background-color: #222;
        color: #fff !important;
    }
    input:hover, select:hover, textarea:hover {
        border-color: red;
        box-shadow: 0 0 5px #ff8c00;
    }

    .stSidebar {
        background: linear-gradient(180deg, rgba(1,10,20,0.88), rgba(0,0,0,0.82));
        border-left: 1px solid rgba(255,255,255,0.02);
        padding-top: 20px;
    }
    .sidebar .css-1d391kg, .stSidebar .block-container {
        background: linear-gradient(180deg, rgba(12,18,24,0.75), rgba(6,10,18,0.66));
        border-radius: 12px;
        padding: 14px;
        box-shadow: inset 0 2px 8px rgba(255,255,255,0.01);
    }

    /* API header inside sidebar */
    .api-card {
        background: linear-gradient(90deg, rgba(255,154,0,0.12), rgba(0,230,255,0.06));
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        border: 1px solid rgba(255,255,255,0.03);
        font-weight: 800;
    }
    .api-card h3 { margin: 0; font-size: 16px; color: #fff; }
    .api-card p { margin: 6px 0 0 0; font-size: 12px; color: rgba(230,255,249,0.9); }

    /* Connect button in sidebar with distinct style */
    .stSidebar .stButton>button {
        background: linear-gradient(90deg,#ffb86b 0%, #ff8c00 100%);
        color: #1b0600;
        font-weight: 900;
        border-radius: 10px;
        padding: 0.55rem 0.95rem;
        width: 100%;
    }

    /* API Key input border */
    div[data-baseweb="input"] input[aria-label="Binance API Key"] {
        border: 2px solid olive !important;
        border-radius: 10px !important;
        background-color: #111 !important;
        color: #fff !important;
        padding: 6px !important;
    }

    /* API Secret input border */
    div[data-baseweb="input"] input[aria-label="Binance API Secret"] {
        border: 2px solid magenta !important;
        border-radius: 10px !important;
        background-color: #111 !important;
        color: #fff !important;
        padding: 6px !important;
    }

    /* Radio buttons */
    div[role="radiogroup"] label {
        background: rgba(255, 165, 0, 0.2);
        padding: 6px 12px;
        margin: 3px;
        border-radius: 8px;
        cursor: pointer;
    }
    div[role="radiogroup"] label:hover {
        background: rgba(255, 140, 0, 0.4);
    }

    /* Style the selectbox for order type */
    .stSelectbox > div[data-baseweb="select"] {
        border: 2px solid grey !important; /* orange border */
        border-radius: 12px !important;
        background-color: teal !important;
        color: #fff !important;
        font-weight: bold !important;
        padding: 6px !important;
        font-size: 16px !important;
    }
    .stSelectbox:hover > div[data-baseweb="select"] {
        border-color: black !important;
        box-shadow: 0 0 8px cyan !important;
    }


    /* Error box styling */
    .stAlert {
        border: 2px solid red;
        border-radius: 10px;
        background: rgba(255,0,0,0.15);
        color: #ff4c4c !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True
)

# Top layout with logo + title
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("https://raw.githubusercontent.com/Kratugautam99/Cryptrizx-Binance-Bot-Project/main/images/icon.png", width=180)
    except Exception:
        st.markdown("<div style='font-size:48px'>https://raw.githubusercontent.com/Kratugautam99/Cryptrizx-Binance-Bot-Project/main/images/icon.png</div>", unsafe_allow_html=True)
with col2:
    st.markdown('''<div class="header-card">
<h1 style="color: silver; margin:0">Cryptrizx-Binance-Bot</h1>
<p style="margin:0; color:yellow;">Created by Kratu Gautam</p>
</div>''', unsafe_allow_html=True)
    

# --- API Credentials ---
st.sidebar.markdown(
    """
    <div class="api-card">
      <h3>🔑 API Credentials</h3>
      <p>Enter your Binance API key & secret below. Get api credentials @ "https://testnet.binancefuture.com"</p>
    </div>
    """,
    unsafe_allow_html=True,
)
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
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.subheader("🎯 Choose Order Type")
order_type = st.selectbox(
    "........................................................................................................................................................................................................",
    ["🏬 Market Order", "⛳ Limit Order", "🪢 Stop-Limit Order", "🎲 OCO Order", "🛠️ TWAP Order", "🧭 Grid Order"]
)
st.markdown('</div>', unsafe_allow_html=True)

# --- Input Forms per Order ---
order_details = None

# Function to handle order response
def show_response(resp, error=None):
    if resp:
        if isinstance(resp, list):  # batch orders
            st.success("✅ Batch Order(s) Placed Successfully!")
            for i, order in enumerate(resp, start=1):
                if 'orderId' in order:
                    st.markdown(
                        f"**Sub-Order {i}:**\n"
                        f"- Symbol: {order['symbol']}\n"
                        f"- Order ID: {order['orderId']}\n"
                        f"- Type: {order['type']}\n"
                        f"- Side: {order.get('side', 'N/A')}\n"
                        f"- Quantity: {order.get('origQty', 'N/A')}\n"
                        f"- Status: {order['status']}"
                    )
                else:  # failed sub-order
                    st.error(f"❌ Sub-Order {i} Failed: {order.get('msg')}")
        else:  # single order
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
        st.error(error or "❌ Failed to place order. Check logs.")


if order_type == "🏬 Market Order":
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.subheader("Market Order")
    symbol = st.text_input("Symbol (e.g., BTCUSDT)")
    side = st.radio("Side", ["BUY", "SELL"])
    quantity = st.number_input("Quantity", min_value=0.0, format="%.2f")
    if st.button("Place Market Order"):
        order_details = {'symbol': symbol, 'side': side, 'type': 'MARKET', 'quantity': quantity}
        resp, error = bot.place_order(order_details)
        show_response(resp, error)
    st.markdown('</div>', unsafe_allow_html=True)

elif order_type == "⛳ Limit Order":
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.subheader("Limit Order")
    symbol = st.text_input("Symbol (e.g., ETHUSDT)")
    side = st.radio("Side", ["BUY", "SELL"])
    quantity = st.number_input("Quantity", min_value=0.0, format="%.3f")
    price = st.number_input("Limit Price", min_value=0.0, format="%.2f")
    if st.button("Place Limit Order"):
        order_details = {'symbol': symbol, 'side': side, 'type': 'LIMIT',
                         'timeInForce': 'GTC', 'quantity': quantity, 'price': price}
        resp, error = bot.place_order(order_details)
        show_response(resp, error)
    st.markdown('</div>', unsafe_allow_html=True)

elif order_type == "🪢 Stop-Limit Order":
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
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
        resp, error = bot.place_order(order_details)
        show_response(resp, error)
    st.markdown('</div>', unsafe_allow_html=True)

elif order_type == "🎲 OCO Order":
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
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
        resp, error = bot.place_batch_order(batch_orders)
        show_response(resp, error)
    st.markdown('</div>', unsafe_allow_html=True)

elif order_type == "🛠️ TWAP Order":
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
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
            resp, error = bot.place_order(order_details)
            show_response(resp, error)
    st.markdown('</div>', unsafe_allow_html=True)

elif order_type == "🧭 Grid Order":
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
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
        resp, error = bot.place_batch_order(batch_orders)
        show_response(resp, error)
    st.markdown('</div>', unsafe_allow_html=True)
