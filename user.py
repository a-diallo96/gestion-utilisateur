
import re
import string 
from tinydb import TinyDB,Query, where
from pathlib import Path
from typing import List

class User:

    DB = TinyDB(Path(__file__).resolve().parent / 'data.json', indent = 4)


    def __init__(self,first_name:str,last_name:str,phone_number:str="",address:str=""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def db_instance(self):
        return User.DB.get(where('first_name')==self.first_name and where('last_name') == self.last_name) #type:ignore
        
    def _checks(self):
        self._check_phone_number()
        self._check_names()
        
   
    def _check_phone_number(self):
        phone_number = re.sub(r"[+()\s]","",self.phone_number)
        if len(phone_number) < 10 or not phone_number.isdigit():
            raise ValueError("numero de téléphone non valide")

    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError("le prenom et le nom de famille ne peuve,t pas être vide ")
        
        special_characters = string.punctuation + string.digits 
        
        for character in self.first_name+self.last_name:
            if character in special_characters:
                raise ValueError("nom invalide {self.full_name}")
        
    def exists(self):
            return bool(self.db_instance)

    def delete(self) -> List[int]:  # type: ignore
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id]) #type: ignore
        return []

    def save(self, validate_data: bool=False):
        if validate_data:
            self._checks()
        if self.exists():
            return "l'utilisateur existe déja"
        else:
            return User.DB.insert(self.__dict__)

    
    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


    def __str__(self):
        return f"{self.full_name}\n{self.phone_number}\n{self.address}"
    



#for testing our module
if __name__ == "__main__":
    from faker import Faker
    fake =Faker(locale="fr_FR")
    for _ in range(10):
        user = User (first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phone_number=fake.phone_number(),
                    address=fake.address())
        print(user)
        print("*"*20)
    aicha = User("aissatou","BA")
    print(aicha.save())
    
        