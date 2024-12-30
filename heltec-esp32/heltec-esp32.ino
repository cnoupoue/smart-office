#include <WiFi.h>
#include <Wire.h>
#include "HT_SSD1306Wire.h"
#include <HardwareSerial.h>
#include "LoRaWan_APP.h"
#include "Arduino.h"
#include <cstring>

// VARIABLES
#define RX_PIN 3  // RX pin connected to TX of RFID module
#define TX_PIN 1  // TX pin connected to RX of RFID module
#define RF_FREQUENCY                                868100000 // Hz

// OTHER VARIABLES
#define OLED_UPDATE_INTERVAL 500
static SSD1306Wire  display(0x3c, 500000, SDA_OLED, SCL_OLED, GEOMETRY_128_64, RST_OLED);
HardwareSerial RFID(2); // Use UART2

#define TX_OUTPUT_POWER                             5        // dBm
#define LORA_BANDWIDTH                              0         // [0: 125 kHz,
#define LORA_SPREADING_FACTOR                       7         // [SF7..SF12]
#define LORA_CODINGRATE                             1         // [1: 4/5,
#define LORA_PREAMBLE_LENGTH                        8         // Same for Tx and Rx
#define LORA_SYMBOL_TIMEOUT                         0         // Symbols
#define LORA_FIX_LENGTH_PAYLOAD_ON                  false
#define LORA_IQ_INVERSION_ON                        false
#define RX_TIMEOUT_VALUE                            1000
#define BUFFER_SIZE                                 30 // Define the payload size here
char txpacket[BUFFER_SIZE];
char rxpacket[BUFFER_SIZE];
double txNumber;
bool lora_idle=true;
static RadioEvents_t RadioEvents;
void OnTxDone( void );
void OnTxTimeout( void );

void setup() {
  // Configure LoRa
  Serial.begin(115200);
  Mcu.begin(HELTEC_BOARD,SLOW_CLK_TPYE);

  txNumber=0;

  RadioEvents.TxDone = OnTxDone;
  RadioEvents.TxTimeout = OnTxTimeout;
  
  Radio.Init( &RadioEvents );
  Radio.SetChannel( RF_FREQUENCY );
  Radio.SetTxConfig( MODEM_LORA, TX_OUTPUT_POWER, 0, LORA_BANDWIDTH,
                                  LORA_SPREADING_FACTOR, LORA_CODINGRATE,
                                  LORA_PREAMBLE_LENGTH, LORA_FIX_LENGTH_PAYLOAD_ON,
                                  true, 0, 0, LORA_IQ_INVERSION_ON, 3000 ); 

  // Configure RFID
  display.init();
  display.flipScreenVertically();
  display.clear();
  display.display();
  
  display.setContrast(255);
  Serial.begin(115200);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  char* data = readRFID();
  if (data == nullptr) {
    display.clear();
    display.drawString(0, 0, "Scan incorrecte.");
    display.drawString(0, 10, "Réessayez.");
    display.display();
    delay(2000);
  } else if (strlen(data) > 0) {
    display.clear();
    display.drawString(0, 0, "Accès accordé.");
    display.display();
    sendMessage(data);
    delay(2000);
  }
  delay(200);
}

char* readRFID() {
  display.clear();
  display.drawString(0, 0, "En attente de la carte...");
  display.display();

  RFID.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN); // Initialize RFID serial
  static char rfidData[50]; // Use a static buffer to store the RFID data
  int index = 0;

  // Clear the buffer before reading
  memset(rfidData, 0, sizeof(rfidData));

  // Wait for the RFID data to be available
  if (RFID.available()) {
    while (RFID.available()) {
      char c = RFID.read();
      rfidData[index++] = c; // Store each character in rfidData
      if (index >= sizeof(rfidData) - 1) break; // Prevent buffer overflow
    }

    // Check the known prefixes and return the matched value
    if (checkRFIDPrefix(rfidData, "270042412501")) {
      return rfidData; // Return the matched RFID data
    } 
    else if (checkRFIDPrefix(rfidData, "0000AEC66800")) {
      return rfidData; // Return the matched RFID data
    }
    else {
      // If the RFID data doesn't match the known values, return null
      return nullptr;
    }
  }

  return ""; // Return nullptr if no data is read
}

bool checkRFIDPrefix(char* rfidData, const char* prefix) {
  if (strstr(rfidData, prefix) != NULL) {
    // Null-terminate the string after the matched prefix
    rfidData[strlen(prefix)] = '\0';
    
    // Display the matched RFID data
    // display.clear();
    // display.drawString(0, 0, "RFID card detected:");
    // display.drawString(0, 10, rfidData); // Show the known part of the RFID data on the display
    // display.display();
    
    return true; // Return true when prefix matches
  }
  return false; // Return false if prefix does not match
}


void sendMessage(const char* message) {
  // prefix
  char prefix[] = "smartoffice:"; 
  char result[256];
  strcpy(result, prefix); 
  strcat(result, message);
  // if(lora_idle == true) {
		txNumber += 0.01;
		sprintf(txpacket,result);  //start a package
		Serial.printf("\r\nsending packet \"%s\" , length %d\r\n",txpacket, strlen(txpacket));
		Radio.Send( (uint8_t *)txpacket, strlen(txpacket) ); //send the package out	
    // lora_idle = false;
	// }
  Radio.IrqProcess( );
}

void OnTxDone( void )
{
	Serial.println("TX done......");
	lora_idle = true;
}

void OnTxTimeout( void )
{
    Radio.Sleep( );
    Serial.println("TX Timeout......");
    lora_idle = true;
}
