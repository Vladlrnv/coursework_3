import re
from src.classes import DBManager
from src.config import config
from src.connecting_API import HeadHunterAPI
from src.create_bd import creature_bd, save_data_to_database, creature_table
from src.utils import str_get_companies_and_vacancies_count, str_get_all_vacancies, str_get_avg_salary, \
    str_get_vacancies_with_higher_salary, str_get_vacancies_with_keyword


def main():
    hh_api = HeadHunterAPI()

    query = input("Введите поисковый запрос: ")
    search_query: list = re.split(", | |;", query)

    # search_query = ["магнит", "авто"]

    hh_data: list = hh_api.load_vacancies(search_query)

    # Создание базы данных
    params = config()
    creature_bd(params)

    # Создание таблиц
    creature_table(params)

    # Запись информации в таблицы
    save_data_to_database(hh_data, params)

    dbm = DBManager(params)

    search = dbm.get_companies_and_vacancies_count()
    result = str_get_companies_and_vacancies_count(search)
    print(result)

    search = dbm.get_all_vacancies()
    result = str_get_all_vacancies(search)
    print(result)

    search = dbm.get_avg_salary()
    result = str_get_avg_salary(search)
    print(result)

    search = dbm.get_vacancies_with_higher_salary()
    result = str_get_vacancies_with_higher_salary(search)
    print(result)

    word_search = input("Введите слово для поиска вакансии: ")

    search = dbm.get_vacancies_with_keyword(word_search)
    result = str_get_vacancies_with_keyword(search)
    print(result)


if __name__ == "__main__":
    main()

    # params = {"host": "localhost",
    #           "user": "postgres",
    #           "password": 1650,
    #           "port": 5432,
    #           "client_encoding": "utf-8"}