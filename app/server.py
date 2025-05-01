# server.py

import json
from fastapi import WebSocket, WebSocketDisconnect
from app.shared_tools import server_ws, subscribed_clients, notify_clients_subscribed, get_clients_count
from app.database import insert_notification, get_notifications

async def websocket_server(websocket: WebSocket):
    try:
        await websocket.accept()
        server_ws[0] = websocket

        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            action = msg.get("action")

            if action == "notify":
                message = msg.get("message", "")
                await notify_clients_subscribed(message)
                await insert_notification(message)
            elif action == "get_notifications":
                notifications = await get_notifications()
                await websocket.send_json({"type": "notifications", "notifications": notifications})

            elif action == "count":
                await server_ws[0].send_text(await get_clients_count())

    except WebSocketDisconnect:
        server_ws[0]= None
