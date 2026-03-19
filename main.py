import asyncio
import ccxt.pro as ccxtpro

# Coinbase utilise USD, pas USDT. BNB n'est pas listé sur Coinbase ni Kraken.
EXCHANGE_SYMBOLS = {
    'bybit': [
        'BTC/USD', 'ETH/USD', 'BNB/USD', 'XRP/USD', 'SOL/USD'
    ],
    'coinbase': [
        'BTC/USD',  'ETH/USD',                'XRP/USD',  'SOL/USD'
    ],
    'kraken': [
        'BTC/USD', 'ETH/USD',               'XRP/USD', 'SOL/USD'
    ],
}

MIN_POURCENTAGE_SPREAD = 0.005
STARTING_MONEY = 200_000

# prices[base_asset][exchange] = last_price
# ex: prices['BTC']['bybit'] = 84000.0
prices = {}

def normalize_symbol(symbol):
    """Extrait le base asset : 'BTC/USDT' -> 'BTC'"""
    return symbol.split('/')[0]

async def watch_exchange(exchange_name, symbols):
    exchange = getattr(ccxtpro, exchange_name)({
        'enableRateLimit': True,
        'timeout': 30_000,
    })
    retry_delay = 1
    try:
        while True:
            try:
                tasks = [watch_symbol(exchange, exchange_name, s) for s in symbols]
                await asyncio.gather(*tasks)
            except ccxtpro.NetworkError as e:
                print(f"Network error on {exchange_name}: {e} - retry in {retry_delay}s")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)
            except Exception as e:
                print(f"Error on {exchange_name}: {e}")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)
    finally:
        await exchange.close()

async def watch_symbol(exchange, exchange_name, symbol):
    base = normalize_symbol(symbol)
    retry_delay = 1
    while True:
        try:
            ticker = await exchange.watch_ticker(symbol)
            price = ticker['last']
            if base not in prices:
                prices[base] = {}
            prices[base][exchange_name] = price
            print(f"[{exchange_name}] {symbol} = {price}")
            retry_delay = 1
            check_arbitrage(base)
        except ccxtpro.NetworkError as e:
            print(f"Network error on {exchange_name}/{symbol}: {e} - retry in {retry_delay}s")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)
        except Exception as e:
            print(f"Error on {exchange_name}/{symbol}: {e}")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)

def check_arbitrage(base):
    global STARTING_MONEY
    asset_prices = prices.get(base, {})
    if len(asset_prices) < 2:
        return
    exchanges = list(asset_prices.keys())
    for i in exchanges:
        for j in exchanges:
            if i == j:
                continue
            price_i = asset_prices[i]
            price_j = asset_prices[j]
            spread = abs(price_i - price_j)
            reference_price = max(price_i, price_j)
            percentage_spread = spread / reference_price
            if percentage_spread > MIN_POURCENTAGE_SPREAD:
                fee = reference_price * 0.001
                profit = spread - fee
                STARTING_MONEY += profit
                print(
                    f"ARBITRAGE {base} | {i} vs {j} | "
                    f"spread: {percentage_spread:.4%} | "
                    f"profit: {profit:.2f} | "
                    f"capital: {STARTING_MONEY:.2f}"
                )

async def main():
    tasks = [
        watch_exchange(name, symbols)
        for name, symbols in EXCHANGE_SYMBOLS.items()
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
