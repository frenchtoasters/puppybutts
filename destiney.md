# DEX CMC

## Components

This section outlines the key components in the DEX CMC design

* Distributed database using some blockchain
	- Only used for historical purposes aka website chart shit

* Compute nodes
	- These are the resources that are being staked by the "community" aka master nodes. 
	- We should also look to run some of these our selves for stability and so that the the front end website we would host would also pull only from these nodes, with option to fork the site your self and select other nodes from which to request computation from.

* Website
	- This is where we demonstrate how all of our api calls work, well most of them
	- Main page is a filtered query that is simply the top 100 coins sorted by volume. 
		- /v1/api/query/{$JSONDATA}
			- $JSONDATA= 
				{
					"jsonrpc": '2.0/3.0/newestversion',
					"method": 'coins.query',
					"params": {
		- /v1/api/....


## How it will work

This section outlines the high level over view of what we are trying to accomplish.

* Functionally will be a distributed source of validated, open sourced, and computaionally secure price index of major crypto currencies. First focused on high value coins in the design phase with the idea in mind to make this ability to add coins community based on voteing by masternode owners. 
	- With a similar system for improvments to the site or api like XMR has.   

* This will be a meta eco-system that is run by masternode owners and the X foundation. With the option to crowad source other features to just be added without a masternode owners vote, you will have to pay a steep few though. 

* Enhancments/Bounty/BugFix program will be similar to XMR once implemented, in that the community will be able to post job's for people to implement shit into the stack, like adding new currency pair to api response for marketcap or 24hourVol.

* Miners/masternodes, will run all computation for the network. This means that all the queries that the foundation will run in order maintain the core top 100 coins will be computed by these nodes.  
	- There will be two type of compute nodes
		- Poller (masternode)
			- These are the nodes that will have all the queries run against them. They will tasked with getting new information from the supported exchanges. These are the smart contract type things that when activated will do a thing like poll a supported exchange for a supported pairing and package the results into JSON... 
		- HistorySyncer (mining node)
			- These run the queries against the all the supported exchanges.
			- Each miner will have a task of quering/listening to all supported exchanges.
			- Each time a new query is put on the stack the miner will run the query.
			- After results have been processed by the miners they verify that the all got the same cryptographic signature(process that is done to compress the data into a hash value) and come to consensus(all the miners got the same hash value) that the value is correct for all of them. A new block is found and the value that was found is written to the DB, the lucky node that gets to write it to the db gets some write bonus tbd, that is paid in the token.  
		

* All this will really be is:
	- Website, that displays query of top 100 coins, with search feature
	- Database, this is a huge thing to think about but simplified it will hold the information of each coin
	- API(Query Engine), this will simplly send a request to the computation nodes which will exectue the given DB query and return that results in a JSONRPC format
	
### DATABASE

This section outlines the layout for the mongoDB:

- Per coin

```
{
	"Data":
		{
			"pair":"BTC/USD",
			"avgUSD":9999.99,
			"24hrVolBTC": 100000.00000000,
			"24hrVolUSD": 100000.00,
			"MarketCapUSD": 111111111111,
			"CirculatingSupply": 16958162,
			"24hrChg%": 50,
			"Soucres": [
				"exch1": link to exch1 query on github,
				"exch2": link to exch2 query on github,
				...
			],
			"lastupdate": 1522880301,
		}
}
```

- 
			
