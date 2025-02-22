#bilder müssen noch importiert werden siehe emial von mama

import json
import socket
import time
import pygame

pygame.init()

HOST = '127.0.0.1'  # Die IP-Adresse des lokalen Hosts, auf dem das Programm lauscht
PORT = 12345        # Der Port, auf dem Daten empfangen werden sollen
BUFFER_SIZE = 1024  # Die maximale Größe eines UDP-Datenpakets in Bytes
DURATION = 10       # Die Dauer (in Sekunden), für die Daten empfangen werden
MAX_PACKETS = 1000  # Die maximale Anzahl von Paketen, die verarbeitet werden

QUIT = pygame.QUIT
KEYDOWN = pygame.KEYDOWN
K_ESCAPE = pygame.K_ESCAPE


def steigen(): #prozedur
    #neuer stream empfangen

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket ist bereit daten zu empfangen
    udp_socket.bind((HOST, PORT)) 

    alpha_values = [] # liste in der alle aufgenommenen daten gespeichert werden
    start_time = time.time()

    while (time.time() - start_time) < DURATION and len(alpha_values) < MAX_PACKETS:
	

        data, schleifenvariable = udp_socket.recvfrom(BUFFER_SIZE) # ist udp packet vom netzwerkstream und fängt daten auf 
        message = json.loads(data.decode('utf-8')) # daten als json stream geliefert und in python objekt konvertiert

          # Alpha-Wert bei Index 2 hinzufügen
        alpha_values.append(message["data"][2]) # gibt wert der liste zurük, nimmt zweiten index raus(nur alpha), bekommt packet und nimmt sich alphawert und fügt ihn am ende der liste hinzu

          #"spiel" beginnt, also bilder werden angezeigt
        while spielaktiv:
              #überprüfen, ob Nutzer eine Aktion durchgeführt hat
            for event in pygame.event.get():
                #Beenden bei [ESC] oder [X]
                if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                    spielaktiv = False

            frame = 0 #frame o bedeutet, luftballon ist im normalzustand
            fenster.blit(ballon[frame], (10, 10))
            pygame.display.flip()
            clock.tick(FPS)

            if alpha_values > alpha_average*1.1: 
                frame = 1 #frame 1 bedeutet, ballon ist nahe spikes
                fenster.blit(ballon[frame], (10, 10))
                pygame.display.flip()
                clock.tick(FPS)

            if alpha_values > alpha_average*1.2:
                frame = 2 #frame 2 bedeutet, ballon ist zerplatzt
                fenster.blit(ballon[frame], (10, 10))
                pygame.display.flip()
                clock.tick(FPS)
                spielaktiv = false  #hier for-schleife abbrechen und udp stream dann beenden

            if alpha_values<alpha_average:
                frame = 0 #bedeutet, ballon ist im normalzustand=
                fenster.blit(ballon[frame], (10, 10))
                pygame.display.flip()
                clock.tick(FPS)
                

            

    udp_socket.close()
