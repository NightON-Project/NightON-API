from mysql.connector import Error
from utils.dao.ConnexionDAO import ClassConnexionDB
from ressources.create_nighton_db import (
    userdata_table_query,
    tenants_table_query,
    owners_table_query,
    login_table_query,
    rental_agreements_table_query,
    properties_table_query
    )


def execute_query(connection, query, log_comment):
    cursor = connection.cursor()
    res = None
    try:
        res = cursor.execute(query)
        print(f"{log_comment} executed successfully")
        if res is not None or 'select' in query.lower():
            print(cursor.fetchall())
            return res
    except Error as e:
        print(f"The error '{e}' occurred for {log_comment}")


def run_migration(dbname="test_db"):

    # create conn to db server
    connection = ClassConnexionDB().getConnexion(MODE="migration_az")
    
    # Create a new database if not exists
    create_database_query = f"CREATE DATABASE IF NOT EXISTS {dbname}"
    use_database_query = f"USE {dbname}"

    execute_query(connection, create_database_query, "Database creation")
    execute_query(connection, use_database_query, f"Switched to db : {dbname}")

    # migration queries 
    migration = execute_query
    check_table = lambda table_name: f"SELECT * FROM {table_name}"

    # userdata > owners > properties > tenants > rental_agreement > login
    migration(connection, userdata_table_query, "Run migration :: userdata")
    migration(connection, owners_table_query, "Run migration :: owners")
    migration(connection, properties_table_query, "Run migration :: properties_table")
    migration(connection, tenants_table_query, "Run migration :: tenants")
    migration(connection, rental_agreements_table_query, "Run migration :: rental_agreements")
    migration(connection, login_table_query, "Run migration :: login_table")
    
    execute_query(connection, check_table('userdata'), "userdata checked")
    execute_query(connection, check_table('tenants'), "tenants checked")
    execute_query(connection, check_table('owners'), "owners checked")
    execute_query(connection, check_table('properties_table'), "properties_table checked")
    execute_query(connection, check_table('rental_agreements'), "rental_agreements checked")
    execute_query(connection, check_table('login_table'), "login_table checked")
