import time
from ..client import BinanceBotClient

def get_user_input():
    """Gets and validates user input for a TWAP order."""
    print("--- Place a New TWAP Order ---")
    print("This strategy breaks a large order into smaller chunks over time.")
    
    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    
    while True:
        side = input("Enter side (BUY or SELL): ").upper()
        if side in ['BUY', 'SELL']:
            break
        print("Invalid side.")
        
    while True:
        try:
            total_quantity = float(input("Enter total quantity to execute: "))
            if total_quantity > 0:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    while True:
        try:
            duration_minutes = int(input("Enter total duration in MINUTES: "))
            if duration_minutes > 0:
                break
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            
    while True:
        try:
            num_orders = int(input("Enter number of smaller orders to place: "))
            if num_orders > 0:
                break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    return {
        'symbol': symbol, 'side': side, 'total_quantity': total_quantity,
        'duration_minutes': duration_minutes, 'num_orders': num_orders
    }

def main():
    try:
        params = get_user_input()
        
        # Calculate order parameters
        quantity_per_order = params['total_quantity'] / params['num_orders']
        interval_seconds = (params['duration_minutes'] * 60) / params['num_orders']
        
        print("\n--- TWAP Execution Plan ---")
        print(f"  Total Quantity: {params['total_quantity']} {params['symbol']}")
        print(f"  Number of Orders: {params['num_orders']}")
        print(f"  Quantity per Order: {quantity_per_order:.8f}")
        print(f"  Interval: {interval_seconds:.2f} seconds")
        print("---------------------------\n")

        bot = BinanceBotClient(testnet=True)
        
        for i in range(params['num_orders']):
            print(f"Placing order {i+1}/{params['num_orders']}...")
            order_details = {
                'symbol': params['symbol'],
                'side': params['side'],
                'type': 'MARKET',
                'quantity': quantity_per_order
            }
            bot.place_order(order_details)
            
            if i < params['num_orders'] - 1:
                print(f"Waiting for {interval_seconds:.2f} seconds...")
                time.sleep(interval_seconds)
                
        print("\n✅ TWAP execution finished.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()