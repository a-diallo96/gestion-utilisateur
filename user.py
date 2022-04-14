
import re
import string 

class User:
    def __init__(self,first_name:str,last_name:str,phone_number:str="",address:str=""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
     
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
        user._check_phone_number()
        user._check_names()
        print("*"*20)
    
        