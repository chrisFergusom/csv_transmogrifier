# plugins/haiku_generator_plugin.py

import json
import random
from plugin_abc import PluginABC

class HaikuGeneratorPlugin(PluginABC):
    def __init__(self):
        self.words = None

    def configure(self):
        # No configuration needed for this plugin
        pass

    def initialize(self):
        self.load_haiku_words()

    def shutdown(self):
        # No cleanup needed for this plugin
        pass

    def execute(self, gui):
        if not self.validate():
            self.initialize()
        self.generate_haiku(gui)

    def validate(self):
        return self.words is not None

    def get_name(self):
        return "Info:Haiku"

    def get_version(self):
        return "1.0"

    def get_description(self):
        return "Generate a two-part haiku reflection"

    def load_haiku_words(self):
        try:
            with open('data/haiku.json', 'r') as f:
                self.words = json.load(f)
        except FileNotFoundError:
            print("Error: haiku.json file not found")
            self.words = None

    def generate_haiku(self, gui):
        if not self.words:
            gui.text_widget.clear()
            gui.text_widget.append("Error: Haiku data not loaded properly.")
            return
        syllable_map = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}
        
        def get_word(syllables, word_type):
            syllable_key = syllable_map[syllables]
            word_list = self.words['syllables'][syllable_key][word_type]
            if word_list:
                word = random.choice(word_list)
                word_list.remove(word)
                return word
            return None

        def generate_line(target_syllables):
            line = []
            current_syllables = 0
            word_types = ['nouns', 'verbs', 'adjectives']
            
            while current_syllables < target_syllables:
                remaining_syllables = target_syllables - current_syllables
                possible_syllables = [s for s in range(1, 6) if s <= remaining_syllables]
                
                if not possible_syllables:
                    break
                
                syllables = random.choice(possible_syllables)
                word_type = random.choice(word_types)
                
                word = get_word(syllables, word_type)
                if word:
                    line.append(word)
                    current_syllables += syllables
                
            return ' '.join(line)

        haiku_parts = []
        for _ in range(2):
            part = [
                generate_line(5),
                generate_line(7),
                generate_line(5)
            ]
            haiku_parts.append('\n'.join(part))

        gui.text_widget.clear()
        gui.text_widget.append("\n\nTwo-part Haiku Reflection:\n" + "\n\n".join(haiku_parts))

# This function is kept for backwards compatibility
def register_plugin():
    return HaikuGeneratorPlugin.register()