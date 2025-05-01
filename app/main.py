# main.py

from fastapi import FastAPI, WebSocket, Form, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pydantic import BaseModel, EmailStr
from app.server import websocket_server
from app.client import websocket_client
from app.config import ID_SERVER, SERVER_URL
from app.auth import generate_confirmation_token, send_confirmation_email, confirm_user, is_email_confirmed, generate_session_token, verify_session_token

app = FastAPI()

app.mount("/pages", StaticFiles(directory="pages"), name="pages")

class EmailRegistration(BaseModel):
    email: EmailStr

@app.get("/")
async def get_client_page():
    with open("pages/client.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/server/{id}")
async def get_server_page(id: str):
    if id != ID_SERVER:
        return HTMLResponse("Invalid access")
    
    with open("pages/server.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/register")
async def register_user(email_data: EmailRegistration):
    token = await generate_confirmation_token(email_data.email)
    email_sent = await send_confirmation_email(email_data.email, token)
    
    if email_sent:
        return JSONResponse(
            status_code=200,
            content={"message": "Confirmation email sent. Please check your inbox."}
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to send confirmation email. Please try again."}
        )

@app.get("/confirm/{token}")
async def confirm_email(token: str):
    success, message = await confirm_user(token)
    
    if success:
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Email Confirmed</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
                .success {{ color: green; }}
                .button {{ 
                    display: inline-block; 
                    background-color: #4C6A92; 
                    color: white; 
                    padding: 10px 20px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    margin-top: 20px; 
                }}
            </style>
        </head>
        <body>
            <h1 class="success">Email Confirmed!</h1>
            <p>{message}</p>
            <a href="/" class="button">Return to Dashboard</a>
        </body>
        </html>
        """)
    else:
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Confirmation Failed</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
                .error {{ color: red; }}
                .button {{ 
                    display: inline-block; 
                    background-color: #4C6A92; 
                    color: white; 
                    padding: 10px 20px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    margin-top: 20px; 
                }}
            </style>
        </head>
        <body>
            <h1 class="error">Confirmation Failed</h1>
            <p>{message}</p>
            <a href="/" class="button">Return to Dashboard</a>
        </body>
        </html>
        """)

@app.post("/login")
async def login_user(email_data: EmailRegistration):
    confirmed = await is_email_confirmed(email_data.email)
    
    if not confirmed:
        return JSONResponse(
            status_code=403,
            content={"message": "Email not confirmed. Please check your inbox and confirm your email."}
        )
    
    session_token = await generate_session_token(email_data.email)
    
    if session_token:
        return JSONResponse(
            status_code=200,
            content={"message": "Login successful", "token": session_token}
        )
    else:
        return JSONResponse(
            status_code=401,
            content={"message": "Login failed"}
        )

@app.get("/check-auth")
async def check_auth(token: str = None):
    if not token:
        return JSONResponse(
            status_code=401,
            content={"authenticated": False}
        )
    
    email = await verify_session_token(token)
    
    if email:
        return JSONResponse(
            status_code=200,
            content={"authenticated": True, "email": email}
        )
    else:
        return JSONResponse(
            status_code=401,
            content={"authenticated": False}
        )

@app.websocket("/ws/client/{user_id}")
async def websocket_client_route(websocket: WebSocket, user_id: str):
    await websocket_client(websocket, user_id)

@app.websocket("/ws/server")
async def websocket_server_route(websocket: WebSocket):
    await websocket_server(websocket)


if __name__ == "__main__":
    import uvicorn
    print(f"Server started at {SERVER_URL}")
    print(f"Server page: {SERVER_URL}/server/{ID_SERVER}")
    uvicorn.run(app, host="0.0.0.0", port=8000)