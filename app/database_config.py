import psycopg2


def connection(url):
    conn = psycopg2.connect(url)
    return conn


def create_tables(url):
    conn = connection(url)
    curr = conn.cursor()
    queries = tables()
    for query in queries:
        curr.execute(query)
    conn.commit()


def destroy_tables(url):
    conn = connection(url)
    curr = conn.cursor()
    # import pdb; pdb.set_trace()
    curr.execute("""DROP TABLE IF EXISTS incidents CASCADE;""")
    curr.execute("""DROP TABLE IF EXISTS users_table CASCADE;""")
    conn.commit()


def tables():
    users_table = """CREATE TABLE IF NOT EXISTS users_table (
        user_id serial PRIMARY KEY NOT NULL,
        firstname character varying(50) NOT NULL,
        lastname character varying(50) NOT NULL,
        othernames character varying(50),
        username character varying(50) NOT NULL,
        email character varying(50),
        phonenumber character varying(50),
        password character varying(50) NOT NULL,
        registered timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
        isAdmin boolean NOT NULL
    )"""

    incidents = """CREATE TABLE IF NOT EXISTS incidents (
        incidents_id serial PRIMARY KEY NOT NULL,
        createdOn timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
        createdBy int NOT NULL REFERENCES users_table(user_id),
        type_of_incident character varying(20) NOT NULL,
        status character varying(100) NOT NULL,
        comment character varying(200) NOT NULL,
        location character varying(200) NOT NULL,
        images character varying(200) NOT NULL,
        videos character varying(200) NOT NULL
    )"""

    queries = [users_table, incidents]
    return queries
