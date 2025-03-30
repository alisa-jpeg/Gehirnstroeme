#fenster mit knopf -- konsoleneingabe
#durchschnitt berechnen und anzeigen
#luftballon steigen, spiel beginnen
#nach ende des spiels auswertung anzeigen?

#nötige dinge importieren
import customtkinter as ctk #für graphiken 

#funktionen importieren
from alt_nutzlos.durchschnitt_berechnen import calculate_average_alpha
from alt_nutzlos.konsoleneingabe import konsoleneingabe
from alt_nutzlos.pygame_kreis import ballon_bewegen


#beginn hauptprogramm

# Hauptfenster der Anwendung erstellen

#farbe der widgets (green, dark-blue, blue)
ctk.set_default_color_theme("green")

#farbe des fensters (Light, Dark, System)
ctk.set_appearance_mode("Dark") 

#größe fenster
appWidth, appHeight = 800, 600

#App Class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#titel fenster
        self.title("Brain-Computer-Interface") 
#größe fenster auf das was zuvor festgelegt wurde
        self.geometry(f"{appWidth}x{appHeight}")
#erstellt button1
        self.generateResultsButton = ctk.CTkButton(self, text = "Durchschnitt berechnen", command = self.alpha_anzeigen) 
        self.generateResultsButton.grid(row=1, column = 1, columnspan = 2, padx = 20, pady=20, sticky ="ew")

#erstellt text box 1 um average_alpha anzuzeigen
        self.displayBox = ctk.CTkTextbox(self, width=300, height=25)
        self.displayBox.grid(row=1, column=4, columnspan=2, padx=20, pady=20, sticky="nsew")

#erstellt text box 2 um endergebnis anzuzeigen
        self.displayBox = ctk.CTkTextbox(self, width=300, height=25)
        self.displayBox.grid(row=3, column=4, columnspan=2, padx=20, pady=20, sticky="nsew")


#erstellt button2
        self.generateResultsButton = ctk.CTkButton(self, text = "Spiel beginnen", command = self.spiel_beginnen)
        self.generateResultsButton.grid(row=3, column = 1, columnspan = 2, padx = 20, pady=20, sticky ="ew")

    def alpha_anzeigen(self):
        self.displayBox.delete("0.0", "200.0")
        text = calculate_average_alpha()
        self.displayBox.insert("0.0", text)
        alpha_average = text

    def spiel_beginnen(self):
        self.displayBox.delete("0.0", "200.0")
        text = "super, du hast es geschafft!" #je nachdem, wie es ging
        self.displayBox.insert("0.0", text)




#initiiert die app
if __name__ == "__main__": 
    app = App()
    app.mainloop()
