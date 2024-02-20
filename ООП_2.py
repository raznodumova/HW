class Student:
  def __init__(self, name, surname, gender):
      self.name = name
      self.surname = surname
      self.gender = gender
      self.finished_courses = []
      self.courses_in_progress = []
      self.grades = {}

  def __str__(self):
      res = f'Имя: {self.name}\n' \
            f'Фамилия: {self.surname}\n' \
            f'Средняя оценка за домашние задания: {self._avg_rate()}\n' \
            f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n' \
            f'Завершенные курсы: {", ".join(self.finished_courses)}\n'
      return res

  def __lt__(self, other):
      if not isinstance(other, Student):
          print("Разные категории людей не сравниваем.")
          return
      return self._avg_rate() < other._avg_rate()

  def _avg_rate(self): #среднее
      total_subject_grades = 0
      count_subject_grades = 0
      for subject, value in self.grades.items():
          total_subject_grades += sum(value)
          count_subject_grades += len(value)
      return total_subject_grades / count_subject_grades

  def avg_rate_course(self, course): #для подсчета общей средней
      sum_course = 0
      len_course = 0
      for crs in self.grades.keys():
          if crs == course:
              sum_course += sum(self.grades[course])
              len_course += len(self.grades[course])
      result = round(sum_course / len_course, 2)
      return result


  def rate_lect(self, lecturer, course, grade): #оценка лекторам
      if isinstance(lecturer, Lecturer):
          if course in lecturer.grades:
              lecturer.grades[course] += [grade]
          else:
              lecturer.grades[course] = [grade]
      else:
          return 'Ошибка'
class Mentor:
  def __init__(self, name, surname):
      self.name = name
      self.surname = surname
      self.courses_attached = []

class Lecturer(Mentor):
  def __init__(self, name, surname):
      super().__init__(name, surname)
      self.grades = {}

  def __str__(self):
      res = f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self._average()}\n'
      return res

  def __lt__(self, other):
      if not isinstance(other, Lecturer):
          print('Ошибочка')
          return
      return self._average() < other._average()

  def _average(self): #среднее по лекциям
      total_subject_grades = 0
      count_subject_grades = 0
      for subject, value in self.grades.items():
          total_subject_grades += sum(value)
          count_subject_grades += len(value)
      return total_subject_grades / count_subject_grades

  def avg_rate_course(self, course): #для подсчета средней суммарной
      sum_crs = 0
      len_crs = 0
      for crs in self.grades.keys():
          if crs == course:
              sum_crs += sum(self.grades[course])
              len_crs += len(self.grades[course])
      result = round(sum_crs / len_crs, 2)
      return result

class Reviewer(Mentor):
  def __init__(self, name, surname):
      super().__init__(name, surname)

  def __str__(self):
      result = f'Имя: {self.name}\nФамилия: {self.surname}\n'
      return result

  def rate_hw(self, student, course, grade):
      if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
          if course in student.grades:
              student.grades[course] += [grade]
          else:
              student.grades[course] = [grade]
      else:
          return 'Ошибка'
# ____________________________экземпляры________________________________________

student_1 = Student('Иван', 'Иванов', 'male')
student_2 = Student('Ирина', 'Иринова', 'female')

student_1.courses_in_progress += ['Python']
student_1.finished_courses += ['JavaScript']
student_2.courses_in_progress += ['Python']
student_2.finished_courses += ['C+']


reviewer_1 = Reviewer('Степан', 'Степанов')
reviewer_2 = Reviewer('Светлана', 'Светланова')
reviewer_1.courses_attached += ['Python', 'JavaScript']
reviewer_2.courses_attached += ['Python']

lecturer_1 = Lecturer('Евгений', 'Евгеньев')
reviewer_1.rate_hw(student_1, 'Python', 9)
reviewer_1.rate_hw(student_2, 'Python', 10)
lecturer_2 = Lecturer('Елена', 'Еленова')
reviewer_2.rate_hw(student_1, 'Python', 8)
reviewer_2.rate_hw(student_2, 'Python', 7)

student_1.rate_lect(lecturer_1, 'Python', 9)
student_1.rate_lect(lecturer_2, 'Python', 9)
student_2.rate_lect(lecturer_1, 'Python', 8)
student_2.rate_lect(lecturer_2, 'Python', 5)

#_________________________________вывод___________________________________________
import gc

print("Проверяющие")
for obj in gc.get_objects():
  if isinstance(obj, Reviewer):
      print(obj)

print("Лекторы")
for obj in gc.get_objects():
  if isinstance(obj, Lecturer):
      print(obj)

print("Студенты")
for obj in gc.get_objects():
  if isinstance(obj, Student):
      print(obj)

#___________________________сравнение студентов_____________________________________

print('Сравнение студентов:')
print('student_1 < student_2:', student_1 < student_2)
print('Сравнение лекторов:')
print('lecturer_1 < lecturer_2:', lecturer_1 < lecturer_2)

# ____________________________подсчет средней оценки______________________________

student_list = [student_1, student_2]
lecturer_list = [lecturer_1, lecturer_2]

def avg_rate_course_std(course, student_list):
  sum_ = 0
  qty_ = 0
  for std in student_list:
      for crs in std.grades:
          std_sum_rate = std.avg_rate_course(course)
          sum_ += std_sum_rate
          qty_ += 1
  res = round(sum_ / qty_, 2)
  return res

def avg_rate_course_lct(course, lecturer_list):
  sum_ = 0
  qty_ = 0
  for lct in lecturer_list:
      for crs in lct.grades:
          lct_sum_rate = lct.avg_rate_course(course)
          sum_ += lct_sum_rate
          qty_ += 1
  res = round(sum_ / qty_, 2)
  return res

print('Суммарная средняя оценка за ДЗ')
print(avg_rate_course_std('Python', student_list))

print('Суммарная средняя оценка за лекции')
print(avg_rate_course_lct('Python', lecturer_list))