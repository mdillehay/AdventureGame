import sqlite3
import os
import sys
import time
from textual.reactive import reactive
from textual import *

# ---------------------------------------------------------------------------------
# Initialized the DB and creates the connector and cursor for the rest of the app
# 
# This likely need to be moved to its own file at somepoint
# ---------------------------------------------------------------------------------
def db_init():
    """Initializes database and returns standard conn and cur"""

    conn = sqlite3.connect("wizard.db")
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


def ClassGetr(class_choice):
    """Return the correct python 'class' based on the character's RACE choice."""

    # Add a check for Human Subrace in order to change value to "Human"
    if "Human" in class_choice:
        class_choice = "Human"
    else:
        pass

    character_classes = {
        "Hill Dwarf": HillDwarf(),
        "Mountain Dwarf": MountainDwarf(),
        "High Elf": HighElf(),
        "Wood Elf": WoodElf(),
        "Dark Elf (Drow)": DarkElf(),
        "Lightfoot Halfling": Lightfoot(),
        "Stout Halfling": Stout(),
        "Human": Human(),
        "Forest Gnome": ForestGnome(),
        "Rock Gnome": RockGnome(),
        "Dragonborn": Dragonborn(),
        "Half-Elf": HalfElf(),
        "Half-Orc": HalfOrc(),
        "Tiefling": Tiefling(),
    }

    class_return = character_classes[class_choice]
    return class_return


class Character:
    """Base Class for all characters"""

    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

        self.strength_mod = 0
        self.dexterity_mod = 0
        self.constitution_mod = 0
        self.intelligence_mod = 0
        self.wisdom_mod = 0
        self.charisma_mod = 0

        self.height = None
        self.weight = None
        self.alignment = None
        self.language_prim = None
        self.language_sec = None

    def setName(self, name: str) -> None:
        """Set the characters Name"""
        self.name = name

    def setRace(self, race: str) -> None:
        """Store the characters Race"""
        self.race = race

    def setClass(self, char_class: str) -> None:
        """Set the characters Class"""
        self.char_class = char_class

    def setAge(self, age: str) -> None:
        """Set the chracters Age"""
        self.age = age

    def setGender(self, gender: str) -> None:
        """Set the characters Gender"""
        self.gender = gender

    def setStrength(self, strength: int) -> None:
        """Set the characters Strength"""
        self.strength = strength + self.strength_mod

    def setDexterity(self, dexterity: int) -> None:
        """Set the characters Dexterity"""
        self.dexterity = dexterity + self.dexterity_mod

    def setConstitution(self, constitution: int) -> None:
        """Set the characters Constiution"""
        self.constitution = constitution + self.constitution_mod

    def setIntelligence(self, intelligence: int) -> None:
        """Set the characters Intelligence"""
        self.intelligence = intelligence + self.intelligence_mod

    def setWisdom(self, wisdom: int) -> None:
        """Set the characters Wisdom"""
        self.wisdom = wisdom + self.wisdom_mod

    def setCharisma(self, charisma: int) -> None:
        """Set the characters Charisma"""
        self.charisma = charisma + self.charisma_mod

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class Dwarf(Character):
    """Class definition of a Dwarf, inherits from Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

        self.constitution_mod = 2
        self.setConstitution(self.constitution)
        self.darkvision = True
        self.combat_training = ["battleaxe", "handaxe", "light hammer", "warhammer"]
        self.speed = 25
        self.poison_adv = True
        self.tool_prof = None
        self.stonecunning = True
        self.language_prim = "Common"
        self.language_sec = "Dwarvish"

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class MountainDwarf(Dwarf):
    """Class definition of Mountain Dwarf, inherits from Dwarf and Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )
        self.strength_mod = 2
        self.setStrength(self.strength)
        self.armor_prof = ["light", "medium"]

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class HillDwarf(Dwarf):
    """Class definition of Hill Dwarf, inherits from Dwarf and Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )
        
        self.strength_mod = 4
        self.setStrength(self.strength)

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class Elf(Character):
    """Class definition of Elf, inherits from Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

        self.constitution_mod = 2
        self.setConstitution(self.constitution)
        self.darkvision = True
        self.keen_senses = True
        self.fey_ancestry = True
        self.language_prim = "Common"
        self.language_sec = "Elvish"

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class HighElf(Elf):
    """Class definitio of High Elf, inherits from Elf and Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

        self.intelligence_mod = 1
        self.setIntelligence(self.intelligence)
        self.combat_training = ["longsword", "shortsword", "shortbow", "longbow"]
        self.cantrip_count = 1
        self.extra_language_count = 1

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class WoodElf(Elf):
    """Class definition of Wood Elf, inherits from Elf and Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

        self.wisdom_mod = 1
        self.setWisdom(self.wisdom)
        self.combat_training = ["longsword", "shortsword", "shortbow", "longbow"]
        self.fleet_feet = True
        self.mask_of_the_wild = True

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class DarkElf(Elf):
    """Class definition of Dark Elf (Drow), inherits from Elf and Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

        self.charisma_mod = 1
        self.setCharisma(self.charisma)
        self.superior_darkvision = True
        self.sunlight_sensitivity = True
        self.drow_magic = True
        self.combat_training = ["rapiers", "shortswords", "hand crossbows"]

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class Halfling(Character):
    """Class definition of Halfling, inherits from Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

        self.dexterity_mod = 2
        self.setDexterity(self.dexterity)
        self.lucky = True
        self.brave = True
        self.nimbleness = True
        self.language_prim = "Common"
        self.language_sec = "Halfling"

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item

