# v_5.3 Full fuctional works

from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """
    Клас для зберігання імені контакту. Обов'язкове поле.
    """
    def __init__(self, name):
        self.name = name


class Phone(Field):
    """
    Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    """
    def __init__(self, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError("Phone number must be 10 digits.")
        self.number = number


class Record:
    """
    Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    """
    def __init__(self, name, *phones):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones]

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.number != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.number == old_phone:
                phone.number = new_phone
                return
        raise ValueError(f"Phone '{old_phone}' not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.number == phone:
                return p
        return None


class AddressBook(UserDict):
    """
    Клас для зберігання та управління записами.
    """
    def add_record(self, record):
        self.data[record.name.name] = record

    def delete_record(self, name):
        del self.data[name]

    def find_record(self, name):
        return self.data.get(name, None)


def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            print(f"Input error: {e}")
    return wrapper


@input_error
def add_contact(address_book, name, *numbers):
    """
    Додає контакт у телефонну книгу.
    """
    record = Record(name, *numbers)
    address_book.add_record(record)
    print(f"Contact '{name}' with number(s) '{', '.join(numbers)}' added successfully.")


@input_error
def change_contact(address_book, name, old_number, new_number):
    """
    Змінює номер телефону для вказаного контакту.
    """
    record = address_book.find_record(name)
    if record:
        record.edit_phone(old_number, new_number)
        print(f"Number for contact '{name}' changed from '{old_number}' to '{new_number}'.")
    else:
        print(f"Contact '{name}' not found.")


@input_error
def show_phone(address_book, name):
    """
    Виводить номер телефону для вказаного контакту.
    """
    record = address_book.find_record(name)
    if record:
        print(f"The phone number(s) for '{name}' is/are {', '.join([p.number for p in record.phones])}.")
    else:
        print(f"No phone number found for contact '{name}'.")


@input_error
def show_all_contacts(address_book):
    """
    Виводить всі контакти телефонної книги.
    """
    print("All contacts in the address book:")
    for name, record in address_book.items():
        print(f"{name}: {', '.join([p.number for p in record.phones])}")


@input_error
def add_phone_to_contact(address_book, name, phone):
    """
    Додає номер телефону до існуючого контакту.
    """
    record = address_book.find_record(name)
    if record:
        record.add_phone(phone)
        print(f"Phone '{phone}' added to contact '{name}'.")
    else:
        print(f"Contact '{name}' not found.")


@input_error
def remove_phone_from_contact(address_book, name, phone):
    """
    Видаляє номер телефону з існуючого контакту.
    """
    record = address_book.find_record(name)
    if record:
        record.remove_phone(phone)
        print(f"Phone '{phone}' removed from contact '{name}'.")
    else:
        print(f"Contact '{name}' not found.")


@input_error
def edit_phone_in_contact(address_book, name, old_phone, new_phone):
    """
    Редагує номер телефону в існуючому контакті.
    """
    record = address_book.find_record(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        print(f"Phone number for contact '{name}' changed from '{old_phone}' to '{new_phone}'.")
    else:
        print(f"Contact '{name}' not found.")


@input_error
def find_phone_in_contact(address_book, name, phone):
    """
    Знаходить номер телефону в існуючому контакті.
    """
    record = address_book.find_record(name)
    if record:
        phone_record = record.find_phone(phone)
        if phone_record:
            print(f"Phone '{phone}' found in contact '{name}'.")
        else:
            print(f"Phone '{phone}' not found in contact '{name}'.")
    else:
        print(f"Contact '{name}' not found.")


def parse_input(command):
    """
    Розбирає введену користувачем команду.
    Повертає кортеж (команда, аргументи).
    """
    parts = command.split()
    if parts:
        return parts[0].lower(), parts[1:]
    return "", []


def main():
    print("Welcome to the assistant bot!")
    address_book = AddressBook()
    while True:
        command = input("Enter a command: ").strip()

        if command.lower() in ["close", "exit"]:
            print("Good bye!")
            break

        cmd, args = parse_input(command)

        match cmd:
            case "hello":
                print("How can I help you?")

            case "add":
                if len(args) >= 2:
                    add_contact(address_book, args[0], *args[1:])
                else:
                    print("Invalid number of arguments for 'add' command.")

            case "change":
                if len(args) == 3:
                    change_contact(address_book, args[0], args[1], args[2])
                else:
                    print("Invalid number of arguments for 'change' command.")

            case "show":
                if len(args) == 1:
                    show_phone(address_book, args[0])
                elif len(args) == 0:
                    show_all_contacts(address_book)
                else:
                    print("Invalid number of arguments for 'show' command.")

            case "add_phone":
                if len(args) == 2:
                    add_phone_to_contact(address_book, args[0], args[1])
                else:
                    print("Invalid number of arguments for 'add_phone' command.")

            case "remove_phone":
                if len(args) == 2:
                    remove_phone_from_contact(address_book, args[0], args[1])
                else:
                    print("Invalid number of arguments for 'remove_phone' command.")

            case "edit_phone":
                if len(args) == 3:
                    edit_phone_in_contact(address_book, args[0], args[1], args[2])
                else:
                    print("Invalid number of arguments for 'edit_phone' command.")

            case "find_phone":
                if len(args) == 2:
                    find_phone_in_contact(address_book, args[0], args[1])
                else:
                    print("Invalid number of arguments for 'find_phone' command.")

            case _:
                print("Invalid command. Type again!")


if __name__ == "__main__":
    main()
