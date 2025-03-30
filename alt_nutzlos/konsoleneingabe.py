
import csv 
from datetime import datetime
import random
    
def fragebogen():
    print("Geben Sie daten ein.")
    daten = {
        "Alter": input("Alter: "),
        "Kaffee getrunken": input("Kaffee getrunken? (ja/nein): "),
        "Händigkeit": input("Links-, Rechts-, Beidhändig?: "),
        "Müdigkeit (0-10)": input("Wie müde fühlst du dich (0-10)?: "),
        "Haarlänge": input("Lange oder kurze Haare?: "),
        "Lautstärkeempfinden": input("Lautstärke?: "),
        "Datenschutz akzeptiert": input("Datenschutz akzeptiert? (ja/nein): "),
        "Zeitstempel": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Zufallsnummer": random.randint(1000, 9999)  # Zufällige Nummer zwischen 1000 und 9999
    }
    return daten
    
def daten_speichern(dateiname, daten):
    with open(dateiname, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=daten.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(daten)
    
def main():
    print("wir sind im main")
    dateiname = "versuchsdaten.csv"
    daten = fragebogen()
    daten_speichern(dateiname, daten)
    print("Daten erfolgreich gespeichert!")
    
if __name__ == "__main__":
    main()
