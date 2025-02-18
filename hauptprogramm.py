#fenster mit knopf -- konsoleneingabe
#durchschnitt berechnen und anzeigen
#luftballon steigen, spiel beginnen
#nach ende des spiels auswertung anzeigen?

#nötige dinge importieren
import customtkinter as ctk #für oberfläche

import csv      #für dateneingabe
from datetime import datetime 

import json    #für datenempfang
import socket 
import time

import pygame    #für luftballon
from pygame.locals import*
pygame.init()

#funktionen importieren
from durchschnitt_berechnen import calculate_average_alpha
from konsoleneingabe import konsoleneingabe
from pygame_kreis import # hier später dann pygame_kreis

# Konfiguration der Netzwerkparameter
HOST = '127.0.0.1'  # Die IP-Adresse des lokalen Hosts, auf dem das Programm lauscht
PORT = 12345        # Der Port, auf dem Daten empfangen werden sollen
BUFFER_SIZE = 1024  # Die maximale Größe eines UDP-Datenpakets in Bytes
DURATION = 10       # Die Dauer (in Sekunden), für die Daten empfangen werden
MAX_PACKETS = 1000  # Die maximale Anzahl von Paketen, die verarbeitet werden


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
