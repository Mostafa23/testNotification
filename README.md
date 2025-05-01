# Real-time Notification & Chat App with FastAPI + WebSocket

This project is a real-time WebSocket-based system built using FastAPI for the backend and HTML/CSS/JavaScript for the frontend. It enables real-time updates between a server and multiple clients. The server tracks the number of connected users and subscribers and supports sending/receiving notifications.

---

## Project Structure
   ```bash
      Project/
      │
      ├── app/                          # Application logic and FastAPI code
      │   ├── main.py                   # FastAPI entry point (handles routing and WebSocket setup)
      │   ├── config.py                 # Configuration file to store environment variables (e.g., MongoDB URI, server ID)
      │   ├── database.py               # MongoDB database operations (insert, retrieve notifications)
      │   ├── server.py                 # Handles WebSocket logic for the server dashboard (manage server-side connections)
      │   ├── client.py                 # Handles WebSocket logic for client subscribers (manage client-side connections)
      │   └── shared_tools.py           # Shared utility functions (e.g., fetching client data, utility functions for WebSockets)
      │
      ├── pages/                         # Front-end files (HTML, CSS, JS, images)
      │   ├── client.html               # Client UI (subscriber interface where clients receive notifications)
      │   ├── server.html               # Server UI (dashboard interface to manage notifications and view data)
      │   ├── css/                      # Stylesheets for the UI
      │   │   ├── client.css            # Styling for client-side UI (visual look of the client page)
      │   │   └── server.css            # Styling for server-side UI (visual look of the server dashboard)
      │   ├── js/                       # JavaScript files for WebSocket handling on the client and server
      │   │   ├── client.js             # JavaScript for client-side WebSocket handling (to connect and manage messages)
      │   │   └── server.js             # JavaScript for server-side WebSocket handling (for receiving and broadcasting messages)
      │   └── images/                   # Images used in the UI (e.g., background images, icons)
      │       └── Server Background.png # Optional background image for the server page
      │
      ├── .env                           # Environment variables file (store secrets like MongoDB URI, server ID, etc.)
      ├── .gitignore                     # Git ignore file to exclude files/folders from version control (e.g., .env)
      └── README.md                      # Project documentation (overview, setup instructions, usage)
  ```
---

## Features

- Real-time bi-directional communication using WebSockets  
- Live tracking of connected clients and subscribers  
- Clients can send messages/notifications to the server  
- Server dashboard displays messages and user counts in real time  
- Responsive web-based UI with FastAPI backend

---

## Requirements

- Python 3.8+  
- FastAPI  
- Uvicorn

Install dependencies:

  ```bash
    pip install fastapi uvicorn orjson motor python-dotenv
  ```

---

## Running the Project

1. Navigate to the project directory:
  ```bash
    cd Project
  ```
2. Start the FastAPI server:
  ```bash
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  ```
3. Open your browser and visit:

- Server Dashboard: localhost/server/{id}  
- Client Page: localhost:8000/

---

## WebSocket Routes

- /ws/server: WebSocket connection for the server dashboard  
- /ws/client: WebSocket connection for individual clients

---

## How It Works

- Clients connect and subscribe via the /ws/client WebSocket route  
- The server connects via /ws/server to monitor and manage communication  
- Clients can send notifications, and the server updates connection stats in real time  
- All communication is handled live using WebSockets for instant feedback

---

## TODO (Optional Enhancements)

- Add user authentication for clients  
- Store and display message history  
- Show timestamps for each message  
- Improve UI responsiveness on mobile devices
