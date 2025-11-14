import requests, json
import websockets # type: ignore
import asyncio

clob_URL = 'wss://ws-subscriptions-clob.polymarket.com/ws/market' #CLOB endpoint for market data
#clob stands for 'central limit order book'
slug = 'who-will-trump-pardon-in-2025?' #event name
event_url = f"https://gamma-api.polymarket.com/events/slug/{slug}"

event_data = requests.get(event_url).json() #event data as a json

event_id = event_data['id'] #id of event

markets = event_data['markets'] #all markets for that event

pardon_diddy_yes_token = '93425298759467682711704940688772441010955525019881668068016025097366958962368' #id of yes token
pardon_diddy_no_token = '110772069756724332116648059385969433526059191442232057731782827132431473437246' #id of no token

wanted_tokens = [pardon_diddy_yes_token, pardon_diddy_no_token]
#market_IDs = [market['id'] for market in markets] #IDs of markets for given event

async def get_polymarket_data():
    ''' continuously gives order book updates and print them to terminal'''
    async with websockets.connect(clob_URL, ping_interval=10) as ws: #establish connection to endpoint with pings to maintain it
        await ws.send(json.dumps({'assets_ids': wanted_tokens, 'type': 'market'})) #what we want
        while True:
            data = await ws.recv() #data we receive
            d = json.loads(data) 
            print(d)

asyncio.run(get_polymarket_data())
        
#print(json.dumps(markets, indent=2))