class Lightfoot(Halfling):
    """Class definition of a Lightfoot Halfling, inherits from Halfling and Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

        self.charisma_mod = 1
        self.setCharisma(self.charisma)
        self.naturally_stealthy = True

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class Stout(Halfling):
    """Class definition of a Stout Halfling, inherits from Halfling and Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

        self.constitution_mod = 1
        self.setConstitution(self.constitution)
        self.stout_resilience = True

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class Human(Character):
    """Class definition of a Human, inherits from Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class Dragonborn(Character):
    """Class definition of a Dragonborn, inherits from Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class Gnome(Character):
    """Class definitio of a Gnome, inherits from Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class ForestGnome(Gnome):
    """Class definition of a Forest Gnome, inherits from Gnome and Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class RockGnome(Gnome):
    """Class definitionm of Rock Gnome, inherits from Gnome and Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class HalfElf(Character):
    """Class definition of a Half-Elf, inherits from Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class HalfOrc(Character):
    """Class definition of a Half-Orc, inherits from Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class Tiefling(Character):
    """Class definition of a Tiefling, inherits from Character"""
    def __init__(
        self,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
    ) -> None:
        super().__init__(
            strength, dexterity, constitution, intelligence, wisdom, charisma
        )

    def __iter__(self):
        for item in self.__dict__.items():
            if item[1] is None:
                pass
            elif item[1] == 0:
                pass
            else:
                yield item


class Wizard(Character):

    """Defines an individual Wizard"""

    # def __init__(self, name, age, gender):

    # Character.__init__(self, name, age, gender)

    def setSpecialty(self, specialty):
        self.specialty = specialty

    def cast(self):
        print(
            f"{self.name} cast an unforgivable curse.\n{self.name} is {self.age} years old.\n{self.name} is a {self.gender}."
        )

    def getName(self):
        return self.name

    def getAge(self):
        return self.age

    def getGender(self):
        return self.gender


def AbilityPointMark(class_choice: str):
    """Returns Markdown for Ability Point Screen"""
    classChoice = class_choice

    content = f"""\
# Choose Your Ability Points

You have 27 points to spend on your ability scores. The cost of each score is shown on the Ability Score Point Cost table (below). Using this method, 15 is
the highest score you can have before applying racial increases. You can't have a score lower than 8.\n
The racial bonuses for a {classChoice} are reflected below.

    """
    return content


def ChooseNameMark():
    """Returns Markdown Choose Name Screen"""
    content = """\
# Choose Your Name

Choose from a pre-selected list of names on the left or create your own name on the right.

    """
    return content


def AbScoreTable():
    """Returns Markdown for Ability Score Point Table"""
    content = """\
# Ability Point Score Table

| Score    | Cost    |
|----------|---------|
| '8'      | 0       |
| '9'      | 1       |
| '10'     | 2       |
| '11'     | 3       |
| '12'     | 4       |
| '13'     | 5       |
| '14'     | 7       |
| '15'     | 9       |   
        """
    return content


def ascii_dice():
    """Returns Markdown for dice ascii image"""

    content = """\
    .----------.     ________
   /          /|    /\       \\
  /     o    /o|   /o \   o   \\
 /__________/  |  /   o\_______\\
 | o        |  | /o    /o      /
 |          |o | \  o /   o   /
 |     o    |  /  \  /      o/
 |          | /    \/_______/
 |_________o|/
        
        
        """
    return content


def DwarfMark():
    """Returns Markdown for Dwarf explanation"""
    content = """\
