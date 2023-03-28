from textual.app import App, ComposeResult, RenderResult
from textual.events import Key
from textual.widget import Widget
from textual.widgets import Button, Header, Label, Input, Static, Footer, TabbedContent, TabPane, RadioButton, RadioSet
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

class Cover(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Static("This is the splash screen for the Game \nWhat will we see", id="words")
        yield Static("Press escape to continue [blink]_[/]", id="words2")
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

    def compose(self) -> ComposeResult:
        yield Footer()

        with TabbedContent():
            with TabPane('Part 1'):
                yield Static("This is ok")
            with TabPane('Part 2'):
                yield Static("More Information")

            
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
            "Drgonborn",
            "Gnome",
            "Half-Elf",
            "Half-Orc",
            "Tiefling",
        )

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
    SCREENS = {"cover": Cover(), "NewCharScreen": NewCharScreen()}
    BINDINGS = [("m", "push_screen('cover')", "Cover"),
                ("q", "quit", "Quit"),
                ("f", "toggle_class('sidebar', '-active')", "Show Sidebar")
    ]
    TITLE = "Adventure Game Menu"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            yield newCharacter()
            yield newCharacterStats()
            yield newCharacterRace()
            yield newCharacterRace()
        yield Footer()
        yield sidebar()        

if __name__ == "__main__":
    app = MainApp()
    app.run()