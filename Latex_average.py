import socket
import json
import time

def calculate_average_alpha():
    # Erstellt einen UDP-Socket für die Kommunikation mit dem EEG 
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bindet den Socket an Host und Port des openBCIs
    udp_socket.bind((HOST, PORT))

    # Speichert die empfangenen Alpha-Werte zur späteren Berechnung des Durchschnitts
    alpha_values = []

    # Startzeit der Empfangsschleife(
    start_time = time.time()

    # Empfängt Daten, bis die maximale Dauer oder Anzahl an Paketen erreicht ist
    while time.time() - start_time < DURATION and len(alpha_values) < MAX_PACKETS:
        try:
            # Dekodiert die JSON-Daten aus dem empfangenen Paket
            message = json.loads(data.decode('utf-8'))
    # Schließt den UDP-Socket nach Beendigung der Empfangsschleife
    udp_socket.close()

    # Berechnet und gibt den Durchschnitt der Alpha-Werte zurück (0, falls keine Werte empfangen wurden)
    return sum(alpha_values) / len(alpha_values) if alpha_values else 0
