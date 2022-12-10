from operator import truediv
from random import *
import random

print("Generating Imp!")
def openfile(str): return open(str, 'r').read().split('\n')
flavors = openfile("Imparea/ImpareaProjects/data/flavors.csv")
adjectives = openfile("Imparea/ImpareaProjects/data/adjectives.csv")
nouns = openfile("Imparea/ImpareaProjects/data/nouns.csv")
colors = openfile("Imparea/ImpareaProjects/data/colors.csv")
alphabet = list("abcdefghijklmnopqrstuvwxyz")

def Get_Pronouns(): 
    return choice(["She/Her","He/Him","They/Them","Ask"])
def Get_255(): 
    return random.randint(0,255)
def Get_Letter(): 
    return choice(alphabet)
def Get_Upper_Letter(): 
    return Get_Letter().upper()
def Get_IO(): 
    return choice(['i','o']) 
def Get_Word_With(letter, listofwords):
    return choice([x for x in listofwords if x.lower().startswith(letter)])
def Get_Flav(letter): 
    return  Get_Word_With(letter,flavors).split(',')[0].capitalize()
def Get_Adj(letter): 
    return  Get_Word_With(letter, adjectives).capitalize()
def Get_Noun(letter): 
    return  Get_Word_With(letter, nouns).capitalize()
def Get_Color(): 
    return  choice(colors)

class Imp:
    def __init__(self, name, transform, pronouns, color):
        self.name = name
        self.transform = transform
        self.pronouns = pronouns
        self.color = color
    def __str__(self):
        return f"   Name: {self.name}\n   Transform: {self.transform}\n   Pronouns: {self.pronouns}\n   Color: {self.color}"


def Generate_An_Imp():
    name = Get_Upper_Letter() + Get_Letter() +Get_Letter() +  Get_IO()
    letter = Get_Letter()
    transform = f"{Get_Adj(letter)}! {Get_Flav(letter)}! {Get_Noun(letter)}!"
    pronouns = Get_Pronouns()
    color = Get_Color()
    return Imp(name, transform, pronouns, color)

imp = Generate_An_Imp()
print(imp)
input("Press any key to close.")