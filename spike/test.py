from spike_lib.robot import hub
from resources.starWars import star_wars_theme
kostka = hub()
def hallo():
    kostka.playNotes(star_wars_theme, 1)