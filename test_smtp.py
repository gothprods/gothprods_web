import smtplib
from dotenv import load_dotenv
import os

load_dotenv('config.env')
SENDER_EMAIL = "goth.prods@gmail.com"
SENDER_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

print(f"Password: {SENDER_PASSWORD}")

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.set_debuglevel(1)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("Login successful!")
    server.quit()
except Exception as e:
    print(f"SMTP Error: {e}")