# Dwarf

Bold and hardy, dwarves are known as skilled warriors, miners,
and workers of stone and metal. Though they stand well under 
5 feet tall, dwarves are so broad and compact that they
can weigh as much as a human standing nearly two feet taller.
Their courage and endurance are also easily a match for any of
the larger folk.

"""
    return content


def ElfMark():
    """Returns Markdown for Elf explanation"""
    content = """\
# Elf

Elves are a magical people of otherworldly grace, living in the world but not entirely a part of it.
They live in places of ethereal beauty, in the midst of ancient forests or in silvery spires glittering with faerie light,
where soft music drifts through the air and gentle fragrences waft on the breeze. Elves love nature and magic, art and artistry, 
music and poetry, and the good things of the world.
"""
    return content


def HalflingMark():
    """Returns Markdown for Halfling explanation"""
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
    """Returns Markdown for Human explanation"""
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
    """Returns Markdown for Calshite explanation"""
    content = "Shorter and slighter in build that most other humans, Calishites have dusky brown skin, hair, and eyes. They're found primarily in southwest Faerun"
    return content


def Chondathan():
    """Returns Markdown for Chondathan explanation"""
    content = "Chondathans are slender, tawny-skinned folk with brown hair that rnages from almost blond to almost black. Most are tall and have green or brown eyes, but these traits are hardly universal. Humans of Chondathan descent dominate the central lands of Faerun, around the Inner Sea."
    return content


def Damaran():
    """Returns Markdown for Damaran explanation"""
    content = """\
Found primarily in the northwest of Faerun, Damarans are of moderate height and build, with skin hues ranging from tawny to fair.
Their hair is usually brown or black, and their eye color varies widely, though brown is most common.            
"""
    return content


def Illuskan():
    """Returns Markdown for Illuskan explanation"""
    content = """\
Illuskans are tall, fair-skinned folk with blue or steely gray eyes. Most have raven-black hair, 
but those who inhabit the extreme northwest have blond, red, or light brown hair.       
"""
    return content


def Mulan():
    """Returns Markdown for Mulan explanation"""
    content = """\
Dominant in the eastern and southeastern shores of the Inner Sea, the Mulan are generally tall, 
slim, and amber-skinned, with eyes of hazel or brown. 
Their hair ranges from black to dark brown, but in the lands where the Mulan are most prominent, 
nobles and many other Mulan shave off all their hair.
"""
    return content


def Rashemi():
    """Returns Markdown for Rashemi explanation"""
    content = """\
Most often found east of the Inner Sea and often intermingled with the Mulan, Rashemis tend to be short, stout, and 
muscular. They usually have dusky skin, dark eyes, and thick black hair.
"""
    return content


def Shou():
    """Returns Markdown for Shou explanation"""
    content = """\
The Shou are the most numerous and powerful ethnic group in Kara-Tur, far to the east of Faerun. They are yellowish-bronze in hue,
with black hair and dark eyes. Shou surnames are usually presented before the given name.
"""
    return content


def Tethyrian():
    """Returns Markdown for Tethyrian explanation"""
    content = """\
Widespread along the entire Sword Coast at the western edge of Faerun, Tethyrians are of medum build and height, with dusky skin that tends to grow
fairer the farther north they dwell. Their hair and eye color varies widely, but brown hair and blue eyes are the most common.
Tethyrians primarily use Chondathan names.
"""
    return content


def Turami():
    """Returns Markdown for Turami explanation"""
    content = """\
Native to the southern shore of the Inner Sea, the Turami people are generally tall and muscular, with dark mahogony skin, curly 
black hair, and dark eyes.
"""
    return content


def DragonbornMark():
    """Returns Markdown for Dragonborn explanation"""
    content = """\
# Dragonborn

Born of dragons, as their name proclaims, the dragonborn walk proudly through the world that greets them with fearful incomprehension.
Shaped by draconic gods or the dragons themselves, dragonborn originally hatched from eggs as a unique race, combining the best attributes 
of dragons and humanoids. Some dragonborn are faithful servants to true dragons, others form the ranks of soldiers in great wars, and still 
others find themselves adrift, with no clear calling in life.
"""
    return content


def GnomeMark():
    """Returns Markdown for Gnome explanation"""
    content = """\
