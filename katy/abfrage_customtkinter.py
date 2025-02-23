#zeitpunkt, zufällige nummer und daten in pdf datei schreiben
#nur ein kreuz möglich machen
#bei slider zahl anzeigen

#nötige dinge importieren
import customtkinter as ctk #für graphiken 
import csv 
from datetime import datetime
import random

root = ctk.CTk()


def daten_speichern(dateiname, daten):
    with open(dateiname, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=daten.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(daten)
    

#farbe der widgets (green, dark-blue, blue)
ctk.set_default_color_theme("green")

#farbe des fensters (Light, Dark, System)
ctk.set_appearance_mode("Dark") 

#größe fenster
appWidth, appHeight = 2000, 600

#App Class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#titel fenster
        self.title("Brain-Computer-Interface-Fragebogen") 
#größe fenster auf das was zuvor festgelegt wurde
        self.geometry(f"{appWidth}x{appHeight}")

#erstes label-überschrift
        self.label = ctk.CTkLabel(self, text="Bitte füllen Sie vor Beginn der Messungen diesen Fragebogen aus, damit wir Ihre Daten auswerten können (immer nur ein Kreuz setzen):")
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

#alter
        self.label = ctk.CTkLabel(self, text="Was ist Ihr Alter?")
        self.label.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.nameEntry = ctk.CTkEntry(self)
        self.nameEntry.grid(row=1, column=2, columnspan=2, padx=20, pady=20, sticky="ew")   

#3. label
        self.label = ctk.CTkLabel(self, text="Wann haben Sie das letzte mal Kaffee getrunken?")
        self.label.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.RadioButton1 = ctk.CTkRadioButton(self, text="Innerhalb der letzten zwei Stunden", value = 1)
        self.RadioButton1.grid(row=2, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton2 = ctk.CTkRadioButton(self, text="Innerhalb der letzten 12 Stunden", value = 1)
        self.RadioButton2.grid(row=2, column=3, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton3 = ctk.CTkRadioButton(self, text="Vor über 12 Stunden", value = 1)
        self.RadioButton3.grid(row=2, column=4, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton4 = ctk.CTkRadioButton(self, text="Ich trinke keinen Kaffee", value = 1)
        self.RadioButton4.grid(row=2, column=5, columnspan=1, padx=20, pady=20, sticky="w")
#4. label
        self.label = ctk.CTkLabel(self, text="Sind Sie links- oder rechtshändig?")
        self.label.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.RadioButton5 = ctk.CTkRadioButton(self, text="Ich bin linkshändig.", value = 1)
        self.RadioButton5.grid(row=3, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton6 = ctk.CTkRadioButton(self, text="Ich bin rechtshändig.", value = 1)
        self.RadioButton6.grid(row=3, column=3, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton7 = ctk.CTkRadioButton(self, text="Ich bin beidhändig.", value = 1)
        self.RadioButton7.grid(row=3, column=4, columnspan=1, padx=20, pady=20, sticky="w")

#5. label
        self.label = ctk.CTkLabel(self, text="Wie müde fühlen Sie sich gerade? (1=Adrenalinschub, 10=Schlaf)")
        self.label.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.slider = ctk.CTkSlider(self, from_=1, to=10, number_of_steps=10)
        self.slider.grid(row=4, column=2, columnspan=2, padx=20, pady=20, sticky="ew")

#6. label
        self.label = ctk.CTkLabel(self, text="Wie dicht/dick ist Ihr Haar?")
        self.label.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.RadioButton8 = ctk.CTkRadioButton(self, text="Ich habe eine Glatze.", value = 1)
        self.RadioButton8.grid(row=5, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton9 = ctk.CTkRadioButton(self, text="Ich habe dünnes Haar.", value = 1)
        self.RadioButton9.grid(row=5, column=3, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton10 = ctk.CTkRadioButton(self, text="Ich habe dickes Haar.", value = 1)
        self.RadioButton10.grid(row=5, column=4, columnspan=1, padx=20, pady=20, sticky="w")


#7. label
        self.RadioButton11 = ctk.CTkRadioButton(self, text="Ihre Daten dürfen für unsere Zwecke verwendet werden.", value = 1)
        self.RadioButton11.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky="w")

#button zum schreiben der daten in ein dokument (später zum öffnen des hauptfensters)
        self.generateResultsButton = ctk.CTkButton(self, text ="Daten speichern", command = self.abschluss)
        self.generateResultsButton.grid(row=7, column = 0, columnspan = 2, padx = 20, pady=20, sticky ="ew")


    def createText(self):
        #.cget("value") gibt den wert des eingabefeldes zurück

        kaffee = ""
        foo = self.RadioButton1.cget("value")
        if self.RadioButton1.cget("value") == 1:
            kaffee = "Innerhalb der letzten zwei Stunden"
        elif self.RadioButton2.cget("value") == 1:
            kaffee = "Innerhalb der letzten 12 Stunden"
        elif self.RadioButton3.cget("value") == 1:
            kaffee = "Vor über 12 Stunden"
        elif self.RadioButton4.cget("value") == 1:
            kaffee = "Ich trinke keinen Kaffee"
        else:
            kaffee = "Keine Angabe"

        haendigkeit = ""
        if self.RadioButton5.cget("value") == 1:
            haendigkeit = "Ich bin linkshändig."
        elif self.RadioButton6.cget("value") == 1:
            haendigkeit = "Ich bin rechtshändig."
        elif self.RadioButton7.cget("value") == 1:
            haendigkeit = "Ich bin beidhändig."
        else:
            haendigkeit = "Keine Angabe"

        haar = ""
        if self.RadioButton8.cget("value") == 1:
            haar = "Ich habe eine Glatze."
        elif self.RadioButton9.cget("value") == 1:
            haar = "Ich habe dünnes Haar."
        elif self.RadioButton10.cget("value") == 1:
            haar = "Ich habe dickes Haar."
        else:
            haar = "Keine Angabe"

        #text-variable füllen
        text = {"Alter": self.nameEntry.cget("value"),
                "Kaffee getrunken": kaffee, 
                "Händigkeit": haendigkeit, 
                "Müdigkeit": self.slider.cget("value"), 
                "Haarlänge": haar, 
                "Zeitstempel": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                "Zufallsnummer": random.randint(1000, 9999)
        }       



        if self.RadioButton11.cget("value") == 0:
            text = {"Die Person hat den Datenschutz nicht akzeptiert."}
        

        return text
    
    def abschluss(self):
        print("wir sind im abschluss")
        dateiname = "versuchsdaten.csv"
        daten = self.createText()
        daten_speichern(dateiname, daten)
        print("Daten erfolgreich gespeichert!")
        root.destroy()

# Hauptfenster der Anwendung erstellen



#initiiert die app
if __name__ == "__main__": 
    app = App()
    app.mainloop()

