#fenster mit knopf -- konsoleneingabe
#durchschnitt berechnen und anzeigen
#luftballon steigen, spiel beginnen
#nach ende des spiels auswertung anzeigen?

#nötige dinge importieren
import customtkinter as ctk #für graphiken 

import json
import socket
import time
import pygame

HOST = '127.0.0.1'  # Die IP-Adresse des lokalen Hosts, auf dem das Programm lauscht
PORT = 12345        # Der Port, auf dem Daten empfangen werden sollen
BUFFER_SIZE = 1024  # Die maximale Größe eines UDP-Datenpakets in Bytes
DURATION = 10      # Die Dauer (in Sekunden), für die Daten empfangen werden
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






def ballon_bewegen():	#base y mus definiert werden + udp stream muss noch gestrartet werden --> im moment noch kein alpha_values verfügbar
        pygame.init()
        background = pygame.image.load("Hintergrundbild.png")
	
	#screen erzeugen
        window_width = 600
        window_height = 800
        window = pygame.display.set_mode((window_width, window_height))
	
	
	#bewegung 
        threshold = 50 # Schwellenwert
        speed = 2 # Geschwindigkeit der Bewegung
        direction = 0 #-1 für nach oben, 1 für nach unten
	
        clock = pygame.time.Clock() #geschwindigkeit regulieren
        running = True #solange true, läuft das spiel
	#eventschleife
        while running:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                running = False
                                erfolg = "Das Spiel wurde abgebrochen. Klick erneut auf Spiel beginnen, um es erneut zu starten."
	# falls escape taste gedrückt - fenster geschlossen
	
                        elif event.type ==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                running = False 
                                erfolg = "Das Spiel wurde abgebrochen. Klick erneut auf Spiel beginnen, um es erneut zu starten."
	
                value = alpha_average #wert aus durchschnittsrechnung abrufen
                max_y1 = base_y - (value*1,5) # je größer value, desto höher geht der kreis, zielhöhe mit alpha values berechnen
                max_y2 = max(50, min(max_y, base_y)) #begrenzung zwischen 50 und base_y -> kreis bewegt sich nicht aus dem bild raus
                if max_y1 > max_y2:
                        max_y = max_y2
                else:
                        max_y = max_y1

                if value > threshold:
                        direction == -1 and y < max_y
                        y -= speed 
                elif direction == 1 and y < base_y: #nach unten zur grundhöhe
                        y +=speed
		
                window.fill((0, 200, 0))
		
	
                pygame.draw.ellipse(window, "red" , [10,30,150,150], 1) # kreis zeichnen, Position, Nummer hinten steht für dicke der Umrandung
                pygame.display.update()
		
                clock.tick(30) #Schleife wird max 30x pro sekunde durchgelaufen -> kreis bewegt sich gleichmäßig
                pygame.display.flip() #bildschirm mit neuesten änderungen wird aktualisiert
        pygame.quit()
        
        if erfolg != "Das Spiel wurde abgebrochen. Klick erneut auf Spiel beginnen, um es erneut zu starten." or erfolg != "Super! Du hast es geschafft, ruhig und entspannt zu bleiben":
            erfolg = "Du hast es leider nicht geschafft, ruhig und entspannt zu bleiben"



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
        text = erfolg
        self.displayBox.insert("0.0", text)




#initiiert die app
if __name__ == "__main__": 
    app = App()
    app.mainloop()