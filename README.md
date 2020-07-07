Работа с PostgreSQL

Реализованы следующие функции для работы с таблицами:
def create_db(): # создает таблицы

def get_students(course_id): # возвращает студентов определенного курса

def add_students(course_id, students): # создает студентов и 
                                       # записывает их на курс

def add_student(student): # просто создает студента.

def get_student(student_id):  # получение студента по id
    
Объекты "Студент" передаются в функцию в виде словаря. 


