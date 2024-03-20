import requests

maisons_villa_nice = [
    "https://v.seloger.com/s/crop/933x645/visuels/1/r/b/j/1rbjmsb2vv3fyalnno9xsk6e9mmtz73enjj39u7c0.jpg",
    "https://v.seloger.com/s/crop/363x320/visuels/0/9/g/l/09glm3kzowv8bedmadzee4jx3mnzplh21fbh8otas.jpg",
    "https://v.seloger.com/s/crop/363x320/visuels/1/h/4/1/1h41ckqa0jdy8136kfx0mxahqy5iej4ekzx6paqms.jpg",
    "https://v.seloger.com/s/cdn/x/visuels/2/3/3/l/233l7szxhh8915jumn4xxrly71uv2mapyh7vmc504.jpg"    
]

testeurs_userdata = [
    {
    "id_user": "", # pas besoin c'est rempli autom en backend
    "firstname_user": "string",
    "lastname_user": "string",
    "birthdate_user": "",
    "email_user": "string",
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
        "complement_adresse_2": "Appt. 21",
    }
]

testeur_tenant = []

testeur_owner = []

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