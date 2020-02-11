import psycopg2

con = psycopg2.connect("dbname=test user=test_owner password=1")
cur = con.cursor()

print("Database opened successfully")

#функция, которая создает таблицы
def create_db(name, columns):
    cur.execute("CREATE TABLE %s (%s);" %(name, columns))
    con.commit()
    print("Table created successfully")

#создаем таблицы students, course, student_course
name = 'students'
columns = 'id serial PRIMARY KEY, name varchar(100), gpa numeric(10, 2), birth timestamp with time zone'
create_db(name, columns)

name = 'course'
columns = 'id serial PRIMARY KEY, name varchar(100)'
create_db(name, columns)

name = 'student_course'
columns = 'id serial PRIMARY KEY, student_id integer REFERENCES students(id), course_id integer REFERENCES course(id)'
create_db(name, columns)


#функция, которая добавляет студента
def add_student(student):
    cur.execute("insert into students (name, gpa, birth) values (%s, %s, %s) RETURNING id", (student['name'], student['gpa'], student['birth']))
    res = cur.fetchone()
    last_id = res[0]
    con.commit()
    print("Student added successfully")
    return last_id

#добавляем студентов
student = {
    'name': 'Dasha',
    'gpa': 5.6,
    'birth': '1980-01-01'
}

add_student(student)

student_1 = {
    'name': 'Dima',
    'gpa': 7.6,
    'birth': '1985-01-01'
}

add_student(student_1)

student_2 = {
    'name': 'Petr',
    'gpa': 5.6,
    'birth': '1981-01-01'
}

add_student(student_2)


#добавляем курсы в таблицу course
cur.execute("insert into course (name) values (%s)", ("Python",))
cur.execute("insert into course (name) values (%s)", ("JS",))
con.commit()


#добавляем связи студент-курс в таблицу student_course
cur.execute("insert into student_course (student_id, course_id) values (%s, %s)", (1, 2))
cur.execute("insert into student_course (student_id, course_id) values (%s, %s)", (2, 1))
con.commit()


#проверяем добавленных студентов и курсы
cur.execute("SELECT * FROM students")
rows = cur.fetchall()

for row in rows:
   print row

cur.execute("SELECT * FROM course")
rows_1 = cur.fetchall()

for row in rows_1:
    print row

#функция, которая возвращает студента по id
def get_student(student_id):
    cur.execute("SELECT name, gpa, birth FROM students WHERE id = %s" %(student_id))
    result = cur.fetchall()
    print(result)

get_student(2)

#функция, которая возвращает студентов курса по id курса
def get_students(course_id):
    cur.execute("SELECT students.id, students.name, course.name FROM student_course join students on students.id = student_course.student_id join course on course.id = student_course.course_id WHERE course.id = %s" %(course_id))
    print(cur.fetchall())

get_students(2)

#функция, которая создает студентов и записывает их на курс
def add_students(course_id, students):
    for student in students:
        last_id = add_student(student)
        cur.execute("insert into student_course (student_id, course_id) values (%s, %s)", (last_id, course_id))
        con.commit()

students_1 = [
{
    'name': 'Pasha',
    'gpa': 6.6,
    'birth': '1981-01-01'
},
{
    'name': 'Masha',
    'gpa': 9.6,
    'birth': '1984-01-01'
}
]
#добавляем студентов, записываем на курс проверяем
add_students(2, students_1)
get_students(2)