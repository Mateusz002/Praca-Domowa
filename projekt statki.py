# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 20:04:11 2021

@author: matim
"""

import random
class Plansza(object):
    
    def __init__(self, statki, szerokosc, wysokosc):
        self.statki = statki
        self.strzaly = []
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc 
        
    def strzal(self, koordynaty):
        trafionySt = None
        trafienie = False
        for s in self.statki:
            idx = s.budowaIndex(koordynaty)
            if idx is not None:
                trafienie = True
                s.trafienia[idx] = True
                trafionySt = s
                break

        self.strzaly.append(Strzal(koordynaty, trafienie))     
        return trafionySt
   
    def wygrana(self):
       return all([s.zniszczony() for s in self.statki])
        # for s in self.statki:
        #     if s.zniszczony():
        #         return False
        # return True
    
class Strzal(object):
    
    def __init__(self, pole, trafienie):
        self.pole = pole
        self.trafienie = trafienie

class Statki(object):
    
    @staticmethod
    def budowa(pozycja, wielkosc, kierunek):
        rodzajStat = []
        for w in range(wielkosc):
            if kierunek == "P":
                st = (pozycja[0], pozycja[1] - w)
            elif kierunek == "Po":
                st = (pozycja[0], pozycja[1] + w)
            elif kierunek == "W":
                st = (pozycja[0] + w, pozycja[1])
            elif kierunek == "Z":
                st = (pozycja[0] - w, pozycja[1])
            
            rodzajStat.append(st)        
        return Statki(rodzajStat) 
    
    def __init__(self, rodzajStat):
        self.rodzajStat = rodzajStat 
        self.trafienia = [False] * len(rodzajStat)

    def budowaIndex(self, pole):
        try:
            return self.rodzajStat.index(pole)
        except ValueError:
            None
    
    def zniszczony(self):
        return all(self.trafienia)
    
class Gracz(object):

    def __init__(self, imie, wystrzal):  
        self.imie = imie
        self.wystrzal = wystrzal 
    
def plansza(menu, pokazStatki = False):
    
    granica = "+" + "*" * menu.szerokosc + "+"
    print(granica)
    
    plansza = []
    for y in range(menu.wysokosc):
        plansza.append([None for x in range(menu.szerokosc)])
    
    
    # for s in menu.statki:
    #     for x, y in s.rodzajStat:
    #         plansza[x][y] = "S"
 
    for st in menu.strzaly:
        x, y = st.pole
        if st.trafienie:
            ch = "X"
        else:
            ch = "O"
        plansza[x][y] = ch
            
    for y in range(menu.wysokosc):
        wiersz = []
        for x in range(menu.szerokosc):
            wiersz.append(plansza[x][y] or "-")
        print("|" + "".join(wiersz) + "|")
        
    print(granica)

def komunikaty(wydarzenie, tekst = {}):
    if wydarzenie == "koniecGry":
        print("%s Wygrales!!" % tekst["gracz"])
    elif wydarzenie == "nowaRunda":
        print("Twoja runda %s" % tekst["gracz"])
        
    if wydarzenie == "pudlo":
        print("Pudlo!!")
    elif wydarzenie == "trafiony":
        print("Trafiony!!")
    elif wydarzenie == "zniszczony":
        print("Trafiony, zatopiony!!")
    
    if wydarzenie == "poczatek":
        print("%s Gdzie chcesz strzelic?" % tekst["gracz"])
        
def komunikatyEng(wydarzenie, tekst = {}):
    if wydarzenie == "koniecGry":
        print("%s You Win!!" % tekst["gracz"])
    elif wydarzenie == "nowaRunda":
        print("Your Turn %s" % tekst["gracz"])
        
    if wydarzenie == "pudlo":
        print("Miss!!")
    elif wydarzenie == "trafiony":
        print("Hit!!")
    elif wydarzenie == "zniszczony":
        print("Hit and Sunken!!")

def ruchAI(koordynaty):
    x = random.randint(0, koordynaty.szerokosc - 1)
    y = random.randint(0, koordynaty.wysokosc - 1)
    return (x,y)

def ruchCzlowiek(koordynaty):
    while True:
        inp = input(komunikaty("poczatek", {"gracz": ruchCzlowiek.imie}))
        xstr, ystr = inp.split(",") 
        if int(xstr) <= koordynaty.szerokosc and int(ystr) <= koordynaty.wysokosc:
            break
    x = int(xstr)
    y = int(ystr)
    return  (x,y)
   
        
if __name__ == "__main__":
      
    statki = [
        Statki.budowa((1,1), 2, "Po"),
        Statki.budowa((5,8), 5, "W"),
    ]
    
    statki2 = [
        Statki.budowa((4,3), 2, "Po"),
        Statki.budowa((7,2), 5, "Z"),
    ]
    
    mapy = [
        Plansza(statki,10,10),
        Plansza(statki2,10,10)
        ]
    
    
    gracze = [
        Gracz("Mateusz", ruchCzlowiek),
        Gracz("komputer", ruchAI)
        ]
    
    atakujacy = 0
    while True:
        broniacy = (atakujacy + 1) % 2
        
        broniacyMapa = mapy[broniacy]
        ruchCzlowiek = gracze[atakujacy]
        
        komunikatyEng("nowaRunda", {"gracz": ruchCzlowiek.imie})
        koordynaty = ruchCzlowiek.wystrzal(broniacyMapa)
        trafionySt = broniacyMapa.strzal(koordynaty)
        if trafionySt is None:
            komunikatyEng("pudlo", {"gracz": ruchCzlowiek.imie})
        else:
            if trafionySt.zniszczony():
                komunikatyEng("zniszczony", {"gracz": ruchCzlowiek.imie})
            else:
                komunikatyEng("trafiony", {"gracz": ruchCzlowiek.imie})
        plansza(broniacyMapa)
        
        if broniacyMapa.wygrana():
            komunikatyEng("koniecGry", {"gracz": ruchCzlowiek.imie})
            break
        atakujacy = broniacy
    
    
    
    
    
    
    
    
    
