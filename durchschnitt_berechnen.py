#json message empfangen, dekodiert in python dictionary,
#alpha wert aufgenommen/ rausgefilter + zur liste hinzugefügt, liste nach 10s abgebrochen, durschnitt ermittelt

import json
import socket
import time

# Konfiguration der Netzwerkparameter
HOST = '127.0.0.1'  # Die IP-Adresse des lokalen Hosts, auf dem das Programm lauscht
PORT = 12345        # Der Port, auf dem Daten empfangen werden sollen
BUFFER_SIZE = 1024  # Die maximale Größe eines UDP-Datenpakets in Bytes
DURATION = 10       # Die Dauer (in Sekunden), für die Daten empfangen werden
MAX_PACKETS = 1000  # Die maximale Anzahl von Paketen, die verarbeitet werden

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
    a=1

    # Schleife läuft, solange die Zeit innerhalb der konfigurierten Dauer ist + maximale Anzahl an Paketen nicht überschritten ist
    while time.time() - start_time < DURATION and len(alpha_values) < MAX_PACKETS:
        # Empfang eines Datenpakets
        data, schleifenvariable = udp_socket.recvfrom(BUFFER_SIZE)
        if a==1:
            print("UDP-Stream läuft")
            a = a+1

        # Konvertieren der empfangenen JSON-Daten in ein Python-Dictionary
        message = json.loads(data.decode('utf-8'))

        # Extrahieren des Alpha-Werts (Index 2) aus den empfangenen Daten und speichere ihn
        alpha_values.append(message["data"][2])

    # Schließen des UDP-Socket, da er nicht mehr benötigt wird
    udp_socket.close()

    # Berechnen des Durchschnitts der Alpha-Werte und gib ihn zurück
    # Falls keine Werte empfangen wurden, gib 0 zurück
    return sum(alpha_values) / len(alpha_values) if alpha_values else 0
