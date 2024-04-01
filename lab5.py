import random
import matplotlib.pyplot as plt
import json

class Schedule: 
   def __init__(self, classes, teachers, subjects, rooms, days=5, lessons=5):
      self.classes = classes
      self.teachers = teachers
      self.subjects = subjects
      self.rooms = rooms
      self.days = days
      self.lessons = lessons
      self.schedule = self.generate_random_schedule()
      
   def generate_random_schedule(self):
      return [[[(random.choice(self.subjects), random.choice(self.teachers), random.choice(self.rooms))
                for _ in range(self.lessons)] for _ in range(self.days)] for _ in range(self.classes)]
    

class GeneticAlgorithm:
   def __init__(self, population_size, mutation_rate, crossover_rate, generations, elite_size):
      self.population_size = population_size
      self.mutation_rate = mutation_rate
      self.crossover_rate = crossover_rate
      self.generations = generations
      self.elite_size = elite_size
      self.fitness_over_time = []
        
   def generate_population(self, start):
      return [Schedule(start.classes, start.teachers, start.subjects, start.rooms, start.days, start.lessons) for _ in range(self.population_size)]
   
   def fitness(self, schedule):
      score = 0
      for class_schedule in schedule.schedule:
         for day_schedule in class_schedule:
            teachers = [lesson[1] for lesson in day_schedule]
            subjects = [lesson[0] for lesson in day_schedule]
            rooms = [lesson[2] for lesson in day_schedule]

            if 'Physical Education' in subjects and 'Gym' not in rooms:
               score += 1
            if 'Choreography' in subjects and 'Dance room' not in rooms:
               score += 1
            if 'Music' in subjects and 'Music room' not in rooms:
               score += 1

            school_subjects = ['Math', 'English', 'History', 'Geography']
            for subject in school_subjects:
               if subject in subjects and not any(
                     classroom in rooms for classroom in ['Room 1', 'Room 2', 'Room 3']):
                  score += 1

            if len(teachers) !=len(set(teachers)):
               score += 1

            if len(subjects) !=len(set(subjects)):
               score += 1

            if len(rooms) !=len(set(rooms)):
               score += 1

      for class_schedule in schedule.schedule:
         school_teachers = [lesson[1] for day_schedule in class_schedule for lesson in day_schedule]
         common_teacher = max(set(school_teachers), key=school_teachers.count)
         if school_teachers.count(common_teacher) < len(school_teachers) // 2:
            score += 1
      
      return score
   
   
   
   def mutate(self, schedule):
      if random.random() < self.mutation_rate:
         day = random.randint(0, schedule.days - 1)
         lesson = random.randint(0, schedule.lessons - 1)
         class_ = random.randint(0, schedule.classes - 1)
         subject = random.choice(schedule.subjects)
         if subject == 'Physical Education':
            room = 'Gym'
         elif subject == 'Choreography':
            room = 'Dance room'
         elif subject == 'Music':
            room = 'Music room'
         elif subject in ['Math', 'English', 'History', 'Geography']:
            room = random.choice(['Room 1', 'Room 2', 'Room 3'])
         else:
            room = random.choice(schedule.rooms)
         teacher = random.choice(schedule.teachers)
         schedule.schedule[class_][day][lesson] = (subject, teacher, room)
      return schedule
      
   
   def crossover(self, parent1, parent2):
      if random.random() < self.crossover_rate:
         crossover_point = random.randint(0, parent1.classes - 1)
         child1 = parent1.schedule[:crossover_point] + parent2.schedule[crossover_point:]
         child2 = parent2.schedule[:crossover_point] + parent1.schedule[crossover_point:]
         parent1.schedule, parent2.schedule = child1, child2
      return parent1, parent2

   def post_process(self, schedule):
      for class_schedule in schedule.schedule:
         for day_schedule in class_schedule:
            subjects = [lesson[0] for lesson in day_schedule]
            rooms = [lesson[2] for lesson in day_schedule]
            for subject, room in zip(subjects, rooms):
               if subject == 'Physical Education' and room != 'Gym':
                  room = 'Gym'
               elif subject == 'Choreography' and room != 'Dance room':
                  room = 'Dance room'
               elif subject == 'Music' and room != 'Music room':
                  room = 'Music room'
               elif subject in ['Math', 'English', 'History', 'Geography'] and room not in ['Room 1', 'Room 2', 'Room 3']:
                  room = random.choice(['Room 1', 'Room 2', 'Room 3'])
      return schedule

   
   def optimize(self, schedule):
      population = sorted(self.generate_population(schedule), key=self.fitness)
      for _ in range(self.generations):
         new_population = population[:self.elite_size]
         while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(population[:50], 2)
            child1, child2 = self.crossover(parent1, parent2)
            new_population += [self.post_process(self.mutate(child1)), self.post_process(self.mutate(child2))]   
         population = sorted(new_population, key=self.fitness)
         self.fitness_over_time.append(self.fitness(population[0]))   
      return population[0]
   
   def plot_fitness_over_time(self):
      plt.plot(self.fitness_over_time)
      plt.title('Fitness over time')
      plt.xlabel('Generation')
      plt.ylabel('Fitness')
      plt.show()

def schedule_print(schedule):
   days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
   classes = ['Class 1', 'Class 2', 'Class 3']

   for idx, class_schedule in enumerate(schedule):
      print(f'===== {classes[idx]} =====')
      for day_idx, day_schedule in enumerate(class_schedule):
         print(f'----- {days[day_idx]} -----')
         for period in day_schedule:
            print(f'Subject: {period[0]}, teacher: {period[1]}, classroom: {period[2]}')
      print('\n')


def save_data(data, file_name):
   with open(file_name, 'w') as file:
      json.dump(data, file)

def load_data(file_name):
   with open(file_name, 'r') as file:
      return json.load(file)

classes = 3
teachers = ['Teacher 1', 'Teacher 2', 'Teacher 3', 'Teacher 4']
subjects = ['Math', 'English', 'History', 'Geography', 'Physical Education', 'Choreography', 'Music']
rooms = ['Room 1', 'Room 2', 'Room 3', 'Gym', 'Dance room', 'Music room']
days = 5
lessons = 5
#days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

schedule = Schedule(classes, teachers, subjects, rooms, days, lessons)
ga = GeneticAlgorithm(100, 0.01, 0.7, 300, 20)
optimize_schedule = ga.optimize(schedule)
ga.plot_fitness_over_time()
schedule_print(optimize_schedule.schedule)

data = {
   'classes': classes,
   'teachers': teachers,
   'subjects': subjects,
   'rooms': rooms,
   'days': days,
   'lessons': lessons
}
save_data(data, "C:\\Users\\user\\Desktop\\AI\\schedule.json")

loaded_data = load_data("C:\\Users\\user\\Desktop\\AI\\schedule.json")
classes = loaded_data['classes']
teachers= loaded_data['teachers']
subjects = loaded_data['subjects']
rooms = loaded_data['rooms']
days = loaded_data['days']
lessons = loaded_data['lessons']
