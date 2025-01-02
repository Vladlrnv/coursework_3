import requests
from requests import RequestException


class HeadHunterAPI:
    """ Класс для работы с API HeadHunter """

    def __init__(self):
        self.__url = 'https://api.hh.ru/employers'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__employers = []

    def __connect(self):
        """ Метод для get запроса """
        try:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code == 200:
                return response
            else:
                raise RequestException
        except Exception as e:
            print(e)

    def load_vacancies(self, keyword: list[str]):
        """ Данный метод позволяет отобрать всю информацию по вакансиям,
        в котором есть ключевое слово (переменная - keyword) """
        for key in keyword[0:10]:
            self.__params['text'] = key
            self.__params['page'] = 0

            while self.__params.get('page') != 10:
                response = self.__connect()
                employers: list[dict] = response.json()['items']
                for emp in employers:
                    if emp["open_vacancies"] > 0:
                        if len(self.__employers) < 10:
                            self.__employers.append(emp)
                            break
                self.__params['page'] += 1
        return self.__employers