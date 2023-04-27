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
import ab_score_summary as abss
import example as classList
import character_dev_lists



TempNewChar = reactive("Hill Dwarf")
TempNewName = ""
TempNewClass = ""



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
            Button("Exit", classes="startScreenBtn", id="exit"), id="startScreenMenu"
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

class StartScreen_SC(Screen):
    def compose(self) -> ComposeResult:
        yield StartScreen()

class AbilityScores(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Markdown(game.AbilityPointMark(TempNewChar), classes="twentyPercentHeight")
        yield Horizontal(
            Container(Markdown(game.AbScoreTable()), classes="AbScoreData"),
            Container(Button("More Info", id="abs_more_info"), classes="AbScoreButton"),
            Container(newCharacterStats(), classes="fiftyPercent_AbScoreScreen"),
            classes="AbScoreHorizHeight"
        )
        

    def on_mount(self):
        app.title = "Choose Ability Score"

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "abs_more_info":
            app.push_screen(ModalScreen_AbScoreSummary())


class namePicker(Widget):
    character_classes = {
        "Hill Dwarf": names.dwarf_names,
        "Mountain Dwarf":names.dwarf_names,
    }

    def compose(self) -> ComposeResult:
        names = self.character_classes.get(TempNewChar)
        length = len(names)
        yield OptionList(*[names[i] for i in range(length)], classes="height80", id="char_names")
        yield Container(Button("Select Name", id="picker_button"), classes="nameCreatorButton")


class nameCreator(Widget):

    def compose(self) -> ComposeResult:
        val = TempNewChar.upper()
        yield Container(Markdown((f"""## Create Your Name \nYou can create your own name for your {val} below"""), classes="nameCreatorMark"), classes="height20")
        yield Vertical(
            Container(Input(placeholder="Your Name Here", classes="nameCreatorInput"),classes="nameCreatorButton"),
            Container(Button("Submit Name", classes="nameCreatorButton", id="creator_button"),classes="nameCreatorButton"),
            classes="nameCreatorCenter"
        )

    def on_button_pressed(self, event: Button.Pressed):
        global TempNewName
        TempNewName = self.query_one("Input").value
        app.push_screen(AbilityScores())


class namePickerScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(Markdown(game.ChooseNameMark(), classes="namePickerMark"), classes="height20")
        yield Horizontal(
            Container(namePicker(), classes="namePickerCenter"),
            Container(nameCreator(), classes="namePickerCenter"),
            classes="namePickerScreenHeight"
        )

    def on_mount(self):
        app.title = "Choose Your Name"

    option_choice = ""
    def on_option_list_option_highlighted(self, event: OptionList.OptionSelected):
        self.option_choice = event.option.prompt
        

    def on_button_pressed(self, event: Button.Pressed) -> None:
        global TempNewName
        if event.button.id == "picker_button":
            TempNewName = self.option_choice
            app.switch_screen(AbilityScores())


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
        yield Label("Score", classes="bold")
        yield Label("Race Bonus", classes="bold")
        yield Label("Cost", classes="bold")

        yield Label("Strength", classes="attributeLabel")
        yield Input(placeholder="0", id="strength")
        yield Input(placeholder=str(choice.strength), disabled=True)
        yield Input(placeholder="0", id="strength_cost", disabled=True)
        yield Label("Dexterity", classes="attributeLabel")
        yield Input(placeholder="0", id="dexterity")
        yield Input(placeholder=str(choice.dexterity), disabled=True)
        yield Input(placeholder="0", id="dexterity_cost", disabled=True)
        yield Label("Constitution", classes="attributeLabel")
        yield Input(placeholder="0", id="constitution")
        yield Input(placeholder=str(choice.constitution), disabled=True)
        yield Input(placeholder="0", id="constitution_cost", disabled=True)
        yield Label("Intelligence", classes="attributeLabel")
        yield Input(placeholder="0", id="intelligence")
        yield Input(placeholder=str(choice.intelligence), disabled=True)
        yield Input(placeholder="0", id="intelligence_cost", disabled=True)
        yield Label("Wisdom", classes="attributeLabel")
        yield Input(placeholder="0", id="wisdom")
        yield Input(placeholder=str(choice.wisdom), disabled=True)
        yield Input(placeholder="0", id="wisdom_cost", disabled=True)
        yield Label("Charisma", classes="attributeLabel")
        yield Input(placeholder="0", id="charisma")
        yield Input(placeholder=str(choice.charisma), disabled=True)
        yield Input(placeholder="0", id="charisma_cost", disabled=True)
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
                pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        total = 0
        for item in self.query("Input"):
            if item.id in list(self.kv_attributes.keys()) and 8>int(item.value)>15:
                app.push_screen(ModalScreen_8_15())
############################################################################################
#THIS    WHOLE AREA IS CURRENTLY BROKEN NEED TO FIGURE OUT A BETTER DATA VALIDATION METHOD
############################################################################################
            if item.id in self.list_cost_labels:
                total = total + int(item.value)

        if total > 27:
            app.push_screen(ModalScreen_27())
        else:
            app.push_screen(ChooseClassScreen())

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

class ModalScreen_8_15(Screen):
    statement = """\
# Score must be between 8 and 15      
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

class ChooseClass(Widget):
    def compose(self) -> ComposeResult:
        self.styles.width = "70w"
        self.styles.align_horizontal = "center"
        with TabbedContent():
            for item in classList.data:
                c_class = item[0]
                desc = item[1]
                hit_die = item[2]
                prim_ability = item[3]
                sav_throw_prof = item[4]
                ar_wpn_prof = item[5]

                md = f"""\
# {c_class}

### Description: \n  {desc}
### Hit Die: \n  {hit_die}
### Primary Ability: \n {prim_ability}
### Saving Throw Proficiencies: \n {sav_throw_prof}
### Armor and Weapon Proficiencies: \n {ar_wpn_prof}
                    
                    """    
                with TabPane(c_class, id=c_class):
                    yield Markdown(md, classes="ta_class")

    def on_button_pressed(self, event: Button.Pressed):
        
        
        text_file = open("sample.txt", "wt")
        text_file.write(str(final_choice_id))
        text_file.write("\n")
        # text_file.write(str(TabbedContent.id))
        text_file.close()



class ChooseClassScreen(Screen):
    
    def compose(self) -> ComposeResult:
        self.styles.align_horizontal = "center"
        yield Header()
        yield Footer()
        yield Horizontal(
            Container(ChooseClass(), classes="choose_race_screen_80"),
            Container(ClassRadioButton(), classes="choose_race_screen_20"),
            classes="choose_race_screen_hz"
        )

    def on_mount(self) -> None:
        app.title = "Choose Your Class"


class ClassRadioButton(Widget):
    def compose(self) -> ComposeResult:
        self.styles.align = ("center", "middle")
        with RadioSet():
            for item in character_dev_lists.character_classes:
                yield RadioButton(item, id=item)

        yield Button("Submit", classes="border")
    
    def on_button_pressed(self, event: Button.Pressed):
        c_class = self.query_one(RadioSet).pressed_button
        global TempNewClass
        TempNewClass = c_class.id


class RaceRadioButton(Widget):
    def compose(self) -> ComposeResult:
        self.styles.align = ("center", "middle")
        with RadioSet():
            for item in character_dev_lists.character_races:
                yield RadioButton(item, id=item)

        yield Button("Submit", classes="border")

    
    def on_button_pressed(self, event: Button.Pressed):
        race = self.query_one(RadioSet).pressed_button
        global TempNewChar
        TempNewChar = race.id
        text_file = open("sample.txt", "wt")
        text_file.write((race.id))
        text_file.write("\n")
        # text_file.write(str(TabbedContent.id))
        text_file.close()
        app.push_screen(namePickerScreen())

class ChooseRace(Widget):
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
        self.styles.align_horizontal = ("center")
        
        with TabbedContent():
            with TabPane('Dwarf'):
                yield Markdown(game.DwarfMark())
            
            with TabPane('Elf'):
                yield Markdown(game.ElfMark())

            with TabPane("Halfling"):
                yield Markdown(game.HalflingMark())

            with TabPane("Human"):
                yield Markdown(game.HumanMark())
                with TabbedContent():
                    for sub in self.human_subraces:
                        yield TabPane(sub, Markdown(self.hum_sub_info[sub]))
                        

            with TabPane("Dragonborn"):
                yield Markdown(game.DragonbornMark())

            with TabPane("Gnome"):
                yield Markdown(game.GnomeMark())

            with TabPane("Half-Elf"):
                yield Markdown(game.HalfelfMark())

            with TabPane("Half-Orc"):
                yield Markdown(game.HalforcMark())

            with TabPane("Tiefling"):
                yield Markdown(game.TieflingMark())


class AbScoreSummary(Widget):
    

    def compose(self) -> ComposeResult:
        self.styles.align_horizontal = ("center")
        with TabbedContent():
            with TabPane("Strength"):
                yield Markdown(abss.strength)
            with TabPane("Dexterity"):
                yield Markdown(abss.dexterity)
            with TabPane("Constitution"):
                yield Markdown(abss.constituion)
            with TabPane("Intelligence"):
                yield Markdown(abss.intelligence)
            with TabPane("Wisdom"):
                yield Markdown(abss.wisdom)
            with TabPane("Charisma"):
                yield Markdown(abss.charisma)

class ModalScreen_AbScoreSummary(Screen):

    def compose(self) -> ComposeResult:
        yield Container(AbScoreSummary(), classes="containerBorder")
        yield Container(Button("Go Back"), classes="containerBorder")

    def on_button_pressed(self, event: Button.Pressed):
        app.pop_screen()

class ChooseRaceScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Horizontal(
            Container(ChooseRace(), classes="choose_race_screen_80"),
            Container(RaceRadioButton(), classes="choose_race_screen_20"),
            classes="choose_race_screen_hz"
        )
    
    def on_mount(self) -> None:
        app.title = "Choose Your Race"


class RaceRadio(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(Static(game.ascii_dice()))

class MainApp(App):
    CSS_PATH = "opening.css"
    # CSS_PATH = "multiple.css"
    SCREENS = {"QuitScreen":QuitScreen(),
               "ChooseRace":ChooseRaceScreen(),
               "AbilityScores":AbilityScores(),
               "TestScreen":ChooseClassScreen(),
               "MenuScreen":StartScreen_SC(),
               }
    BINDINGS = [("m", "push_screen('MenuScreen')", "Menu"),
                ("q", "push_screen('QuitScreen')", "Quit"),
                ("t", "push_screen('TestScreen')", "Test Screen")
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
        elif event.button.id == "exit":
            app.push_screen(QuitScreen())
        else:
            pass



if __name__ == "__main__":
    app = MainApp()
    app.run()