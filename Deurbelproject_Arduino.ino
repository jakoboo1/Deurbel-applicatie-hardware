//@author Joost

const int flexSensorPin = A0;
int flexSensorValue = 0; 
unsigned long currentMillis = 0; 
unsigned long previousMillis = 0; 
const long interval = 10000; // Interval van 10 seconden tussen het opvangen van het signaal
bool firstTime = true; // Instellen of het de eerste keer is dat het systeem gebruikt wordt om de 10 seconden interval te vermijden

void setup() {
  Serial.begin(9600); // Initialiseren van de Serial communicatie                     
  pinMode(flexSensorPin, INPUT);
}

void loop() {
  currentMillis = millis(); 
  flexSensorValue = analogRead(flexSensorPin);                // Lees de waarde van de flexsensor 
  if (flexSensorValue >= 1020) {                              // Controleren of de waarde van de flexsensor >= 1020
    if(firstTime) {                                           // Controleren of het de eerste keer is dat het systeem gebruikt wordt
      firstTime = false;                                      // Nadat de eerste keer gedetecteerd is deze functie uitschakelen
      Serial.println("Signal detected!");
    } else if (currentMillis - previousMillis >= interval) {  // Controleren of de currentMillis - previousMillis >= aan de interval
      previousMillis = currentMillis;                         // Updaten van de previousMillis
      Serial.println("Signal detected!"); 
    }
  }
}
