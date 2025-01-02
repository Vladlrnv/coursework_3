import psycopg2


class DBManager:

    def __init__(self, params):
        self.params = params

    def connects(self, button: str):
        """ Метод подключения к БД и открытия курсора """
        try:
            if button == "start":
                conn = psycopg2.connect(database="data_headhunter", **self.params)
                cur = conn.cursor()
                return cur

            elif button == "stop":
                conn = psycopg2.connect(database="data_headhunter", **self.params)
                cur = conn.cursor()

                cur.close()
                conn.close()
        except Exception as e:
            print(e)

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """  Метод, который получает список всех компаний и
        количество вакансий у каждой компании """

        cur = self.connects("start")
        list_companies_and_vacancies_count = []

        cur.execute(
            "SELECT employers.name, COUNT(vacancies.id_employers) "
            "FROM employers INNER JOIN vacancies USING(id_employers) GROUP BY employers.name")

        employers_name = cur.fetchall()

        self.connects("stop")

        for name_and_quantity in employers_name:
            dict_name_and_quantity = {"name": name_and_quantity[0], "quantity": name_and_quantity[1]}

            list_companies_and_vacancies_count.append(dict_name_and_quantity)
        #  [{}]
        return list_companies_and_vacancies_count

    def get_all_vacancies(self) -> list[dict]:
        """ Метод, получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию """
        list_information_on_vacancies = []
        cur = self.connects("start")

        cur.execute(
            "SELECT employers.name, vacancies.name, vacancies.salary, vacancies.alternate_url "
            "FROM employers INNER JOIN vacancies USING(id_employers)")

        vacancies = cur.fetchall()
        self.connects("stop")

        for vacancy in vacancies:
            information_vacancies = {'name_employer': vacancy[0],
                                     'name_vacanci': vacancy[1],
                                     'salary': vacancy[2],
                                     'alternate_url': vacancy[3]}

            list_information_on_vacancies.append(information_vacancies)
        #  [{}]
        return list_information_on_vacancies

    def get_avg_salary(self) -> int:
        """ Метод, получает среднюю зарплату по вакансиям """
        cur = self.connects("start")

        cur.execute("SELECT AVG(salary) FROM vacancies")

        c = cur.fetchall()
        avg_salary = round(c[0][0])

        self.connects("stop")

        return avg_salary

    def get_vacancies_with_higher_salary(self) -> list[dict]:
        """ Метод, получает список всех вакансий, у которых зарплата
        выше средней по всем вакансиям """
        list_salary_above_average = []
        cur = self.connects("start")

        cur.execute("SELECT name, id_vacancies FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)")

        salary_above_average = cur.fetchall()
        self.connects("stop")

        for vacancy in salary_above_average:
            dict_name_and_id = {'name': vacancy[0], 'id_vacancies': vacancy[1]}
            list_salary_above_average.append(dict_name_and_id)

        return list_salary_above_average

    def get_vacancies_with_keyword(self, word_search: str) -> list[dict]:
        """ Метод, получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python """
        list_vacancy = []
        cur = self.connects("start")

        if isinstance(word_search, str):
            cur.execute(f"SELECT * FROM vacancies WHERE name LIKE '%{word_search[1:]}%'")

            vacancies = cur.fetchall()
            self.connects("stop")

            for vacancy in vacancies:
                dict_vacancy = {'id_vacancies': vacancy[0],
                                'id_employers': vacancy[1],
                                'name': vacancy[2],
                                'salary': vacancy[3],
                                'alternate_url': vacancy[4]}
                list_vacancy.append(dict_vacancy)

        return list_vacancy