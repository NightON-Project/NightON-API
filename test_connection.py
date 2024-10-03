import json, time
import mysql.connector
from mysql.connector import Error
from utils.controller.migrationC import *

# test_db
# test_db02

def test_connection():
    pass

def test_migration():
    run_migration(dbname="nighton_db")
