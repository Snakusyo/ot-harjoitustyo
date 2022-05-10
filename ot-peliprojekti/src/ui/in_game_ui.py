from doctest import DocTestRunner
from random import randint

#TESTING SOMETHING

#ANYTHING

#mountain generation testing

s = 128

def meri(koko: int):
    kartta = []
    for rivi in range(koko):
        karttarivi = []
        for ruutu in range(koko):
            karttarivi.append(0)
        kartta.append(karttarivi)
    return kartta


for rivi in meri(s):
 if len(rivi) != 128:
     print("perse")
