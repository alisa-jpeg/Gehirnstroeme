#nötige dinge importieren
import threading
import json
import socket
import time
import pygame
import customtkinter as ctk #für graphiken 
import csv 
from datetime import datetime
import random
import tkinter.messagebox as msgbox

HOST = '127.0.0.1'  # Die IP-Adresse des lokalen Hosts, auf dem das Programm lauscht
PORT = 12345        # Der Port, auf dem Daten empfangen werden sollen
BUFFER_SIZE = 1024  # Die maximale Größe eines UDP-Datenpakets in Bytes
DURATION = 2        # Die Dauer (in Sekunden), für die Daten empfangen werden
DURATION_GAME = 10  # Die Dauer (in Sekunden), für die das Spiel läuft
MAX_PACKETS = 1000  # Die maximale Anzahl von Paketen, die verarbeitet werden

root = ctk.CTk()

success = ""
alpha_value = 0
    

#farbe der widgets (green, dark-blue, blue)
ctk.set_default_color_theme("green")

#farbe des fensters (Light, Dark, System)
ctk.set_appearance_mode("Dark") 

#größe fenster
appWidth= 1585
appHeight = 515

radio_var0 = ctk.IntVar()
radio_var1 = ctk.IntVar()
radio_var2 = ctk.IntVar()



#App Class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.frame_list = [] #Liste für die Frames
        self.data = {} #Daten-Variable für die Speicherung der Daten
        self.filename = "versuchsdaten.csv" #Dateiname für die Speicherung der Daten

#titel fenster
        self.title("Brain-Computer-Interface-Fragebogen") 
        self.geometry(f"{appWidth}x{appHeight}") #größe fenster auf das was zuvor festgelegt wurde


        self.protocol("WM_DELETE_WINDOW", self.on_closing) #behandlung des schließen des fensters


        # Initialisieren der Flagge für "Daten nicht speichern"
        self.show_only_flag = False

        self.frame1 = ctk.CTkFrame(self)
        self.frame2 = ctk.CTkFrame(self)

        self.frame1.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.frame2.grid(row=0, column=0, padx=20, pady=20, sticky="ew")


#erstes label-überschrift
        self.label = ctk.CTkLabel(self.frame1, text="Bitte füllen Sie vor Beginn des Spiels diesen Fragebogen aus, damit wir Ihre Daten auswerten können:")
        self.label.grid(row=0, column=0, padx=20, pady=20, columnspan=2,  sticky="ew")

#alter
        self.label = ctk.CTkLabel(self.frame1, text="Was ist Ihr Alter?")
        self.label.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.nameEntry = ctk.CTkEntry(self.frame1)
        self.nameEntry.grid(row=1, column=2, columnspan=2, padx=20, pady=20, sticky="ew")   

