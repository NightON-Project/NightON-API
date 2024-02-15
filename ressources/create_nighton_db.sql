CREATE TABLE IF NOT EXISTS userdata(
    id_user VARCHAR(255) PRIMARY KEY, 
    firstname_user VARCHAR(80), 
    lastname_user VARCHAR(80), 
    birthdate_user VARCHAR(80), 
    email_user VARCHAR(80), 
    telephone_user VARCHAR(80), 
    pays VARCHAR(80), 
    code_postal VARCHAR(80), 
    ville VARCHAR(80), 
    numero_rue VARCHAR(80), 
    nom_rue VARCHAR(80), 
    complement_adresse_1 VARCHAR(80), 
    complement_adresse_2 VARCHAR(80));

CREATE TABLE IF NOT EXISTS login_table(
    email_user VARCHAR(80) PRIMARY KEY,
    code VARCHAR(5));


CREATE TABLE IF NOT EXISTS tenants(
    id_tenant VARCHAR(255) PRIMARY KEY,
    id_user VARCHAR(255),
    email_user VARCHAR(255),
    status_demande VARCHAR(80),
    date_demande VARCHAR(80),
    id_property VARCHAR(255),
    CONSTRAINT fk_id_properties_table_tenants FOREIGN KEY(id_property) REFERENCES properties_table(id_property) ON DELETE CASCADE
    CONSTRAINT fk_userdata_tenants FOREIGN KEY(id_user) REFERENCES userdata(id_user) ON DELETE CASCADE
);

ALTER TABLE `u169130812_nighton_test`.`tenants` ADD starting_date_demand VARCHAR(80);
ALTER TABLE `u169130812_nighton_test`.`tenants` ADD ending_date_demand VARCHAR(80);


