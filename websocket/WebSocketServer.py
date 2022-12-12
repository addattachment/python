import ast
import asyncio
import time
import functools
import pandas as pd
import websockets


def write_to_file(message, file):
    with open(file, 'a+') as f:
        f.write("{}\n".format(message))


async def ws_handler(websocket, params, output_file):
    # first sending base parameters to unity (name child etc)
    for i in params:
        await websocket.send(str(i))
    # then handling incoming messages
    async for message in websocket:
        print(message)
        write_to_file(message, output_file)
        # message_dict = ast.literal_eval(message)
        # for key, value in message_dict.items():
        #     match key:
        #         case "connectMessage":
        #             print("connected with {}".format(value))
        #         case "_time":
        #             print("connection time is {}".format(value))
        #         case "caregiver_rating":
        #             print("care giver got a rating of {}".format(value))
        #         case default:
        #             print("no know command: {}".format(key))


async def start_ws_server(params=None, output_file="", ip: str = 'localhost',
                          port: int = 8080):
    if params is None:
        params = [{"i": "test", "name": "Charles"}]
    print("starting websocket server")
    async with websockets.serve(functools.partial(ws_handler, params=params, output_file=output_file), ip, port) as ws:
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    websocket_data = [
        {"id": "123"},
        {"contingency": "20"}
    ]
    asyncio.run(start_ws_server(params=websocket_data, output_file="test.csv", ip='192.168.50.188'))
    # loop = asyncio.get_event_loop()
    # task = loop.create_task(startWsServer())
    # try:
    #     loop.run_until_complete(task)
    # except asyncio.CancelledError:
    #     pass
    # while True:
    #     print("a")
    #     time.sleep(2)
