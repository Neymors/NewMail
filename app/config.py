import os
from dotenv import load_dotenv

load_dotenv()

MAIL_DESTINATARIO = os.getenv("MAIL_DESTINATARIO")
MAIL_ASUNTO = os.getenv("MAIL_ASUNTO", "Resumen diario de noticias")
MAIL_CUERPO = os.getenv("MAIL_CUERPO", "Adjunto encontrarás el resumen diario.")
# config.py
MAIL_USER = os.getenv("MAIL_USER")  # Correo electrónico del remitente
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # Contraseña/App Password