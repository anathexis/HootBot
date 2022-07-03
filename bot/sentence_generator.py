from random import choice
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import List


class SentenceGeneratorBase(metaclass=ABCMeta):
    @abstractmethod
    def draw_sentence(self, message: str) -> str:
        pass

class TextFileSentenceGenerator(SentenceGeneratorBase):
    def __init__(self, text_file_location: Path):
        self.text_file_location = text_file_location

    def get_sentence_list_from_path(self) -> List[str]:
        with self.text_file_location.open() as f:
            sentence_list = f.readlines()
        return sentence_list

    def draw_sentence(self, message: str) -> str:
        sentence_list = self.get_sentence_list_from_path()
        if message.isnumeric() and int(message) < len(sentence_list):
            return sentence_list[int(message)]
        return choice(sentence_list)


class SentenceGenerator(SentenceGeneratorBase):
    '''Returns a generated sentence. Currently POC.'''
    list_of_sentences = [
        'you understand the reality of life on this server: you are all puppets to an almighty sadistic dungeon master.',
        'you delve too much into the number crunching in relation with atmospheric modelling and end up to 42.000 due to a rounding error.',
        'you get convinced that an orgonite crystal will neutralize your second covid-19 jab.',
        'well, yes, but actually no.',
        'you attend a seminar given by a known fruity guru and try to find a hidden truth in the pips of a cucumber.',
        'the library in you grandfather house is so large it lets you enter the L-space. You end up unable to find that copy of Hamlet without all the \'e\'.',
        'you find yourself tied -- alone -- to a tramway tracks. Luckily, the person operating the switch chose the other tracks. Unluckily, the creator of the tramway dilemma forgot about the third rail.',
        'mandatory corporate events lead by your n+∞ (aka, his Fabiengness) are really not good for your sanity.',
        'you try to connect to the server hosting the coffee machine and end up with a 418 error.',
        'you look at a map of the USA and mixes Farhenreit and Celsius degrees, sending Las Vegas to hell for a dozen of days.',
        'you realize that the communication in the organisation chart is so transverse axis symbiotic that you didn\'t know your n+6 was the Prime Minister of Latvia.',
        'you face extra challenging circomstances due to covid-27 -- actually a 34th wave of covid-19 who mutated to infect mice and... Wait, you are a mouse now?',
        'the complexity of the application landscape makes you mishear a Dutch-speaking friend and pour him some apple juice instead.'
    ]
    
    def __init__(self):
        pass
    
    def draw_sentence(self) -> str:
         return choice(self.list_of_sentences)