# Gnome

A constant hum of busy activity pervades the warrens and neighborhoods where gnomes form their close-knit communities. Louder sounds 
punctuate the hum: a crunch of grinding gears here, a minor explosion there, a yelp of surprise or triumph, and especially bursts of laughter. 
Gnomes take delight in life, enjoying every moment of invention, exploration, investigation, creation, and play.
"""
    return content


def HalfelfMark():
    """Returns Markdown for Hafl-Elf explanation"""
    content = """\
# Half-Elf

Walking in two worlds but truly belonging to neither, half-elves combine what some say are the best qualities of their elf and human parents: 
human curiosity, inventiveness, and ambition tempered by the refined senses, love of nature, and artistic tastes of the elves. Some half-elves 
live among humans, set apart by their emotional and physical differences, watching friends and loved ones age while time barely touches them.
Others live with the elves, growing restless as they reach adulthood in the timeless elven realms, while their peers continue to live as children.
Many half-elves, unable to fit into either society, choose lives of solitary wandering or join with other misfits and outcasts in the adventuring 
life.                
"""
    return content


def HalforcMark():
    """Returns Markdown for Half-Orc explanation"""
    content = """\
# Half-Orc

Whether united under the leadsership of a mighty warlock or having fought to a standstill after years of conflict, ord and human tribes sometimes 
form aliances, joining forces into a larger horde to the terror of civilized lands nearby. When these alliances are sealed by marriages, half-orcs are born. 
Some half-orcs rise to become proud chiefs of orc tribes, their human blood giving them an edge over their full-blooded orc rivals. Some venture into 
the world to prove their worth among humans and other more civilized races. Many of these become adventurers, achieving greatness for their mighty 
deeds and notoriety for their barbaric customs and savage fury.        
"""
    return content


def TieflingMark():
    """Returns Markdown for Tiefling explanation"""
    content = """\
# Tiefling

To be greeted with stares and whispers, to suffer violence and insult on the street, to see mistrust and fear in every eye: this is the lot of the 
tiefling. And to twist the knife, tieflings know that this is because of a pcat struck generations ago infused with the essence of Asmodeus--overlord 
of the Nine Hells--into their bloodline. Their appearance and their nature are not their fault but the result of an ancient sin, for which they and 
their children and their children's children will always be held accountable.        
"""
    return content


class Spell:
    """Defines an individual Spell"""

    def __init__(self, name: str, spell_type: str, IsActive: bool):
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


# Function to create a Character
def createCharacter():
    name = input("What is your new character's name? -- ")
    print("\n")
    age = input("How old is " + name + "? --")
    print("\n")
    gender = input("Is " + name + " a male or female? --")

    newChar = Character(name, int(age), gender)
    return newChar


# Function to insert an instance of Wizard Class into the db
def WizardEntry(conn, cur, wiz):
    db_insert = "INSERT INTO Wizards(name,age,gender) VALUES(?,?,?)"

    cur.execute(db_insert, (wiz.name, wiz.age, wiz.gender))
    conn.commit()


# Test function REMOVE before release
def test_function():
    x = createCharacter()
    print(x.name, x.age, x.gender)

    y = Wizard(x.name, x.age, x.gender)
    print(y.age)
    y.setSpecialty("Ice")
    print(y.specialty)

    s = Spell("Achio", "Utility", False)
    s.setLevel(10)

    print(f"{s.name} is a {s.spell_type} spell with a power level of {s.level}.")
    if s.IsActive == False:
        print(f"{s.name} is not currently active")
    else:
        print(f"{s.name} is currently active")

    i = Item()
    i.setName("Mjolnir")
    i.setType("Melee")
    i.setLevel(100)
    print("\n")
    print(f"{i.name} is a {i.itemType} weapon with a power level of {i.level}")

    time.sleep(10)
    os.system("clear")


# Main menu
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
        os.system("clear")
        if selection == "1":
            test_function()
        elif selection == "2":
            print(ElfMark())
        elif selection == "3":
            pass
        elif selection == "4":
            sys.exit()
        else:
            print("Invalid Selection!")


if __name__ == "__main__":
    main()
