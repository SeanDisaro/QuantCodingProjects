from scriptsForDailyRun.plotCDFStockPrices import *
from scriptsForDailyRun.getNewsSummary import *
import os

try:
    api_key = os.environ["OPENAI_API_KEY"]
except:
    api_key = None


if __name__ == "__main__":
    plotCDFStockPrices()
    createSummaryAndRating(api_key)