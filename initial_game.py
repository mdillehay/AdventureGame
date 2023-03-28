import sqlite3
import os
import sys
import time

#Initialized the DB and creates the connector and cursor for the rest of the app
def db_init():
    conn = sqlite3.connect('wizard.db')
    cur = conn.cursor()

    cur.execute(
"""
CREATE TABLE if not exists Wizards
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL
    )
"""
    )
    cur.execute(
"""
CREATE TABLE IF NOT EXISTS Spells
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        SpellName TEXT NOT NULL,
        SpellType TEXT NOT NULL,
        IsActive TEXT NOT NULL,
        Wiz_id INTEGER NOT NULL,
        FOREIGN KEY (Wiz_id)
            REFERENCES Wizards (id)
    )

"""
    )

    conn.commit()
    return conn, cur


class Character:

    def __init__(self, strength = 0, dexterity = 0, constitution = 0, intelligence = 0, wisdom = 0, charisma = 0) -> None:
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

    def setName(self, name: str) -> None:
        self.name = name

    def setAge(self, age: str) -> None:
        self.age = age

    def setGender(self, gender: str) -> None:
        self.gender = gender        

    def setStrength(self, strength: int) -> None:
        self.strength = strength

    def setDexterity(self, dexterity: int) -> None:
        self.dexterity = dexterity

    def setConstitution(self, constitution: int) -> None:
        self.constitution = constitution

    def setIntelligence(self, intelligence: int) -> None:
        self.intelligence = intelligence

    def setWisdom(self, wisdom: int) -> None:
        self.wisdom = wisdom

    def setCharisma(self, charisma: int) -> None:
        self.charisma = charisma    

class MountainDwarf(Character):
    def __init__(self, strength=0, dexterity=0, constitution=0, intelligence=0, wisdom=0, charisma=0) -> None:
        
        self.setStrength(4)



class Wizard(Character):

    """Defines an individual Wizard"""

    #def __init__(self, name, age, gender):

        #Character.__init__(self, name, age, gender)

    def setSpecialty(self, specialty):
        self.specialty = specialty

    def cast(self):
        print(f'{self.name} cast an unforgivable curse.\n{self.name} is {self.age} years old.\n{self.name} is a {self.gender}.')

    def getName(self):
        return self.name

    def getAge(self):
        return self.age
    
    def getGender(self):
        return self.gender


class Spell:
    """Defines an individual Spell"""

    def __init__(self,name: str, spell_type: str, IsActive: bool):
        self.name = name
        self.spell_type = spell_type
        self.IsActive = IsActive

    def getName(self):
        return self.name

    def getSpellType(self):
        return self.spell_type

    def IsActive(self):
        return self.IsActive

    def setLevel(self, level):
        self.level = level
    
    def getLevel(self):
        return self.level

class Item:
    """Defines an individual item"""

    def __init__(self) -> None:
        pass
        
    def setName(self, name: str):
        self.name = name
    
    def setType(self, itemType: str):
        self.itemType = itemType

    def setLevel(self, level: int):
        self.level = level


#Function to create a Character
def createCharacter():
    name = input("What is your new character's name? -- ")
    print('\n')
    age = input("How old is " + name + "? --")
    print('\n')
    gender = input("Is "+name+" a male or female? --")

    newChar = Character(name,int(age),gender)
    return newChar


#Function to insert an instance of Wizard Class into the db
def WizardEntry(conn,cur,wiz):
    db_insert = "INSERT INTO Wizards(name,age,gender) VALUES(?,?,?)"

    cur.execute(db_insert,(wiz.name,wiz.age,wiz.gender))
    conn.commit()


#Test function REMOVE before release
def test_function():
    x = createCharacter()
    print(x.name, x.age, x.gender)

    y = Wizard(x.name,x.age,x.gender)
    print(y.age)
    y.setSpecialty("Ice")
    print(y.specialty)

    s = Spell('Achio','Utility',False)
    s.setLevel(10)

    print(f'{s.name} is a {s.spell_type} spell with a power level of {s.level}.')
    if s.IsActive == False:
        print(f'{s.name} is not currently active')
    else:
        print(f'{s.name} is currently active')

    i = Item()
    i.setName('Mjolnir')
    i.setType('Melee')
    i.setLevel(100)
    print("\n")
    print(f'{i.name} is a {i.itemType} weapon with a power level of {i.level}')



    time.sleep(10)
    os.system('clear')

#Main menu
def main_menu():
    print(
"""
##############-----Menu Options-----##############

    --> 1: Option 1
    --> 2: Option 2
    --> 3: Option 3
    --> 4: Option 4
"""
)



def main():
    conn, cur = db_init()

    while True:
        main_menu()
        selection = input("Enter Selection: ")
        os.system('clear')
        if selection == '1':
            test_function()
        elif selection == "2":
            pass
        elif selection == "3":
            pass
        elif selection == "4":
            sys.exit()
        else:
            print("Invalid Selection!")

if __name__ == '__main__':
    main()
