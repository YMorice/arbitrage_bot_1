# Librairies Importation
import asyncio
import ccxt.pro as ccxtpro

# List of exchanges
exchanges = ['binance', 'coinbase', 'kraken']

# List of symbols
symbols = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'BNB/USDT', 'SOL/USDT']

# List parameters
POURCENTAGE_OF_ERROR = 0.02
MIN_POURCENTAGE_SPREAD = 0.005
STARTING_MONEY = 200000

# Main definition
def main():
    while True:
        try : 
        for i in exchanges:
            for j in exchanges:
                exchange1 = getattr(ccxtpro, i)()
                exchange2 = getattr(ccxtpro, j)()
                ticker1 = await exchange.watch_ticker('BTC/USDT')
                ticker2 = await exchange.watch_ticker('BTC/USDT')
                spread = 0
                if ticker1['last'] >= ticker2['last']:
                    spread = ticker1['last'] - ticker2['last']
                    POURCENTAGE_SPREAD = spread*100/ticker1['last']
                    if MIN_POURCENTAGE_SPREAD < POURCENTAGE_SPREAD :
                        
                else :
                    spread = ticker2['last'] - ticker1['last']
                    spread*100/ticker2['last']


        except Exception as e:
            log.error(f"Unexpected error in main loop: {e}", exc_info=True)