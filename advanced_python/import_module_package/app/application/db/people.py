import pandas as pd
import psycopg2
from advanced_python.import_module_package.app.core.config import HOST, DATABASE, USER, PASSWORD, PORT


class Person:
    def get_person(self) -> pd.DataFrame:
        """Получает всех сотрудников из таблицы hr.person и возвращает DataFrame."""
        conn = None
        try:
            conn = psycopg2.connect(
                host=HOST,
                database=DATABASE,
                user=USER,
                password=PASSWORD,
                port=PORT
            )

            query = """
                    SELECT person_id, first_name, middle_name, last_name, dob
                    FROM hr.person;
                    """
            return pd.read_sql(query, conn)  # Автоматически создаёт DataFrame

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Ошибка при получении данных: {error}")
            return pd.DataFrame()
        finally:
            if conn is not None:
                conn.close()

    def get_salary(self):
        """
        Получает последнюю зарплату сотрудника из таблицы employee_salary в PostgreSQL.
        """
        conn = None
        try:
            # Подключение к базе данных + указание схемы через options
            conn = psycopg2.connect(
                host=HOST,
                database=DATABASE,
                user=USER,
                password=PASSWORD,
                port=PORT
            )
            cur = conn.cursor()

            query = """
                select person_id, salary 
                from (
                    select emp_id,
                            salary,
                            row_number() over (partition by emp_id order by effective_from desc) as rn
                    from hr.employee_salary es) t
                join hr.employee e on e.emp_id  = t.emp_id
                where rn = 1;
            """

            return pd.read_sql(query, conn)

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Ошибка при получении данных: {error}")
            return pd.DataFrame()
        finally:
            if conn is not None:
                conn.close()


#выдает предупреждение UserWarning: pandas only supports SQLAlchemy, но работает, лень переделывать

if __name__ == "__main__":
    person_instance = Person()
    persons = person_instance.get_person()
    salary = person_instance.get_salary()
    print(persons.info())
    print(salary.head())