import ast
import asyncio
import time
import functools

import websockets


async def ws_handler(websocket, params):
    # first sending base parameters to unity (name child etc)
    for i in params:
        await websocket.send(str(i))
    # then handling incoming messages
    async for message in websocket:
        print(message)
        message_dict = ast.literal_eval(message)
        for key, value in message_dict.items():
            match key:
                case "connectMessage":
                    print("connected with {}".format(value))
                case "_time":
                    print("connection time is {}".format(value))
                case "caregiver_rating":
                    print("care giver got a rating of {}".format(value))
                case default:
                    print("no know command: {}".format(key))


async def startWsServer(params: list[dict] = [{"i": "test"}], ip: str = 'localhost', port: int = 8080):
    print("starting websocket server")
    async with websockets.serve(functools.partial(ws_handler, params=params), ip, port) as ws:
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    websocket_data = [
        {"id": "123"},
        {"contingency": "20"}
    ]
    asyncio.run(startWsServer(params=websocket_data, ip='10.46.235.49'))
    # loop = asyncio.get_event_loop()
    # task = loop.create_task(startWsServer())
    # try:
    #     loop.run_until_complete(task)
    # except asyncio.CancelledError:
    #     pass
    # while True:
    #     print("a")
    #     time.sleep(2)
