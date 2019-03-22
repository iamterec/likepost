from celery import Celery
from config.secret import CLEARBIT_KEY, DATABASE_USER, DATABASE_PASSWORD
import clearbit
import psycopg2
import json


clearbit.key = CLEARBIT_KEY

celery_app = Celery("users", broker="pyamqp://rabbitmq:5672")


def add_data_to_user(user, data):
    query = "UPDATE users SET aditional_data = '{}' WHERE id = {}".\
        format(json.dumps(data), user["id"])
    try:
        conn = psycopg2.connect(host="postgres", database="likepost",
                                user=DATABASE_USER, password=DATABASE_PASSWORD)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    # TO DO: Add more except cases here
    except:
        print("Error when save aditional data for user")
    finally:
        cursor.close()
        conn.close()


@celery_app.task
def get_aditional_data_for_user(user):
    lookup = clearbit.Enrichment.find(email=user["email"])
    add_data_to_user(user, lookup)

@celery_app.task
def verify_email(user):
    pass
