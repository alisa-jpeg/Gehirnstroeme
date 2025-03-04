import customtkinter as ctk
import threading
import json
import socket
import time
import pygame

# UDP-Konfiguration
HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024
DURATION = 5  # Dauer für den UDP-Stream
MAX_PACKETS = 1000

# Ballon-Steuerungsparameter
SENSITIVITY = 0.10  # 10% Anstieg → Ballon steigt
CRITICAL_LIMIT = 0.50  # 50% Anstieg → Spielabbruch

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Titel und Fenstergröße
        self.title("Brain-Computer-Interface")
        self.geometry("1200x200")

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
        self.displayBox1.grid(row=1, column=4, columnspan=2, padx=20, pady=20, sticky="s")

        self.displayBox2 = ctk.CTkTextbox(self, width=300, height=25)
        self.displayBox2.grid(row=3, column=4, columnspan=2, padx=20, pady=20, sticky="s")

        self.generateResultsButton = ctk.CTkButton(self, text="Spiel beginnen", command=self.spiel_beginnen)
        self.generateResultsButton.grid(row=3, column=1, columnspan=2, padx=20, pady=20, sticky="w")

        self.displayBox3 = ctk.CTkTextbox(self, width=500, height=25)
        self.displayBox3.grid(row=1, column=6, columnspan=2, padx=20, pady=20, sticky="w")
        self.displayBox3.insert("0.0", "UDP-Stream nicht gestartet - Bitte lassen Sie den Durchschnitt berechnen")

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
        pygame.init()
        window_width, window_height = 600, 800
        window = pygame.display.set_mode((window_width, window_height))
        clock = pygame.time.Clock()

        base_y = 500
        y = base_y
        speed = 2
        balloon_color = (0, 255, 0)  # Grün
        font = pygame.font.SysFont(None, 36)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Ballonbewegung basierend auf dem Alpha-Wert
            if self.alpha_average > self.alpha_average*2:
                pygame.quit()
                return "Spiel abgebrochen! Alpha-Wert überschreitet das kritische Limit."

            if self.alpha_average > self.alpha_average:
                y -= speed  # Ballon steigt

            if self.alpha_average < self.alpha_average:
                y += speed #Ballon sinkt

            window.fill((0, 0, 0))  # Bildschirm löschen
            pygame.draw.circle(window, balloon_color, (window_width // 2, y), 50)  # Ballon zeichnen

            # Text anzeigen, der den aktuellen alpha_average anzeigt
            text = font.render(f"Alpha Average: {self.alpha_average:.2f}", True, (255, 255, 255))
            window.blit(text, (10, 10))

            pygame.display.flip()
            clock.tick(60)  # 60 FPS

        pygame.quit()
        return "Spiel beendet"

# Hauptanwendung starten
if __name__ == "__main__":
    app = App()
    app.mainloop()
