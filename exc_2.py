contacts = {}

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
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(name, new_phone_number):
    if name in contacts:
        contacts[name] = new_phone_number
        print("Contact updated.")
    else:
        raise KeyError("Contact not found.")

@input_error
def show_phone(name):
    if name in contacts:
        print(f"Phone Number for {name}: {contacts[name]}")
    else:
        raise KeyError("Contact not found.")

def main():
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        
        if command in ['hello', 'hi']:
            print("How can I help you?")

        elif command == 'add':
            print(add_contact(args, contacts))

        elif command == 'change':
            name = input("Enter the contact's name: ")
            new_phone_number = input("Enter the new phone number: ")
            change_contact(name, new_phone_number)

        elif command == 'phone':
            name = input("Enter the contact's name: ")
            show_phone(name)

        elif command == 'all':
            print("All Contacts:")
            for name, phone_number in contacts.items():
                print(f"Name: {name}, Phone Number: {phone_number}")

        elif command in ['exit', 'close']:
            print("Goodbye!")
            break

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()