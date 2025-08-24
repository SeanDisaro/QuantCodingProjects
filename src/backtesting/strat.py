import numpy as np
import pandas as pd
import abc

class Strategy(object):
    def __init__(self):
        pass
    

    @abc.abstractmethod
    def updatePortfolio(self, oldPortfolio, cash, pricesAssets, assets):
        return oldPortfolio