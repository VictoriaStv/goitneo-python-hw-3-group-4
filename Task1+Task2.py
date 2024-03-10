def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name." 
        except NameError as e:
            return str(e)
        except PhoneError as e:
            return str(e)
    return inner


class PhoneError(Exception):
    pass


class NameError(Exception):
    pass


def validate_phone(phone):
    if not phone.isdigit() or len(phone) != 10:
        raise PhoneError("Your phone number is incorrect. Please enter a valid 10-digit phone number.")


def validate_name(name):
    if not name.isalpha():
        raise NameError("Invalid name. Please enter a name containing only letters.")


@input_error
def add_contact(args, contacts):
    name, phone = args
    validate_name(name)
    validate_phone(phone)
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        validate_phone(phone)
        contacts[name] = phone
        return "Contact updated." 
    else:
        return "Contact not found."


@input_error    
def show_phone(args, contacts):
    name = args[0]
    if name in contacts:
         return contacts[name]
    else:
        return "Contact not found."


def show_all(contacts):
     if contacts:
        contacts_info = "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])
        return contacts_info
     else:
        return "No contacts"


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))   
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))           
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()