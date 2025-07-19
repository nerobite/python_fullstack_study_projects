import pandas as pd

from advanced_python.import_module_package.app.application.db.people import Person


def person_salary():
    person_instance = Person()
    salary = person_instance.get_salary()
    person = person_instance.get_person()
    return pd.merge(person, salary, how='left', on='person_id')


if __name__ == '__main__':
    info = person_salary()
    print(info)