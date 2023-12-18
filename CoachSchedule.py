from pyllist import sllist
import json
import csv
  
class WeeklySchedule:
    def __init__(self, filename):
        self.__days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.__time = ["8:00-9:00","9:00-10:00","10:00-11:00","11:00-12:00","12:00-13:00","13:00-14:00","15:00-16:00","16:00-17:00"]
        name = "nera"
        self.__weekschedule = sllist()
        startdate = input("Enter date (e.g. 2023-11-03): ")
        for day in self.__days:
            self.__dayschedule = sllist()
            for timeslot in self.__time:
                workout = {
                    'Data': startdate,
                    'Laikas': timeslot,
                    'Kliento Vardas': name,
                    'Kliento Pavarde': name,
                    'Pratimai': name
                }
                self.__dayschedule.append(workout)
            self.__weekschedule.append(self.__dayschedule)
            
            startdate = self.increasedate(startdate)
        filename += ".json"
        with open(filename, 'r') as file:
            scheduledata = json.load(file)
            for dayindex, dayschedule in enumerate(scheduledata["schedule"]):
                for timeslot in self.__time:
                    workout = next((workout for workout in dayschedule if workout["Laikas"] == timeslot), None)
                    if workout is not None:
                        self.__weekschedule.nodeat(dayindex).value.nodeat(self.__time.index(timeslot)).value['Kliento Vardas'] = workout["Kliento Vardas"]
                        self.__weekschedule.nodeat(dayindex).value.nodeat(self.__time.index(timeslot)).value['Kliento Pavarde'] = workout["Kliento Pavarde"]
                        self.__weekschedule.nodeat(dayindex).value.nodeat(self.__time.index(timeslot)).value['Pratimai'] = workout["Pratimai"]
                        
    def increasedate(self, currentdate):
        year, month, day = map(int, currentdate.split("-"))
        day += 1
        if day > 31:
            day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1
        return f"{year:04d}-{month:02d}-{day:02d}"
    
    def removeworkout(self):
        dayindex = int(input("Enter the day index (1-7): ")) - 1
        timeslot_to_remove = input("Enter the time slot to remove (e.g. 17:00-18:00): ")

        if 0 <= dayindex < len(self.__weekschedule):
            dayschedule = self.__weekschedule.nodeat(dayindex).value
            timeindex = None

            for i, time in enumerate(self.__time):
                if timeslot_to_remove == time:
                    timeindex = i
                    break

            if timeindex is not None:
                removedworkout = dayschedule.nodeat(timeindex)
                dayschedule.remove(removedworkout)
                print("Workout removed successfully.")
            else:
                print("Workout not found for the specified time slot.")
        else:
            print("Invalid day index.")
            
    def displayschedule(self):
        for day, self.__dayschedule in zip(self.__days, self.__weekschedule):
            print(f"{day} Schedule:")
            for workout in self.__dayschedule:
                print(f"Data: {workout['Data']}")
                print(f"Laikas: {workout['Laikas']}")
                print(f"Kliento Vardas: {workout['Kliento Vardas']}")
                print(f"Kliento Pavarde: {workout['Kliento Pavarde']}")
                print(f"Pratimai: {workout['Pratimai']}")
                print()
    
    def editschedule(self):
        dayindex = int(input("Enter the day index (1-7): ")) - 1
        timeslots = input("Enter the time slot index (e.g. 17:00-18:00): ")
        for i, time in enumerate(self.__time):
            if timeslots == time:
                timeindex = i
                break
        if 0 <= dayindex < len(self.__weekschedule) and 0 <= timeindex < len(self.__time):
            dayschedule = self.__weekschedule.nodeat(dayindex).value
            timeslot = self.__time[timeindex]
            
            newname = input("Enter the new client name: ")
            newsurname = input("Enter the new client surname: ")
            exercises = input("Enter what exercises should Client do: ")
            
            dayschedule.nodeat(timeindex).value['Kliento Vardas'] = newname
            dayschedule.nodeat(timeindex).value['Kliento Pavarde'] = newsurname
            dayschedule.nodeat(timeindex).value['Pratimai'] = exercises
            
            print("Task edited successfully.")
        else:
            print("Invalid data")
    
    def addworkout(self):
        dayindex = int(input("Enter the day index (1-7): ")) - 1

        if 0 <= dayindex < len(self.__weekschedule):
            dayschedule = self.__weekschedule.nodeat(dayindex).value
            
            newtimeslot = input("Enter the new time slot (e.g. 17:00-18:00): ")
            newname = input("Enter the new client name: ")
            newsurname = input("Enter the new client surname: ")
            newexercises = input("Enter what exercises should Client do: ")

            workout = {
                'Data': dayschedule[0]['Data'],
                'Laikas': newtimeslot,
                'Kliento Vardas': newname,
                'Kliento Pavarde': newsurname,
                'Pratimai': newexercises
            }
            dayschedule.append(workout)

            print("Workout added successfully.")
        else:
            print("Invalid day index.")
    
    def findClientsExercises(self):
        clientname = input("Enter the client's name: ")
        clientsurname = input("Enter the client's surname: ")

        totalreps = 0
        exercisereps = {}
        foundworkouts = []

        for day, self.__dayschedule in zip(self.__days, self.__weekschedule):
            for workout in self.__dayschedule:
                if workout['Kliento Vardas'] == clientname and workout['Kliento Pavarde'] == clientsurname:
                    print(f"{day} - {workout['Laikas']}: {workout['Pratimai']}")
                    foundworkouts.append([day, workout['Laikas'], workout['Pratimai']])
                    exercises = workout['Pratimai']
                    parts = exercises.split(',')
                    for part in parts:
                        subparts = part.split()
                        repetitions = 0
                        exercisename = ""
                        for subpart in subparts:
                            if subpart.isdigit():
                                repetitions = int(subpart)
                            else:
                                exercisename += subpart + " "
                        exercisename = exercisename.strip()
                        if exercisename in exercisereps:
                            exercisereps[exercisename] += repetitions
                        else:
                            exercisereps[exercisename] = repetitions

        if not exercisereps:
            print(f"No workouts found for {clientname} {clientsurname}.")
        else:
            filenameCSV = f"{clientname}_{clientsurname}_workouts.csv"
            with open(filenameCSV, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Day", "Time", "Exercises"])
                writer.writerows(foundworkouts)
                
            filenameTXT = f"{clientname}_{clientsurname}_ataskaita.txt"
            with open(filenameTXT, mode='w') as file:
                file.write(f"Workouts for {clientname} {clientsurname}:\n")
                file.write("Exercises\tRepetitions\n")
                for exercise, repetitions in exercisereps.items():
                    file.write(f"{exercise}\t{repetitions}\n")
                    totalreps += repetitions
                file.write(f"Total Repetitions: {totalreps}")

    def saveschedule(self, filename):
        filename += ".json"
        scheduledata = {
            "schedule": []
        }
        for dayschedule in self.__weekschedule:
            scheduledata["schedule"].append(list(dayschedule))

        with open(filename, 'w') as file:
            json.dump(scheduledata, file, indent=4)
                         
if __name__ == "__main__":
    filename = input("Enter file name: ")
    schedule = WeeklySchedule(filename)
    while True:
        print("\nOptions:")
        print("1. Add a workout")
        print("2. Edit workout")
        print("3. Display the weekly schedule")
        print("4. Find Client's exercises")
        print("5. Remove a workout")
        print("6. Exit")
        
        choice = int(input("Enter your choice:"))
        if choice == 1:
            schedule.addworkout()
        if choice == 2:
            schedule.editschedule()
        if choice == 3:
            schedule.displayschedule()
        if choice == 4:
            schedule.findClientsExercises()
        if choice == 5:
            schedule.removeworkout()
        if choice == 6:
            schedule.saveschedule(filename)
            break
        
        