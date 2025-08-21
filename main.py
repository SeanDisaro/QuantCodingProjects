from scriptsForDailyRun.plotCDFStockPrices import *
import os

try:
    api_key = os.environ["OPENAI_API_KEY"]
except:
    api_key = None
if __name__ == "__main__":
    plotCDFStockPrices()
    print(api_key[:2])