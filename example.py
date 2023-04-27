from textual.app import App, ComposeResult, RenderResult
from textual.events import Key
from textual.widget import Widget
from textual.widgets import Button, Header, DataTable, Label, Input, Static, Footer, TabbedContent, TabPane, RadioButton, RadioSet, Markdown
from textual.reactive import reactive
import initial_game as game
import time
from textual.containers import Horizontal, Vertical, Container
from textual.screen import Screen



data = [
    # ("Class","Description","Hit Die","Primary Ability","Saving Throw Proficiencies","Armor and Weapon Proficiencies"),
    ("Barbarian","A fierce warrior of primitive background who can enter a battle rage","d12","Strength","Strength & Constitution","Light and medium armor, shields, simple and martial weapons"),
    ("Bard","An inspiring magician whose power echoes the music of creation","d8","Charisma","Dexterity & Charisma","Light armor, simple weapons, hand crossbows, longswords, rapiers, shortswords"),
    ("Cleric","A priestly champion who wields divine magic in service of a higher power","d8","Wisdom","Wisdom & Charisma","Light and medium armor, shields, simple weapons"),
    ("Druid","A priest of the Old Faith, wielding the powers of nature - moonlight and plant growth, fire and lightning - and adopting animal forms","d8","Wisdom","Intelligence & Wisdom","Light and medium armor (nonmetal), shields (nonmetal), clubs, daggers, darts, javelins, maces, quarterstaffs, scimitars, sickles, slings, spears"),
    ("Fighter","A master of martial combat, skilled with a variety of weapons and armor","d10","Strength or Dexterity","Strength & Constitution","All armor, shields, simple and martial weapons"),
    ("Monk","A master of martial arts, harnessing the power of the body in pursuit of physical and spiritual perfection","d8","Dexterity & Wisdom","Strength & Dexterity","Simple weapons, shortswords"),
    ("Paladin","A holy warrior bound to a sacred oath","d10","Strength & Charisma","Wisdom & Charisma","All armor, shields, simple and martial weapons"),
    ("Ranger","A warrior who uses martial prowess and nature magic to combat threats on the edges of civilization","d10","Dexterity & Wisdom","Strength & Dexterity","Light and medium armor, shields, simple and martial weapons"),
    ("Rogue","A scoundrel who uses stealth and trickery to overcome obstacles and enemies","d8","Dexterity","Dexterity & Intelligence","Light armor, simple weapons, hand crossbows, longswords, rapiers, shortswords"),
    ("Sorcerer","A spellcaster who draws on inherent magic from a gift or bloodline","d6","Charisma","Constitution & Charisma","Daggers, darts, slings, quarterstaffs, light crossbows"),
    ("Warlock","A wielder of magic that is derived from a bargain with an extraplanar entity","d8","Charisma","Wisdom & Charisma","Light armor, simple weapons"),
    ("Wizard","A scholarly magic-user capable of manipulating the structures of reality","d6","Intelligence","Intelligence & Wisdom","Daggers, darts, slings, quarterstaffs, light crossbows"),
]


class MainApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        rows = iter(data)
        table.add_columns(*next(rows))
        table.add_rows(rows)




if __name__ == "__main__":
    app = MainApp()
    app.run()