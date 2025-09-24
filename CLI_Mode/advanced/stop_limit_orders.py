from ..client import BinanceBotClient

def get_user_input():
    """Gets and validates user input for a stop-limit order with hints."""
    print("--- Place a New Stop-Limit Order ---")
    print("First, check the current market price of your symbol.")
    
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
            
    while True:
        try:
            if side == 'BUY':
                prompt = "Enter trigger/stop price (must be ABOVE current market): "
            else: # SELL
                prompt = "Enter trigger/stop price (must be BELOW current market): "
            stop_price = float(input(prompt))
            if stop_price > 0:
                break
            print("Stop price must be a positive number.")
        except ValueError:
            print("Invalid price. Please enter a number.")
            
    while True:
        try:
            price = float(input("Enter limit price (the price your order will be placed at): "))
            if price > 0:
                break
            print("Price must be a positive number.")
        except ValueError:
            print("Invalid price. Please enter a number.")

    return {'symbol': symbol, 'side': side, 'quantity': quantity, 'price': price, 'stop_price': stop_price}

def main():
    try:
        user_order = get_user_input()

        order_details = {
            'symbol': user_order['symbol'],
            'side': user_order['side'],
            'type': 'STOP',  
            'timeInForce': 'GTC', 
            'quantity': user_order['quantity'],
            'price': user_order['price'],
            'stopPrice': user_order['stop_price']
        }
        
        bot = BinanceBotClient(testnet=True)
        bot.place_order(order_details)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()