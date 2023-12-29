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
    moyen_paiement VARCHAR(80),
    CONSTRAINT fk_userdata_tenants FOREIGN KEY(id_user) REFERENCES userdata(id_user) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS owners(
    id_owner VARCHAR(255) PRIMARY KEY,
    id_user VARCHAR(255),
    moyen_paiement VARCHAR(80),
    CONSTRAINT fk_userdata_owners FOREIGN KEY(id_user) REFERENCES userdata(id_user) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS properties(
    id_property VARCHAR(255) PRIMARY KEY,
    id_owner VARCHAR(255),
    type_property VARCHAR(255),
    is_available BOOLEAN,
    renting_price_amount FLOAT,
    renting_caution_amount FLOAT,
    global_description VARCHAR(1000),
    is_insured BOOLEAN,
    CONSTRAINT fk_properties_owners FOREIGN KEY(id_owner) REFERENCES owners(id_owner) ON DELETE CASCADE
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