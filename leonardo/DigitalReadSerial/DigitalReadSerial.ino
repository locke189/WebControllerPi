/* Sensor and actuator controller 2015/11 by Juan Insuasti*/
/* FIRMWARE = V0.1

/* HARDWARE
 *    -ARDUINO LEONARDO
 */

/* 
 *  Contents
 *  
 *  $001$ Includes and defines
 *  $002$ Global Variable Definitions
 *  $003$ Setup and Initialization
 *  $005$ Function Definitions
 *  $006$ Main loop
 *     
 */


/* $001$ Includes and defines */

//Temperature and Humidity Sensor definitions DHT11
#include "DHT.h"            //Loading of  DHT
#define   DHTPIN     11     //DHT Sensor PIN
#define   DHTTYPE    DHT11  //Sensor type selection DHT11 (There are other DHT sensors)
DHT dht(DHTPIN, DHTTYPE);   //declaration of DHT object

//Serial Port Definitions
#define   SOH     0x01
#define   EOT     0x04
#define   RS      0x1E

 
//Device definitions
#define   LASER_ON      0x2B
#define   LASER_OFF     0x2D
#define   DEVICE_ID     0x41

//Sensor definitions
#define   SUMMARY         0x2F
#define   LASER_TOGGLE    0x30
#define   LASER_STATUS    0x31
#define   LASER_ID        0x30
#define   TEMPERATURE_ID  0x32
#define   TEMP_OFFSET     7     // Offset debido al error de medicion
#define   HUMIDITY_ID     0x33
#define   DHT_POLL        5     // Poll sensor data each 5 interrupts
#define   SENSOR_TIME     10000 // 10 seconds
//Sensor/actuator pins
#define LASER_PIN     12
#define BOARD_LED     13


//Serial parameters
#define BITRATE       57600

//Timer settings
#define TIMEOUT       5000 // 5 seg


/*   $002$ Global Variable Definitions */

/* Use a variable called byteRead to temporarily store
   the data coming from the computer */

// Serial Data
int byteRead;
String serialData;

//Actuator Flags
boolean   laser_state = false;


//Sensor Variables and flags
float     humidity = 0;
float     temperature = 0;

//Device Info and flags
boolean  volatile deviceEnabled = false;
boolean volatile  timeout = false;
String    dataStream;
int     volatile interruptCounter = 0;

//Time
unsigned long volatile timeStamp = 0;
unsigned long volatile sensor_timeStamp = 0;


/* $003$ Setup and Initialization  */


//------Setup Functions---------

void setup() {                
// Turn the Serial Protocol ON
  Serial1.begin(BITRATE);
  Serial.begin(BITRATE);

//Laser pin 12
  pinMode(LASER_PIN, OUTPUT);
  digitalWrite(LASER_PIN, LOW);

//Enable signal to internal LED pin 13
  pinMode(BOARD_LED, OUTPUT);
  digitalWrite(BOARD_LED, LOW);

//DHT sensor initialization
  dht.begin(); //Se inicia el sensor


  sensor_timeStamp = millis();
}

//------------------------------------------



/*    $005$ Function Definitions */

void activateDevice(void){
  deviceEnabled  = true;
  digitalWrite(BOARD_LED, HIGH);
  }


void deactivateDevice(void){
  deviceEnabled = false;
  digitalWrite(BOARD_LED, LOW);
  }  



//------------------------------------------


/*     $006$ Main loop   */

void loop() {
  /*  check if data has been sent from the master device:  */
  if (Serial1.available()) {
    
    /* read the most recent byte */
    //byteRead = Serial1.read();
    serialData = Serial1.readStringUntil(EOT);


   /* Serial handshake with Master Device */
    if ((serialData[0] == SOH ) && (serialData[1] == DEVICE_ID) && (deviceEnabled == false)){
        activateDevice();
        Serial1.write(DEVICE_ID);
        timeStamp = millis();
     }


   /* Operation "/".  Summary of all sensor data and actuator status */
    if( ( serialData[2] == SUMMARY ) && ( deviceEnabled == true )  ){

          
          //laser state
          Serial1.write(RS);
          Serial1.write(LASER_ID);
          if( laser_state == true ){
            Serial1.write(LASER_ON);
            }
          else{
            Serial1.write(LASER_OFF);
            }
    
          //Temperature
          Serial1.write(RS);
          Serial1.write(TEMPERATURE_ID);
          Serial1.print(temperature);
    
          //Humidity
          Serial1.write(RS);
          Serial1.write(HUMIDITY_ID);
          Serial1.print(humidity);
    
          //end
          Serial1.write(EOT);
      }
  
   
   /*  Operation "0" laser toggle  */ 
    if( (serialData[2] == LASER_TOGGLE) && (deviceEnabled == true) && (laser_state == false) ){
         Serial1.write(LASER_ID);
         Serial1.write(LASER_ON);
         Serial1.write(0x04);
         digitalWrite (LASER_PIN, HIGH);
         laser_state = true;

    }
    
    if( (serialData[2] == LASER_TOGGLE) && (deviceEnabled == true) && (laser_state == true) ){
         Serial1.write(LASER_ID);
         Serial1.write(LASER_OFF);
         Serial1.write(EOT); 
         digitalWrite (LASER_PIN, LOW);
         laser_state = false;
 
    }

    /* Operation "1" hex31 read laser status */
    if( (serialData[2] == LASER_STATUS) && (deviceEnabled == true) ){   
         Serial1.write(LASER_ID);
         if( laser_state == true ){
            Serial1.write(byte(LASER_ON)); 
          }
          else{
            Serial1.write(byte(LASER_OFF));
            }
          
          //Serial1.write(byte(laser_state));

    }


    /* Operation 2 => hex 32 read temperature value */
    if( (serialData[2] == TEMPERATURE_ID) && (deviceEnabled == true) ){
         //read temperature/humidity data
         //temperature       =   dht.readTemperature() - TEMP_OFFSET; //Se lee la temperatura - offset
         Serial1.write(TEMPERATURE_ID);
         Serial1.print(temperature);
         Serial1.write(EOT);

    }

     /* Operation 3 => hex 33 read humidity value   */
    if( (serialData[2] == HUMIDITY_ID) && (deviceEnabled == true) ){
         //humidity = dht.readHumidity();
         Serial1.write(HUMIDITY_ID);
         Serial1.print(humidity);
         Serial1.write(EOT);
    }


     //deactivate device at the end of serial read
     deactivateDevice();

  }


  //Sensor Updates! in main loop
  if ( ((millis() - sensor_timeStamp) >= SENSOR_TIME) || ( ((millis() - sensor_timeStamp) < 0 ) ) ){
    temperature       =   dht.readTemperature();
    humidity = dht.readHumidity(); 
    sensor_timeStamp = millis();
    }


       
}

//--------------------EOF-------------------






