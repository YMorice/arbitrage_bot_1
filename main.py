import asyncio
import ccxt.pro as ccxtpro
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

exchanges = ['binance', 'coinbase', 'kraken']
symbols = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'BNB/USDT', 'SOL/USDT']

POURCENTAGE_OF_ERROR = 0.02
MIN_POURCENTAGE_SPREAD = 0.005
STARTING_MONEY = 200000

async def main():
    instances = {name: getattr(ccxtpro, name)() for name in exchanges}
    try:
        while True:
            for i in exchanges:
                for j in exchanges:
                    if i == j:
                        continue
                    try:
                        ticker1 = await instances[i].watch_ticker('BTC/USDT')
                        ticker2 = await instances[j].watch_ticker('BTC/USDT')

                        price1 = ticker1['last']
                        price2 = ticker2['last']

                        spread = abs(price1 - price2)
                        reference_price = max(price1, price2)
                        percentage_spread = spread / reference_price

                        if percentage_spread > MIN_POURCENTAGE_SPREAD:
                            fee = reference_price * 0.0025 * 2  # fee on both sides
                            profit = spread - fee
                            STARTING_MONEY += profit
                            log.info(f"{i} vs {j} | spread: {percentage_spread:.4%} | profit: {profit:.2f} | capital: {STARTING_MONEY:.2f}")

                    except Exception as e:
                        log.error(f"Error on {i} vs {j}: {e}", exc_info=True)
    finally:
        for exchange in instances.values():
            await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())