import pygame
from durchschnitt_berechnen import calculate_average_alpha

import json
import socket
import time

HOST = '127.0.0.1'  # Die IP-Adresse des lokalen Hosts, auf dem das Programm lauscht
PORT = 12345        # Der Port, auf dem Daten empfangen werden sollen
BUFFER_SIZE = 1024  # Die maximale Größe eines UDP-Datenpakets in Bytes
DURATION = 60      # Die Dauer (in Sekunden), für die Daten empfangen werden
MAX_PACKETS = 1000  # Die maximale Anzahl von Paketen, die verarbeitet werden


def ballon_bewegen():	
	pygame.init()
	background = pygame.image.load("Hintergrundbild.png")
	
	#screen erzeugen
	window_width = 600
	window_height = 800
	window = pygame.display.set_mode((window_width, window_height))
	
	
	#bewegung 
	threshold = 50 # Schwellenwert
	speed = 2 # Geschwindigkeit der Bewegung
	direction = 0 #-1 für nach oben, 1 für nach unten
	base_y = 400 # Maximalhöhe des Ballons
	
	clock = pygame.time.Clock() #geschwindigkeit regulieren
	running = True #solange true, läuft das spiel
	#eventschleife

	#hierhin udp-stream 

	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket ist bereit daten zu empfangen
	udp_socket.bind((HOST, PORT)) 

	alpha_values = [] # liste in der alle aufgenommenen daten gespeichert werden
	start_time = time.time()

	

	while running and (time.time() - start_time) < DURATION and len(alpha_values) < MAX_PACKETS:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
	# falls escape taste gedrückt - fenster geschlossen
	
			elif event.type ==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False 
		
		data, schleifenvariable = udp_socket.recvfrom(BUFFER_SIZE) # ist udp packet vom netzwerkstream und fängt daten auf 
		message = json.loads(data.decode('utf-8')) # daten als json stream geliefert und in python objekt konvertiert

	# Alpha-Wert bei Index 2 hinzufügen
		alpha_values.append(message["data"][2]) # gibt wert der liste zurük, nimmt zweiten index raus(nur alpha), bekommt packet und nimmt sich alphawert und fügt ihn am ende der liste hinzu
	
		value = calculate_average_alpha #wert aus durchscnittsrechnung abrufen
		max_y1 = base_y - (value*1,5) # je größer value, desto höher geht der kreis, zielhöhe mit alpha values berechnen
		max_y2 = max(50, min(max_y, base_y)) #begrenzung zwischen 50 und base_y -> kreis bewegt sich nicht aus dem bild raus
		if max_y1 > max_y2:
			max_y = max_y2
		else:
			max_y = max_y1

		if value > threshold:
			direction == -1 and y < max_y
			y -= speed 
		elif direction == 1 and y < base_y: #nach unten zur grundhöhe
			y +=speed
			
		window.fill((0, 200, 0))
			
		
		pygame.draw.ellipse(window, "red" , [10,30,150,150], 1) # kreis zeichnen, Position, Nummer hinten steht für dicke der Umrandung
		pygame.display.update()
			
		clock.tick(30) #Schleife wird max 30x pro sekunde durchgelaufen -> kreis bewegt sich gleichmäßig
		pygame.display.flip() #bildschirm mit neuesten änderungen wird aktualisiert
		if((time.time() - start_time) >= DURATION and len(alpha_values) >= MAX_PACKETS):
			erfolg = "Super! Du hast es geschafft, ruhig und entspannt zu bleiben"


pygame.quit()
# Schließen des UDP-Socket, da er nicht mehr benötigt wird
udp_socket.close()
