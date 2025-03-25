class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lector(self, lector, course, grade):
        if isinstance(lector, Lecturer) and course in lector.courses_attached and course in self.courses_in_progress:
            if not (0 <= grade <= 10):
                return "Ошибка: оценка должна быть от 0 до 10"
            if course in lector.grades:
                lector.grades[course] += [grade]
            else:
                lector.grades[course] = [grade]
        else:
            return 'Ошибка'

    def average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __le__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() <= other.average_grade()

    def __ge__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() >= other.average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() == other.average_grade()


    def __str__(self):
        avg_grade = self.average_grade()
        return (f'Студент\n'
                f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg_grade:.2f}\n'
                f'Курсы в процессе изучения: {", ".join(self.courses_in_progress) if self.courses_in_progress else "Нет"}\n'
                f'Завершенные курсы: {", ".join(self.finished_courses) if self.finished_courses else "Нет"}\n')



class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() <= other.average_grade()

    def __ge__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() >= other.average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() == other.average_grade()

    def __str__(self):
        avg_rate_lector = self.average_grade()
        return f'Лектор\n' \
               f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n' \
               f'Средняя оценка за лекции: {avg_rate_lector:.2f}\n'


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_student_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if not (0 <= grade <= 10):
                return "Ошибка: оценка должна быть от 0 до 10"
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Проверяющий\n' \
               f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n'


student1 = Student("Иван", "Иванов", "муж")
student1.courses_in_progress = ["Python", "Java"]
student1.finished_courses = ["Основы программирования"]
student1.grades = {"Python": [9, 10], "Java": [8, 7, 8]}

student2 = Student("Наталья", "Крыжовникова", "жен")
student2.courses_in_progress = ["Python", "Java"]
student2.finished_courses = ["Основы программирования"]
student2.grades = {"Python": [6, 7], "Java": [8, 10, 9]}

lector1 = Lecturer("Петр", "Петров")
lector1.courses_attached = ["Python"]
student1.rate_lector(lector1, "Python", 6)
student1.rate_lector(lector1, "Python", 7)
student2.rate_lector(lector1, "Python", 4)
student2.rate_lector(lector1, "Python", 5)

lector2 = Lecturer("Сергей", "Бондарев")
lector2.courses_attached = ["Python"]
student1.rate_lector(lector2, "Python", 9)
student1.rate_lector(lector2, "Python", 10)
student2.rate_lector(lector2, "Python", 5)
student2.rate_lector(lector2, "Python", 6)

reviewer1 = Reviewer("Алексей", "Смирнов")
reviewer1.courses_attached = ["Python"]
reviewer1.rate_student_hw(student1, "Python", 9)

print(student1)
print(student2)
print(lector1)
print(lector2)
print(reviewer1)


print(student1 >= student2)
print(student1 <= student2)
print(student1 == student2)


def student_avg_rate(students, course):
    avg_grade = []
    for student in students:
        if course in student.grades and student.grades[course]:
            avg_student_grade = sum(student.grades[course]) / len(student.grades[course])
            avg_grade.append(avg_student_grade)
    if avg_grade:
        return f'Средняя оценка студента по курсу {course} равна {sum(avg_grade) / len(avg_grade):.2f}\n'
    else:
        return f'Оценок по курсу {course} пока нет.\n'

def lector_avg_rate(lectors, course):
    avg_grade = []
    for lector in lectors:
        if course in lector.grades and lector.grades[course]:
            avg_lector_grade = sum(lector.grades[course]) / len(lector.grades[course])
            avg_grade.append(avg_lector_grade)
    if avg_grade:
        return f'Средняя оценка преподавателя по курсу {course} равна {sum(avg_grade) / len(avg_grade):.2f}\n'
    else:
        return f'Оценок по курсу {course} пока нет.\n'

students = [student1, student2]
print(student_avg_rate(students, "Python"))

lectors = [lector1, lector2]
print(lector_avg_rate(lectors, "Python"))
