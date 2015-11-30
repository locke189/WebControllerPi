/* Simple Serial ECHO script : Written by ScottC 03/07/2012 */

#include "DHT.h" //cargamos la librería DHT
#define DHTPIN 11 //Seleccionamos el pin en el que se //conectará el sensor
#define DHTTYPE DHT11 //Se selecciona el DHT11 (hay //otros DHT)
DHT dht(DHTPIN, DHTTYPE); //Se inicia una variable que será usada por Arduino para comunicarse con el sensor

/* Use a variable called byteRead to temporarily store
   the data coming from the computer */
int byteRead;
boolean laser;
boolean thisDevice;
int thisDeviceNumber;
float humidity;
float temperature;

void setup() {                
// Turn the Serial Protocol ON
  Serial1.begin(9600);
  Serial.begin(9600);
  pinMode (12, OUTPUT);
  digitalWrite (12, LOW);
  pinMode (13, OUTPUT);
  digitalWrite (13, LOW);
  
  dht.begin(); //Se inicia el sensor
  
  laser = false;
  thisDeviceNumber = 0x41; //device "A"
}

void loop() {
 

   /*  check if data has been sent from the computer: */
  if (Serial1.available()) {
    /* read the most recent byte */

   byteRead = Serial1.read();
    /*ECHO the value that was read, back to the serial port. */

   //handshake
   if ((byteRead == thisDeviceNumber) && (thisDevice == false)){
    thisDevice = true;
    digitalWrite (13, HIGH);
    Serial1.write(thisDeviceNumber);
    }

   //operation "0" laser toggle hex30 
   if( (byteRead == 0x30) && (thisDevice == true) && (laser == false) ){
    
         digitalWrite (12, HIGH);
         Serial1.write(0x30);
         laser = true;
         thisDevice = false;
         digitalWrite (13, LOW);
    }
    
    if( (byteRead == 0x30) && (thisDevice == true) && (laser == true) ){
    
         digitalWrite (12, LOW);
         Serial1.write(0x31);
         laser = false;
         thisDevice = false;
         digitalWrite (13, LOW);
    }

    //operation "1" hex31 read laser status 
    if( (byteRead == 0x31) && (thisDevice == true) ){   
         Serial1.println(laser);
         thisDevice = false;
         digitalWrite (13, LOW);
    }


    //operation 2 => hex 32 read temperature value
    if( (byteRead == 0x32) && (thisDevice == true) ){
         //read temperature/humidity data
         temperature = dht.readTemperature() - 7; //Se lee la temperatura - offset
         Serial.println(temperature);
         Serial1.println(temperature);
         thisDevice = false;
         digitalWrite (13, LOW);
    }

     //operation 3 => hex 33 read humidity value
    if( (byteRead == 0x33) && (thisDevice == true) ){
         humidity = dht.readHumidity(); //Se lee la humedad
         Serial.println(humidity);
         Serial1.println(humidity);
         thisDevice = false;
         digitalWrite (13, LOW);
    }

    //no actions available 
    if(byteRead != 0x74){
      //Serial1.write(0x40);
      //thisDevice = false;
      }
  
  
  }
}

