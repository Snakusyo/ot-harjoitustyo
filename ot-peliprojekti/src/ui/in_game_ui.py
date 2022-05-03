from random import randint

#TESTING SOMETHING

#ANYTHING

lista = ["Hei: 0", "Moi: 20", "Kaveri: 10"]



def update_item(mjono: str, luku: int):

    numbers = ""
    for merkki in mjono:
        if merkki.isdigit():
            numbers += merkki

    return mjono.replace(numbers, str(luku))


x = "Hei"

for juttu in lista:
    if x in juttu:
        lista[lista.index(juttu)] = update_item(juttu, 20)

print(lista)