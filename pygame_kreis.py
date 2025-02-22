
import pygame
from durchschnitt_berechnen import calculate_average_alpha

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
	
	clock = pygame.time.Clock() #geschwindigkeit regulieren
	running = True #solange true, läuft das spiel
	#eventschleife
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
	# falls escape taste gedrückt - fenster geschlossen
	
			elif event.type ==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False 
	
		value = alpha_values() #wert aus durchscnittsrechnung abrufen
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
	pygame.quit()
