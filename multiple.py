from textual.app import App, ComposeResult, RenderResult
from textual.events import Key
from textual.widget import Widget
from textual.widgets import Button, Header, Label, Input, Static, Footer, TabbedContent, TabPane, RadioButton, RadioSet, Markdown
from textual.reactive import reactive
import initial_game as game
import time
from textual.containers import Horizontal, Vertical
from textual.screen import Screen

dbConn, dbCur = game.db_init()

'''
This is a little project to better understand how Textual works in order to use it
for important things.

'''
MAIN_TITLE = """
             _                 _                     _____                      
    /\      | |               | |                   / ____|                     
   /  \   __| |_   _____ _ __ | |_ _   _ _ __ ___  | |  __  __ _ _ __ ___   ___ 
  / /\ \ / _` \ \ / / _ \ '_ \| __| | | | '__/ _ \ | | |_ |/ _` | '_ ` _ \ / _ \\
 / ____ \ (_| |\ V /  __/ | | | |_| |_| | | |  __/ | |__| | (_| | | | | | |  __/
/_/    \_\__,_| \_/ \___|_| |_|\__|\__,_|_|  \___|  \_____|\__,_|_| |_| |_|\___|
                                                                                
    
    """


DWARVES = """\
# Dwarf

Bold and hardy, dwarves are known as skilled warriors, miners,
and workers of stone and metal. Though they stand well under 
5 feet tall, dwarves are so broad and compact that they
can weigh as much as a human standing nearly two feet taller.
Their courage and endurance are also easily a match for any of
the larger folk.

"""
ELVES = game.ElfMark()
HALFLING = game.HalflingMark()
HUMANS = game.HumanMark()

class Cover(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(MAIN_TITLE, id="words")
        yield Footer()


class NewCharScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Go Back")]

    def compose(self) -> ComposeResult:
        yield newCharacterStats()
        yield Footer()

class RaceScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Go Back")]

    def compose(self) -> ComposeResult:
        yield Footer()
        yield newCharacterRace()

class MenuScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Go Back")]

    dwarf_subraces = ["Hill Dwarf", "Mountain Dwarf"]
    elf_subraces = ["High Elf", "Wood Elf","Dark Elf (Drow)"]
    halfling_subraces = ["Lightfoot","Stout"]
    human_subraces = ["Calishite","Chondathan","Damaran","Illuskan","Mulan","Rashemi","Shou","Tethyrian","Turami"]
    gnome_subraces = ["Forest Gnome","Rock Gnome"]
    hum_sub_info = {"Calishite":game.Calishite(), "Chondathan": game.Chondathan(), "Damaran":game.Damaran(), "Illuskan":game.Illuskan(), "Mulan":game.Mulan(), "Rashemi":game.Rashemi(),
                    "Shou":game.Shou(), "Tethyrian":game.Tethyrian(), "Turami":game.Turami()
                    }

    def compose(self) -> ComposeResult:
        yield Footer()

        with TabbedContent():
            with TabPane('Dwarf'):
                yield Markdown(DWARVES)
                for sub in self.dwarf_subraces:
                    yield RadioButton(sub) 
            
            with TabPane('Elf'):
                yield Markdown(game.ElfMark())
                for sub in self.elf_subraces:
                    yield RadioButton(sub)

            with TabPane("Halfling"):
                yield Markdown(HALFLING)
                for sub in self.halfling_subraces:
                    yield RadioButton(sub)

            with TabPane("Human"):
                yield Markdown(HUMANS)
                with TabbedContent():
                    for sub in self.human_subraces:
                        yield TabPane(sub, Markdown(self.hum_sub_info[sub]))

            with TabPane("Dragonborn"):
                yield Markdown(game.DragonbornMark())
                yield RadioButton("Dragonborn")

            
class EnterButton(Widget):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button("Enter", id="charSubmit")
        )

newChar = game.Character()

class sidebar(Widget):
    def compose(self) -> ComposeResult:
        yield Button("New Character", id= "SideBar1")
        yield Button("Menu")
        yield Button("Race", id="RaceButton")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "SideBar1":
            self.app.push_screen('NewCharScreen')
        elif event.button.id == "RaceButton":
            self.app.push_screen(RaceScreen())
        else:
            self.app.push_screen(MenuScreen())

class newCharacterRace(Widget):

    def compose(self) -> ComposeResult:
        yield Label("Choose your Race...")
        yield RadioSet(
            "Dwarf",
            "Elf",
            "Halfling",
            "Human",
            "Dragonborn",
            "Gnome",
            "Half-Elf",
            "Half-Orc",
            "Tiefling",
        )
        yield Label(id="class_button_pressed")
        yield Button("Test")

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
       self.query_one("#class_button_pressed", Label).update(
            f"{event.pressed.label}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        text_file = open("sample.txt", "wt")
        text_file.write(str(self.query_one("#class_button_pressed").renderable))
        text_file.close()





class newCharacterClass(Widget):
    def compose(self) -> ComposeResult:
        yield Label("Choose your Class...")
        yield RadioSet(
            "Barbarian",
            "Bard",
            "Cleric",
            "Druid",
            "Fighter",
            "Monk",
            "Paladin"
        )

        


class newCharacterStats(Widget):

    def compose(self) -> ComposeResult:
        yield Label("Strength", classes="label")
        yield Input(placeholder="0", id="strength")
        yield Label("Dexterity", classes="label")
        yield Input(placeholder="0", id="dexterity")
        yield Label("Constitution", classes="label")
        yield Input(placeholder="0", id="constitution")
        yield Label("Intelligence", classes="label")
        yield Input(placeholder="0", id="intelligence")
        yield Label("Wisdom", classes="label")
        yield Input(placeholder="0", id="wisdom")
        yield Label("Charisma", classes="label")
        yield Input(placeholder="0", id="charisma")
        # yield Label()
        # yield Button('Enter', id="charSubmit")



class newCharacter(Widget):
    
    
    def compose(self) -> ComposeResult:
        yield Vertical(
            Input(placeholder="name", id="name"),
            Input(placeholder="age", id="age"),
            Input(placeholder="gender", id="gender"),
            Button("Enter")
            
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        newChar.setName(self.query_one('#name').value)
        newChar.setAge(self.query_one('#age').value)
        newChar.setGender(self.query_one('#gender').value)
        game.WizardEntry(dbConn,dbCur,newChar)

        fe = game.MountainDwarf()

        text_file = open("sample.txt", "wt")
        n = text_file.write(str(fe.strength))
        text_file.close()
        

class MainApp(App):
    CSS_PATH = "multiple.css"
    SCREENS = {"cover": Cover(),
               "NewCharScreen": NewCharScreen(),
               "MenuScreen": MenuScreen()}
    BINDINGS = [("m", "push_screen('MenuScreen')", "Menu"),
                ("q", "quit", "Quit"),
                ("f", "toggle_class('sidebar', '-active')", "Show Sidebar"),
                ("t", "push_screen('cover')", "Title")
    ]

    TITLE = "Adventure Game Menu"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            yield newCharacter()
            yield newCharacterStats()
            yield newCharacterRace()
            yield newCharacterClass()
        yield Footer()
        yield sidebar()    

        

if __name__ == "__main__":
    app = MainApp()
    app.run()