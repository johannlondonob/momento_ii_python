from os import environ
from dotenv import load_dotenv, find_dotenv
import pymysql

load_dotenv(find_dotenv())


def database():
    try:  
        return pymysql.connect(
            host=environ.get("APP_DATABASE_HOST"),
            user=environ.get("APP_DATABASE_USER"),
            passwd=environ.get("APP_DATABASE_PSSW"),
            database=environ.get("APP_DATABASE_NAME"),
        )
    except pymysql.Error as error:
        print("No se pudo establecer conexión a la base de datos")
        return False
