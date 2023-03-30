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


def ElfMark():
    content = """\
# Elf

Elves are a magical people of otherworldly grace, living in the world but entirely a part of it.
They live in places of ethereal beauty, in the midst of ancient forests or in silvery spires glittering with faerie light,
where soft music drifts through the air and gentle fragrences waft on the breeze. Elves love nature and magic, art and artistry, 
music and poetry, and the good things of the world.
"""
    return content
    
def HalflingMark():
    content = """\
# Halfling

The conforts of home are the goals of most halfings' lives: a place to settle in peace and quiet, far from marauding monsters and clashing
armies; a blazing fire and a generous meal; fine drink and fine conversation. Though some halflings live out their days in remote agricultural
communities, others form nomadic bands that travel constantly, lured by the open road and the wide horizon to dicover the wonders of new land and 
peoples. But even these wanderes love peace, food, hearth, and home, though home might be a wagon jostling along a dirt road or a raft floating 
downriver.        
"""
    return content

def HumanMark():
    content = """\
# Human

In the reckonings of most worlds, humans are the youngest of the common races, 
late to arrive on the world scene and short-lived in comparison to dwarves, elves, 
and dragons. Perhaps it is because of their shorter lives that they strive to achieve
as much as they can in the years they are given. Or maybe they feel they have 
something to prove to the elder races, and that's why they build their mighty 
empires on the foundation of conquest and trade. Whatever drives them, humans are 
the innovators, the achievers, and the pioneers of the worlds.
"""
    return content

def Calishite():
    content = "Shorter and slighter in build that most other humans, Calishites have dusky brown skin, hair, and eyes. They're found primarily in southwest Faerun"
    return content

def Chondathan():
    content = "Chondathans are slender, tawny-skinned folk with brown hair that rnages from almost blond to almost black. Most are tall and have green or brown eyes, but these traits are hardly universal. Humans of Chondathan descent dominate the central lands of Faerun, around the Inner Sea."
    return content

def Damaran():
    content = """\
Found primarily in the northwest of Faerun, Damarans are of moderate height and build, with skin hues ranging from tawny to fair.
Their hair is usually brown or black, and their eye color varies widely, though brown is most common.            
"""
    return content

def Illuskan():
    content = """\
Illuskans are tall, fair-skinned folk with blue or steely gray eyes. Most have raven-black hair, 
but those who inhabit the extreme northwest have blond, red, or light brown hair.       
"""
    return content

def Mulan():
    content = """\
Dominant in the eastern and southeastern shores of the Inner Sea, the Mulan are generally tall, 
slim, and amber-skinned, with eyes of hazel or brown. 
Their hair ranges from black to dark brown, but in the lands where the Mulan are most prominent, 
nobles and many other Mulan shave off all their hair.
"""
    return content

def Rashemi():
    content = """\
Most often found east of the Inner Sea and often intermingled with the Mulan, Rashemis tend to be short, stout, and 
muscular. They usually have dusky skin, dark eyes, and thick black hair.
"""
    return content

def Shou():
    content = """\
The Shou are the most numerous and powerful ethnic group in Kara-Tur, far to the east of Faerun. They are yellowish-bronze in hue,
with black hair and dark eyes. Shou surnames are usually presented before the given name.
"""
    return content

def Tethyrian():
    content = """\
Widespread along the entire Sword Coast at the western edge of Faerun, Tethyrians are of medum build and height, with dusky skin that tends to grow
fairer the farther north they dwell. Their hair and eye color varies widely, but brown hair and blue eyes are the most common.
Tethyrians primarily use Chondathan names.
"""
    return content

def Turami():
    content = """\
Native to the southern shore of the Inner Sea, the Turami people are generally tall and muscular, with dark mahogony skin, curly 
black hair, and dark eyes.
"""
    return content

def DragonbornMark():
    content = """\
# Dragonborn

Born of dragons, as their name proclaims, the dragonborn walk proudly through the world that greets them with fearful incomprehension.
Shaped by draconic gods or the dragons themselves, dragonborn originally hatched from eggs as a unique race, combining the best attributes 
of dragons and humanoids. Some dragonborn are faithful servants to true dragons, others form the ranks of soldiers in great wars, and still 
others find themselves adrift, with no clear calling in life.
"""
    return content

def GnomeMark():
    content = """\
# Gnome

A constant hum of busy activity pervades the warrens and neighborhoods where gnomes form their close-knit communities. Louder sounds 
punctuate the hum: a crunch of grinding gears here, a minor explosion there, a yelp of surprise or triumph, and especiallybursts of laughter. 
Gnomes take delight in life, enjoying every moment of invention, exploration, investigation, creation, and play.
"""
    return content

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
            print(ElfMark())
        elif selection == "3":
            pass
        elif selection == "4":
            sys.exit()
        else:
            print("Invalid Selection!")

if __name__ == '__main__':
    main()