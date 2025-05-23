import customtkinter as ctk
import threading
import json
import socket
import time
import pygame
import pygame.surfarray

# UDP-Konfiguration
HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024
DURATION = 2  # Dauer für den UDP-Stream
DURATION_GAME = 60 # Dauer für das Spiel
MAX_PACKETS = 1000



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.alpha_value = 0

        # Titel und Fenstergröße
        self.title("Brain-Computer-Interface")
        self.geometry("1200x1200")

        # UI-Farbeinstellungen
        ctk.set_default_color_theme("green")
        ctk.set_appearance_mode("Dark")

        # Initialwerte
        self.alpha_average = 0
        self.erfolg = ""

        # Buttons & Anzeige-Elemente
        self.generateResultsButton = ctk.CTkButton(self, text="Durchschnitt berechnen", command=self.durchschnitt_berechnen)
        self.generateResultsButton.grid(row=1, column=1, columnspan=2, padx=20, pady=20, sticky="w")

        self.displayBox1 = ctk.CTkTextbox(self, width=300, height=25)
        self.displayBox1.grid(row=1, column=4, columnspan=2, padx=20, pady=20, sticky="w")

        self.displayBox2 = ctk.CTkTextbox(self, width=700, height=25)
        self.displayBox2.grid(row=3, column=4, columnspan=5, padx=20, pady=20, sticky="w")

        self.generateResultsButton = ctk.CTkButton(self, text="Spiel beginnen", command=self.spiel_beginnen)
        self.generateResultsButton.grid(row=3, column=1, columnspan=2, padx=20, pady=20, sticky="w")

        self.displayBox3 = ctk.CTkTextbox(self, width=500, height=25)
        self.displayBox3.grid(row=1, column=6, columnspan=2, padx=20, pady=20, sticky="w")
        self.displayBox3.insert("0.0", "UDP-Stream nicht gestartet - Bitte lassen Sie den Durchschnitt berechnen")

        self.canvas = ctk.CTkCanvas(self, width=1000, height=1000)
        self.canvas.pack()
        self.pygame_running = False

    def durchschnitt_berechnen(self):
        self.displayBox3.delete("0.0", "end")
        self.displayBox3.insert("0.0", "UDP-Stream läuft - Bitte warten Sie einen Moment")
        threading.Thread(target=self.alpha_anzeigen).start()

    def alpha_anzeigen(self):
        self.alpha_average = self.calculate_average_alpha()
        self.displayBox1.delete("0.0", "end")
        self.displayBox1.insert("0.0", str(self.alpha_average))
        self.displayBox3.delete("0.0", "end")
        self.displayBox3.insert("0.0", "UDP-Stream abgeschlossen - Das Spiel kann beginnen!")

    def calculate_average_alpha(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((HOST, PORT))
        alpha_values = []
        start_time = time.time()

        while time.time() - start_time < DURATION and len(alpha_values) < MAX_PACKETS:
            try:
                data, _ = udp_socket.recvfrom(BUFFER_SIZE)
                message = json.loads(data.decode('utf-8'))

                if "data" in message and isinstance(message["data"], list) and len(message["data"]) > 2:
                    alpha_values.append(message["data"][2])

            except json.JSONDecodeError:
                print("Fehler beim Dekodieren des JSON-Pakets.")
            except Exception as e:
                print(f"Unerwarteter Fehler: {e}")

        udp_socket.close()
        return sum(alpha_values) / len(alpha_values) if alpha_values else 0

    def spiel_beginnen(self):
        self.displayBox2.delete("0.0", "end")
        self.erfolg = self.ballon_bewegen()
        self.displayBox2.insert("0.0", self.erfolg)

    def ballon_bewegen(self):
        #variablen festlegen
        y = 350
        speed = 3
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((HOST, PORT))
        alpha_values = []
        start_time = time.time()

        #pygame initialisieren
        pygame.init()
        window_width, window_height = 800, 800
        window = pygame.display.set_mode((window_width, window_height))
        clock = pygame.time.Clock()
        background = pygame.image.load("Hintergrundbild.png")
        ballon = pygame.image.load("ballon.png")

        #hintergrund festlegen
        background=pygame.transform.scale(background,(window_width,window_height))
        window.blit(background,(0,0))
    
        #ballon erstellen
        ballon=pygame.transform.scale(ballon,(100,200))
        window.blit(ballon,(360, int(y)))


        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    #udp stream starten
            if time.time() - start_time < DURATION_GAME and len(alpha_values) < MAX_PACKETS: 
                try:
                    data, _ = udp_socket.recvfrom(BUFFER_SIZE)
                    message = json.loads(data.decode('utf-8'))

                    if "data" in message and isinstance(message["data"], list) and len(message["data"]) > 2:
                        self.alpha_value = (message["data"][2])
                        alpha_values.append(message["data"][2])

                except json.JSONDecodeError:
                    print("Fehler beim Dekodieren des JSON-Pakets.")
                except Exception as e:
                    print(f"Unerwarteter Fehler: {e}")

                # Ballonbewegung basierend auf dem Alpha-Wert
                if y > window_height or y < 0:    #abbruch
                    pygame.quit()
                    return "Spiel abgebrochen! Alpha-Wert über- oder unterschreitet das kritische Limit für zu lang."

                if self.alpha_value > self.alpha_average:
                    y -= speed  # Ballon steigt

                if self.alpha_value < self.alpha_average:
                    y += speed #Ballon sinkt

                # Hintergrund und Ballon neu zeichnen
                window.blit(background, (0, 0))
                window.blit(ballon, (360, int(y)))

                pygame.display.update()
                clock.tick(60)  # FPS

        udp_socket.close()
        pygame.quit()
        return "Spiel beendet - Ballon erfolgreich gesteuert."


# Hauptprogramm starten
if __name__ == "__main__":
    app = App()
    app.mainloop()
