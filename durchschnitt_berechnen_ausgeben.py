import json
import socket
import time

# Konfiguration der Netzwerkparameter
HOST = '127.0.0.1'  # Die IP-Adresse des lokalen Hosts, auf dem das Programm lauscht
PORT = 12345        # Der Port, auf dem Daten empfangen werden sollen
BUFFER_SIZE = 1024  # Die maximale Größe eines UDP-Datenpakets in Bytes
DURATION = 10       # Die Dauer (in Sekunden), für die Daten empfangen werden
MAX_PACKETS = 1000  # Die maximale Anzahl von Paketen, die verarbeitet werden

# Hauptprogramm zur Initialisierung des Empfangs und der Berechnung
    # Rufe die Funktion zur Durchschnittsberechnung auf
alpha_average = calculate_average_alpha()

    # Ausgabe des berechneten Durchschnitts der Alpha-Werte
print(alpha_average)
