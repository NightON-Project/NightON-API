import mailerNightON

mailer = mailerNightON.Mailer(timeout=5)
e = mailer.sendEmail(
    emailDestination="titouan.schotte@gmail.com",
    mailTitle='VOTRE CODE DE CONNEXION',
    mailContentTemplateFile='code_verification',
    placeholders={
        "surname": "Titouan",
        "name": "Schotté"
    }
)
print(e)