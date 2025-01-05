import smtplib
from email.mime.text import MIMEText

def send_notification(message):
    msg = MIMEText(message)
    msg['Subject'] = 'Alerte automatisation'
    msg['From'] = 'slazarevic@myges.fr'
    msg['To'] = 'slazarevic@myges.fr'

    with smtplib.SMTP('smtp.example.com', 587) as serveur:
        serveur.starttls()
        serveur.login('slazarevic@myges.fr', 'mot_de_passe')
        serveur.send_message(msg)
        print("Notification envoyée.")

if __name__ == "__main__":
    send_notification("Test d'alerte depuis le projet FlashScore.") 
           