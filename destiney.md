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

* Should be noted that there will be a foundation that gets part of all the block reward like XMR foundation and shit you know 
	
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

- Distributed Ledger to provide a decentralized multi-version concurrency control mechanism and status of shared facts in trustless environment. 
	- How this will work
		- You will have writers that are trusted nodes wallet addresses that are allow to run certian functions in your smart contract. Just require that to send the contract a request you send your address, then access the address[] values.

```
pragma solidity 0.4.20;
contract poopyIndex {
    address public owner;
	uint256 public contractCost;
	uint256 public contractVal;
	uint256 public incrementingVal;
	uint256 public MAX_ALLOWED_INT_SIZE = 100;
	//This defines an array of address type... aka array of eth addresses
	address[] public writerNodeAddresses;

	//Each address sends a payload with them that maps to the below
	struct write {
		uint256 avgUSD;
		uint256 24hrVolBTC;
	}

    // The address of the writer and => the user info   
    mapping(address => writer) public writerInfo;

	//Constructor
    function poopyIndex(uint256 _*) public {
		//_* == wildcard
		//dont know what values will be needed on start yet leaving open ended atm
		//would need init the mongoDB stuff here
		//would set one of the values 
       	owner = msg.sender;
	
		//Ex. of thing to do here maybe validation?
       	if(_* != 0 ) contractCost = _*;
    }
	
	//Destructor
    function kill() public {
       	if(msg.sender == owner) selfdestruct(owner);
    }

	//Validator
   	function checkIfWriteIDAllowed(address writer) public constant returns(bool){
		//allowed writer nodes == masternode address
		//Will need to access the mongodb with a query looking for the list of allowed writer nodes
		//then search though the list of allowed contract writers and return if the user is allowed
    	for(uint256 i = 0; i < writer.length; i++){
			if(writers[i] == writer) return true;
      	}
      	return false;
   	}
	
    //Validated API Call
	//payable means that you send eth??? need to verify
    function update(uint256 _**) public payable {
		//_** == all values needed for a single pair entry into the mongodb
		
		//requires are if statments basically and if one evals to false the contract breaks
       	require(checkIfWriteIDAllowed(msg.sender));
       	require(24hrVolBTC > -1.0 && 24hVolBTC <= MAX_ALLOWED_INT_SIZE);
		//...validate other variables that are inserted into mongoDB

		//Check that value sent is enough to update DB
       	require(msg.value >= contractCost);

       	writerInfo[msg.sender].avgUSD = avgUSD;
       	writerInfo[msg.sender].24hrVolBTC = 24hrVolBTC;
		//...all other required be entry values

		//Random constanst shit
       	incrementingVal++;

		//Put the address on the array of writerNodeAddresses
       	writerNodeAddresses.push(msg.sender);

		//Add to some total contract value
       	contractVal += msg.value;

		//...you would then preform a simple DB insert into the mongoDB hosted via IPFS

		//...call function that cleanly exits contract
		cleanExit(_*)
		//delete writerInfo[writerAddress];
    }

	//UnValidated API Call
	function query(unit256 _*) public payable{
		//_* == wildcard
		//unsure what params would be needed at this time
		
		require(validInput(_*));
		
		//...run mongodb query to get the results based on the filters in the _*

		//...call function that cleanly exits contract
		cleanExit(_*)
		//delete writerInfo[writerAddress];
	}

	//Utility function
	function reward(unit256 _*) public {
		//Preform some action that doesnt need access to the chain value
		unit256 localVal=0

		//Call function to send out like node reward to some address
		rewardNode(_*)
	}

	function rewardNode(unit256 _*) public {
		//_*** == unknown value
		//this would reward a sender if they have some value that is correct in the struct write
		//would have that contract require some random number or some shit maybe 

		unit256 count = 0;
		address[MAX_MASTERNODE_SIZE] memory winners;
		for (unit256 i = 0; i < writerNodeAddresses; i++){
			address writerAddress = writerNodeAddresses[i];
			if(writerInfo[writerAddress]._*** == _***){
				winners[count] = writerAddress;
				count++;
			}

			//Would need to do this for a clean exit basically
			delete writerInfo[writerAddress];
		}
		
		//clean up all the variables that we set
		// Delete all the writerInfo array, this might need to be moved to say a cleanUp(_*)
		//writerInfo.length = 0; 
		cleanUp(_*)

      	uint256 winnerEtherAmount = contractVal / winners.length; // How much each winner gets
      	for(uint256 j = 0; j < count; j++){
        	if(winners[j] != address(0)) // Check that the address in this fixed array is not empty
         	winners[j].transfer(winnerEtherAmount);
      	}
	}
}
```
- ReRead: https://medium.com/@merunasgrincalaitis/the-ultimate-end-to-end-tutorial-to-create-and-deploy-a-fully-descentralized-dapp-in-ethereum-18f0cf6d7e0e

- Need to setup some kind of IPFS infrastrcture. To host the mongoDB database json file

- The above contract just says that hey I want to interact with this mongoDB in this way.
	- must be in writerNodeAddresses to be able to update
	- any can run get
	- The contract also will come with a index.js that displays the Top 100 coins based something
		- Use react or something like that 
		- have some CSS shit

- IPFS will be used by masternode owners to stake a value of coin in the network, then run this masternode setup that gives them the list of IPFS peers that they can connect to and thus see the mongoDB that is being shared. Cause they will download the latest copy when they download the chain? It will also publish their address to the IPFS peers list. HAS TO REMOVE WHEN SERVICE STOPPED! 

- Will need to do something like this https://github.com/ipfs/examples/tree/master/examples/websites
	- That will give you the human readable name for stuff

- With IPFS we can host the data on the masternode systems

### How Do we call the update function?

This section will cover how the update function is called, via what systems, what parameters, etc...

- All of these update scripts will be on github and version controlled in a public repo

- They will just be the basic scrapers I already created but abstracted a bit more to just do every exchange we can
	- Could have the need to create custom ones that should be created by the community? Or bounty programs to add an integration to a new DEX!!!!
	- Would have support for all the major exchanges to gather the data

- How do we run this type of computation???: (Get masternode's to run it? Need to figure out computation aspect of this) 
	- Pull from the git repo all the scrapers
	- Not allow them to edit them? 
		- Or is this where blockchain concensus comes into play? Doubtfulishness here
	- Start a big scrape of all the exchanges
		- Calling DB update, async - MUST

