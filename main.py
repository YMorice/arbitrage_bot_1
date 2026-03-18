# Librairies Importation
import asyncio
import ccxt.pro as ccxtpro

# List of exchanges
exchanges = ['binance', 'coinbase', 'kraken']

# List of symbols
symbols = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'BNB/USDT', 'SOL/USDT']

async def main():
    for i in exchanges:
        exchange = getattr(ccxtpro, i)()
        ticker = await exchange.watch_ticker('BTC/USDT')
        print(ticker)

asyncio.run(main())