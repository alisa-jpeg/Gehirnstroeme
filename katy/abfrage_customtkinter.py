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

radio_var0 = ctk.IntVar()
radio_var1 = ctk.IntVar()
radio_var2 = ctk.IntVar()
radio_var3 = ctk.IntVar()


#App Class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toplevel_window = None
#titel fenster
        self.title("Brain-Computer-Interface-Fragebogen") 
#größe fenster auf das was zuvor festgelegt wurde
        self.geometry(f"{appWidth}x{appHeight}")

        #wenn fenster geschlossen wird, danna auch das geamte programm
        self.protocol("WM_DELETE_WINDOW", self.on_closing)




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

        self.RadioButton1 = ctk.CTkRadioButton(self, text="Innerhalb der letzten zwei Stunden", value = 1, variable = radio_var0)
        self.RadioButton1.grid(row=2, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton2 = ctk.CTkRadioButton(self, text="Innerhalb der letzten 12 Stunden", value = 2, variable = radio_var0)
        self.RadioButton2.grid(row=2, column=3, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton3 = ctk.CTkRadioButton(self, text="Vor über 12 Stunden", value = 3, variable = radio_var0)
        self.RadioButton3.grid(row=2, column=4, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton4 = ctk.CTkRadioButton(self, text="Ich trinke keinen Kaffee", value = 4, variable = radio_var0)
        self.RadioButton4.grid(row=2, column=5, columnspan=1, padx=20, pady=20, sticky="w")
#4. label
        self.label = ctk.CTkLabel(self, text="Sind Sie links- oder rechtshändig?")
        self.label.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.RadioButton5 = ctk.CTkRadioButton(self, text="Ich bin linkshändig.", value = 1, variable = radio_var1)
        self.RadioButton5.grid(row=3, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton6 = ctk.CTkRadioButton(self, text="Ich bin rechtshändig.", value = 2, variable = radio_var1)
        self.RadioButton6.grid(row=3, column=3, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton7 = ctk.CTkRadioButton(self, text="Ich bin beidhändig.", value = 3, variable = radio_var1)
        self.RadioButton7.grid(row=3, column=4, columnspan=1, padx=20, pady=20, sticky="w")

#5. label
        self.label = ctk.CTkLabel(self, text="Wie müde fühlen Sie sich gerade? (1=Adrenalinschub, 10=Schlaf)")
        self.label.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.slider = ctk.CTkSlider(self, from_=1, to=10, number_of_steps=10, command = self.slider_event)
        self.slider.grid(row=4, column=2, columnspan=2, padx=20, pady=20, sticky="ew")

        self.label = ctk.CTkLabel(self, text="1")




#6. label
        self.label = ctk.CTkLabel(self, text="Wie dicht/dick ist Ihr Haar?")
        self.label.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.RadioButton8 = ctk.CTkRadioButton(self, text="Ich habe eine Glatze.", value = 1, variable = radio_var2)
        self.RadioButton8.grid(row=5, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton9 = ctk.CTkRadioButton(self, text="Ich habe dünnes Haar.", value = 2, variable=radio_var2)
        self.RadioButton9.grid(row=5, column=3, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton10 = ctk.CTkRadioButton(self, text="Ich habe dickes Haar.", value = 3, variable=radio_var2)
        self.RadioButton10.grid(row=5, column=4, columnspan=1, padx=20, pady=20, sticky="w")


#7. label
        self.RadioButton11 = ctk.CTkRadioButton(self, text="Ihre Daten dürfen für unsere Zwecke verwendet werden.", value = 1, variable=radio_var3)
        self.RadioButton11.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky="w")

#button zum schreiben der daten in ein dokument (später zum öffnen des hauptfensters)
        self.generateResultsButton = ctk.CTkButton(self, text ="Daten speichern", command =self.abschluss)
        self.generateResultsButton.grid(row=7, column = 0, columnspan = 2, padx = 20, pady=20, sticky ="ew")

    def slider_event(self, value):
        self.label = ctk.CTkLabel(self, text=value)
        self.label.grid(row=4, column=4, columnspan=2, padx=20, pady=20, sticky="w")



    def createText(self):
        #.cget("value") gibt den wert des eingabefeldes zurück
        v0 = radio_var0.get()
        v1 = radio_var1.get()
        v2 = radio_var2.get()
        v3 = radio_var3.get()

        kaffee = ""
        if v0 == 1:
            kaffee = "Innerhalb der letzten zwei Stunden"
        elif v0 == 2:
            kaffee = "Innerhalb der letzten 12 Stunden"
        elif v0  == 3:
            kaffee = "Vor über 12 Stunden"
        elif v0 == 4:
            kaffee = "Ich trinke keinen Kaffee"
        else:
            kaffee = "Keine Angabe"

        haendigkeit = ""
        if v1 == 1:
            haendigkeit = "Ich bin linkshändig."
        elif v2 == 2:
            haendigkeit = "Ich bin rechtshändig."
        elif v1 == 3:
            haendigkeit = "Ich bin beidhändig."
        else:
            haendigkeit = "Keine Angabe"

        haar = ""
        if v2 == 1:
            haar = "Ich habe eine Glatze."
        elif v2 == 2:
            haar = "Ich habe dünnes Haar."
        elif v2 == 3:
            haar = "Ich habe dickes Haar."
        else:
            haar = "Keine Angabe"

        #text-variable füllen
        text = {"Alter": self.nameEntry.get(),
                "Kaffee getrunken": kaffee, 
                "Händigkeit": haendigkeit, 
                "Müdigkeit": self.slider.get(), 
                "Haarlänge": haar, 
                "Zeitstempel": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                "Zufallsnummer": random.randint(1000, 9999)
        }       



        if v3 != 1:
            text = {"Die Person hat den Datenschutz nicht akzeptiert."}
        

        return text
    
    def abschluss(self):
        print("wir sind im abschluss")
        dateiname = "versuchsdaten.csv"
        daten = self.createText()
        daten_speichern(dateiname, daten)
        print("Daten erfolgreich gespeichert!")
        self.open_toplevel()
    
    def open_toplevel(self):
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow(self) #Toplevelwindow-fenster erstellen wenn es noch nicht existiert
                self.toplevel_window.focus_set() #fokus auf das Toplevelwindow-fenster setzen
            else:
                self.toplevel_window.focus_set() #wenn Toplevelwindow-fenster schon da ist, fokus darauf setzen


    def on_closing(self):
        if self.toplevel_window is not None:
            self.toplevel_window.destroy()
        self.destroy()
        self.quit()


# Hauptfenster der Anwendung erstellen

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Brain-Computer-Interface-Spiel")
        self.geometry(f"{appWidth}x{appHeight}")
        self.toplevel_window = None


        #hierhin kommt der restliche code für das spiel



#initiiert die app
if __name__ == "__main__": 
    app = App()
    app.mainloop()
