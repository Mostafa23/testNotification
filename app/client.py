# client.py

import asyncio
from starlette import status
from fastapi import WebSocket, WebSocketDisconnect
from app.shared_tools import server_ws, subscribed_clients, clients, get_clients_count

async def websocket_client(websocket: WebSocket, user_id: str):
    try:
        if user_id in clients:
            old_websocket = clients[user_id]
            await old_websocket.close(code=status.WS_1000_NORMAL_CLOSURE, reason="Another session started.")
            await asyncio.sleep(0.1) # wait for the old connection to close

        await websocket.accept()
        clients[user_id] = websocket

        if server_ws[0]:
            await server_ws[0].send_text(await get_clients_count())

        while True:
            if clients.get(user_id) != websocket:
                break # old connection closed

            data = await websocket.receive_text()

            if data == "subscribe":
                subscribed_clients[user_id] = websocket
            elif data == "unsubscribe":
                subscribed_clients.pop(user_id, None)

            if server_ws[0]:
                await server_ws[0].send_text(await get_clients_count())

    except WebSocketDisconnect:
        if clients.get(user_id) == websocket:
            clients.pop(user_id, None)
            subscribed_clients.pop(user_id, None)
            if server_ws[0]:
                await server_ws[0].send_text(await get_clients_count())

    except Exception as e:
        print(f"WebSocket Error ({user_id}):", e)
