from ..client import BinanceBotClient

def get_user_input():
    """Gets and validates user input for an OCO order with hints."""
    print("--- Place a New OCO (One-Cancels-the-Other) Order ---")
    print("This places a Take Profit and a Stop Loss at the same time.")
    print("First, check the current market price of your symbol.")
    
    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    
    while True:
        side = input("Enter side to CLOSE the position (BUY or SELL): ").upper()
        if side in ['BUY', 'SELL']:
            break
        print("Invalid side. Please enter 'BUY' or 'SELL'.")

    while True:
        try:
            quantity = float(input("Enter quantity to close: "))
            if quantity > 0:
                break
            print("Quantity must be a positive number.")
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            
    while True:
        try:
            if side == 'SELL':
                prompt = "Enter Take Profit price (must be ABOVE current market): "
            else: # BUY
                prompt = "Enter Take Profit price (must be BELOW current market): "
            take_profit_price = float(input(prompt))
            if take_profit_price > 0:
                break
            print("Price must be a positive number.")
        except ValueError:
            print("Invalid price. Please enter a number.")

    while True:
        try:
            if side == 'SELL':
                prompt = "Enter Stop Loss price (must be BELOW current market): "
            else: # BUY
                prompt = "Enter Stop Loss price (must be ABOVE current market): "
            stop_loss_price = float(input(prompt))
            if stop_loss_price > 0:
                break
            print("Price must be a positive number.")
        except ValueError:
            print("Invalid price. Please enter a number.")

    return {
        'symbol': symbol, 
        'side': side, 
        'quantity': quantity, 
        'take_profit_price': take_profit_price, 
        'stop_loss_price': stop_loss_price
    }

def main():
    try:
        user_order = get_user_input()

        bot = BinanceBotClient(testnet=True)
        
        batch_orders = [
            {
                'symbol': user_order['symbol'],
                'side': user_order['side'],
                'type': 'TAKE_PROFIT_MARKET',
                'quantity': str(user_order['quantity']),
                'stopPrice': str(user_order['take_profit_price']),
                'reduceOnly': 'true'
            },
            {
                'symbol': user_order['symbol'],
                'side': user_order['side'],
                'type': 'STOP_MARKET',
                'quantity': str(user_order['quantity']),
                'stopPrice': str(user_order['stop_loss_price']),
                'reduceOnly': 'true'
            }
        ]
        
        bot.place_batch_order(batch_orders)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()