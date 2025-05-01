# shared_tools.py

import json

server_ws = [None]
clients = {}
subscribed_clients = {}  

async def notify_clients_subscribed(message: str):
    for client in subscribed_clients.values():
        try:
            await client.send_json({
                "type": "notification",
                "message": message
            })
        except Exception as e:
            print(f"Failed to notify client: {e}")

async def get_clients_count():
    return json.dumps({
        "type": "counts",
        "subscribers": len(subscribed_clients),
        "clients": len(clients),
    })

async def get_clients_data():
    return {
        "type": "clients",
        "subscribers": list(subscribed_clients.keys()),
        "clients": len(clients),
    }
