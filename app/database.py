import psycopg2



with psycopg2.connect("dbname = vorex_db user = charantm" ) as conn:

    with conn.cursor() as cur:

        # cur.execute(
        #     """create table if not exists post (id SERIAL PRIMARY KEY, title CHARACTER VARYING(50) NOT NULL, content CHARACTER VARYING(500) NOT NULL, public BOOLEAN DEFAULT TRUE, created_at DATE DEFAULT NOW())"""
        # )

        # cur.execute(
        #     """insert into post(title , content) values ('cities', 'i need to explore the cities in karnataka')"""
        # )

        cur.execute("select username from auth_user")
        print(cur.fetchall())

        conn.commit()


