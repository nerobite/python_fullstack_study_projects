from advanced_python.import_module_package.app.application.salary import person_salary
from advanced_python.logger.logger_2 import logger

@logger('main.log')
def main():
    return print(person_salary())

if __name__ == '__main__':
    main()