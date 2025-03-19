

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


root = ctk.CTk()


HOST = '127.0.0.1'  # Die IP-Adresse des lokalen Hosts, auf dem das Programm lauscht
PORT = 12345        # Der Port, auf dem Daten empfangen werden sollen
BUFFER_SIZE = 1024  # Die maximale Größe eines UDP-Datenpakets in Bytes
DURATION = 2        # Die Dauer (in Sekunden), für die Daten empfangen werden
DURATION_GAME = 10  # Die Dauer (in Sekunden), für die das Spiel läuft
MAX_PACKETS = 1000  # Die maximale Anzahl von Paketen, die verarbeitet werden

erfolg = ""
alpha_value = 0

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

        # Initialisieren der Flagge für "Daten nicht speichern"
        self.show_only_flag = False



#erstes label-überschrift
        self.label = ctk.CTkLabel(self, text="Bitte füllen Sie vor Beginn der Messungen diesen Fragebogen aus, damit wir Ihre Daten auswerten können:")
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



#button zum schreiben der daten in ein dokument
        self.generateResultsButton = ctk.CTkButton(self, text ="Daten speichern (damit stimmen Sie den Datenschutzrichtlinien zu)", command =self.abschluss)
        self.generateResultsButton.grid(row=7, column = 0, columnspan = 2, padx = 20, pady=20, sticky ="ew")       
        
         # Button für die Option keine Daten zu speichern (nur Anschauungszwecke)
        self.showOnlyButton = ctk.CTkButton(self, text="Daten nicht speichern (nur zu Anschauungszwecken)", command=self.show_only)
        self.showOnlyButton.grid(row=7, column=2, columnspan=2, padx=20, pady=20, sticky="ew")





    def slider_event(self, value):
        self.label = ctk.CTkLabel(self, text=value)
        self.label.grid(row=4, column=4, columnspan=2, padx=20, pady=20, sticky="w")



    def createText(self):
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
    
    def abschluss(self):
        if not self.validate_inputs():
            return
        print("wir sind im abschluss")
        dateiname = "versuchsdaten.csv"
        daten = self.createText()
        daten_speichern(dateiname, daten)
        msgbox.showinfo("Erfolg", "Die Daten wurden erfolgreich gespeichert.")
        self.open_toplevel()
    
    def open_toplevel(self):
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow(self) #Toplevelwindow-fenster erstellen wenn es noch nicht existiert
                self.toplevel_window.grab_set() #fokus auf das Toplevelwindow-fenster setzen
                self.toplevel_window.protocol("WM_DELETE_WINDOW", self.on_closing) # Protokoll für das Schließen des Toplevel-Fensters festlegen

    def on_closing(self):
        if self.toplevel_window is not None:
            self.toplevel_window.destroy()
        self.destroy()
        self.quit()

    # Wenn der Benutzer nur zu Anschauungszwecken arbeitet (keine Speicherung)
    def show_only(self):
        self.show_only_flag = True
        msgbox.showinfo("Nur zur Ansicht", "Keine Daten werden gespeichert. Dies dient nur der Anschauung.")
        self.show_only_flag = False
        self.open_toplevel()


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


# Hauptfenster der Anwendung erstellen

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Brain-Computer-Interface")
        self.geometry(f"{appWidth}x{appHeight}")
        self.toplevel_window = None

        self.generateResultsButton = ctk.CTkButton(self, text = "Durchschnitt berechnen", command = self.durchschnitt_berechnen) 
        self.generateResultsButton.grid(row=1, column = 1, columnspan = 2, padx = 20, pady=20, sticky ="w")

        #erstellt text box 1 um average_alpha anzuzeigen
        self.displayBox1 = ctk.CTkTextbox(self, width=300, height=25)
        self.displayBox1.grid(row=1, column=4, columnspan=2, padx=20, pady=20, sticky="w")

        #erstellt text box 2 um endergebnis anzuzeigen
        self.displayBox2 = ctk.CTkTextbox(self, width=700, height=25)
        self.displayBox2.grid(row=3, column=4, columnspan=3, padx=20, pady=20, sticky="w")


        #erstellt button2
        self.generateResultsButton = ctk.CTkButton(self, text = "Spiel beginnen", command = self.spiel_beginnen)
        self.generateResultsButton.grid(row=3, column = 1, columnspan = 2, padx = 20, pady=20, sticky ="w")

        #erstellt textfeld, damit man sieht ob udp-stream läuft
        self.displayBox3 = ctk.CTkTextbox(self, width=500, height=25)
        self.displayBox3.grid(row=1, column=6, columnspan=2, padx=20, pady=20, sticky="w")
        self.displayBox3.insert("0.0", "UDP-Stream nicht gestartet - Bitte lassen Sie den Durchschnitt berechnen")

    def durchschnitt_berechnen(self):
        self.displayBox3.delete("0.0", "end")
        self.displayBox3.insert("0.0", "UDP-Stream läuft - Bitte warten Sie einen Moment")
        threading.Thread(target=self.alpha_anzeigen).start()

    def alpha_anzeigen(self):
        self.alpha_average = calculate_average_alpha()
        self.displayBox1.delete("0.0", "end")
        self.displayBox1.insert("0.0", self.alpha_average)
        self.displayBox3.delete("0.0", "end")
        self.displayBox3.insert("0.0", "UDP-Stream ist abgeschlossen - Das Spiel kann beginnen!")


    def spiel_beginnen(self):
        self.displayBox2.delete("0.0", "end")
        erfolg = self.ballon_bewegen()
        text = erfolg
        self.displayBox2.insert("0.0", text)

    def ballon_bewegen(self): 
        #Variablen für die Ballpostion und Geschwindigkeit festlegen
                y = 350
                speed = 1 
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

                background=pygame.transform.scale(background,(window_width,window_height))
                window.blit(background,(0,0))
        
                #Ballonbild laden und skalieren
                ballon=pygame.transform.scale(ballon,(100,200))
                window.blit(ballon,(360, int(y)))

                #Spielschleife läuft 
                running = True
                while running:
                    #Verarbeitung von Benutzereingaben
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
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
                                if y > window_height or y < 100:    #Falls aus sichtbaren Bereich fliegt-Abbruch
                                        pygame.quit()
                                    return "Spiel abgebrochen! Alpha-Wert über- oder unterschreitet das kritische Limit für zu lang."
                               
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
                return "Spiel beendet - Ballon erfolgreich gesteuert."




#initiiert die app
if __name__ == "__main__": 
    app = App()
    app.mainloop()
