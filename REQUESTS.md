# Requests and Endpoints

## Price

### Getting a quote from token to worthy coin

#### Request

`curl -X 'GET' \
  'https://api.1inch.io/v4.0/56/quote?fromTokenAddress=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE&toTokenAddress=0x7EC1EdCB89343A8DF4329Ad94C174458225105aE&amount=1' \
  -H 'accept: application/json'`

#### Parameters

- chainId: 56
- worthy token address
- user token address
- amount (always = 1)

#### Observation

Worthy token will be USDC on Binance, Ethereum or Polygon, to avoid the extra step of converting BNB/USD.

## Transaction

### Get user transactions

#### Request

`https://api.bscscan.com/api?module=account&action=txlist&address=0x68E596b8122Ac6F4Ddc2C897CFf816C31E309eB3&page=1&startblock=0&endblock=999999999&sort=asc&apikey=V1SXBSXMIG95CKUZST79DRCD2NIFSFY279`

or

`https://api.etherscan.io/api?module=account&action=txlist&address=0x906fb300B424806Ba33F451E372fd09C6E1eB1A6&page=1&startblock=0&endblock=999999999&sort=asc&apikey=S46JREZEKRV6PXR17C16GTRK2QVFBEEZ1D`

or

`https://api.polygonscan.com/api?module=account&action=txlist&address=0x906fb300B424806Ba33F451E372fd09C6E1eB1A6&page=1&startblock=0&endblock=999999999&sort=asc&apikey=J7APK7P6QCB7EWCTA3FWA8DIG8PXWZFMX3`

#### Parameters

- address - user wallet address
- start block - last block found on previous search
- Liquidity pool - token's liquidity pool to which the user is buying/selling from

#### Observation

The endpoint should give a count and timestamp of transactions relevant to user's token. Nothing more.

### Check if transaction is successful / complete

#### Request

`https://api.bscscan.com/api?module=transaction&action=gettxreceiptstatus&txhash=0x5a4e84ce632297f08a2c90e5fccb3116d44071e7a211908ce7bf50e61ff9a553&apikey=V1SXBSXMIG95CKUZST79DRCD2NIFSFY279`

or

`https://api.etherscan.io/api?module=transaction&action=gettxreceiptstatus&txhash=0x48a3c7db5fc1a336204d9a19a0c9cf7330a051e9fdbe07ac07c7d5a9a6d3861b&apikey=S46JREZEKRV6PXR17C16GTRK2QVFBEEZ1D`

or

`https://api.polygonscan.com/api?module=transaction&action=gettxreceiptstatus&txhash=0x48a3c7db5fc1a336204d9a19a0c9cf7330a051e9fdbe07ac07c7d5a9a6d3861b&apikey=J7APK7P6QCB7EWCTA3FWA8DIG8PXWZFMX3`

#### Parameters

- transaction id

## Holders and Balance

### Get list of holders who interacted with the LP

#### Request

`https://api.bscscan.com/api?module=account&action=tokentx&address=0xffaac354BF590257CdDfAF46049555c8f5457430&page=1&startblock=0&endblock=999999999&sort=asc&apikey=V1SXBSXMIG95CKUZST79DRCD2NIFSFY279`

or

`https://api.etherscan.io/api?module=account&action=tokentx&address=0xffaac354BF590257CdDfAF46049555c8f5457430&page=1&startblock=0&endblock=999999999&sort=asc&apikey=S46JREZEKRV6PXR17C16GTRK2QVFBEEZ1D`

or

`https://api.polygonscan.com/api?module=account&action=tokentx&address=0xffaac354BF590257CdDfAF46049555c8f5457430&page=1&startblock=0&endblock=999999999&sort=asc&apikey=J7APK7P6QCB7EWCTA3FWA8DIG8PXWZFMX3`

#### Parameters

address - liquidity pool address
token address
startblock - last block this service returned

#### Observations

1. Black list addresses

I have to build a list of ignored To/From addresses. For instance:

- Null address: 0x0000000000000000000000000000000000000000
- Reserved: 0x9c4350f527ff7f96b650ee894ae9103bdfec0432

2. Filter contract address

Make sure to filter results using "contractAddress" output = user's token address

3. To/From are important, but I'm not able to detect a pattern yet. The txn hash doesn't appear on this endpoint, now the block number matches. :( To this first version, I won't differentiate between buy/sells, unless someone asks

### Get holder's balance on token

#### Request

`https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x7EC1EdCB89343A8DF4329Ad94C174458225105aE&address=0x68E596b8122Ac6F4Ddc2C897CFf816C31E309eB3&page=1&startblock=0&endblock=999999999&sort=asc&apikey=V1SXBSXMIG95CKUZST79DRCD2NIFSFY279`

or

`https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0x7EC1EdCB89343A8DF4329Ad94C174458225105aE&address=0x68E596b8122Ac6F4Ddc2C897CFf816C31E309eB3&page=1&startblock=0&endblock=999999999&sort=asc&apikey=S46JREZEKRV6PXR17C16GTRK2QVFBEEZ1D`

or

`https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress=0x7EC1EdCB89343A8DF4329Ad94C174458225105aE&address=0x68E596b8122Ac6F4Ddc2C897CFf816C31E309eB3&page=1&startblock=0&endblock=999999999&sort=asc&apikey=J7APK7P6QCB7EWCTA3FWA8DIG8PXWZFMX3`

#### Parameters

- token address
- wallet address - holder's wallet address

#### Description

Assumes the holder wallet address is known

## Token

### Get token max supply

#### Request

`https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress=0x7EC1EdCB89343A8DF4329Ad94C174458225105aE&apikey=V1SXBSXMIG95CKUZST79DRCD2NIFSFY279`

#### Parameters

token address
