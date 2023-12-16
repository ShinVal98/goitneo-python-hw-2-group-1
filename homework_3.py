from collections import UserDict, defaultdict
from datetime import datetime, timedelta

def get_birthdays_per_week(users):
    birthdays_by_day = defaultdict(list)
    today = datetime.today().date()
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    current_weekday = today.weekday()
    start_of_week = (today - timedelta(days=current_weekday))
 
    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=birthday_this_year.year + 1)
        
        delta_days = (birthday_this_year - today).days
        
        if 0 <= delta_days < 7:
            day_of_week = (today.weekday() + delta_days) % 7
            
            if start_of_week <= birthday_this_year <= start_of_week + timedelta(days=6):
                birthdays_by_day[weekdays[day_of_week]].append(name)
    
    result = dict(birthdays_by_day)

    sorted_result = {day: result[day] for day in sorted(result, key=lambda x: weekdays.index(x))}
    return sorted_result

class Birthday:
    def __init__(self, date=None):
        self.date = date if date else None

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not self.value.strip():
            raise ValueError("Name cannot be empty")

    def __str__(self):
        return str(self.value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not self.value.isdigit() or len(self.value) != 10:
            raise ValueError("Phone number must contain 10 digits")

    def __str__(self):
        return str(self.value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        for index, phone in enumerate(self.phones):
            if str(phone) == old_phone:
                self.phones[index] = Phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return phone
        return None

    def add_birthday(self, date):
        if self.birthday:
            raise ValueError("Birthday already exists for this contact.")
        self.birthday = Birthday(date)

    def __str__(self):
        phone_values = '; '.join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name}, phones: {phone_values}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

book = AddressBook()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            error_messages = {
                KeyError: "Contact not found.",
                ValueError: "Give me name and phone please.",
                IndexError: "Invalid index."
            }
            return error_messages.get(type(e), 'An error occurred. Please try again.')
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    book[name] = phone
    return "Contact added."

@input_error
def change_contact(name, new_phone_number):
    if name in book:
        book[name] = new_phone_number
        print("Contact updated.")
    else:
        raise KeyError("Contact not found.")

@input_error
def show_phone(name):
    if name in book:
        print(f"Phone Number for {name}: {book[name]}")
    else:
        raise KeyError("Contact not found.")

@input_error
def add_birthday(name, birthday_str):
    birthday_date = datetime.strptime(birthday_str, '%d.%m.%Y').date()
    contact = book.find(name)
    if contact:
        contact.add_birthday(birthday_date)
        return f"Birthday added for {name}."
    else:
        raise KeyError("Contact not found.")

@input_error
def show_birthday(name):
    contact = book.find(name)
    if contact and contact.birthday:
        return f"{name}'s birthday: {contact.birthday.date.strftime('%d.%m.%Y')}"
    elif contact and not contact.birthday:
        return f"{name} has no birthday specified."
    else:
        raise KeyError("Contact not found.")
    
@input_error
def birthdays():
    upcoming_birthdays = book.get_birthdays_per_week()
    if upcoming_birthdays:
        return f"Upcoming birthdays:\n{upcoming_birthdays}"
    else:
        return "No upcoming birthdays this week."

def main():
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        
        if command in ['hello', 'hi']:
            print("How can I help you?")

        elif command == 'add':
            print(add_contact(args, book))

        elif command == 'change':
            name = input("Enter the contact's name: ")
            new_phone_number = input("Enter the new phone number: ")
            change_contact(name, new_phone_number)

        elif command == 'phone':
            name = input("Enter the contact's name: ")
            show_phone(name)

        elif command == 'add-birthday':
            name = args[0]
            birthday = args[1]
            print(add_birthday(name, birthday))

        elif command == 'show-birthday':
            name = args[0]
            print(show_birthday(name))

        elif command == 'birthdays':
            print(birthdays())

        elif command == 'all':
            print("All Contacts:")
            for name, phone_number in book.items():
                print(f"Name: {name}, Phone Number: {phone_number}")

        elif command in ['exit', 'close']:
            print("Goodbye!")
            break

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()