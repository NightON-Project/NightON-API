# NightON-API

L'API interface entre la bdd et la partie backend du site. <br>

Déjà fait : 
  - définition de la dataclass "UserClass" qui permet de faire valider les données communiquées à la bdd et qui transitent par l'API.
  - test de l'endpoint enregister_utilsateur (requête post).
  - vérification de la présence effective des données envoyées dans la base sur le localhost.

Utilisation : 
  - installer + configurer un serveur sql (mysql server ou mamp ou xamp ...)
  - créer une bdd avec les infos spécifiées dans le fichier <i>config.json</i>
  - créer la table userdata (user_id, user_email, display_user_name)
  - exécuter le UserClass.py (dans vscode)
  - <b>Résultat attendu :</b>
      * uvicorn (de fastAPI) envoie un lien (dans le terminal) qui permet de se connecter sur le swaggerUI
      * A partir du swaggerUI on peut tester l'API (pour moment seul l'endpoint "enregistrer_utilisateur" est utilisable).
      * Ce dernier permet d'ajouter des instances de users à la base sur le localhost.
      * Après, avec une requête sql, on peut vérifier que les données ont bien été enregistrées.

Reste à faire : 
  - dockeriser mysql server pour rendre flexible l'utilisation de l'api en mode dev.
  - modéliser la bdd (théorie)
  - écrire un script sql qui créé la bdd
  - automatiser le tout dans un main.py
