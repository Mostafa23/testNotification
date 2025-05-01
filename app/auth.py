# auth.py

import uuid
from datetime import datetime, timezone, timedelta
import jwt
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGODB_URI_REMOTE, SERVER_URL, EMAIL_PASSWORD, EMAIL_USERNAME, SECRET_KEY

# MongoDB setup
client = AsyncIOMotorClient(MONGODB_URI_REMOTE)
db = client["Notification"]
users_collection = db["users"]

# Email sending function with better error handling
async def send_confirmation_email(email, confirmation_token):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USERNAME
        msg['To'] = email
        msg['Subject'] = "Confirm your registration"
        
        confirmation_link = f"{SERVER_URL}/confirm/{confirmation_token}"
        body = f"""
        <html>
        <body>
            <h2>Welcome to Notification App!</h2>
            <p>Please click the link below to confirm your email address:</p>
            <p><a href="{confirmation_link}">Confirm Email</a></p>
            <p>This link will expire in 24 hours.</p>
            <p>If you didn't register for this service, you can ignore this email.</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        context = ssl.create_default_context()
        
        print(f"Attempting to send email to: {email}")
        print(f"Using account: {EMAIL_USERNAME}")
        
        # Connect with SSL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            # Login
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            print("SMTP Login successful")
            
            # Send email
            server.send_message(msg)
            print(f"Email sent successfully to {email}")
        
        return True
    except smtplib.SMTPAuthenticationError as auth_error:
        print(f"SMTP Authentication Error: {auth_error}")
        print("This is likely due to incorrect email/password or Gmail security settings.")
        print("For Gmail, you need to:")
        print("1. Enable 2-Step Verification on your Google account")
        print("2. Create an App Password at https://myaccount.google.com/apppasswords")
        print("3. Use that App Password instead of your regular password")
        return False
    except smtplib.SMTPException as smtp_error:
        print(f"SMTP Error: {smtp_error}")
        return False
    except Exception as e:
        print(f"General error sending email: {e}")
        return False

# Generate confirmation token
async def generate_confirmation_token(email):
    token = str(uuid.uuid4())
    expiration = datetime.now(timezone.utc) + timedelta(hours=24)
    
    user = await users_collection.find_one({"email": email})
    
    if user:
        # Update existing user
        await users_collection.update_one(
            {"email": email},
            {
                "$set": {
                    "confirmation_token": token,
                    "token_expiry": expiration,
                    "is_confirmed": False
                }
            }
        )
    else:
        # Create new user
        await users_collection.insert_one({
            "email": email,
            "confirmation_token": token,
            "token_expiry": expiration,
            "is_confirmed": False,
            "created_at": datetime.now(timezone.utc)
        })
    
    return token

# Verify token and confirm user
async def confirm_user(token):
    user = await users_collection.find_one({"confirmation_token": token})
    
    if not user:
        return False, "Invalid confirmation token"
    
    if user.get("is_confirmed", False):
        return True, "Email already confirmed"
    
    # Fix: Convert token_expiry to datetime with timezone if it isn't already
    token_expiry = user.get("token_expiry")
    current_time = datetime.now(timezone.utc)
    
    # Check if token_expiry has a timezone; if not, assume it's UTC
    if token_expiry.tzinfo is None:
        token_expiry = token_expiry.replace(tzinfo=timezone.utc)
    
    if token_expiry < current_time:
        return False, "Confirmation token expired"
    
    await users_collection.update_one(
        {"confirmation_token": token},
        {
            "$set": {
                "is_confirmed": True,
                "confirmed_at": datetime.now(timezone.utc)
            }
        }
    )
    
    return True, "Email confirmed successfully"

# Check if email is confirmed
async def is_email_confirmed(email):
    user = await users_collection.find_one({"email": email})
    if not user:
        return False
    return user.get("is_confirmed", False)

# Get user ID from email
async def get_user_id(email):
    user = await users_collection.find_one({"email": email})
    if not user:
        return None
    return str(user.get("_id"))

# Generate session token for confirmed users
async def generate_session_token(email):
    user = await users_collection.find_one({"email": email})
    if not user or not user.get("is_confirmed", False):
        return None
    
    payload = {
        "sub": str(user["_id"]),
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    
    session_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    return session_token

# Verify session token
async def verify_session_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = await users_collection.find_one({"_id": payload["sub"], "email": payload["email"]})
        
        if not user:
            return None
        
        return payload["email"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None