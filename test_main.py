import requests

testeurs_Userdata = [
  {
    "id_user": "010",
    "name_user": "Sophie Martin",
    "birthdate_user": "12/05/1998",
    "email_user": "sophie.martin@testeur.com",
    "telephone_user": "06 12 34 56 78",
    "pays": "France",
    "code_postal": "75000",
    "ville": "Paris",
    "numero_rue": "12",
    "nom_rue": "Rue de la République",
    "complement_adresse_1": "",
    "complement_adresse_2": ""
  },
  {
    "id_user": "011",
    "name_user": "Alexandre Dupont",
    "birthdate_user": "03/09/1997",
    "email_user": "alex.dupont@testeur.com",
    "telephone_user": "06 98 76 54 32",
    "pays": "France",
    "code_postal": "69000",
    "ville": "Lyon",
    "numero_rue": "27",
    "nom_rue": "Avenue des Fleurs",
    "complement_adresse_1": "",
    "complement_adresse_2": "Appt. 21"
  },
  {
    "id_user": "012",
    "name_user": "Emma Lefevre",
    "birthdate_user": "18/11/1999",
    "email_user": "emma.lefevre@testeur.com",
    "telephone_user": "07 45 32 12 89",
    "pays": "France",
    "code_postal": "31000",
    "ville": "Toulouse",
    "numero_rue": "8",
    "nom_rue": "Boulevard de la Liberté",
    "complement_adresse_1": "Résidence Belle Vue",
    "complement_adresse_2": "Bâtiment C"
  },
  {
    "id_user": "013",
    "name_user": "Thomas Moreau",
    "birthdate_user": "22/07/1996",
    "email_user": "thomas.moreau@testeur.com",
    "telephone_user": "06 77 88 99 00",
    "pays": "France",
    "code_postal": "44000",
    "ville": "Nantes",
    "numero_rue": "16",
    "nom_rue": "Rue des Alizés",
    "complement_adresse_1": "",
    "complement_adresse_2": "Porte 4"
  },
  {
    "id_user": "014",
    "name_user": "Camille Roussel",
    "birthdate_user": "29/04/1997",
    "email_user": "camille.roussel@testeur.com",
    "telephone_user": "06 23 45 67 89",
    "pays": "France",
    "code_postal": "33000",
    "ville": "Bordeaux",
    "numero_rue": "18",
    "nom_rue": "Avenue des Vignes",
    "complement_adresse_1": "Résidence du Lac",
    "complement_adresse_2": "Appt. 5"
  },
  {
    "id_user": "015",
    "name_user": "Leroy",
    "birthdate_user": "15/07/1999",
    "email_user": "leroy@example.fr",
    "telephone_user": "06 98 76 54 32",
    "pays": "France",
    "code_postal": "69000",
    "ville": "Lyon",
    "numero_rue": "12",
    "nom_rue": "Avenue des Fleurs",
    "complement_adresse_1": "Batiment C, Etage 2",
    "complement_adresse_2": ""
  },
  {
    "id_user": "015",
    "name_user": "Leroy",
    "birthdate_user": "15/07/2006",
    "email_user": "leroy@testeur.fr",
    "telephone_user": "06 98 76 54 32",
    "pays": "France",
    "code_postal": "69000",
    "ville": "Lyon",
    "numero_rue": "12",
    "nom_rue": "Avenue des Fleurs",
    "complement_adresse_1": "Batiment C",
    "complement_adresse_2": "Etage 2"
  }
]

if __name__=='__main__':

    ROOT_URL = 'http://localhost:8000/users/'
    # Assuming your FastAPI server URL and endpoint
    # url = ROOT_URL  # URL à modifier 
    # data = testeurs_Userdata[-2]
    # response = requests.post(url, json=data)
    # print(response.json()) 

    url = ROOT_URL
    print(f'Connecting to {url}')
    new_data = testeurs_Userdata[-1]
    response = requests.put(url+str(new_data["id_user"]), json=new_data)
    print(response.json())

    response = requests.put('http://your-fastapi-endpoint/users/001', json=update_data)
