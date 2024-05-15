from typing import Union
import numpy as np

class Geo():
    def __init__(self) -> None:
        self.draw = ''
    def add(self, item) -> None:
        if isinstance(item, Geo):
            self.draw += f"{item.__str__()}\n"
        elif isinstance(item, str):
            self.draw += f"{item}\n"
        elif isinstance(item, list) or isinstance(item, tuple):
            for i in item:
                self.add(i)
        else:
            raise ValueError("Invalid item type. Item can only be a Geo object or a string.")

    def __str__(self) -> str:
        return self.draw
    
    def __repr__(self) -> str:
        return self.draw

    