from machine import UART, Pin, Signal
import time

# Configuration des broches UART
uart = machine.UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1), timeout=5000 )

# Fonction pour envoyer une commande AT et attendre une réponse
def send_at_command(command): # envoie une commande AT et renvoie la réponse du module SIM800L
    uart.write(command + '\r\n')
    time.sleep(0.01)
    response = b''
    while uart.any():
        response += uart.read(1)
    return response.decode('utf-8')

# Fonction pour lire les réponses
#def read_responses():
#    response = b''
#    while uart.any():
#        response += uart.read(1)
#    return response

# Envoi de la commande AT pour lire la date et l'heure


# Lecture de toutes les réponses disponibles
#print("Lecture des réponses")
#response = read_responses()
#print("Réponses reçues:", response.decode())



# Fonction pour récupérer et stocker les informations de date et d'heure
def get_datetime():
    global year, month, day, hour, minute, second, timezone
    response = send_at_command('AT+CCLK?')
    response_str = response.decode('utf-8')
    if '+CCLK: ' in response_str:
        datetime_str = response_str.split('+CCLK: ')[1].strip()
        year = int("20" + datetime_str[0:2]) # Format YYYY lecture caractère 0 inclus à 2 exclus
        month = int(datetime_str[3:5])
        day = int(datetime_str[6:8])
        hour = int(datetime_str[9:11])
        minute = int(datetime_str[12:14])
        second = int(datetime_str[15:17])
        timezone_quarters = int(datetime_str[17:])  # Fuseau horaire en quarts d'heure
        timezone_minutes = timezone_quarters * 15 * 4  # Convertit les quarts d'heure en minutes
        if timezone_minutes >= 0:
            timezone_sign = '+'
        else:
            timezone_sign = '-'
            timezone_minutes = abs(timezone_minutes)
        timezone_hours, timezone_minutes = divmod(timezone_minutes, 60)  # Convertit en heures et minutes
        timezone = "{}{:02d}:{:02d}".format(timezone_sign, timezone_hours, timezone_minutes)
        print("Date:", day, "/", month, "/", year)
        print("Heure:", hour, ":", minute, ":", second)
        print("Fuseau horaire:", timezone)
    else:
        print("Erreur lors de la récupération de la date et de l'heure.")
        
        
print("Envoi de la commande AT pour lire la date et l'heure")
response = send_at_command(b'AT+CCLK?')
print("Réponse:", response.decode())
#get_datetime()


while True:
    at_command = input("Entrez une commande AT (ou 'exit' pour quitter) : ").strip()
    if at_command.lower() == 'exit':
        print("Fin du programme.")
        break
    else:
        response = send_at_command(at_command)
        print("Réponse:", response)



