import smtplib
from email.message import EmailMessage
from app import config

def enviar_correo(archivo_adjunto):
    msg = EmailMessage()
    msg['Subject'] = config.MAIL_ASUNTO
    msg['From'] = config.MAIL_USER
    msg['To'] = config.MAIL_DESTINATARIO
    msg.set_content(config.MAIL_CUERPO)

    with open(archivo_adjunto, 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(config.MAIL_USER, config.MAIL_PASSWORD)  # Usar variables del config
        smtp.send_message(msg)
