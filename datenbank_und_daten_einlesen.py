#datenbank für fragen am anfang

import sqlite3  # Modul zum Arbeiten mit SQLite-Datenbanken
import customtkinter as ctk  # Modul für erweiterte Tkinter-GUIs

# Verbindung zur SQLite-Datenbank herstellen 
conn = sqlite3.connect("personen_daten.db")
cursor = conn.cursor()

# Erstellen der Tabelle 'personen'
cursor.execute('''
CREATE TABLE IF NOT EXISTS personen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  # Eindeutige ID für jede Person
    name TEXT NOT NULL,                    # Name der Person
    alter INTEGER NOT NULL,                # Alter der Person
    stress_level INTEGER NOT NULL,         # Stresslevel der Person (1-10)
    schlaf_stunden REAL NOT NULL           # Anzahl der Schlafstunden
)
''')
conn.commit()  # Änderungen an der Datenbank speichern

# Funktion zum Hinzufügen von Daten in die Datenbank
def daten_hinzufuegen():
    # Werte aus den Eingabefeldern abrufen
    name = name_entry.get()
    alter = alter_entry.get()
    stress_level = stress_level_entry.get()
    schlaf_stunden = schlaf_stunden_entry.get()

    # Überprüfen, ob alle Felder ausgefüllt sind
    if name and alter and stress_level and schlaf_stunden:
        try:
            # Einfügen der Daten in die Tabelle 'personen'
            cursor.execute(
                "INSERT INTO personen (name, alter, stress_level, schlaf_stunden) VALUES (?, ?, ?, ?)",
                (name, int(alter), int(stress_level), float(schlaf_stunden))
            )
            conn.commit()  # Änderungen speichern
            # Erfolgsnachricht anzeigen
            ausgabe_label.configure(text="Daten erfolgreich hinzugefügt!", text_color="blue")
        except Exception as e:
            # Fehlermeldung anzeigen, falls ein Fehler auftritt
            ausgabe_label.configure(text=f"Fehler: {e}", text_color="red")
    else:
        # Warnung anzeigen, wenn nicht alle Felder ausgefüllt sind
        ausgabe_label.configure(text="Bitte alle Felder ausfüllen!", text_color="red")

# Hauptfenster der Anwendung erstellen
app = ctk.CTk()
app.title("Datenbank-Eingabe")  # Titel des Fensters
app.geometry("400x400")  # Größe des Fensters

# Label und Eingabefeld für den Namen
ctk.CTkLabel(app, text="Name:").pack(pady=5)
name_entry = ctk.CTkEntry(app, placeholder_text="Name Eingabe")
name_entry.pack(pady=5)

# Label und Eingabefeld für das Alter
ctk.CTkLabel(app, text="Alter:").pack(pady=5)
alter_entry = ctk.CTkEntry(app, placeholder_text="Alter Eingabe")
alter_entry.pack(pady=5)

# Label und Eingabefeld für den Stresslevel
ctk.CTkLabel(app, text="Stress Level (1-10):").pack(pady=5)
stress_level_entry = ctk.CTkEntry(app, placeholder_text="Stress Level Eingabe")
stress_level_entry.pack(pady=5)

# Label und Eingabefeld für die Schlafstunden
ctk.CTkLabel(app, text="Schlaf Stunden:").pack(pady=5)
schlaf_stunden_entry = ctk.CTkEntry(app, placeholder_text="Schlaf in Stunden Eingabe")
schlaf_stunden_entry.pack(pady=5)

# Button zum Hinzufügen der Daten
hinzufuegen_button = ctk.CTkButton(app, text="Daten hinzufügen", command=daten_hinzufuegen)
hinzufuegen_button.pack(pady=20)

# Label für Ausgaben (Erfolgs- oder Fehlermeldungen)
ausgabe_label = ctk.CTkLabel(app, text="")
ausgabe_label.pack(pady=5)

# Hauptschleife der Anwendung starten
app.mainloop()

# Verbindung zur Datenbank schließen, wenn die Anwendung beendet wird
conn.close()
