import smtplib
from abc import *
class Contact:
    counter = 1
    def __init__(self, name, lastname, email, phone, address, id_=None):
        self.name = name
        self.lastname = lastname
        self.phone = phone
        self.email = email
        self.address = address
        if id_ == None:
            self.id_ = Contact.counter
            Contact.counter += 1
        else:
            self.id_ =id_


    def __str__(self):
        info = "NAME: {}\nLASTNAME:{}\nPHONE:{}\nEMAIL:{}\nADDRESS:{}"
        return info.format(self.name, self.lastname, self.phone, self.email, self.address)


class Panel:
    def __init__(self):
        self.repo = DatabaseRepository()

    def menu(self):
        print("1-Add New Contact")
        print("2-Search Contact")
        print("3-delete contact")
        print("4-update contact")
        print("5-show all contacts")
        print("6-Send Email to contact")
        print("7-Send SMS to contact")
        print("8-exit")

    def add_new_contact(self):
        name = input("enter name ")
        lastname = input("enter lastname ")
        phone = input("enter phone ")
        email = input("enter email ")
        address = input("enter address ")
        c = Contact(name,lastname,email,phone,address)
        self.repo.save(c)

    def search_contact(self):
        name = input("enter name ")
        result = self.repo.search(name)
        for contact in result:
            print(contact)
            print("="*20)


    def start(self):
        while True:
            self.menu()
            choice = int(input("choose an option"))
            if choice == 1:
                self.add_new_contact()
            elif choice == 2:
                self.search_contact()
            elif choice == 3:
                self.delete_contact()
            elif choice == 4:
                self.update_contact()
            elif choice == 5:
                self.show_all_contacts()
            elif choice == 6:
                self.send_mail()
            elif choice == 8:
               exit(0)
            else:
                print("Get Away")

    def delete_contact(self):
        name = input("enter name ")
        result = self.repo.search(name)
        for contact in result:
            print(contact)
            answer = input("Do You Want to Delete This Contact?[y/n]")
            if answer == 'y':
                self.repo.delete(contact.id_)
                break

    def update_contact(self):
        name = input("enter name ")
        result = self.repo.search(name)
        for contact in result:
            print(contact)
            answer = input("Do You Want to Update This Contact?[y/n]")
            if answer == 'y':
                name = input("enter name ")
                lastname = input("enter lastname ")
                phone = input("enter phone ")
                email = input("enter email ")
                address = input("enter address ")
                name = contact.name if name=="" else name
                lastname = contact.lastname if lastname=="" else lastname
                phone = contact.phone if phone=="" else phone
                email = contact.email if email=="" else email
                address = contact.address if address=="" else address
                new_contact = Contact(name, lastname, email,phone,address, contact.id_)
                self.repo.update(contact.id_, new_contact)
                break

    def show_all_contacts(self):
        contacts = self.repo.find_all()
        for contact in contacts:
            print("="*20)
            print(contact)

    def send_mail(self):
        name = input("enter name ")
        result = self.repo.search(name)
        for contact in result:
            print(contact)
            answer = input("Do You Want to Send Mail to This Contact?[y/n]")
            if answer=='y':
                message = input("enter message")
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("samira.developer.python@gmail.com", "12qwaszx!@")
                server.sendmail("samira.developer.python@gmail.com", contact.email, message)
            break



class Repository(ABC):

    @abstractmethod
    def save(self, contact):
        pass

    @abstractmethod
    def delete(self, id_):
        pass

    @abstractmethod
    def update(self, id_, contact):
        pass

    @abstractmethod
    def search(self, name):
        pass

    @abstractmethod
    def find_all(self):
        pass


class FileRepository(Repository):
    pass


class DatabaseRepository(Repository):
    pass


class CollectionRepository(Repository):
    def __init__(self):
        self.__contacts = {}

    def save(self, contact):
        self.__contacts[contact.id_] = contact # {10:contact, 11:contact}

    def update(self, id_, contact): #(10, contact1)
        self.__contacts[id_] = contact # {}{10:contact1, 11:contact}

    def delete(self, id_):
        del self.__contacts[id_]

    def search(self, name):
        result = []
        for contact in self.__contacts.values():
            if contact.name == name:
                result.append(contact)
        return result

    def find_all(self):
        return self.__contacts.values()

p = Panel()
p.start()