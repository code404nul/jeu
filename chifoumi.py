import random
import time

score_pers = 0
score_machine = 0
boucle = 1
while boucle == 1:
    list = ["papier","scissors","pierre"]
    Word = random.choice(list)

    print ("pierre")
    time.sleep(1)
    print ("feuille")
    time.sleep(1)
    print ("scissors")
    time.sleep(1)
    print (" ")
    print ("j'ai deviné", Word)
    demande_score = input ("es-que j'ai gagné ? Y / n ou egalité = e : ")

    if demande_score == "Y":
        print ("cool")
        score_machine = score_machine + 1
        print ("votre score est de" + str (score_pers))
        print ("mon score est de" + str(score_machine))
        
    elif demande_score == "n":
        print ("ho, non")
        score_pers = score_pers + 1
        print ("votre score est de" + str (score_pers))
        print ("mon score est de" + str(score_machine))
    elif demande_score == "e":
        print ("ok...")
        score_pers + 1
        score_machine + 1
        print ("votre score est de" + str (score_pers))
        print ("mon score est de" + str(score_machine))
