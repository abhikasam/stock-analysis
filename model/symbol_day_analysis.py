from datetime import date
from typing import Union
import re

class SymbolDayAnalysis:
    def __init__(self):
        self.symbol:str=''
        self.day:Union[date,None]=None
        self.open:float=0
        self.high:float=0
        self.low:float=0
        self.close:float=0
        self.volume:int=0
