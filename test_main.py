import requests


testeurs_userdata = [
    {
    "id_user": "",
    "firstname_user": "Joel",
    "lastname_user": "Duval",
    "birthdate_user": "",
    "email_user": "titouchkpoubelle@gmail.com",
    "telephone_user": "",
    "pays": "",
    "code_postal": "",
    "ville": "",
    "numero_rue": "",
    "nom_rue": "",
    "complement_adresse_1": "",
    "complement_adresse_2": "",
    "url1_piece": "",
    "url2_piece": ""
    },
    { #auth/from firebase
    "id_user": "",
    "firstname_user": "",
    "lastname_user": "",
    "birthdate_user": "",
    "email_user": "titouan.scht@gmail.com",
    "telephone_user": "",
    "pays": "",
    "code_postal": "",
    "ville": "",
    "numero_rue": "",
    "nom_rue": "",
    "complement_adresse_1": "",
    "complement_adresse_2": "",
    "url1_piece": "",
    "url2_piece": ""
    }
]

testeur_tenant = [
    {
  "email_user": "",
  "nom": "Joel",
  "prenom": "Duval",
  "date_naissance": "19-03-2023",
  "numero_rue": "02",
  "nom_rue": "Square Thiers",
  "ville": "Paris",
  "code_postal": "75016",
  "url_piece1": "https://www.petiterepublique.com/wp-content/uploads/2017/02/changement-identite-paul.jpeg",
  "url_piece2": "https://www.petiterepublique.com/wp-content/uploads/2017/02/changement-identite-paul.jpeg",
  "status_demande": "waiting",
  "date_demande": "20-03-2024",
  "id_logement": "",
  "starting_date_demand": "15-04-2024",
  "ending_date_demand": "20-04-2024"
}
]


testeur_owner = [
    {
  "email_user": "",
  "nom": "Dupont",
  "prenom": "Youssef",
  "date_naissance": "20-03-1990",
  "numero_rue": "03",
  "nom_rue": "Rue de la paix",
  "ville": "Cergy",
  "code_postal": "95002",
  "url_piece1": "https://www.lemondedesartisans.fr/sites/lemondedesartisans.fr/files/illustrations/articles/filigrane-facile.png",
  "url_piece2": "https://th.bing.com/th/id/OIP.h6dYURehTyTE9-bOIEyCVgHaE4?w=253&h=180&c=7&r=0&o=5&dpr=1.4&pid=1.7",
  "status_demande": "waiting",
  "date_demande": "19-03-2024",
  "logements": [
    {
      "id_property": "",
      "nom_affichage": "Blue Senses Villa",
      "prix": 2700,
      "availabilty_status": "dispo",
      "date_dispo_debut": "01-04-2024",
      "date_dispo_fin": "01-05-2024",
      "category": "Maison",
      "ss_category": "Villa",
      "nbre_pieces": 12,
      "nbre_rooms": 10,
      "sup_totale_m2": 500,
      "has_bathroom": true,
      "nbre_bathrooms": 5,
      "has_toilets": true,
      "nbre_toilets": 5,
      "has_garden": true,
      "sup_garden": 0,
      "has_pool": true,
      "has_cameras": true,
      "wifi_available": true,
      "has_detecteur_fumee": true,
      "has_climatiseur": true,
      "has_place_parking": true,
      "has_objets_cassables": true,
      "descr_complementaire": "Blue Senses Balcony Villa (55 Sq m) is part of a two-storey Villa in Santorini Island that can accommodate up to 8 guests in total-couples, friends or families.It is at the upper Floor,  fully autonomous and can host up to 4 guests. Fitted with a King size bed and two single sofa-beds, en-suite bathroom with shower and fully equipped kitchenette. Its  balcony overlooks the surrounding landscapes, and the Aegean Sea. Included: a private swimming pool at the ground-backside level of the complex.",
      "url1": "https://a0.muscache.com/im/pictures/295d536e-95a1-4df3-a01e-7098590f1a2f.jpg?im_w=1200",
      "url2": "https://a0.muscache.com/im/pictures/f7a53928-0b01-4efe-9407-bee0e7da68fa.jpg?im_w=720",
      "url3": "https://a0.muscache.com/im/pictures/6d96b1f6-faa1-459c-af92-44648295556a.jpg?im_w=720",
      "url4": "https://a0.muscache.com/im/pictures/41375439-c922-4cfc-b5cc-ba8d1946dfe3.jpg?im_w=1200",
      "url5": "https://a0.muscache.com/im/pictures/4620f962-8bea-45e7-bac1-665c8bc02d98.jpg?im_w=1200",
      "url6": "https://a0.muscache.com/im/pictures/f38a6b55-b608-4806-ad8a-cac0024f71ae.jpg?im_w=720",
      "url7": "https://a0.muscache.com/im/pictures/3a9ef28b-4576-4885-82df-4a52e686db05.jpg?im_w=1200",
      "url8": "https://a0.muscache.com/im/pictures/af25888c-8c48-4005-a4a1-03d4d7f173c7.jpg?im_w=720",
      "url9": "",
      "url10": "",
      "pays": "",
      "code_postal": "78120",
      "ville": "Rambouillet",
      "numero_rue": "51",
      "nom_rue": "Allée des Cerisiers",
      "complement_adresse_1": "",
      "complement_adresse_2": "",
      "nighton_caution": false,
      "nighton_caution_id": "",
      "id_owner": "",
      "confirmation_mairie": true,
      "n0_declaration_meuble_mairie": "string",
      "assert_is_RP": true,
      "assert_is_RS": true
    }
  ]
}
]

testeur_property = []

test_login = []



if __name__ == "__main__":

    ROOT_URL = ""

    url = ROOT_URL
    print(f"Connecting to {url}")
    new_data = testeurs_Userdata[-1]
    response = requests.put(url + str(new_data["id_user"]), json=new_data)
    print(response.json())

    response = requests.put("http://your-fastapi-endpoint/users/001", json=update_data)

    # u1 u2 creations de compte
    # u1 login auth request
    # u1 login 
    # u2 firebase auth
    # u2 login
    # u1 dmd publication
    # afficher l'accueil -> pas de p1
    # validation demande u1
    # afficher accueil -> p1
    # u2 dmd résa p1
    # validation dmd u2
    # ... 