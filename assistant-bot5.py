# v0.5 
# додати можливість зберігання одного й того ж контакта з різними номерами. Зараз відбувається перезапис по імені контакту
# додати можливість видалення контакту як за ім'ям так і за номером

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


class AddressBook(UserDict):
    """
    Клас для зберігання та управління записами.
    """
    def add_record(self, record):
        self.data[record.name.name] = record.phones

    def delete_record(self, name):
        del self.data[name]

    def find_record(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def add_phone(self, name, phone):
        if name in self.data:
            self.data[name].append(Phone(phone))
        else:
            raise KeyError(f"Contact '{name}' not found in the address book.")

    def delete_phone(self, name, phone):
        if name in self.data:
            self.data[name] = [p for p in self.data[name] if p.number != phone]
        else:
            raise KeyError(f"Contact '{name}' not found in the address book.")

    def change_phone(self, name, old_phone, new_phone):
        if name in self.data:
            for p in self.data[name]:
                if p.number == old_phone:
                    p.number = new_phone
                    break
            else:
                raise ValueError(f"Phone '{old_phone}' not found for contact '{name}'.")
        else:
            raise KeyError(f"Contact '{name}' not found in the address book.")


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
    address_book.change_phone(name, old_number, new_number)
    print(f"Number for contact '{name}' changed from '{old_number}' to '{new_number}'.")


@input_error
def show_phone(address_book, name):
    """
    Виводить номер телефону для вказаного контакту.
    """
    numbers = address_book.find_record(name)
    if numbers:
        print(f"The phone number(s) for '{name}' is/are {', '.join([p.number for p in numbers])}.")
    else:
        print(f"No phone number found for contact '{name}'.")


@input_error
def show_all_contacts(address_book):
    """
    Виводить всі контакти телефонної книги.
    """
    print("All contacts in the address book:")
    for name, numbers in address_book.items():
        print(f"{name}: {', '.join([p.number for p in numbers])}")


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

        if cmd == "hello":
            print("How can I help you?")

        elif cmd == "add":
            if len(args) >= 2:
                add_contact(address_book, args[0], *args[1:])
            else:
                print("Invalid number of arguments for 'add' command.")

        elif cmd == "change":
            if len(args) == 3:
                change_contact(address_book, args[0], args[1], args[2])
            else:
                print("Invalid number of arguments for 'change' command.")

        elif cmd == "show":
            if len(args) == 1:
                show_phone(address_book, args[0])
            elif len(args) == 0:
                show_all_contacts(address_book)
            else:
                print("Invalid number of arguments for 'show' command.")

        else:
            print("Invalid command. Type again!")


if __name__ == "__main__":
    main()
