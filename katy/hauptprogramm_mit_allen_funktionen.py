#fenster mit knopf -- konsoleneingabe
#durchschnitt berechnen und anzeigen
#luftballon steigen, spiel beginnen
#nach ende des spiels auswertung anzeigen?

#nötige dinge importieren
import customtkinter as ctk #für graphiken 
import threading
import json
import socket
import time
import pygame

HOST = '127.0.0.1'  # Die IP-Adresse des lokalen Hosts, auf dem das Programm lauscht
PORT = 12345        # Der Port, auf dem Daten empfangen werden sollen
BUFFER_SIZE = 1024  # Die maximale Größe eines UDP-Datenpakets in Bytes
DURATION = 2        # Die Dauer (in Sekunden), für die Daten empfangen werden
MAX_PACKETS = 1000  # Die maximale Anzahl von Paketen, die verarbeitet werden

erfolg = ""




# Funktion zur Berechnung des Durchschnitts der Alpha-Werte
def calculate_average_alpha():
    # Erstelle einen UDP-Socket, um Daten zu empfangen
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Binden des Sockets an die konfigurierte IP-Adresse und den Port
    udp_socket.bind((HOST, PORT))

    # Liste zum Speichern der empfangenen Alpha-Werte
    alpha_values = []

    # Startzeit, um die Empfangsdauer zu überwachen
    start_time = time.time()
  
    while time.time() - start_time < DURATION and len(alpha_values) < MAX_PACKETS:
        try:
            # Empfang eines Datenpakets
            data, _ = udp_socket.recvfrom(BUFFER_SIZE)
            message = json.loads(data.decode('utf-8'))
            alpha_values.append(message["data"][2])

            # Prüfe, ob "data" vorhanden ist und genügend Elemente enthält
            if "data" in message and isinstance(message["data"], list) and len(message["data"]) > 2:
                alpha_values.append(message["data"][2])
            else:
                print("Ungültiges Paket erhalten:", message)

        except json.JSONDecodeError:
            print("Fehler beim Dekodieren des JSON-Pakets.")
        except Exception as e:
            print(f"Unerwarteter Fehler: {e}")

            # Schließen des UDP-Socket, da er nicht mehr benötigt wird
    udp_socket.close()


    # Berechnen des Durchschnitts der Alpha-Werte und gib ihn zurück
    # Falls keine Werte empfangen wurden, gib 0 zurück
    return sum(alpha_values) / len(alpha_values) if alpha_values else 0






def ballon_bewegen(): 
        # hier pygame_kreis einfügen und erfolg je nach ausgang umsetzen

        return erfolg
        


#beginn hauptprogramm

# Hauptfenster der Anwendung erstellen

#farbe der widgets (green, dark-blue, blue)
ctk.set_default_color_theme("green")

#farbe des fensters (Light, Dark, System)
ctk.set_appearance_mode("Dark") 

#größe fenster
appWidth, appHeight = 1200, 200

#App Class
class App(ctk.CTk):
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
        #titel fenster
                self.title("Brain-Computer-Interface") 
        #größe fenster auf das was zuvor festgelegt wurde
                self.geometry(f"{appWidth}x{appHeight}")
        #erstellt button1
                self.generateResultsButton = ctk.CTkButton(self, text = "Durchschnitt berechnen", command = self.durchschnitt_berechnen) 
                self.generateResultsButton.grid(row=1, column = 1, columnspan = 2, padx = 20, pady=20, sticky ="w")

        #erstellt text box 1 um average_alpha anzuzeigen
                self.displayBox1 = ctk.CTkTextbox(self, width=300, height=25)
                self.displayBox1.grid(row=1, column=4, columnspan=2, padx=20, pady=20, sticky="s")

        #erstellt text box 2 um endergebnis anzuzeigen
                self.displayBox2 = ctk.CTkTextbox(self, width=300, height=25)
                self.displayBox2.grid(row=3, column=4, columnspan=2, padx=20, pady=20, sticky="s")


        #erstellt button2
                self.generateResultsButton = ctk.CTkButton(self, text = "Spiel beginnen", command = self.spiel_beginnen)
                self.generateResultsButton.grid(row=3, column = 1, columnspan = 2, padx = 20, pady=20, sticky ="w")

        #erstellt textfeld, damit man sieht ob udp-stream läuft
                self.displayBox3 = ctk.CTkTextbox(self, width=500, height=25)
                self.displayBox3.grid(row=1, column=6, columnspan=2, padx=20, pady=20, sticky="w")
                self.displayBox3.insert("0.0", "UDP-Stream nicht gestartet - Bitte lassen Sie den Durchschnitt berechnen")

        def durchschnitt_berechnen(self):
                self.displayBox3.delete("0.0", "200.0")
                self.displayBox3.insert("0.0", "UDP-Stream läuft - Bitte warten Sie einen Moment")
                threading.Thread(target=self.alpha_anzeigen).start()

        def alpha_anzeigen(self):
                text = calculate_average_alpha()
                self.displayBox1.delete("0.0", "200.0")
                self.displayBox1.insert("0.0", text)
                self.displayBox3.delete("0.0", "200.0")
                self.displayBox3.insert("0.0", "UDP-Stream ist abgeschlossen - Das Spiel kann beginnen!")
                alpha_average = text


        def spiel_beginnen(self):
                self.displayBox2.delete("0.0", "200.0")
                text = erfolg
                self.displayBox2.insert("0.0", text)




#initiiert die app
if __name__ == "__main__": 
    app = App()
    app.mainloop()