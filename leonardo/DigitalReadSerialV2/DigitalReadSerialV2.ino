/* Sensor and actuator controller 2015/11 by Juan Insuasti*/
/* FIRMWARE = V0.2

/* Updates:
 * Data will be sent periodically to master device, serial read methods will be deprecated.
 */


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


//Actions
#define   SUMMARY         0x2F

//Sensor definitions
#define   TEMPERATURE_ID  0x32
#define   TEMP_OFFSET     7     // Offset debido al error de medicion
#define   HUMIDITY_ID     0x33
#define   DHT_POLL        5     // Poll sensor data each 5 interrupts
#define   PIR0_ID         0x34
#define   PIR0_STATUS     0x34
#define   LIGHT0_ID       0x35
#define   LIGHT0_STATUS   0x35

//Actuator definitions
#include <Servo.h>
#define   SERVO0_ID           0x61
#define   SERVO0_STEP_UP      0x61
#define   SERVO0_STEP_DOWN    0x62
#define   SERVO0_SET          0x63
#define   LASER_ID            0x30
#define   LASER_TOGGLE        0x30
#define   LASER_STATUS        0x31

// Time options
#define   SENSOR_TIME     10000 // 10 seconds
#define   UPDATE_TIME     5000 // 5 seconds

//Sensor/actuator pins
#define LASER_PIN     12
#define BOARD_LED     13
#define SERVO0_PIN     9
#define PIR0_PIN       2
#define LIGHT0_PIN     0


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

// Servos

Servo servo0;
int servo0_pos = 0;


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

//PIR
int pir0;

//Light Analog Sensor
int light0_value = 0;

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

//Servo configuration
  servo0.attach(SERVO0_PIN);

//first timestamp
  sensor_timeStamp = millis();
  timeStamp = millis();

//PIR
  pinMode(PIR0_PIN, INPUT);

//Analog Light Sensor
  pinMode(A0, INPUT);
  
  
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
        Serial1.write(RS);
     }


   /* Operation "/".  Summary of all sensor data and actuator status */
    //if( ( serialData[2] == SUMMARY ) && ( deviceEnabled == true )  ){
      //DEPRECATED
    //  }
   
   /*  Operation "0" laser toggle  */ 
    if( (serialData[2] == LASER_TOGGLE) && (deviceEnabled == true) && (laser_state == false) ){
         Serial1.write(LASER_ID);
         Serial1.write(LASER_ON);
         Serial1.write(RS);
         Serial1.write(EOT);
         digitalWrite (LASER_PIN, HIGH);
         laser_state = true;
         deactivateDevice();

    }
    
    if( (serialData[2] == LASER_TOGGLE) && (deviceEnabled == true) && (laser_state == true) ){
         Serial1.write(LASER_ID);
         Serial1.write(LASER_OFF);
         Serial1.write(RS);
         Serial1.write(EOT); 
         digitalWrite (LASER_PIN, LOW);
         laser_state = false;
         deactivateDevice();
 
    }

    /* Operation "1" hex31 read laser status */
    //if( (serialData[2] == LASER_STATUS) && (deviceEnabled == true) ){   
      // DEPRECATED

    //}


    /* Operation 2 => hex 32 read temperature value */
    //if( (serialData[2] == TEMPERATURE_ID) && (deviceEnabled == true) ){
         //DEPRECATED
    //}

     /* Operation 3 => hex 33 read humidity value   */
    //if( (serialData[2] == HUMIDITY_ID) && (deviceEnabled == true) ){
         //DEPRECATED
    //}


    /* Operation 4 => hex 34 read from PIR*/

    /*SERVO ROUTINES*/

    /*SERVO STEP UP -  5 degrees*/
      if( (serialData[2] == SERVO0_STEP_UP) && (deviceEnabled == true) ){
         servo0_pos += 5;
         if (servo0_pos > 180){
             servo0_pos = 180;
         }
         servo0.write(servo0_pos);
         Serial1.write(SERVO0_ID);
         Serial1.print(servo0_pos);
         Serial1.write(RS);
         Serial1.write(EOT); 
    }

    /*SERVO STEP DOWN -  5 degrees*/
      if( (serialData[2] == SERVO0_STEP_DOWN) && (deviceEnabled == true) ){
         servo0_pos -= 5;
         if (servo0_pos < 0){
             servo0_pos = 0;
         }
         servo0.write(servo0_pos);
         Serial1.write(SERVO0_ID);
         Serial1.print(servo0_pos);
         Serial1.write(RS);
         Serial1.write(EOT); 
    }

    /*SERVO SET -  ? degrees*/
      if( (serialData[2] == SERVO0_SET && (deviceEnabled == true) ) ) {
         int x = 2;
         int pos = 0;
         int num,mult;
         
         while (serialData[x+1]){
              x +=1;
          }
         Serial.print(x);
         for( int i = x ; i >= 3; i -= 1){
            Serial.print("-");
            Serial.print(i);
            Serial.print("/");
            num  = int(serialData[i]) - 48;
            Serial.println(num);
            Serial.print("-");
            mult = int(pow(10,(x-i)));
            pos  = pos + num * mult;
         }

         
         servo0_pos = pos;
         if (servo0_pos < 0){
             servo0_pos = 0;
         }
         else if (servo0_pos > 180){
             servo0_pos = 180;
         }
         
         servo0.write(servo0_pos);
         Serial1.write(SERVO0_ID);
         Serial1.print(servo0_pos);
         Serial1.write(RS);
         Serial1.write(EOT); 
    }



     //deactivate device at the end of serial read
     deactivateDevice();

  }


  //Sensor Updates! in main loop
  if ( ((millis() - sensor_timeStamp) >= SENSOR_TIME) || ( ((millis() - sensor_timeStamp) < 0 ) ) ){
    temperature       =   dht.readTemperature();
    humidity = dht.readHumidity();

    //light also measured
    light0_value = analogRead(LIGHT0_PIN);
    
    //Reset timestamp 
    sensor_timeStamp = millis();
    }

  
  
  
  //Periodic sensor reports

  if ( ((millis() - timeStamp) >= UPDATE_TIME) || ( ((millis() - timeStamp) < 0 ) ) ){

          Serial1.write(DEVICE_ID);
          Serial1.write(RS);
          //laser state
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

          //Servo0
          Serial1.write(RS);
          Serial1.write(SERVO0_ID);
          Serial1.print(servo0_pos);


          //PIR
          Serial1.write(RS);
          Serial1.write(PIR0_ID);
          pir0 = digitalRead(PIR0_PIN);
          Serial1.print(pir0);


          //light sensor
          Serial1.write(RS);
          Serial1.write(LIGHT0_ID);
          Serial1.print(light0_value);
    
          //end
          Serial1.write(RS);
          Serial1.write(EOT);

          timeStamp = millis();
  }
}

//--------------------EOF-------------------






