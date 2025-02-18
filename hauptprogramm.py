#fenster mit knopf -- konsoleneingabe
#durchschnitt berechnen und anzeigen
#luftballon steigen, spiel beginnen
#nach ende des spiels auswertung anzeigen?

#nötige dinge importieren
import customtkinter as ctk #für graphiken 

#funktionen importieren
from durchschnitt_berechnen import calculate_average_alpha
from konsoleneingabe import konsoleneingabe
from pygame_kreis import ballon_bewegen


#beginn hauptprogramm

# Hauptfenster der Anwendung erstellen
app = ctk.CTk()
app.title("Brain-Computer-Interface mittels EEG")  # Titel des Fensters
app.geometry("400x400")  # Größe des Fensters

button = customtkinter.CTkButton(master=root_tk, text="fragebogen ausfüllen", command=konsoleneingabe)
button.grid(row= 0, column = 0, padx=20, pady=10)

button = customtkinter.CTkButton(master=root_tk, text="durchschnittliches Alpha berechnen", command=calculate_average_alpha)
button.grid(row = 0, column = 25, padx=20, pady=10)

button = customtkinter.CTkButton(master=root_tk, text="spiel beginnen", command=steigen)
button.grid(row = 0, column = 50, padx=20, pady=10)
