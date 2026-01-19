#vraag 1: Bereken hoeveel 1 koekje heeft aan cal, vet, kol & eiw aan de hand van de voedingswaarden
#vraag 2: Maak een gebruiker input hoeveel koekjes iemand heeft gegegeten (Gebruik integer)
#vraag 3: Bereken hoeveel calorien etc, heeft verbruikt aan de hand van input van koekjes en geef dat aan de gebruiker weer (gebruik een float)
#vraag 4: Waarschuw de gebruiker als die 750 calorieen overschrijdt, en meldt dat die moet stoppen met het eten van deze "verdomd heerlijke koekjes"

#vraag 1: Het zijn de voedingswaarden voor 2 koekjes, je moet ze dus door twee gaan delen, en dit printen
#vraag 2: Maak een vraag hoeveel koekjes iemand gegeten heeft, string gebruiken voor de vraag, plus een input voor hoeveel koekjes
#vraag 3: De integer input moet de hoeveelheid calo etc vermenigvuldigen, gebruik hierbij een list met floats
#vraag 4: Gebruik een if statement met groter dan, waar je twee verschillende prints van strings gebruikt


#Vraag1: Er wordt naar 1 koekje gevraagd, daarom eerst de waardes delen door 2
print("start test")
cal2 = int(210)
vet2 = float(10.5)
kol2 = int(27)
eiw2 = int(2)

cal = (cal2 / 2)
vet = (vet2 / 2)
kol = (kol2 / 2)
eiw = (eiw2 / 2)

#Vraag2: Hier maak in een mogelijkheid voor de gebruiker om aan te geven hoeveel koekjes diegene heeft gegeten
aantal_koekjes = int(input("Hoeveel koekjes heb je gegeten?"))

#Vraag 3: Voor deze vraag moest ik de int van aantal koekjes gebruiken om de waarden te berekenen, vervolgens heb ik strings + totals gebruikt om te printen wat de gebruiker binnenkrijgt
total_cal = (cal * aantal_koekjes)
total_vet = (vet * aantal_koekjes)
total_kol = (kol * aantal_koekjes)
total_eiw = (eiw * aantal_koekjes)

print("Je hebt", total_cal, "kcal,", total_vet, "g vet,", total_kol, "g koolhydraten", total_eiw, "g eiwit binnengekregen.")

#Toen ik dit probeerde de draaien, kwam er niks uit de console, ik heb via chatgpt de run format naar dedicated console veranderd, en dat werkte
#Toen ik dit testte realiseerde ik me dat Spyder automatisch floats heeft gemaakt van de integers van de drie voedingswaarden (vet was al een float)

#Vraag 4: Het opzetten van de if/else statement was vrij snel te bedenken, belangrijk dat de syntax goed ging

if total_cal > 750:
    print("Stop met het eten van deze verdomd heerlijke koekjes!")
else: 
    print("Neem er anders nog een!")