CREATE TABLE IF NOT EXISTS owners(
    id_owner VARCHAR(255) PRIMARY KEY,
    id_user VARCHAR(255),
    email_user VARCHAR(255),
    status_demande VARCHAR(80),
    date_demande VARCHAR(80),
    CONSTRAINT fk_userdata_owners FOREIGN KEY(id_user) REFERENCES userdata(id_user) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS rental_agreements(
    id_contrat VARCHAR(255) PRIMARY KEY,
    id_tenant VARCHAR(255),
    id_owner VARCHAR(255),
    id_property VARCHAR(255),
    starting_date_act_rent VARCHAR(255),
    ending_date_act_rent VARCHAR(255),
    CONSTRAINT fk_rental_agreements_tenants FOREIGN KEY(id_tenant) REFERENCES tenants(id_tenant) ON DELETE CASCADE,
    CONSTRAINT fk_rental_agreements_owners FOREIGN KEY(id_owner) REFERENCES owners(id_owner) ON DELETE CASCADE,
    CONSTRAINT fk_rental_agreements_properties FOREIGN KEY(id_property) REFERENCES properties(id_property) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS sessions_infos(
    session_id VARCHAR(255) PRIMARY KEY,
    email_user VARCHAR(255),
    mail_code VARCHAR(5),
    is_active BOOLEAN,
    access_token VARCHAR(1000),
    refresh_token VARCHAR(1000)
)


CREATE TABLE IF NOT EXISTS properties(
    id_property VARCHAR(255) PRIMARY KEY,
    id_owner VARCHAR(255),
    categ_property VARCHAR(255),
    ss_categ_property VARCHAR(255),
    is_available BOOLEAN,
    renting_price_amount FLOAT,
    renting_caution_amount FLOAT,
    global_description VARCHAR(1000),
    is_insured BOOLEAN,
    CONSTRAINT fk_properties_owners FOREIGN KEY(id_owner) REFERENCES owners(id_owner) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS properties_table(

    -- general : 8
    id_property VARCHAR(255) PRIMARY KEY,
    nom_affichage VARCHAR(80),
    prix FLOAT, 
    availability_status VARCHAR(80), -- field validator ou enum {dispo, reservé, plus dispo}
    date_dispo_debut VARCHAR(80), -- type date
    date_dispo_fin VARCHAR(80), -- aussi
    category VARCHAR(80), -- (RP, Terrain, RS)
    ss_category VARCHAR(80), -- (Maison, Appart)
    
    -- details global 17
    nbre_pieces INT(2), -- 1 - 100 int
    nbre_rooms INT(2), -- # 1-100 int
    sup_totale_m2 FLOAT,
    has_bathroom BOOLEAN,
    nbre_bathrooms INT(2),
    has_toilets INT(2),
    nbre_toilets INT(2),
    has_garden BOOLEAN,
    sup_garden FLOAT,
    has_pool BOOLEAN,

    has_cameras BOOLEAN,
    has_available BOOLEAN, --- wifi
    has_detecteur_fumee BOOLEAN,

    has_climatiseur BOOLEAN,
    has_place_parking BOOLEAN,
    has_objets_cassables BOOLEAN,
    descr_complementaire TEXT,

    -- images 10
    url1 VARCHAR(1000),
    url2 VARCHAR(1000),
    url3 VARCHAR(1000),
    url4 VARCHAR(1000),
    url5 VARCHAR(1000),
    url6 VARCHAR(1000),
    url7 VARCHAR(1000),
    url8 VARCHAR(1000),
    url9 VARCHAR(1000),
    url10 VARCHAR(1000),

    -- localisation 7
    pays VARCHAR(80),
    code_postal VARCHAR(80),
    ville VARCHAR(255),
    numero_rue VARCHAR(80),
    nom_rue VARCHAR(255),
    complement_adresse_1 VARCHAR(255),
    complement_adresse_2 VARCHAR(255),

    -- legal 7 
    nighton_caution BOOLEAN,
    nighton_caution_id VARCHAR(1000),
    id_owner VARCHAR(255),
    confirmation_mairie BOOLEAN,
    n0_declaration_meuble_mairie VARCHAR(1000),
    assert_is_RP BOOLEAN,
    assert_is_RS BOOLEAN,

    CONSTRAINT fk_properties_table_owners FOREIGN KEY(id_owner) REFERENCES owners(id_owner) ON DELETE CASCADE
);

-- TESTEURS
---- USER FICTIF -> OWNER 
SELECT * from userdata; --- f072baa9-c261-445c-b0a2-e930f0d952df	:: emma taumme

---- PROPRIO FICTIF
INSERT INTO owners VALUES ("testeur_1", "f072baa9-c261-445c-b0a2-e930f0d952df", "XXXX-0000-smtg");

---- BIEN FICTIF 
INSERT INTO properties_table VALUES (
    'property_1', 'Belle Maison', 2500.00, 'dispo', '2023-01-01', '2023-12-31', 'RP', 'Maison', 
    5, 3, 400.5, true, 2, true, 2, true, 100.5, true, false, true, true, true, false, true, 'Salon spacieux, cuisine moderne', 
    'https://exemple.com/image1.jpg', 
    'https://exemple.com/image2.jpg', 
    'https://exemple.com/image3.jpg', 
    'https://exemple.com/image4.jpg', 
    'https://exemple.com/image5.jpg', 
    'https://exemple.com/image6.jpg', 
    'https://exemple.com/image7.jpg', 
    'https://exemple.com/image8.jpg', 
    'https://exemple.com/image9.jpg', 
    '', 
    'France', '75001', 'Paris', '123', 'Rue Principale', 'Près de la station de métro', 'Proche des écoles', 
    true, 'ID123456', 'testeur_1', true, 'D123456', true, false
);

INSERT INTO properties_table VALUES (
    'property_2', 'Belle Villa avec Piscine en province', 1500.00, 'dispo', '2023-01-01', '2024-12-31', 'RS', 'Maison', 
    5, 3, 400.5, true, 2, true, 2, true, 100.5, true, false, true, true, true, false, true, 'Salon et cuisine modernes. Déco minimaliste.', 
    'https://exemple2.com/image1.jpg', 
    'https://exemple2.com/image2.jpg', 
    'https://exemple2.com/image3.jpg', 
    'https://exemple2.com/image4.jpg', 
    'https://exemple2.com/image5.jpg', 
    'https://exemple2.com/image6.jpg', 
    '', 
    '', 
    '', 
    '', 
    'France', '35007', 'Rennes', '27', 'Rue du maïs', '', '', 
    true, 'ID123456', 'testeur_1', true, 'D75810', false, true
);