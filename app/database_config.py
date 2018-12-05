import psycopg2
import os

#url = "dbname='ireporter' host='localhost' port='5432' user='postgres' password='123abc'"
url = os.getenv('DATABASE_URL')


def connection(url):
    conn = psycopg2.connect(url)
    return conn


def init_db():
    conn = connection(url)
    return conn


def create_tables():
    conn = connection(url)
    curr = conn.cursor()
    queries = tables()
    for query in queries:
        curr.execute(query)
    conn.commit()
    #curr = conn.cursor
    #queries = tables()


def destroy_tables():
    pass


def tables():
    users_table = """CREATE TABLE IF NOT EXISTS users (
        user_id serial PRIMARY KEY NOT NULL,
        firstname character varying(50) NOT NULL,
        lastname character varying(50) NOT NULL,
        othernames character varying(50),
        username character varying(50) NOT NULL,
        email character varying(50),
        phonenumber character varying(50),
        registered timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
        isAdmin boolean NOT NULL
    )"""

    incidents_table = """CREATE TABLE IF NOT EXISTS incidents (
        incidents_id serial PRIMARY KEY NOT NULL,
        type character varying(20) NOT NULL,
        status character varying(100) NOT NULL,
        comment character varying(200) NOT NULL,
        createdOn timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
        location character varying(200) NOT NULL,
        images character varying(200) NOT NULL,
        videos character varying(200) NOT NULL
    )"""

    queries = [users_table, incidents_table]
    return queries
