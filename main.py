import asyncio
import ccxt.pro as ccxtpro

EXCHANGES = {
    'bybit':    'BTC/USDT',
    'coinbase': 'BTC/USD',
    'kraken':   'BTC/USDT',
}

MIN_POURCENTAGE_SPREAD = 0.005
STARTING_MONEY = 200000
prices = {}

async def watch_exchange(name, symbol):
    exchange = getattr(ccxtpro, name)({
        'enableRateLimit': True,
        'timeout': 30_000,
    })
    retry_delay = 1
    try:
        while True:
            try:
                ticker = await exchange.watch_ticker(symbol)
                prices[name] = ticker['last']
                print(f"[{name}] {symbol} = {ticker['last']}")  # <-- debug
                retry_delay = 1
                check_arbitrage()
            except ccxtpro.NetworkError as e:
                print(f"Network error on {name}: {e} — retry in {retry_delay}s")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)
            except Exception as e:
                print(f"Error on {name}: {e}")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)
    finally:
        await exchange.close()

def check_arbitrage():
    if len(prices) < 2:
        return
    names = list(prices.keys())
    for i in names:
        for j in names:
            if i == j:
                continue
            price_i = prices[i]
            price_j = prices[j]
            spread = abs(price_i - price_j)
            reference_price = max(price_i, price_j)
            percentage_spread = spread / reference_price
            if percentage_spread > MIN_POURCENTAGE_SPREAD:
                fee = reference_price * 0.0025 * 2
                profit = spread - fee
                print(
                    f"ARBITRAGE {i} vs {j} | "
                    f"spread: {percentage_spread:.4%} | "
                    f"profit: {profit:.2f} | "
                    f"capital: {STARTING_MONEY:.2f}"
                )

async def main():
    tasks = [watch_exchange(name, symbol) for name, symbol in EXCHANGES.items()]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
