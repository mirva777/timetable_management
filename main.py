from tabulate import tabulate

class TimetableManager:
    def __init__(self, classes, professors, groups, time_slots, rooms, room_capacities=None):
        self.classes = classes
        self.professors = professors
        self.groups = groups
        self.time_slots = time_slots  
        self.rooms = rooms
        # If room capacities are not provided, assign default capacity of 30
        self.room_capacity = room_capacities if room_capacities else {room: 30 for room in rooms}
        self.class_sizes = {cls['name']: cls.get('size', 20) for cls in classes}  # Default size is 20
        self.professor_preferences = {prof: [] for prof in professors}  # Preferences for professors
        self.group_preferences = {group: [] for group in groups}  # Preferences for groups
        self.professor_schedule = {prof: {} for prof in professors}  # Initialize professor schedules
        self.group_schedule = {group: {} for group in groups}  # Initialize group schedules

    def set_professor_preferences(self, professor, preferences):
        """Set preferred time slots for a professor."""
        if professor in self.professor_preferences:
            self.professor_preferences[professor] = preferences

    def set_group_preferences(self, group, preferences):
        """Set preferred time slots for a group."""
        if group in self.group_preferences:
            self.group_preferences[group] = preferences

    def generate_schedule(self):
        for cls in self.classes:
            assigned = False
            preferred_slots = self.get_preferred_slots(cls)
            for time_slot in preferred_slots + self.time_slots:
                for room in self.rooms:
                    if self.is_valid(cls, time_slot, room):
                        self.assign_schedule(cls, time_slot, room)
                        assigned = True
                        break
                if assigned:
                    break
            if not assigned:
                self.provide_feedback(cls)

    def get_preferred_slots(self, cls):
        """Get combined preferences for professor and group."""
        prof_preferences = self.professor_preferences.get(cls['professor'], [])
        group_preferences = self.group_preferences.get(cls['group'], [])
        return list(set(prof_preferences) & set(group_preferences))

    def is_valid(self, cls, time_slot, room):
        prof = cls['professor']
        group = cls['group']
        class_size = self.class_sizes[cls['name']]

        return (
            time_slot not in self.professor_schedule[prof] and
            time_slot not in self.group_schedule[group] and
            class_size <= self.room_capacity[room]
        )

    def assign_schedule(self, cls, time_slot, room):
        prof = cls['professor']
        group = cls['group']
        self.professor_schedule[prof][time_slot] = {'class': cls['name'], 'room': room, 'group': group}
        self.group_schedule[group][time_slot] = {'class': cls['name'], 'room': room, 'professor': prof}

    def provide_feedback(self, cls):
        prof = cls['professor']
        group = cls['group']
        class_size = self.class_sizes[cls['name']]
        issues = []

        if all(time_slot in self.professor_schedule[prof] for time_slot in self.time_slots):
            issues.append(f"No available time slots for professor {prof}.")

        if all(time_slot in self.group_schedule[group] for time_slot in self.time_slots):
            issues.append(f"No available time slots for group {group}.")

        if all(class_size > self.room_capacity[room] for room in self.rooms):
            issues.append(f"No rooms with sufficient capacity for class {cls['name']} (size: {class_size}).")

        if issues:
            print(f"Unable to assign class {cls['name']} for group {group} by professor {prof}. Reasons:")
            for issue in issues:
                print(f"- {issue}")

    def display_schedules(self):
        print("\nProfessor Schedules:")
        for prof, schedule in self.professor_schedule.items():
            print(f"\nSchedule for {prof}:")
            table = [[time_slot, details['class'], details['room'], details['group']] for time_slot, details in schedule.items()]
            print(tabulate(table, headers=["Time Slot", "Class", "Room", "Group"], tablefmt="grid"))

        print("\nGroup Schedules:")
        for group, schedule in self.group_schedule.items():
            print(f"\nSchedule for {group}:")
            table = [[time_slot, details['class'], details['room'], details['professor']] for time_slot, details in schedule.items()]
            print(tabulate(table, headers=["Time Slot", "Class", "Room", "Professor"], tablefmt="grid"))

# Example Usage
rooms = ['Room 101', 'Room 102', 'Room 103']
room_capacities = {'Room 101': 20, 'Room 102': 50, 'Room 103': 40} 
classes = [
    {'name': 'Math', 'professor': 'Prof. A', 'group': 'Group 1', 'size': 25},
    {'name': 'Physics', 'professor': 'Prof. B', 'group': 'Group 2', 'size': 20},
    {'name': 'Chemistry', 'professor': 'Prof. C', 'group': 'Group 3', 'size': 35},
    {'name': 'Chemistry', 'professor': 'Prof. C', 'group': 'Group 3', 'size': 35},
    {'name': 'Chemistry', 'professor': 'Prof. C', 'group': 'Group 3', 'size': 35}
]
professors = ['Prof. A', 'Prof. B', 'Prof. C']
groups = ['Group 1', 'Group 2', 'Group 3']
time_slots = [
    ('Monday', '9:00-10:00'), ('Monday', '10:00-11:00'), ('Monday', '11:00-12:00'),
    ('Tuesday', '9:00-10:00'), ('Tuesday', '10:00-11:00'), ('Tuesday', '11:00-12:00')
]

# Pass custom room capacities
timetable_manager = TimetableManager(classes, professors, groups, time_slots, rooms, room_capacities)

timetable_manager.set_professor_preferences('Prof. A', [('Monday', '9:00-10:00'), ('Tuesday', '10:00-11:00')])
timetable_manager.set_group_preferences('Group 1', [('Monday', '9:00-10:00'), ('Monday', '10:00-11:00')])

timetable_manager.generate_schedule()
timetable_manager.display_schedules()

