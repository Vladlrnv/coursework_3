import psycopg2
import requests


def creature_bd(params: dict):
    """ Создание/подключение к базе данных """
    # -*- coding: utf-8 -*-

    conn = psycopg2.connect(database="postgres", **params)
    conn.autocommit = True

    with conn.cursor() as curs:
        curs.execute("DROP DATABASE Data_HeadHunter;")
        curs.execute("CREATE DATABASE Data_HeadHunter;")

    # curs.execute("ALTER DATABASE Data_HeadHunter CHARACTER SET utf8 COLLATE utf8_unicode_ci;")
    conn.close()


def creature_table(params: dict):
    """ Функция для создания таблиц в БД """
    con = psycopg2.connect(database="data_headhunter", **params)

    with con.cursor() as cur:

        # cur.execute("DROP TABLE vacancies")
        # cur.execute("DROP TABLE employers")

        cur.execute("""CREATE TABLE employers (
                        id_employers INT PRIMARY KEY,
                        name VARCHAR,
                        alternate_url TEXT,
                        open_vacancies INT)""")

        cur.execute("""CREATE TABLE vacancies (
                        id_vacancies INT PRIMARY KEY,
                        id_employers INT,
                        name VARCHAR,
                        salary INT,
                        alternate_url TEXT,
                        FOREIGN KEY (id_employers) REFERENCES employers(id_employers)
                        )""")

    con.commit()
    con.close()


def save_data_to_database(hh_data: list[dict], params: dict):
    """ Функция для записи данных в таблицы """
    conn = psycopg2.connect(database="data_headhunter", **params)
    conn.autocommit = True

    for data in hh_data:
        with conn.cursor() as cur:

            # cur.execute("TRUNCATE TABLE vacancies CASCADE")
            # cur.execute("TRUNCATE TABLE employers CASCADE")

            cur.execute(
                "INSERT INTO employers(id_employers, name, alternate_url, open_vacancies) "
                "VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (data.get('id'), data.get('name'), data.get('alternate_url'), data.get('open_vacancies')))

            response = requests.get(data.get('vacancies_url'))
            if response.status_code == 200:
                list_vacancies: list[dict] = response.json()['items']

                for vac in list_vacancies:
                    if vac.get('salary') is not None:
                        if vac.get('salary').get('to') is not None:
                            cur.execute("INSERT INTO vacancies"
                                        "(id_vacancies, id_employers, name, salary, alternate_url) "
                                        "VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                                        (vac.get('id'), data.get('id'), vac.get('name'), vac.get('salary').get('to'),
                                         vac.get('alternate_url')))
                        else:
                            cur.execute("INSERT INTO vacancies"
                                        "(id_vacancies, id_employers, name, salary, alternate_url) "
                                        "VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                                        (vac.get('id'), data.get('id'), vac.get('name'), vac.get('salary').get('from'),
                                         vac.get('alternate_url')))

    conn.close()