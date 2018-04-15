from datetime import datetime
import requests,json,re,time,logging,sys,ccxt,asyncio,asyncio_mongo

'''
Gather.py

-Requirements:
Python 3.5+ for asyncio
MongoDB instance up at 127.0.0.1:27017, with no auth

-Start:
python prodVol.py *exchange_name* //Recommeneded one exchange at per loader

-Synopsis: This is the python script that will do that basic gathering of the exchange data and update a local mongoDB instance of the information that it currently has. 
'''


@asyncio.coroutine
def orderBookData():
    '''
    This function gathers the orderBookData for all the BTC pairs and adds them to the local MongoDB.
    It will do this infinitly 
    -Input: None
    -Output: True
    '''
    #Setup DB connection
    client = yield from asyncio_mongo.Connection.create('localhost', 27017)
    db=client.ccxt_coins
    ex_list=[sys.argv[1]]
    while True:
        try:
            for exchange_name in ex_list:
                id = exchange_name
                exchange = eval ('ccxt.%s ({"enableRateLimit": True})' % id) 
                markets = exchange.load_markets ()
                for symbol in markets:
                    #Data is the orderbook
                    rg=re.compile('.*?(BTC)',re.IGNORECASE|re.DOTALL)
                    m=rg.search(symbol)
                    if m:
                        data = exchange.fetch_order_book (symbol)
                    else:
                        continue
                        
                    #Below calculate the amount of given cur being bought
                    for ask in data['asks']:
                        asks=asks+float(ask[0] * ask[1])
                    for bid in data['bids']:
                        bids=bids+float(bid[0] * bid[1])
                        
                    #Gather Ticker Information
                    ticker=exchange.fetch_ticker (symbol)
                    #Set BTC volume
                    #TODO
                    #Write query to run to gather average based on timestamp
                    #Write insert that conforms to standard layed out in destiney.md
                    if (ticker['quoteVolume']):
                        btc_volume=ticker['quoteVolume']
                    else:
                        btc_volume=ticker['baseVolume']
                    #Set last Price
                    last=ticker['last']
                    cur_bid=ticker['bid']
                    cur_ask=ticker['ask']
                    #Check if coinPair already in DB, if present update instead of insert new doc, else insert new doc
                    cursor = yield from db.posts.find({"name":symbol,'values.exchange':id})
                    if cursor:
                        #do update
                        post_id=yield from db.posts.update({'name':symbol},{"$set":{'values.cur_bid':cur_bid,'values.cur_ask':cur_ask,'values.bidVol':bids,'values.last':last,'values.quoteVol':btc_volume,'values.timeStamp':datetime.fromtimestamp(int(time.time()))}},safe=True)
                    else:
                        #do insert
                        post_id=yield from db.posts.insert({'name':symbol, 'values':{'cur_bid':cur_bid,'cur_ask':cur_ask,'exchange':id,'last':last,'quoteVol':btc_volume,'timeStamp':datetime.fromtimestamp(int(time.time()))}},safe=True)
        except Exception as e:
            logging.error(e)
            logging.error('Unable to work in MongoDB, is it running? Command: sudo docker run --name coins-mongo -v /opt/mongodb:/data/db -p 27017:27017 -d mongo:3.6.0-jessie')
            logging.error('Test Docker container: docker exec -it coins-mongo mongo admin')
            logging.error('Test Connection to MongoDB. Command: mongo 127.0.0.1:27017')
            time.sleep(10)
            
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(orderBookData())
