import serial
import requests

import mysql.connector as mdb
from datetime import datetime

def getDayOfWeek(dayNumber):
    dayOfWeek = ''
    # Dagen toewijzen aan de nummers - @author Joost
    dayMap = {
        0: 'Maandag',
        1: 'Dinsdag',
        2: 'Woensdag',
        3: 'Donderdag',
        4: 'Vrijdag',
        5: 'Zaterdag',
        6: 'Zondag'
    }

    # Met de get() methode de naam van de dag ophalen
    # Als het nummer van de dag niet bestaat, stuur dan een bericht dat het nummer niet bestaat - @author Joost
    dayOfWeek = dayMap.get(dayNumber, 'Dit nummer bestaat niet')
    return dayOfWeek

# Test de functie getDayOfWeek - @author Joost
# for i in range(7):
#     print(f"{i}: {getDayOfWeek(i)}")

def databaseConnection(host, port, database, user, password):
    # Connectie leggen met de online database - @author Joost
    try:
        conn = mdb.connect(host=host,
                           port=port,
                           database=database,
                           user=user,
                           password=password)
        return conn

    # Stuur een foutmelding op het moment dat er geen connectie kan worden gemaakt met de database -@ author Joost
    except mdb.Error as error:
        print("Error: Er kan geen connectie worden gemaakt met de database")
        print(error)
        return None

# Ophalen van de huidige datum en tijd en deze als variable 'timestamp' opslaan - @author Joost
timestamp = datetime.now()

# Ophalen van de huidige dag van de week uit functie 'getDayofWeek' en deze als variable 'day' opslaan - @author Joost
day = getDayOfWeek(timestamp.weekday())

# Data uit variabelen 'timestamp' en 'day' naar de database toesturen - @author Joost
insertQuery = f"INSERT INTO bezoeken VALUES('','{timestamp}','{day}')"

def sendNotification():
    # De url aanroepen waar de PHP file met de server- en notificatiegegevens opstaan - @author Joost
    serverUrl = "https://projects.adainforma.tk/deurbel/push/"

    # Maak een verzoek naar de server om de gegevens op te halen - @author Joost
    response = requests.get(serverUrl)

    # Print de reactie uit die de server teruggeeft -@ author Joost
    print(response.text)
    print("Status code:", response.status_code)
    if response.status_code == 200:
        print("Notificatie succesvol verstuurd!")
    else:
        print("Fout bij het verzenden van de notificatie")

# for row in result:
#     print(row[1])

# USB-connectie met Arduino - @author Joost
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        # Lees het signaal dat binnenkomt vanaf de Arduino - @author Joost
        signal = ser.readline().decode('utf-8').rstrip()
        print(signal)

        # Als de signaalwaarde == 1, stuur dan de data naar de database en een notificatie naar de gebruiker -@author Joost
        if signal:
            print("Het werkt!")
            conn = databaseConnection('adainforma.tk', 3306, 'projects_deurbel', 'deurbel', '23J7Ft%^-M')
            stm = conn.cursor()
            stm.execute(insertQuery)
            conn.commit()
            sendNotification()

        # Als de signaalwaarde != 1, doe dan niets - @author Joost
        else:
            pass





