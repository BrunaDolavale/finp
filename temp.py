import pyrebase
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

firebase_config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "databaseURL": os.getenv('FIREBASE_DATABASE_URL'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID'),
    "measurementId": os.getenv('FIREBASE_MEASUREMENT_ID')
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

def upload_salaries():
    salaries_data = {
        "2024-06": {
            "bruna": 5000,
            "bruno": 2000
        },
        "2024-07": {
            "bruna": 5200,
            "bruno": 2100
        },
        "2024-08": {
            "bruna": 5300,
            "bruno": 2200
        }
        # Adicione mais meses e salários conforme necessário
    }

    for yearmonth, salaries in salaries_data.items():
        db.child("salaries").child(yearmonth).set(salaries)
        print(f"Salaries for {yearmonth} uploaded successfully.")

if __name__ == "__main__":
    upload_salaries()
