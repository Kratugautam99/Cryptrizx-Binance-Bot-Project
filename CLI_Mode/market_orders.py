from client import BinanceBotClient

def get_user_input():
    """Gets and validates user input for a market order."""
    print("--- Place a New Market Order ---")
    
    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    
    while True:
        side = input("Enter side (BUY or SELL): ").upper()
        if side in ['BUY', 'SELL']:
            break
        print("Invalid side. Please enter 'BUY' or 'SELL'.")
        
    while True:
        try:
            quantity = float(input("Enter quantity: "))
            if quantity > 0:
                break
            print("Quantity must be a positive number.")
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            
    return {'symbol': symbol, 'side': side, 'quantity': quantity}

def main():
    try:
        user_order = get_user_input()
        
        order_details = {
            'symbol': user_order['symbol'],
            'side': user_order['side'],
            'type': 'MARKET',
            'quantity': user_order['quantity']
        }
        
        bot = BinanceBotClient(testnet=True)
        bot.place_order(order_details)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()