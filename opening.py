from textual.app import App, ComposeResult, RenderResult
from textual.events import Key
from textual.widget import Widget
from textual.widgets import Button, Header, DataTable, Label, Input, Static, Footer, TabbedContent, TabPane, RadioButton, RadioSet, Markdown
from textual.reactive import reactive
import initial_game as game
import time
from textual.containers import Horizontal, Vertical, Container
from textual.screen import Screen


TempNewChar = {"char_class":"",}


MAIN_TITLE = """
             _                 _                     _____                      
    /\      | |               | |                   / ____|                     
   /  \   __| |_   _____ _ __ | |_ _   _ _ __ ___  | |  __  __ _ _ __ ___   ___ 
  / /\ \ / _` \ \ / / _ \ '_ \| __| | | | '__/ _ \ | | |_ |/ _` | '_ ` _ \ / _ \\
 / ____ \ (_| |\ V /  __/ | | | |_| |_| | | |  __/ | |__| | (_| | | | | | |  __/
/_/    \_\__,_| \_/ \___|_| |_|\__|\__,_|_|  \___|  \_____|\__,_|_| |_| |_|\___|
                                                                                
    
    """

class startScreenButton(Widget):

    def compose(self) -> ComposeResult:
        
        self.styles.border = ("ascii","green")

        yield Horizontal(
            Button("Start Game", classes="startScreenBtn"),
            Button("Continue Game", classes="startScreenBtn"),
            Button("Create New Character", classes="startScreenBtn", id="CreateCharacter"),
            Button("Exit", classes="startScreenBtn"), id="startScreenMenu"
        )

    # def on_button_pressed(self, event: Button.Pressed) -> None:
    #     if event.button.label == "Create New Character":
    #         app.push_screen("ChooseRace")
    #     else:
    #         pass



class StartScreen(Widget):
    def compose(self) -> ComposeResult:
        self.styles.align = ("center","middle")
        yield Container(Static(MAIN_TITLE, id="words"), classes="containerBorder")
        yield Container(startScreenButton(), classes="containerBorder")

class AbilityScores(Screen):
    TITLE = "Choose Ability Score"

    data = [
        ("Score","Cost"),
        ("8","0"),
        ("9","1"),
        ("10","2"),
        ("11","3"),
        ("12","4"),
        ("13","5"),
        ("14","7"),
        ("15","9")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Markdown(game.AbilityPointMark(), classes="twentyPercentHeight")
        yield Horizontal(
            Container(newCharacterStats(), classes="fiftyPercent_AbScoreScreen"),
            Container(Markdown(game.AbScoreTable(),classes="AbScoreData"), classes="AbScoreData"),
            classes="AbScoreHorizHeight"
        )


class newCharacterStats(Widget):

    def compose(self) -> ComposeResult:
        yield Label("Strength")
        yield Input(placeholder=str(game.MountainDwarf().strength), id="strength")
        yield Label("Dexterity")
        yield Input(placeholder="0", id="dexterity")
        yield Label("Constitution")
        yield Input(placeholder="0", id="constitution")
        yield Label("Intelligence")
        yield Input(placeholder="0", id="intelligence")
        yield Label("Wisdom")
        yield Input(placeholder="0", id="wisdom")
        yield Label("Charisma")
        yield Input(placeholder="0", id="charisma")

class QuitScreen(Screen):
    
    question = """\
# Do you really want to quit?
        """

    def compose(self) -> ComposeResult:
        yield Container(Markdown(self.question), classes="containerBorder")
        yield Horizontal(
            Button("Yes", id="quit_yes", classes="startScreenBtn"),
            Button("No", id="quit_no", classes="startScreenBtn"), id="startScreenMenu"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit_yes":
            app.exit()
        else:
            app.pop_screen()

class ModalScreen_TooMany(Screen):
    statement = """\
# You can only choose one Class        
    """

    def compose(self) -> ComposeResult:
        yield Container(Markdown(self.statement), classes="containerBorder")
        yield Container(Button("Go Back"), classes="containerBorder")

    def on_button_pressed(self, event: Button.Pressed):
        app.pop_screen()

class ChooseRace(Screen):
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
        self.styles.align_horizontal = ("center")
        # self.styles.height = ("70vh")
        
        with TabbedContent():
            with TabPane('Dwarf'):
                yield Markdown(game.DwarfMark())
                for sub in self.dwarf_subraces:
                    yield RadioButton(sub) 
            
            with TabPane('Elf'):
                yield Markdown(game.ElfMark())
                for sub in self.elf_subraces:
                    yield RadioButton(sub)

            with TabPane("Halfling"):
                yield Markdown(game.HalflingMark())
                for sub in self.halfling_subraces:
                    yield RadioButton(sub)

            with TabPane("Human"):
                yield Markdown(game.HumanMark())
                with TabbedContent():
                    for sub in self.human_subraces:
                        yield TabPane(sub, Markdown(self.hum_sub_info[sub]),RadioButton(sub))
                        

            with TabPane("Dragonborn"):
                yield Markdown(game.DragonbornMark())
                yield RadioButton("Dragonborn")

            with TabPane("Gnome"):
                yield Markdown(game.GnomeMark())
                for sub in self.gnome_subraces:
                    yield RadioButton(sub)

            with TabPane("Half-Elf"):
                yield Markdown(game.HalfelfMark())
                yield RadioButton("Half-Elf")

            with TabPane("Half-Orc"):
                yield Markdown(game.HalforcMark())
                yield RadioButton("Half-Orc")

            with TabPane("Tiefling"):
                yield Markdown(game.TieflingMark())
                yield RadioButton("Tiefling")

        yield Container(Button("Create Character", classes="containerBorder"), classes="_1fr")

    def on_button_pressed(self, event: Button.Pressed):
        radio_count = self.query("RadioButton")
        counter = 0
        char_class = ""
        for Radio_Button in radio_count:
            if Radio_Button.value == True:
                counter = counter + 1
                char_class = str(Radio_Button.label)
            else:
                pass
        
        if counter != 1:
            app.push_screen(ModalScreen_TooMany())
        else:
            TempNewChar["char_class"] = char_class
            text_file = open("sample.txt", "wt")
            text_file.write(char_class)
            text_file.write("\n")
            text_file.write(str(TempNewChar["char_class"]))
            text_file.close()
            app.push_screen(AbilityScores())

class MainApp(App):
    CSS_PATH = "opening.css"
    # CSS_PATH = "multiple.css"
    SCREENS = {"QuitScreen":QuitScreen(),
               "ChooseRace":ChooseRace(),
               }
    BINDINGS = [("m", "push_screen('MenuScreen')", "Menu"),
                ("q", "push_screen('QuitScreen')", "Quit")
                # ("f", "toggle_class('sidebar', '-active')", "Show Sidebar"),
                # ("t", "push_screen('cover')", "Title")
    ]

    TITLE = "Adventure Game"

    def compose(self) -> ComposeResult:
        self.styles.align = ("center","middle")
        yield Header(show_clock=True)
        yield StartScreen()
        yield Footer()
     
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "CreateCharacter":
            app.push_screen("ChooseRace")
        else:
            pass



if __name__ == "__main__":
    app = MainApp()
    app.run()