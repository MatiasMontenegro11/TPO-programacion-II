# Envía el reporte por mail con Gmail, con un Excel y un gráfico adjuntos.

import os
import smtplib
import ssl
import certifi
from email.message import EmailMessage

SERVIDOR_SMTP = "smtp.gmail.com"
PUERTO_SMTP = 465            # puerto de Gmail para conexión segura (SSL)


def enviar_reporte(usuario, password, destinatarios, asunto, cuerpo, adjuntos):

    # mensaje
    mensaje = EmailMessage()
    mensaje["From"] = usuario
    mensaje["To"] = ", ".join(destinatarios)
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo)

    # Adjunta archivos
    for ruta in adjuntos:
        with open(ruta, "rb") as archivo:
            contenido = archivo.read()
        nombre = os.path.basename(ruta)
        mensaje.add_attachment(contenido, maintype="application", subtype="octet-stream", filename=nombre)
        
    # Se conecta a Gmail de forma segura y lo envia
    contexto = ssl.create_default_context(cafile=certifi.where())
    try:
        with smtplib.SMTP_SSL(SERVIDOR_SMTP, PUERTO_SMTP, context=contexto) as servidor:
            servidor.login(usuario, password)
            servidor.send_message(mensaje)
        print(f"  Mail enviado a: {', '.join(destinatarios)}")
    except Exception:
        print("  No se pudo enviar el mail. Revisá el usuario y la contraseña de aplicación del .env.")