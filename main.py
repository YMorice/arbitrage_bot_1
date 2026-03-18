# Librairies Importation
import asyncio
import ccxt.pro as ccxtpro

# List of exchanges
exchanges = ['binance', 'coinbase', 'kraken']

# List of symbols
symbols = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'BNB/USDT', 'SOL/USDT']

async def main():
    for i in exchanges:
        exchange = ccxtpro.i()
        while True:
            ticker = await exchange.watch_ticker('BTC/USDT')
            print(ticker)  # Live updates!
        await exchange.close()

asyncio.run(main())