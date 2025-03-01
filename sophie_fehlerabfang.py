import customtkinter as ctk
import csv
from datetime import datetime
import tkinter.messagebox as msgbox

# Funktion zum Speichern der Daten in einer CSV-Datei
def daten_speichern(dateiname, daten):
    with open(dateiname, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=daten.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(daten)

# Setze das Standardfarbschema auf "grün"
ctk.set_default_color_theme("green")
# Setze das Erscheinungsbild des Fensters auf "dunkel"
ctk.set_appearance_mode("Dark")

# Definiere die Fenstergröße
appWidth, appHeight = 2000, 600

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Brain-Computer-Interface-Fragebogen")
        self.geometry(f"{appWidth}x{appHeight}")

        # Initialisieren der Flagge für "Daten nicht speichern"
        self.show_only_flag = False

        # Label zur Anweisung
        self.label = ctk.CTkLabel(self, text="Bitte füllen Sie vor Beginn der Messungen diesen Fragebogen aus, damit wir Ihre Daten auswerten können (immer nur ein Kreuz setzen):")
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Frage nach dem Alter
        self.label = ctk.CTkLabel(self, text="Was ist Ihr Alter?")
        self.label.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.nameEntry = ctk.CTkEntry(self)
        self.nameEntry.grid(row=1, column=2, columnspan=2, padx=20, pady=20, sticky="ew")

        # Frage nach dem Kaffeekonsum
        self.label = ctk.CTkLabel(self, text="Wann haben Sie das letzte mal Kaffee getrunken?")
        self.label.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        # RadioButtons für Kaffeekonsum
        self.RadioButton1 = ctk.CTkRadioButton(self, text="Innerhalb der letzten zwei Stunden", value=1)
        self.RadioButton1.grid(row=2, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton2 = ctk.CTkRadioButton(self, text="Innerhalb der letzten 12 Stunden", value=1)
        self.RadioButton2.grid(row=2, column=3, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton3 = ctk.CTkRadioButton(self, text="Vor über 12 Stunden", value=1)
        self.RadioButton3.grid(row=2, column=4, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton4 = ctk.CTkRadioButton(self, text="Ich trinke keinen Kaffee", value=1)
        self.RadioButton4.grid(row=2, column=5, columnspan=1, padx=20, pady=20, sticky="w")

        # Frage zur Händigkeit
        self.label = ctk.CTkLabel(self, text="Sind Sie links- oder rechtshändig?")
        self.label.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.RadioButton5 = ctk.CTkRadioButton(self, text="Ich bin linkshändig.", value=1)
        self.RadioButton5.grid(row=3, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton6 = ctk.CTkRadioButton(self, text="Ich bin rechtshändig.", value=1)
        self.RadioButton6.grid(row=3, column=3, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton7 = ctk.CTkRadioButton(self, text="Ich bin beidhändig.", value=1)
        self.RadioButton7.grid(row=3, column=4, columnspan=1, padx=20, pady=20, sticky="w")

        # Frage zur Müdigkeit
        self.label = ctk.CTkLabel(self, text="Wie müde fühlen Sie sich gerade? (1=Adrenalinschub, 10=Schlaf)")
        self.label.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.slider = ctk.CTkSlider(self, from_=1, to=10, number_of_steps=10)
        self.slider.grid(row=4, column=2, columnspan=2, padx=20, pady=20, sticky="ew")

        # Frage zum Haartyp
        self.label = ctk.CTkLabel(self, text="Wie dicht/dick ist Ihr Haar?")
        self.label.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.RadioButton8 = ctk.CTkRadioButton(self, text="Ich habe eine Glatze.", value=1)
        self.RadioButton8.grid(row=5, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton9 = ctk.CTkRadioButton(self, text="Ich habe dünnes Haar.", value=1)
        self.RadioButton9.grid(row=5, column=3, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton10 = ctk.CTkRadioButton(self, text="Ich habe dickes Haar.", value=1)
        self.RadioButton10.grid(row=5, column=4, columnspan=1, padx=20, pady=20, sticky="w")

        # RadioButton für Datenschutz-Zustimmung
        self.RadioButton11 = ctk.CTkRadioButton(self, text="Ihre Daten dürfen für unsere Zwecke verwendet werden.", value=1)
        self.RadioButton11.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        # Button zum Speichern der Daten
        self.generateResultsButton = ctk.CTkButton(self, text="Daten speichern", command=self.abschluss)
        self.generateResultsButton.grid(row=7, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Button für die Option keine Daten zu speichern (nur Anschauungszwecke)
        self.showOnlyButton = ctk.CTkButton(self, text="Daten nicht speichern (nur zu Anschauungszwecken)", command=self.show_only)
        self.showOnlyButton.grid(row=7, column=2, columnspan=2, padx=20, pady=20, sticky="ew")

    # Validierung der Benutzereingaben
    def validate_inputs(self):
        # Wenn der Benutzer "Daten nicht speichern" gewählt hat, keine Validierung erforderlich
        if self.show_only_flag:
            return True

        try:
            alter = int(self.nameEntry.get())
            if alter < 1 or alter > 120:
                raise ValueError
        except ValueError:
            msgbox.showerror("Fehler", "Bitte geben Sie ein gültiges Alter zwischen 1 und 120 ein.")
            return False

        if not (self.RadioButton1.get() or self.RadioButton2.get() or self.RadioButton3.get() or self.RadioButton4.get()):
            msgbox.showerror("Fehler", "Bitte wählen Sie eine Option für den Kaffeekonsum.")
            return False

        if not (self.RadioButton5.get() or self.RadioButton6.get() or self.RadioButton7.get()):
            msgbox.showerror("Fehler", "Bitte wählen Sie eine Option für Ihre Händigkeit.")
            return False

        if not (self.RadioButton8.get() or self.RadioButton9.get() or self.RadioButton10.get()):
            msgbox.showerror("Fehler", "Bitte wählen Sie eine Option für Ihren Haartyp.")
            return False

        if not self.RadioButton11.get():
            msgbox.showerror("Fehler", "Bitte stimmen Sie der Nutzung Ihrer Daten zu.")
            return False

        return True

    # Erstelle den Text für die Speicherung basierend auf den Eingaben
    def createText(self):
        kaffee = ""
        if self.RadioButton1.get() == 1:
            kaffee = "Innerhalb der letzten zwei Stunden"
        elif self.RadioButton2.get() == 1:
            kaffee = "Innerhalb der letzten 12 Stunden"
        elif self.RadioButton3.get() == 1:
            kaffee = "Vor über 12 Stunden"
        elif self.RadioButton4.get() == 1:
            kaffee = "Ich trinke keinen Kaffee"

        haendigkeit = ""
        if self.RadioButton5.get() == 1:
            haendigkeit = "Ich bin linkshändig."
        elif self.RadioButton6.get() == 1:
            haendigkeit = "Ich bin rechtshändig."
        elif self.RadioButton7.get() == 1:
            haendigkeit = "Ich bin beidhändig."

        haar = ""
        if self.RadioButton8.get() == 1:
            haar = "Ich habe eine Glatze."
        elif self.RadioButton9.get() == 1:
            haar = "Ich habe dünnes Haar."
        elif self.RadioButton10.get() == 1:
            haar = "Ich habe dickes Haar."

        alter = self.nameEntry.get()
        muede = self.slider.get()
        daten = {
            "Alter": alter,
            "Kaffee": kaffee,
            "Händigkeit": haendigkeit,
            "Müdigkeit": muede,
            "Haartyp": haar,
            "Daten Nutzung": "Ja" if self.RadioButton11.get() else "Nein",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return daten

    # Wenn die Daten gespeichert werden sollen
    def abschluss(self):
        if not self.validate_inputs:
            return 
        daten = self.createText()
        dateiname = "fragebogen_daten.csv"
        daten_speichern(dateiname, daten)
        msgbox.showinfo("Erfolg", "Die Daten wurden erfolgreich gespeichert.")

    # Wenn der Benutzer nur zu Anschauungszwecken arbeitet (keine Speicherung)
    def show_only(self):
        self.show_only_flag = True
        msgbox.showinfo("Nur zur Ansicht", "Keine Daten werden gespeichert. Dies dient nur der Anschauung.")
        self.show_only_flag = False

# Starten der Anwendung
if __name__ == "__main__":
    app = App()
    app.mainloop()

    



