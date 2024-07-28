from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2


# Verbindungsinformationen
connection_info  = "postgresql://solai:GQNzIM7spKw6vo7l1KsAGP3SxkndnPa1@dpg-cqj7b1ij1k6c739o2gvg-a.frankfurt-postgres.render.com/feedbacks_db_i3xb"


# FastAPI-Instanz erstellen
app = FastAPI()

# CORS-Einstellungen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hier kannst du die erlaubten Ursprünge einstellen
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],  # Hier kannst du die erlaubten HTTP-Methoden einstellen
    allow_headers=["*"],
)

# Pydantic-Modell für die Datenstruktur definieren
class Feedback(BaseModel):
    name: str
    email: str
    feedback: str

# Endpunkt zum Speichern der Daten
@app.post("/insert-feedback/")
async def create_feedback(feedback: Feedback):
    try:
        # Verbindung zur Datenbank herstellen
        conn = psycopg2.connect(**connection_info)

        # Cursor erstellen
        cur = conn.cursor()

        # SQL-Befehl zum Einfügen der Daten ausführen
        cur.execute("INSERT INTO fdback (name, email, feedback) VALUES (%s, %s, %s)", (feedback.name, feedback.email, feedback.feedback))

        # Transaktion bestätigen
        conn.commit()

        # Verbindung schließen
        cur.close()
        conn.close()

        return {"message": "Feedback wurde erfolgreich gespeichert"}

    except Exception as e:
        return {"error": f"Fehler beim Speichern des Feedbacks: {e}"}

# Endpunkt zum Abrufen von Feedback-Daten
@app.get("/get-feedback/")
async def get_feedback():
    try:
        # Verbindung zur Datenbank herstellen
        conn = psycopg2.connect(**connection_info)

        # Cursor erstellen
        cur = conn.cursor()

        # SQL-Befehl zum Abrufen der Feedback-Daten ausführen
        cur.execute("SELECT * FROM fdback")

        # Feedback-Daten abrufen
        feedback_data = cur.fetchall()

        # Verbindung schließen
        cur.close()
        conn.close()

        return {"feedback": feedback_data}

    except Exception as e:
        return {"error": f"Fehler beim Abrufen des Feedbacks: {e}"}

# Endpunkt zum Löschen von Feedback-Daten aus der Datenbank
@app.delete("/del-feedback/{feedback_id}")
async def delete_feedback(feedback_id: int):
    try:
        # Verbindung zur Datenbank herstellen
        conn = psycopg2.connect(**connection_info)

        # Cursor erstellen
        cur = conn.cursor()

        # SQL-Befehl zum Löschen eines Datensatzes ausführen
        cur.execute("DELETE FROM fdback WHERE id = %s", (feedback_id,))

        # Transaktion bestätigen
        conn.commit()

        # Verbindung schließen
        cur.close()
        conn.close()

        return {"message": f"Feedback-Datensatz mit ID {feedback_id} wurde erfolgreich gelöscht"}

    except Exception as e:
        return {"error": f"Fehler beim Löschen des Feedbacks: {e}"}
