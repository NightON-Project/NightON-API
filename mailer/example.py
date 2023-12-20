import mailerNightON


# Envoi d'un mail simple
mailer = mailerNightON.Mailer(5) # Temps de refresh en secondes
mailer.sendEmail("titouan.schotte@gmail.com", "MAIL TEST", "test", {
    "surname": "Titouan",
    "name": "Schotté",
})


# Envoi du mail de code.
code, operationResult = mailer.sendEmailCode("titouan.schotte@gmail.com")

if operationResult:
    print(code)