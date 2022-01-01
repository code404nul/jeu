from math import e
import time
import random
import getpass

print ("are you ready / es tu prêt")
time.sleep(1)
rep_game = input ("Y or n : ")
if rep_game == "Y":
    print (" solo / ensemble")
    time.sleep(1)
    rep1_game = input ("s/e : ")
    if rep1_game == "s":
        tentative = 0
        while tentative <= 7:
            print ("Attention, si vous jouer beaucoup a se jeux, vour aurez plusieurs fois le même mot")
            print ("vous avez 7 tentative ! ")
            WORDS = ("python", "magazine", "facile", "lit", "table",  "xylophone", "musique", "armoire", "jeux", "film", "code","histoire", "carte", "pantalon", "violon","ordinateur", "souris", "dessin")
            Word = random.choice(WORDS)
            solution = Word
            tentatives = 7
            lettres_trouvees = ""
            while tentatives>0:
                print("Mot à deviner : ")
                proposition = input("proposez une lettre : ")
                if proposition in solution:
                    lettres_trouvees = lettres_trouvees + proposition
                    print("-> Bien vu!")
                    nombre_de_lettre =  len(solution)
                else:
                    tentatives = tentatives - 1
                    print("-> Nope. Il vous reste", tentatives, "tentatives")
                    print ("il vous reste", len(solution),"lettre")
            print(solution)


    else:
        phrasetext = getpass.getpass("phrase ? : ")
        solution = phrasetext
        score = len(phrasetext)
        print ("le mot contient",score, "lettre")
        tentatives = 7
        lettres_trouvees = ""
    while tentatives>0:
        print("Mot à deviner : ")
        proposition = input("proposez une lettre : ")
        if proposition in solution:
            lettres_trouvees = lettres_trouvees + proposition
            print("-> Bien vu!")
        else:
            tentatives = tentatives - 1
            print("-> Nope. Il vous reste", tentatives, "tentatives")
    