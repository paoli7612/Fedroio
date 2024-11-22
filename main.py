from random import randint

n = randint(1, 10)

i = int(input("Prova ad indovinare: "))

if n == i:
    print("Hai indovinato, il numero era", n)
elif n > i:
    print("Il numero era più alto:", n)
else:
    print("Il numero era più basso:", n)