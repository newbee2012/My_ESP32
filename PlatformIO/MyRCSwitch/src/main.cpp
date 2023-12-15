/*
  Simple example for receiving
  
  https://github.com/sui77/rc-switch/
*/


//#include <Arduino.h>
#include <RCSwitch.h>
#include <RH_ASK.h>
#ifdef RH_HAVE_HARDWARE_SPI
#include <SPI.h> // Not actually used but needed to compile
#endif
#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
RCSwitch receSwitch = RCSwitch();
RCSwitch sendSwitch = RCSwitch();
#define PIN_RECE_ID 34
#define PIN_SEND_ID 32

//RH_ASK driver(2000, PIN_RECE_ID, PIN_SEND_ID,0); // ESP8266 or ESP32: do not use pin 11 or 2

static const char* bin2tristate(const char* bin);
static char * dec2binWzerofill(unsigned long Dec, unsigned int bitLength);

void output(unsigned long decimal, unsigned int length, unsigned int delay, unsigned int* raw, unsigned int protocol) {

  const char* b = dec2binWzerofill(decimal, length);
  Serial.print("Decimal: ");
  Serial.print(decimal);
  Serial.print(" (");
  Serial.print( length );
  Serial.print("Bit) Binary: ");
  Serial.print( b );
  Serial.print(" Tri-State: ");
  Serial.print( bin2tristate( b) );
  Serial.print(" PulseLength: ");
  Serial.print(delay);
  Serial.print(" microseconds");
  Serial.print(" Protocol: ");
  Serial.println(protocol);
  
  Serial.print("Raw data: ");
  for (unsigned int i=0; i<= length*2; i++) {
    Serial.print(raw[i]);
    Serial.print(",");
  }
  Serial.println();
  Serial.println();
}

static const char* bin2tristate(const char* bin) {
  static char returnValue[50];
  int pos = 0;
  int pos2 = 0;
  while (bin[pos]!='\0' && bin[pos+1]!='\0') {
    if (bin[pos]=='0' && bin[pos+1]=='0') {
      returnValue[pos2] = '0';
    } else if (bin[pos]=='1' && bin[pos+1]=='1') {
      returnValue[pos2] = '1';
    } else if (bin[pos]=='0' && bin[pos+1]=='1') {
      returnValue[pos2] = 'F';
    } else {
      return "not applicable";
    }
    pos = pos+2;
    pos2++;
  }
  returnValue[pos2] = '\0';
  return returnValue;
}

static char * dec2binWzerofill(unsigned long Dec, unsigned int bitLength) {
  static char bin[64]; 
  unsigned int i=0;

  while (Dec > 0) {
    bin[32+i++] = ((Dec & 1) > 0) ? '1' : '0';
    Dec = Dec >> 1;
  }

  for (unsigned int j = 0; j< bitLength; j++) {
    if (j >= bitLength - i) {
      bin[j] = bin[ 31 + i - (j - (bitLength - i)) ];
    } else {
      bin[j] = '0';
    }
  }
  bin[bitLength] = '\0';
  
  return bin;
}


void recv_rcswitch(){
  if (receSwitch.available()) {
    output(receSwitch.getReceivedValue(), receSwitch.getReceivedBitlength(), receSwitch.getReceivedDelay(), receSwitch.getReceivedRawdata(),receSwitch.getReceivedProtocol());
    receSwitch.resetAvailable();
  }
}

// void recv_radiohead()
// {
//   uint8_t buf[RH_ASK_MAX_MESSAGE_LEN];
//   uint8_t buflen = sizeof(buf);

//   if (driver.recv(buf, &buflen)) // Non-blocking
//   {
//       int i;

//       // Message with a good checksum received, dump it.
//       driver.printBuffer("Got:", buf, buflen);
//       Serial.println("Received data! ");
//   }
// }

void recv_basic(){
  int value = digitalRead(PIN_RECE_ID);
  Serial.println(value);
}

void RecvFunction(void *pvParameters) {
  (void) pvParameters; // 仅为了避免编译器警告
  Serial.println("Received thread started! ");
  while(1){
      recv_rcswitch();
      //recv_radiohead();
      delay(1); // 任务延时
  }
}

struct Signal {
    int level;
    int duration;
};

