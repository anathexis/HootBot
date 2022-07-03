from calendar import c
from random import seed, choice, randint
from typing import List

class Die():  
    '''Represent a die of n faces'''
    @staticmethod
    def get_available_dice():
        # List of commonly used dice
        return [Die(20), Die(12), Die(10), Die(8), Die(6), Die(4)]

    def __init__(self, faces: int):
        self.faces = faces
    
    def __repr__(self) -> str:
        return f'<Die {self.faces}>'

    def __str__(self) -> str:
        return f'd{self.faces}'

    def roll(self) -> int:
        return randint(1, self.faces)

class Cast():
    @staticmethod
    def get_cast_from_ndn_string(ndn_string: str) -> 'Cast':
        dice_number, dice_faces = map(int, ndn_string.split('d'))
        return Cast(dice_number, dice=Die(dice_faces))

    @staticmethod
    def get_random_cast(min_number_of_dice=4, max_number_of_dice=16, min_number_of_faces:int=0, max_number_of_faces:int=500):
        return Cast(
                # Choose a random number of dices
                randint(min_number_of_dice, max_number_of_dice),
                # Choose a commonly used dice (get_available_dice) in the list of dice
                choice([die for die in Die.get_available_dice() if (die.faces >= min_number_of_faces and die.faces <= max_number_of_faces)]))

    '''Represents a finite number of dices to be thrown'''
    def __init__(self, dice_number: int, dice: Die):
        self.dice_number = dice_number
        self.dice = dice
        self.current_throw: List[int] = []

    def __repr__(self) -> str:
        return f'<Cast {self.dice_number} Dice {self.dice.faces}>'

    def __str__(self) -> str:
        return f'{self.dice_number}{self.dice}'

    def throw(self) -> List[int]:
        self.current_throw = [self.dice.roll() for roll in range(self.dice_number)]
        return self.current_throw
    
    def get_thrown_sum(self) -> int:
        self.throw()
        return sum(self.current_throw)

if __name__ == '__main__':
    cast = Cast.get_cast_from_ndn_string('carrots')
    print(cast.get_thrown_sum())
