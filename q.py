from collections import defaultdict, UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Your phone number is incorrect. Please enter a valid 10-digit phone number.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Please use DD.MM.YYYY format.")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if str(p) == old_phone:
                p.value = new_phone
                break

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_info = '; '.join(str(p) for p in self.phones)
        birthday_info = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_info}{birthday_info}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[str(record.name)] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        birthdays_by_weekday = defaultdict(list)
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days
                birthday_weekday = (today + timedelta(days=delta_days)).strftime("%A")

                if 0 <= delta_days < 7:
                    if birthday_weekday in ["Saturday", "Sunday"]:
                        birthday_weekday = "Monday"

                    birthdays_by_weekday[birthday_weekday].append(record.name.value)

        for day, names in birthdays_by_weekday.items():
            print(f"{day}: {', '.join(names)}")


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name." 
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
def add_contact(args, book):
    name, phone = args
    validate_name(name)
    validate_phone(phone)
    if name not in book:
        book.add_record(Record(name))
    else:
        return "Contact already exists. Use 'change' command to update the phone number."
    book[name].add_phone(phone)
    return "Contact added."


@input_error
def change_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        validate_phone(phone)
        record.edit_phone(record.phones[0].value, phone)
        return "Contact updated."
    else:
        return "Contact not found."


@input_error    
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return record.phones[0]
    else:
        return "Contact not found."


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday
    elif record and not record.birthday:
        return "Birthday not set for this contact."
    else:
        return "Contact not found."


def birthdays(book):
    book.get_birthdays_per_week()


def show_all(book):
    if book:
        contacts_info = "\n".join([str(record) for record in book.data.values()])
        return contacts_info
    else:
        return "No contacts"


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))   
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            birthdays(book)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
from collections import defaultdict, UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Your phone number is incorrect. Please enter a valid 10-digit phone number.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Please use DD.MM.YYYY format.")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if str(p) == old_phone:
                p.value = new_phone
                break

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_info = '; '.join(str(p) for p in self.phones)
        birthday_info = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_info}{birthday_info}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[str(record.name)] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        birthdays_by_weekday = defaultdict(list)
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days
                birthday_weekday = (today + timedelta(days=delta_days)).strftime("%A")

                if 0 <= delta_days < 7:
                    if birthday_weekday in ["Saturday", "Sunday"]:
                        birthday_weekday = "Monday"

                    birthdays_by_weekday[birthday_weekday].append(record.name.value)

        for day, names in birthdays_by_weekday.items():
            print(f"{day}: {', '.join(names)}")


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name." 
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
def add_contact(args, book):
    name, phone = args
    validate_name(name)
    validate_phone(phone)
    if name not in book:
        book.add_record(Record(name))
    else:
        return "Contact already exists. Use 'change' command to update the phone number."
    book[name].add_phone(phone)
    return "Contact added."


@input_error
def change_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        validate_phone(phone)
        record.edit_phone(record.phones[0].value, phone)
        return "Contact updated."
    else:
        return "Contact not found."


@input_error    
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return record.phones[0]
    else:
        return "Contact not found."


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday
    elif record and not record.birthday:
        return "Birthday not set for this contact."
    else:
        return "Contact not found."


def birthdays(book):
    book.get_birthdays_per_week()


def show_all(book):
    if book:
        contacts_info = "\n".join([str(record) for record in book.data.values()])
        return contacts_info
    else:
        return "No contacts"


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))   
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            birthdays(book)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
