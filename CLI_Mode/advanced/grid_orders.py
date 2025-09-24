from ..client import BinanceBotClient
import math

def get_user_input():
    """Gets and validates user input for a Grid order."""
    print("--- Place a New Grid of Orders ---")
    print("This places buy orders below and sell orders above the current price.")
    
    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    
    while True:
        try:
            lower_price = float(input("Enter the lower price boundary of the grid: "))
            upper_price = float(input("Enter the upper price boundary of the grid: "))
            if lower_price > 0 and upper_price > lower_price:
                break
            print("Prices must be positive, and upper price must be greater than lower price.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    while True:
        try:
            num_grids = int(input("Enter the number of grid lines (e.g., 5): "))
            # Binance batch order limit is 10 for futures, so num_grids-1 should be <= 10
            if 2 <= num_grids <= 11: 
                break
            print("Number of grids must be between 2 and 11.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    while True:
        try:
            quantity_per_grid = float(input("Enter the quantity for each grid order: "))
            if quantity_per_grid > 0:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    return {
        'symbol': symbol, 'lower_price': lower_price, 'upper_price': upper_price,
        'num_grids': num_grids, 'quantity_per_grid': quantity_per_grid
    }

def main():
    try:
        params = get_user_input()
        bot = BinanceBotClient(testnet=True)
        
        current_price = bot.get_current_price(params['symbol'])
        if not current_price:
            print("Could not determine current market price. Exiting.")
            return

        print(f"\n--- Grid Placement Plan ---")
        print(f"  Range: {params['lower_price']} - {params['upper_price']}")
        print(f"  Current Price: {current_price}")
        print("---------------------------\n")

        price_step = (params['upper_price'] - params['lower_price']) / (params['num_grids'] - 1)
        grid_prices = [params['lower_price'] + i * price_step for i in range(params['num_grids'])]
        
        batch_orders = []
        for price in grid_prices:
            # Round price to a reasonable precision for futures
            price_str = f"{price:.2f}" 
            if price < current_price:
                # Place a BUY order below current price
                order_type = 'BUY'
            elif price > current_price:
                # Place a SELL order above current price
                order_type = 'SELL'
            else:
                continue # Skip placing an order at the exact current price

            batch_orders.append({
                'symbol': params['symbol'],
                'side': order_type,
                'type': 'LIMIT',
                'timeInForce': 'GTC',
                'quantity': str(params['quantity_per_grid']),
                'price': price_str
            })
            
        if not batch_orders:
            print("No valid grid orders to place. Current price might be outside your grid range.")
            return
            
        print(f"Preparing to place {len(batch_orders)} grid orders.")
        bot.place_batch_order(batch_orders)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()