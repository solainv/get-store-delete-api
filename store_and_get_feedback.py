# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 14:42:36 2024

@author: solai
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS-Einstellungen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Erlaube Anfragen von allen Ursprüngen
    allow_credentials=True,  # Erlaube Cookies in Anfragen
    allow_methods=["*"],  # Erlaube bestimmte HTTP-Methoden
    allow_headers=["*"],  # Erlaube alle Header in Anfragen
)

# SQLite-Datenbankverbindungsfunktionen
def create_connection():
    return sqlite3.connect('feedbacks_db.db')

def close_connection(conn):
    conn.close()

# Tabelle für Feedbacks erstellen, wenn sie nicht existiert
def create_feedbacks_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedbacks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 email TEXT,
                 feedback TEXT)''')
    conn.commit()

class Feedback(BaseModel):
    id: int = None  # Optional für das Speichern, automatisch generiert
    name: str
    email: str
    feedback: str

@app.post("/api/submit_feedback")
async def submit_feedback(feedback: Feedback):
    conn = create_connection()
    create_feedbacks_table(conn)
    c = conn.cursor()
    c.execute("INSERT INTO feedbacks (name, email, feedback) VALUES (?, ?, ?)",
              (feedback.name, feedback.email, feedback.feedback))
    conn.commit()
    close_connection(conn)
    return {"message": "Feedback received successfully"}

@app.get("/api/get_feedbacks")
async def get_feedbacks():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM feedbacks")
    rows = c.fetchall()
    feedbacks = [{"id": row[0], "name": row[1], "email": row[2], "feedback": row[3]} for row in rows]
    close_connection(conn)
    return feedbacks

@app.delete("/api/delete_feedback/{feedback_id}")
async def delete_feedback(feedback_id: int):
    conn = create_connection()
    c = conn.cursor()
    c.execute("DELETE FROM feedbacks WHERE id=?", (feedback_id,))
    conn.commit()
    close_connection(conn)
    return {"message": f"Feedback with ID {feedback_id} deleted successfully"}








# # store_and_get_feedback.py reply email automaticly
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import sqlite3
# from fastapi.middleware.cors import CORSMiddleware
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# app = FastAPI()

# # CORS-Einstellungen
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Erlaube Anfragen von allen Ursprüngen
#     allow_credentials=True,  # Erlaube Cookies in Anfragen
#     allow_methods=["*"],  # Erlaube bestimmte HTTP-Methoden
#     allow_headers=["*"],  # Erlaube alle Header in Anfragen
# )

# # SQLite-Datenbankverbindung
# conn = sqlite3.connect('feedbacks.db')
# c = conn.cursor()

# # Tabelle für Feedbacks erstellen, wenn sie nicht existiert
# c.execute('''CREATE TABLE IF NOT EXISTS feedbacks
#              (id INTEGER PRIMARY KEY AUTOINCREMENT,
#              name TEXT,
#              email TEXT,
#              feedback TEXT)''')
# conn.commit()

# class Feedback(BaseModel):
#     id: int = None  # Optional für das Speichern, automatisch generiert
#     name: str
#     email: str
#     feedback: str

# @app.post("/api/feedback")
# async def submit_feedback(feedback: Feedback):
#     # Feedback in SQLite-Datenbank einfügen
#     c.execute("INSERT INTO feedbacks (name, email, feedback) VALUES (?, ?, ?)",
#               (feedback.name, feedback.email, feedback.feedback))
#     conn.commit()
#     # Senden der automatischen Antwort-E-Mail
#     send_email(feedback.email, feedback.name)
#     return {"message": "Feedback received successfully"}

# @app.get("/api/feedback")
# async def get_feedbacks():
#     # Alle Feedbacks aus der SQLite-Datenbank abrufen
#     c.execute("SELECT * FROM feedbacks")
#     rows = c.fetchall()
#     feedbacks = [{"id": row[0], "name": row[1], "email": row[2], "feedback": row[3]} for row in rows]
#     return feedbacks

# @app.delete("/api/feedback/{feedback_id}")
# async def delete_feedback(feedback_id: int):
#     c.execute("DELETE FROM feedbacks WHERE id=?", (feedback_id,))
#     conn.commit()
#     return {"message": f"Feedback with ID {feedback_id} deleted successfully"}

# def send_email(to_email, name):
#     SMTP_SERVER = 'smtp.gmail.com'  # SMTP-Server-Adresse
#     SMTP_PORT = 587  # SMTP-Server-Port
#     EMAIL_ADDRESS = 'karroumisolaiman0@gmail.com'  # Deine E-Mail-Adresse
#     APP_PASSWORD = '0808'  # Dein App-Passwort

#     msg = MIMEMultipart()
#     msg['From'] = EMAIL_ADDRESS
#     msg['To'] = to_email
#     msg['Subject'] = 'Vielen Dank für Ihr Feedback!'

#     body = f"""
#     Sehr geehrte/r {name},

#     Vielen Dank für Ihr wertvolles Feedback! Wir schätzen Ihre Meinung sehr und werden uns bemühen, Ihren Anliegen nachzukommen.

#     Mit freundlichen Grüßen,
#     Solaiman Karroumi
#     """
#     msg.attach(MIMEText(body, 'plain'))

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(EMAIL_ADDRESS, APP_PASSWORD)
#         server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