std::vector<Signal> signals = {
    // Signal  放
        {1, 200},{0, 550},
        {1, 200},{0, 550},
        {1, 200},{0, 550},
        {1, 200},{0, 550},
        {1, 200},{0, 550},
        {1, 200},{0, 550},
        {1, 200},{0, 550},
        {1, 200},{0, 550},
        {1, 200},{0, 550},
        {1, 200},{0, 550},
        {1, 2000},{0, 550},
        {1, 200},{0, 550},//1
        {1, 200},{0, 550},//2
        {1, 500},{0, 550},//3
        {1, 200},{0, 550},//4
        {1, 500},{0, 550},//5
        {1, 200},{0, 550},//6
        {1, 200},{0, 550},//7
        {1, 500},{0, 550},//8
        {1, 200},{0, 550},//9
        {1, 200},{0, 550},//10
        {1, 200},{0, 550},//11
        {1, 500},{0, 550},//12
        {1, 200},{0, 550},//13
        {1, 200},{0, 550},//14
        {1, 500},{0, 550},//15
        {1, 200},{0, 550},//16
        {1, 200},{0, 550},//17
        {1, 200},{0, 550},//18
        {1, 200},{0, 550},//19
        {1, 200},{0, 550},//20
        {1, 200},{0, 550},//21
        {1, 200},{0, 550},//22
        {1, 200},{0, 550},//23
        {1, 500},{0, 550},//24
        {1, 200},{0, 550},//25
        {1, 200},{0, 550},//26
        {1, 500},{0, 550},//27
        {1, 500},{0, 550},//28
        {1, 500},{0, 550},//29
        {1, 200},{0, 550},//30
        {1, 500},{0, 550},//31
        {1, 200},{0, 550},//32  
        {1, 500},{0, 4700} //syncFactor

      // Signal  收
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 2000},{0, 550},
        // {1, 200},{0, 550},//1
        // {1, 200},{0, 550},//2
        // {1, 500},{0, 550},//3
        // {1, 200},{0, 550},//4
        // {1, 500},{0, 550},//5
        // {1, 200},{0, 550},//6
        // {1, 200},{0, 550},//7
        // {1, 500},{0, 550},//8
        // {1, 200},{0, 550},//9
        // {1, 200},{0, 550},//10
        // {1, 200},{0, 550},//11
        // {1, 500},{0, 550},//12
        // {1, 200},{0, 550},//13
        // {1, 200},{0, 550},//14
        // {1, 500},{0, 550},//15
        // {1, 200},{0, 550},//16
        // {1, 200},{0, 550},//17
        // {1, 200},{0, 550},//18
        // {1, 200},{0, 550},//19
        // {1, 200},{0, 550},//20
        // {1, 200},{0, 550},//21
        // {1, 200},{0, 550},//22
        // {1, 500},{0, 550},//23
        // {1, 200},{0, 550},//24
        // {1, 200},{0, 550},//25
        // {1, 200},{0, 550},//26
        // {1, 500},{0, 550},//27
        // {1, 500},{0, 550},//28
        // {1, 500},{0, 550},//29
        // {1, 200},{0, 550},//30
        // {1, 200},{0, 550},//31
        // {1, 500},{0, 550},//32  
        // {1, 500},{0, 4700} //syncFactor
      
      //刹车
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 200},{0, 550},
        // {1, 2000},{0, 550},
        // {1, 200},{0, 550},//1
        // {1, 200},{0, 550},//2
        // {1, 500},{0, 550},//3
        // {1, 200},{0, 550},//4
        // {1, 500},{0, 550},//5
        // {1, 200},{0, 550},//6
        // {1, 200},{0, 550},//7
        // {1, 500},{0, 550},//8
        // {1, 200},{0, 550},//9
        // {1, 200},{0, 550},//10
        // {1, 200},{0, 550},//11
        // {1, 500},{0, 550},//12
        // {1, 200},{0, 550},//13
        // {1, 200},{0, 550},//14
        // {1, 500},{0, 550},//15
        // {1, 200},{0, 550},//16
        // {1, 200},{0, 550},//17
        // {1, 200},{0, 550},//18
        // {1, 200},{0, 550},//19
        // {1, 200},{0, 550},//20
        // {1, 200},{0, 550},//21
        // {1, 200},{0, 550},//22
        // {1, 200},{0, 550},//23
        // {1, 200},{0, 550},//24
        // {1, 200},{0, 550},//25
        // {1, 200},{0, 550},//26
        // {1, 500},{0, 550},//27
        // {1, 500},{0, 550},//28
        // {1, 500},{0, 550},//29
        // {1, 200},{0, 550},//30
        // {1, 500},{0, 550},//31
        // {1, 500},{0, 550},//32  
        // {1, 500},{0, 4700} //syncFactor
    };


void send_basic(){
  int n = signals.size();
    while(1){
    for(int i=0; i<n; i++){
      Signal& signal = signals[i];
      digitalWrite(PIN_SEND_ID, signal.level);
      delayMicroseconds(signal.duration);
    }
  }

  //delay(500);
  //digitalWrite(PIN_SEND_ID, HIGH);
  //delayMicroseconds(100);
  //digitalWrite(PIN_SEND_ID, LOW);
  //delayMicroseconds(100);
}

void send_rcswitch(){
  /* See Example: TypeA_WithDIPSwitches */
  //sendSwitch.switchOn("11111", "00010");
  // delay(1000);
  // sendSwitch.switchOff("11111", "00010");
  // delay(1000);

  /* Same switch as above, but using decimal code */
  //sendSwitch.send(44444444, 32);

  /* Same switch as above, but using binary code */
  sendSwitch.send("000000000001010100010001");
  //delay(1000);  
  //sendSwitch.send("000000000001010100010100");
  // delay(1000);

  // /* Same switch as above, but tri-state code */ 
  // sendSwitch.sendTriState("00000FFF0F0F");
  // delay(1000);  
  // sendSwitch.sendTriState("00000FFF0FF0");
  // delay(1000);

  delay(1);
}

// void send_radiohead(){
//     const char *msg = "hello";
//     driver.send((uint8_t *)msg, strlen(msg));
//     driver.waitPacketSent();
//     delay(1000);
// }

void send(){
  send_rcswitch();
  //send_radiohead();
  //send_basic();
}

void setup() {
  Serial.begin(115200);
  int rc_switch_protocol = 1;
  sendSwitch.setRepeatTransmit(3);
  sendSwitch.setProtocol(rc_switch_protocol);
  receSwitch.setProtocol(rc_switch_protocol);
  pinMode(PIN_RECE_ID, INPUT);
  pinMode(PIN_SEND_ID, OUTPUT);
  //if (!driver.init())
  //        Serial.println("init failed");
  //driver.setModeRx();
  //driver.setModeTx();
  receSwitch.enableReceive(PIN_RECE_ID);
  sendSwitch.enableTransmit(PIN_SEND_ID);
  
  xTaskCreate(
    RecvFunction, // 任务函数
    "Task1",      // 任务名称
    2048,         // 栈大小
    NULL,         // 任务输入参数
    1,            // 任务优先级
    NULL        // 任务句柄
    );           // 指定要在哪个核心上运行，0是ESP32的核心ID
}

void loop() {
    send();
}
