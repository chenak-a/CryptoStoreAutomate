from __future__ import annotations

import os
import time

from binance.client import Client
from dotenv import load_dotenv

from package.crypto import Coin, Crypto
from package.datastore import Datastore
from package.strategyBuySell import BuySellLongTerm, BuySellmidTerm
from package.user import User

load_dotenv('/Users/chena/AI/ai/.idea/.env')
class Controller: 
    #short cut to long to write dont ask question
    HOUR1H = Client.KLINE_INTERVAL_1HOUR
    HOUR4H = Client.KLINE_INTERVAL_4HOUR
    HOUR1D = Client.KLINE_INTERVAL_1DAY
    def __init__(self) -> None:
        self.user : dict[str,User] = {}
        self.store = Crypto("store")
        self.store.parent = None
    
        Datastore(Client(api_key=os.getenv("APIKEY"),
                        api_secret=os.getenv("APISEC")))
        
    def addUser(self ,Username ,api_key , api_secret) -> Controller:
        self.user[Username] = User(api_key,api_secret)
        return self
    
    def getbalance(self,user) -> Controller:
        self.user[user].balance()
        return self
    def addcoinUser(self,user:str,name :str) -> Controller:
     
        Datastore().connectUserandcoin(name,self.user[user])
        self.user[user].addAsset(name)
        
        
        return self
    def removecoinUser(self,user,name) -> Controller:
        self.user[user].removeAsset(name)
        return self
    def addcoin(self , name : str) -> Controller:
        name = name.upper()
        val = Crypto(name)
      
        Datastore().addcoin(val)
        val.add(Coin(name + self.HOUR1H,self.HOUR1H,BuySellmidTerm()))
        val.add(Coin(name + self.HOUR4H,self.HOUR4H,BuySellmidTerm()))
        val.add(Coin(name + self.HOUR1D,self.HOUR1D,BuySellmidTerm()))
        self.store.add(val)
        return self
    
    def data(self,name:str = "",hour :str = "") -> Controller:
      
        if name is not "":
            print("dsa")
            self.store.getcoin(name,name+hour)
        else :
            print("dsacc")
            self.store.data()
        return self
    
    def getjson(self,name:str = "",hour :str = ""):
        self.store.getcoin(name,name+hour)
def run():
    run = Controller()
    run.addUser("me",api_key=os.getenv("APIKEY"),api_secret=os.getenv("APISEC"))
    run.addcoin("FETUSDT").addcoin("IOTAUSDT")
    run.addcoinUser("me","FETUSDT").getbalance("me").data() 
    
if __name__ == '__main__':
    start_time = time.time()
    run()
    print("--- %s seconds ---" % (time.time() - start_time))
   
    

    