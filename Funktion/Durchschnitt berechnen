#json message empfangen, dekodiert in python dictionary,
#alpha wert aufgenommen/ rausgefilter + zur liste hinzugefügt, liste nach 10s abgebrochen, durschnitt ermittelt


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

    # Schleife läuft, solange die Zeit innerhalb der konfigurierten Dauer ist + maximale Anzahl an Paketen nicht überschritten ist
    while time.time() - start_time < DURATION and len(alpha_values) < MAX_PACKETS:
        # Empfang eines Datenpakets
        data, schleifenvariable = udp_socket.recvfrom(BUFFER_SIZE)

        # Konvertieren der empfangenen JSON-Daten in ein Python-Dictionary
        message = json.loads(data.decode('utf-8'))

        # Extrahieren des Alpha-Werts (Index 2) aus den empfangenen Daten und speichere ihn
        alpha_values.append(message["data"][2])

    # Schließen des UDP-Socket, da er nicht mehr benötigt wird
    udp_socket.close()

    # Berechnen des Durchschnitts der Alpha-Werte und gib ihn zurück
    # Falls keine Werte empfangen wurden, gib 0 zurück
    return sum(alpha_values) / len(alpha_values) if alpha_values else 0
