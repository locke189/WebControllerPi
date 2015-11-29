/* Simple Serial ECHO script : Written by ScottC 03/07/2012 */

/* Use a variable called byteRead to temporarily store
   the data coming from the computer */
int byteRead;
boolean laser;
boolean thisDevice;
int thisDeviceNumber;

void setup() {                
// Turn the Serial Protocol ON
  Serial1.begin(9600);
  pinMode (12, OUTPUT);
  digitalWrite (12, LOW);
  pinMode (13, OUTPUT);
  digitalWrite (13, LOW);
  
  
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

   //operation "0" laser toggle 
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


    

    //no actions available 
    if(byteRead != 0x74){
      //Serial1.write(0x40);
      //thisDevice = false;
      }
  
  
  }
}

