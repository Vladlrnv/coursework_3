def str_get_companies_and_vacancies_count(sum_vacancies: list[dict]) -> str:
    """ Функция для вывода данных в виде строки, полученных после метода:
    get_companies_and_vacancies_count """
    response = ''

    for vacancies in sum_vacancies:
        print(vacancies)
        res = f'Компания: {vacancies.get('name')}, Количество открытых вакансий: {vacancies.get('quantity')}\n'
        response += res

    return response


def str_get_all_vacancies(sum_vacancies: list[dict]) -> str:
    """ Функция для вывода данных в виде строки, полученных после метода:
    get_all_vacancies """
    response = ''

    for vacancies in sum_vacancies:
        res = (f'Название компании: {vacancies.get('name_employer')}, '
               f'Название вакансии: {vacancies.get('name_vacanci')}, '
               f'Зарплата: {vacancies.get('salary')}, '
               f'Альтернативный урл: {vacancies.get('alternate_url')}\n')
        response += res

    return response


def str_get_avg_salary(sum_vacancies: int) -> str:
    """ Функция для вывода данных в виде строки, полученных после метода:
    get_avg_salary """
    response = (f'Средняя зарплаты по вакансиям: {sum_vacancies}\n')

    return response


def str_get_vacancies_with_higher_salary(sum_vacancies: list[dict]) -> str:
    """ Функция для вывода данных в виде строки, полученных после метода:
    get_vacancies_with_higher_salary """
    response = ''

    for vacancies in sum_vacancies:
        res = (f'Название компании: {vacancies.get('name')}, '
               f'ID компании: {vacancies.get('id_vacancies')}\n')
        response += res

    return response


def str_get_vacancies_with_keyword(sum_vacancies: list[dict]) -> str:
    """ Функция для вывода данных в виде строки, полученных после метода:
    get_vacancies_with_keyword """
    response = ''

    for vacancies in sum_vacancies:
        res = (f'ID компании: {vacancies.get('id_vacancies')}, '
               f'ID вакансии: {vacancies.get('id_employers')}, '
               f'Название вакансии: {vacancies.get('name')}, '
               f'Зарплата: {vacancies.get('salary')}, '
               f'Альтернативный урл: {vacancies.get('alternate_url')}\n')
        response += res

    return response


if __name__ == "__main__":
    list_v = [{"name": 'gd', "quantity": 8}, {"name": 'erghte', "quantity": 9}]
    print(str_get_companies_and_vacancies_count(list_v))