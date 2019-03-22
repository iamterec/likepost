import clearbit
import psycopg2
import json
from psycopg2 import ProgrammingError
from celery import Celery
from config import secret
from pyhunter import PyHunter
from requests.exceptions import ConnectionError

celery_app = Celery("users", broker="pyamqp://rabbitmq:5672")


def save_additional_data(user, data):
    query = "UPDATE users SET aditional_data = '{}' WHERE id = {}".\
        format(json.dumps(data), user["id"])
    try:
        conn = psycopg2.connect(host="postgres", database="likepost",
                                user=secret.DATABASE_USER,
                                password=secret.DATABASE_PASSWORD)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    # TO DO: Add more except cases here
    except ProgrammingError:
        print("ProgrammingError was raised during saving data")
    except:
        print("Error when save aditional data for user")
    finally:
        cursor.close()
        conn.close()

def save_verification(verdict, user):
    query = "UPDATE users SET verified = {} WHERE id = {}".\
        format(verdict, user["id"])
    print("Query is: ", query)
    try:
        conn = psycopg2.connect(host="postgres", database="likepost",
                                user=secret.DATABASE_USER,
                                password=secret.DATABASE_PASSWORD)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except ProgrammingError:
        print("ProgrammingError was raised during saving data")
    except:
        print("Error when save aditional data for user")
    finally:
        cursor.close()
        conn.close()

@celery_app.task
def get_aditional_data_for_user(user):
    clearbit.key = secret.CLEARBIT_KEY
    lookup = clearbit.Enrichment.find(email=user["email"])
    save_additional_data(user, lookup)

@celery_app.task
def verify_email(user):
    hunter = PyHunter(secret.EMAILHUNTER_KEY)
    try:
        result = hunter.email_verifier(user["email"]) #  returns a dict
        # print("Result is: ", result)
        # result data is a garbage, result is the same for a real email and
        # randomly generated one. So here is a magic rule for verification decision.
        verdict = True if result["score"] >= 70 and result["gibberish"] == False else False
        save_verification(verdict, user)
    except ConnectionError as e:
        print("ConnectionError was raised during email verification: ", e)
    except e:
        print("Exception was raised during email verification: ", e)

