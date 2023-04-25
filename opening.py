from __future__ import annotations
from textual.app import App, ComposeResult, RenderResult
from textual.events import Key
from textual.widget import Widget
from textual.widgets import Button, Header, DataTable, Label, Input, Static, Footer, TabbedContent, TabPane, RadioButton, RadioSet, Markdown, OptionList
from textual.reactive import reactive
import initial_game as game
import time
import names
from textual.containers import Horizontal, Vertical, Container
from textual.screen import Screen
from rich.table import Table
from textual.widgets.option_list import Option, Separator



TempNewChar = reactive("Hill Dwarf")


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
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Markdown(game.AbilityPointMark(), classes="twentyPercentHeight")
        yield Horizontal(
            Container(Markdown(game.AbScoreTable(),classes="AbScoreData"), classes="AbScoreData"),
            Container(newCharacterStats(), classes="fiftyPercent_AbScoreScreen"),
            classes="AbScoreHorizHeight"
        )
        

    def on_mount(self):
        app.title = "Choose Ability Score"


class namePicker(Widget):
    character_classes = {
        "Hill Dwarf": names.dwarf_names,
        "Mountain Dwarf":names.dwarf_names,
    }

    

    def compose(self) -> ComposeResult:
        names = self.character_classes.get(TempNewChar)
        length = len(names)
        yield OptionList(*[names[i] for i in range(length)], classes="height80")
        yield Button("Select Name")

class namePickerScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(Markdown(game.ChooseNameMark(), classes="namePickerMark"), classes="height20")
        yield Horizontal(
            Container(namePicker(), classes="namePickerCenter"),
            Container(namePicker(), classes="namePickerCenter")
        )

    def on_mount(self):
        app.title = "Choose Your Name"

class newCharacterStats(Widget):
    
    kv_attributes = {
        "strength":"#strength_cost",
        "dexterity":"#dexterity_cost",
        "constitution":"#constitution_cost",
        "intelligence":"#intelligence_cost",
        "wisdom":"#wisdom_cost",
        "charisma":"#charisma_cost",
    }

    kv_costs = {
        "8":"0",
        "9":"1",
        "10":"2",
        "11":"3",
        "12":"4",
        "13":"5",
        "14":"7",
        "15":"9",

    }

    list_cost_labels = [
        "strength_cost",
        "dexterity_cost",
        "constitution_cost",
        "intelligence_cost",
        "wisdom_cost",
        "charisma_cost"
    ]
    
    def compose(self) -> ComposeResult:
        choice = game.ClassGetr(TempNewChar)
        yield Label("Attribute", classes="bold")
        yield Label("Points", classes="bold")
        yield Label("Cost", classes="bold")
        yield Label("Strength", classes="attributeLabel")
        yield Input(placeholder="0 + " + str(choice.strength), id="strength")
        yield Input(placeholder="0", id="strength_cost")
        yield Label("Dexterity", classes="attributeLabel")
        yield Input(placeholder=str(choice.dexterity), id="dexterity")
        yield Input(placeholder="0", id="dexterity_cost")
        yield Label("Constitution", classes="attributeLabel")
        yield Input(placeholder=str(choice.constitution), id="constitution")
        yield Input(placeholder="0", id="constitution_cost")
        yield Label("Intelligence", classes="attributeLabel")
        yield Input(placeholder=str(choice.intelligence), id="intelligence")
        yield Input(placeholder="0", id="intelligence_cost")
        yield Label("Wisdom", classes="attributeLabel")
        yield Input(placeholder=str(choice.wisdom), id="wisdom")
        yield Input(placeholder="0", id="wisdom_cost")
        yield Label("Charisma", classes="attributeLabel")
        yield Input(placeholder=str(choice.charisma), id="charisma")
        yield Input(placeholder="0", id="charisma_cost")
        yield Button("Submit Ability Scores", classes="abilityScreenBtn")

    def on_input_changed(self, event: Input.Changed) -> None:
        att_name = event.input.id
        att_value = event.input.value
        
        if att_name in self.kv_attributes:
            # cost_val = self.query_one("#strength_cost")
            # cost_val.value = att_value
            if att_value in self.kv_costs:
                var = self.kv_attributes.get(att_name)
                cost_val = self.query_one(var)
                cost_val.value = self.kv_costs.get(att_value)
            else:
                pass  #Need to implement the Error if score is outside of acceptable range

    def on_button_pressed(self, event: Button.Pressed) -> None:
        total = 0
        for item in self.query("Input"):
            if item.id in self.list_cost_labels:
                total = total + int(item.value)

        if total > 27:
            app.push_screen(ModalScreen_27())
        else:
            app.push_screen(Work_Continues())

class Work_Continues(Screen):
    
    def compose(self) -> ComposeResult:
        yield Static("The Work Continues ... more to follow", classes="containerBorder")

class ModalScreen_27(Screen):
    statement = """\
# Cost total cannot exceed 27      
    """

    def compose(self) -> ComposeResult:
        yield Container(Markdown(self.statement), classes="containerBorder")
        yield Container(Button("Go Back"), classes="containerBorder")

    def on_button_pressed(self, event: Button.Pressed):
        app.pop_screen()    



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
    global TempNewChar

    def compose(self) -> ComposeResult:
        yield Footer()
        self.styles.align_horizontal = ("center")
        
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
            
            global TempNewChar
            TempNewChar = char_class
            text_file = open("sample.txt", "wt")
            text_file.write(char_class)
            text_file.write("\n")
            text_file.write(str(TempNewChar))
            text_file.close()
            # app.push_screen(AbilityScores())
            app.push_screen(namePickerScreen())

class MainApp(App):
    CSS_PATH = "opening.css"
    # CSS_PATH = "multiple.css"
    SCREENS = {"QuitScreen":QuitScreen(),
               "ChooseRace":ChooseRace(),
               "AbilityScores":AbilityScores(),
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