#3. label
        self.label = ctk.CTkLabel(self.frame1, text="Wann haben Sie das letzte mal Kaffee getrunken?")
        self.label.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.RadioButton1 = ctk.CTkRadioButton(self.frame1, text="Innerhalb der letzten zwei Stunden", value = 1, variable = radio_var0)
        self.RadioButton1.grid(row=2, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton2 = ctk.CTkRadioButton(self.frame1, text="Innerhalb der letzten 12 Stunden", value = 2, variable = radio_var0)
        self.RadioButton2.grid(row=2, column=3, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton3 = ctk.CTkRadioButton(self.frame1, text="Vor über 12 Stunden", value = 3, variable = radio_var0)
        self.RadioButton3.grid(row=2, column=4, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton4 = ctk.CTkRadioButton(self.frame1, text="Ich trinke keinen Kaffee", value = 4, variable = radio_var0)
        self.RadioButton4.grid(row=2, column=5, columnspan=1, padx=20, pady=20, sticky="w")
#4. label
        self.label = ctk.CTkLabel(self.frame1, text="Sind Sie links- oder rechtshändig?")
        self.label.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.RadioButton5 = ctk.CTkRadioButton(self.frame1, text="Ich bin linkshändig.", value = 1, variable = radio_var1)
        self.RadioButton5.grid(row=3, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton6 = ctk.CTkRadioButton(self.frame1, text="Ich bin rechtshändig.", value = 2, variable = radio_var1)
        self.RadioButton6.grid(row=3, column=3, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton7 = ctk.CTkRadioButton(self.frame1, text="Ich bin beidhändig.", value = 3, variable = radio_var1)
        self.RadioButton7.grid(row=3, column=4, columnspan=1, padx=20, pady=20, sticky="w")

#5. label
        self.label = ctk.CTkLabel(self.frame1, text="Wie müde fühlen Sie sich gerade? (1=Adrenalinschub, 10=Schlaf)")
        self.label.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.slider = ctk.CTkSlider(self.frame1, from_=1, to=10, number_of_steps=10, command = self.slider_event)
        self.slider.grid(row=4, column=2, columnspan=2, padx=20, pady=20, sticky="ew")

        self.label = ctk.CTkLabel(self.frame1, text="1")




#6. label
        self.label = ctk.CTkLabel(self.frame1, text="Wie dicht/dick ist Ihr Haar?")
        self.label.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.RadioButton8 = ctk.CTkRadioButton(self.frame1, text="Ich habe eine Glatze.", value = 1, variable = radio_var2)
        self.RadioButton8.grid(row=5, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton9 = ctk.CTkRadioButton(self.frame1, text="Ich habe dünnes Haar.", value = 2, variable=radio_var2)
        self.RadioButton9.grid(row=5, column=3, columnspan=1, padx=20, pady=20, sticky="w")

        self.RadioButton10 = ctk.CTkRadioButton(self.frame1, text="Ich habe dickes Haar.", value = 3, variable=radio_var2)
        self.RadioButton10.grid(row=5, column=4, columnspan=1, padx=20, pady=20, sticky="w")



#button zum schreiben der daten in ein dokument
        self.saveDataButton = ctk.CTkButton(self.frame1, text ="Daten speichern (damit stimmen Sie den Datenschutzrichtlinien zu)", command =self.end_frame)
        self.saveDataButton.grid(row=7, column = 0, columnspan = 2, padx = 20, pady=20, sticky ="ew")       
        
         # Button für die Option keine Daten zu speichern (nur Anschauungszwecke)
        self.showOnlyButton = ctk.CTkButton(self.frame1, text="Daten nicht speichern (nur zu Anschauungszwecken)", command=self.show_only)
        self.showOnlyButton.grid(row=7, column=2, columnspan=2, padx=20, pady=20, sticky="ew")




        #2. frame

        #spielerklärung

        self.label = ctk.CTkLabel(self.frame2, text="Spielanleitung: \n\nIn diesem Spiel steuern Sie einen Ballon, indem Sie Ihre Gehirnaktivität (Alpha-Wellen), die von dem EEG gemessen wird, verwenden. \n\n Je mehr Alpha-Wellen das EEG empfängt, desto entspannter sind Sie, einfach gesagt. \n\nIhr Ziel ist es, den Ballon in der Luft zu halten, indem Sie Ihre Alpha-Wellen steuern, indem Sie sich entspannen oder nicht. \n\nWenn Ihr Alpha-Wert über dem Durchschnitt liegt, Sie also sehr entspannt sind, steigt der Ballon. Wenn er darunter liegt, Sie also sehr aufgeregt sind, sinkt der Ballon. \n\nDas Spiel dauert 60 Sekunden. Viel Spaß!")
        self.label.grid(row=0, column=0, columnspan=10, padx=20, pady=20, sticky="w")

        self.generateAverageButton = ctk.CTkButton(self.frame2, text = "Durchschnitt berechnen", command = self.threading_average_alpha) 
        self.generateAverageButton.grid(row=5, column = 1, columnspan = 2, padx = 20, pady=20, sticky ="w")

        #erstellt text box 1 um average_alpha anzuzeigen
        self.displayBox1 = ctk.CTkTextbox(self.frame2, width=300, height=25)
        self.displayBox1.grid(row=5, column=4, columnspan=2, padx=20, pady=20, sticky="w")

        #erstellt text box 2 um endergebnis anzuzeigen
        self.displayBox2 = ctk.CTkTextbox(self.frame2, width=700, height=25)
        self.displayBox2.grid(row=6, column=4, columnspan=3, padx=20, pady=20, sticky="w")

        #erstellt button2
        self.startGameButton = ctk.CTkButton(self.frame2, text = "Spiel beginnen", state = "disabled", command = self.start_countdown)
        self.startGameButton.grid(row=6, column = 1, columnspan = 2, padx = 20, pady=20, sticky ="w")

        #erstellt textfeld, damit man sieht ob udp-stream läuft
        self.displayBox3 = ctk.CTkTextbox(self.frame2, width=500, height=25)
        self.displayBox3.grid(row=5, column=6, columnspan=2, padx=20, pady=20, sticky="w")
        self.displayBox3.insert("0.0", "UDP-Stream nicht gestartet - Bitte lassen Sie den Durchschnitt berechnen")

        #schließen des fensters
        self.closeButton = ctk.CTkButton(self.frame2, text = "Schließen", command = self.quit)
        self.closeButton.grid(row=8, column = 0, columnspan = 10, padx = 20, pady=20, sticky ="ew")       

        self.frame1.tkraise()

    def on_closing(self):
        #Beendet das Programm, wenn das Fenster geschlossen wird.
        self.quit()  # Beendet die tkinter-Schleife
        self.destroy()  # Zerstört das Fenster
        pygame.quit()  # Beendet pygame, falls es läuft
        exit(0)  # Beendet das gesamte Programm

    def forward(self):
        self.frame1.destroy()
        self.frame2.tkraise()



    def slider_event(self, value):
        self.label = ctk.CTkLabel(self.frame1, text=value)
        self.label.grid(row=4, column=4, columnspan=2, padx=20, pady=20, sticky="w")



    def create_textt(self):
        #.cget("value") gibt den wert des eingabefeldes zurück
        v0 = radio_var0.get()
        v1 = radio_var1.get()
        v2 = radio_var2.get()


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
                "Erfolg": "",
                "Zeitstempel": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                "Zufallsnummer": random.randint(1000, 9999)
        }       
        return text
    
    # Validierung der Benutzereingaben
    def validate_inputs(self):

        v0 = radio_var0.get()
        v1 = radio_var1.get()
        v2 = radio_var2.get()

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

        if v0 == 0:
            msgbox.showerror("Fehler", "Bitte wählen Sie eine Option für den Kaffeekonsum.")
            return False

        if v1 == 0:
            msgbox.showerror("Fehler", "Bitte wählen Sie eine Option für Ihre Händigkeit.")
            return False

        if v2 == 0:
            msgbox.showerror("Fehler", "Bitte wählen Sie eine Option für Ihren Haartyp.")
            return False


        return True
    
    def end_frame(self):
        if not self.validate_inputs():
            return
        self.data = self.create_textt()
        msgbox.showinfo("Erfolg", "Die Daten wurden erfolgreich gespeichert.")
        self.forward()
    

    # Wenn der Benutzer nur zu Anschauungszwecken arbeitet (keine Speicherung)
    def show_only(self):
        self.show_only_flag = True
        msgbox.showinfo("Nur zur Ansicht", "Keine Daten werden gespeichert. Dies dient nur der Anschauung.")
        self.show_only_flag = False
        self.forward()

    def threading_average_alpha(self):
        self.startGameButton.configure(state = "disabled")        
        self.displayBox3.delete("0.0", "end")
        self.displayBox3.insert("0.0", "UDP-Stream läuft - Bitte warten Sie einen Moment")
        threading.Thread(target=self.show_alpha).start()

    def show_alpha(self):
        self.alpha_average = calculate_average_alpha()
        self.displayBox1.delete("0.0", "end")
        self.displayBox1.insert("0.0", self.alpha_average)
        self.displayBox3.delete("0.0", "end")
        self.displayBox3.insert("0.0", "UDP-Stream ist abgeschlossen - Das Spiel kann beginnen!")
        self.startGameButton.configure(state = "normal")


    def start_countdown(self):
        self.label = ctk.CTkLabel(self.frame2, text="3...")
        self.label.grid(row=7, column=0, columnspan=2, padx=20, pady=20, sticky="w")
        self.after(1000, lambda: self.update_label("2..."))
        self.after(2000, lambda: self.update_label("1..."))
        self.after(3000, lambda: self.update_label("Los!"))
        self.after(4000, self.run_game)


    def update_label(self, text):
        self.label.configure(text=text)


    def run_game(self):
        self.label.configure(text = "") #Label zurücksetzen
        self.label.grid_forget() #Label ausblenden

        # CustomTkinter-Fenster deaktivieren
        self.attributes("-disabled", True)


        #Variablen für die Ballpostion und Geschwindigkeit festlegen
        y = 350
        speed = 5
        #UDP socket für den Empfang von Alpha-Werten einrichten
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((HOST, PORT))
        
        alpha_values = [] #Liste zur Speicherung der empfangegen Alpha-Werte
        start_time = time.time() #Startzeit des Spiels speichern

        #pygame initialisieren
        pygame.init()
        window_width, window_height = 825, 800 #Fenstergröße definieren
        window = pygame.display.set_mode((window_width, window_height)) #Fenster erstellen
               
        clock = pygame.time.Clock() #Pygame-Uhr zur Steuerung der FPS (Frames per Second) um die Bildwiedergabe zu kontrollieren

        #Hintergrund laden und auf die Fenstergröße skalieren
        background = pygame.image.load("Hintergrundbild.png")
        ballon = pygame.image.load("ballon.png")
        burst = pygame.image.load("zerplatzt.png")

        background=pygame.transform.scale(background,(window_width,window_height))
        window.blit(background,(0,0))
        
        #Ballonbild laden und skalieren
        ballon=pygame.transform.scale(ballon,(100,200))
        window.blit(ballon,(360, int(y)))

        #Spielschleife läuft 
        running = True
        game_aborted = False
        while running:
            #Verarbeitung von Benutzereingaben
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_aborted = True
                        running = False

            #udp stream starten, solange spiel läuft und genug pakete empfangen wurden 
            if time.time() - start_time < DURATION_GAME and len(alpha_values) < MAX_PACKETS: 
                try:
                    #ALpha-Wert über UDP empfangen
                    data, _ = udp_socket.recvfrom(BUFFER_SIZE)
                    message = json.loads(data.decode('utf-8'))

                    #Prüfen ob das empfangene Paket gültig ist und die Daten enthält
                    if "data" in message and isinstance(message["data"], list) and len(message["data"]) > 2:
                        self.alpha_value = (message["data"][2]) #Wert aus Liste speichern
                        alpha_values.append(message["data"][2]) #Wert zur Liste hinzufügen

                except json.JSONDecodeError:
                    print("Fehler beim Dekodieren des JSON-Pakets.") #Falls JSON fehlerhaft ist
                                    
                except Exception as e:
                    print(f"Unerwarteter Fehler: {e}") #allgemeiner fehlerfall

                #Prüfen ob Ballon außerhalb des Spielfeldes ist
                if y > 700 or y < 50:    #Falls aus sichtbaren Bereich fliegt-Abbruch
                    window.blit(background, (0, 0))
                    ballon=pygame.transform.scale(burst,(100,200)) #ballon ersetzen durch zerplatzten ballon
                    window.blit(ballon,(360, int(y)))
                    pygame.display.update()
                    time.sleep(2) #5 Sekunden warten
                    pygame.quit()
                    success = "Spiel abgebrochen! Alpha-Wert über- oder unterschreitet das kritische Limit für zu lang." 
                    self.displayBox2.delete("0.0", "end")
                    self.displayBox2.insert("0.0", success)
                    break
                               
                #Ballon Bewegung basierend auf Alpha-Wert
                if self.alpha_value > self.alpha_average: #Wenn Alpha-Wert größer als Durchschnitt ist
                    y -= speed  # Ballon steigt

                if self.alpha_value < self.alpha_average: #Wenn Alpha-Wert kleiner als Durchschnitt ist
                    y += speed #Ballon sinkt

                # Hintergrund und Ballon neu zeichnen
                window.blit(background, (0, 0))
                window.blit(ballon, (360, int(y)))
                pygame.display.update() #Anzeige aktualisieren
                clock.tick(60)  # Spielgeschwindigkeit auf 60 FPS begrenzen

            else:
                running=False #Wenn Zeit abgelaufen ist oder genug Pakete empfangen wurden, Spiel beenden

        udp_socket.close()
        pygame.quit()

        # CustomTkinter-Fenster wieder aktivieren
        self.attributes("-disabled", False)
        self.lift()  # Bringt das Fenster in den Vordergrund

        if game_aborted:
            success = "Spiel abgebrochen! Das Fenster wurde geschlossen."
            self.displayBox2.delete("0.0", "end")
            self.displayBox2.insert("0.0", success)
        else:
            success = "Spiel beendet - Ballon erfolgreich gesteuert!"
            self.displayBox2.delete("0.0", "end")
            self.displayBox2.insert("0.0", success)

        self.data["Erfolg"] = success #Erfolg in die Daten einfügen
        self.safe_data(self.filename, self.data)


    def safe_data(self, filename, data):
        if self.show_only_flag:
            with open(filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data.keys())
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(data)

        
# Funktion zur Berechnung des Durchschnitts der Alpha-Werte
def calculate_average_alpha():
    # Erstelle einen UDP-Socket, um Daten zu empfangen.AF_INET bezeichnet hierbei Adress-Family-Inzternet” das bedeutet, dass wir einen IPv4-Socket erstellen (für IP-Adressen der Form XXX.XXX.X.X).
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Binden des Sockets an eine spezifische IP-Adresse und einen Port (PORT)
    # Dadurch kann der Socket ankommende UDP Pakete von anderen Geräten oder Programmen empfangen und die Daten an diese Adresse senden.
    
    udp_socket.bind((HOST, PORT))

    # Initialisiert eine Liste, um die empfangenen Alpha-Werte zu speichern. Dabei werden die Alpha Werte aus den empfangenen JSON Daten extrahiert.
    alpha_values = []

    # Die Schleife läuft solange, bis die maximale Empfangsdauer (DURATION) erreicht ist oder die maximale Anzahl an Paketen (MAX_PACKETS) empfangen wurde. 
    start_time = time.time()
  
    while time.time() - start_time < DURATION and len(alpha_values) < MAX_PACKETS:
        try:
            # Wartet auf den Empfang eines Datenpakets mit einer maximalen Größe von BUFFER_SIZE Bytes. Da UDP verbindungslos ist, muss jedes Paket einzeln verarbeitet werden. recvfrom() gibt daher normalerweise die empfangenen Daten, sowie auch die Adresse (IP + Port) des Absenders zurück, damit man weiß, von wem das Paket kam. In unserem Code wird diese Adresse jedoch mit _ ignoriert, weil sie für die Verarbeitung nicht benötigt wird. Es ist dennoch notwendig es zu integrieren, da  Python eine exakte Anzahl an Variablen für Rückgabewerte erwartet.Deshalb muss die Adresse auch dann erfasst werden, wenn man sie nicht braucht, weilrecvfrom()ein Tupel (data, addr) zurückgibt.Ohne eine zweite Variable würde es zu einem Fehler kommen.

          
            data, _ = udp_socket.recvfrom(BUFFER_SIZE)
            #Dekodiert das empfangene JSON-Format in ein Python Objekt
            
            message = json.loads(data.decode('utf-8'))
            alpha_values.append(message["data"][2])

            #Prüft, ob die empfangenen Daten die erwartete Struktur besitzen. Die Datenstruktur enthält ein "data"-Feld, das eine Liste ist.
            if "data" in message and isinstance(message["data"], list) and len(message["data"]) > 2:

                #Extrahiert den Wert aus der Liste und speichert ihn in der Liste Alpha Values.
                alpha_values.append(message["data"][2])
            else:
                #falls das empfangene Paket nicht die erwartete Struktur hat, wird ungültiges Paket ausgegeben. 
                print("Ungültiges Paket erhalten:", message)

        except json.JSONDecodeError:
            #falls das empfangene Datenpaket keine gültige JSON-Struktur hat, wird ein Fehler ausgegeben. 
            print("Fehler beim Dekodieren des JSON-Pakets.")
        except Exception as e:
            #fange alle unerwarteten fehler ab und gebe die Fehlermeldung aus.
            print(f"Unerwarteter Fehler: {e}")

    #Nachdem die Empfangsschleife beendet ist, wird der UDP-Socket geschlossen.
    udp_socket.close()


    #Berechnen des Durchschnitts der Alpha-Werte und wird zurückgegeben.
    # Falls keine Werte empfangen wurden, wird 0 zurückgegeben.
    return sum(alpha_values) / len(alpha_values) if alpha_values else 0



#initiiert die app
if __name__ == "__main__": 
    app = App()
    app.mainloop()
