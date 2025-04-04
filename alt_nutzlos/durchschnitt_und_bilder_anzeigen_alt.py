#json message empfangen, dekodiert in python dictionary,

#alpha wert aufgenommen/ rausgefilter + zur liste hinzugefügt, liste nach 10s abgebrochen, durschnitt ermittelt


import json 
import socket 
#importieren und initialisieren von pygame
import pygame

from alt_nutzlos.durchschnitt_berechnen import calculate_average_alpha
from alt_nutzlos.Luftballom_steigt_sinkt_alt import steigen

pygame.init()

#variablen/konstanten für pygame fenter setzen
W, H = 800, 600
FPS = 30
SCHWARZ = (0,0,0)
WEISS = (255, 255, 255)
GRAU = (155, 155, 155)
spielaktiv = True

# Konfiguration der Netzwerkparameter
HOST = '127.0.0.1'  # Die IP-Adresse des lokalen Hosts, auf dem das Programm lauscht
PORT = 12345        # Der Port, auf dem Daten empfangen werden sollen
BUFFER_SIZE = 1024  # Die maximale Größe eines UDP-Datenpakets in Bytes
DURATION = 10       # Die Dauer (in Sekunden), für die Daten empfangen werden
MAX_PACKETS = 1000  # Die maximale Anzahl von Paketen, die verarbeitet werden
# Define QUIT as pygame.QUIT und den rest auch
QUIT = pygame.QUIT
KEYDOWN = pygame.KEYDOWN
K_ESCAPE = pygame.K_ESCAPE

#Öffnen neuen Fensters
fenster = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# Hauptprogramm
alpha_average = calculate_average_alpha()
print(f"Durchschnitt der Alpha-Werte: {alpha_average:.6f}")


#zweiten datenstream empfangen, mit durchschnitt vergleichen und bilder anzeigen

#bilder importieren

ballon = ['','','']
ballon[0] = pygame.image.load("Ballon1.jpeg")
ballon[1] = pygame.image.load("Ballon2.jpeg")
ballon[2] = pygame.image.load("Ballon3.jpeg")

while spielaktiv:
    #überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        #Beenden bei [ESC] oder [X]
        if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
            spielaktiv = False

#neuer stream empfangen

steigen


