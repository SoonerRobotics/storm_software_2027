#include "StormBus.hpp"

// === define pins (GPIO #) ===
// #define UART0_TX 0
// #define UART0_RX 1

#define TX_ENABLE_PIN 2
#define RX_ENABLE_PIN 3

#define DEBUG_LED1 5
#define DEBUG_LED2 6

#define PICO_DEBUG_LED 25

#define BATTERY_VOLTAGE 28
// === /pins ===


// === STORM Bus ===
// serial1 defaults to GPIO0 and GPIO1, might need to call
// Serial1.setPins() to change them if your board is different.
// also change the Address to be specific to your board.
StormBus bus = StormBus(Address::all, &Serial1, TX_ENABLE_PIN, RX_ENABLE_PIN, PICO_DEBUG_LED, false);
StormMessage msg;
// =================

void setup() {
    // start communication
    bus.Init();
}


void loop() {
    // if there is a message addressed to us
    if (bus.HasMessage()) {
        // get the message
        msg = bus.GetMessage();

        // and do something diffrent based on what message it is
        switch (msg.type) {
            // standard messages everyone receives
            case Configuration: {
                auto converted = msg.AsConfiguration();

                // bus.CONFIG[converted.ID] = converted.value;

                //TODO: if there are PID constants n stuff then update the drivebase object
                
                break;
            }
            case ConfigComplete: {
                auto converted = msg.AsConfigurationComplete();
                
                break;
            }
            case RobotVelocity: {
                auto converted = msg.AsRobotVelocity();
                
                break;
            }
            case DriveVelocity: {
                auto converted = msg.AsDriveVelocity();
                
                break;
            }
            case DriveVoltage: {
                auto converted = msg.AsDriveVoltage();

                // spec calls for instantaneous voltage, though we might want to sample it and keep a rolling average maybe
                // uint8_t battVoltage = (analogRead(BATTERY_VOLTAGE) / (3.3f * 12.0f));
                
                break;
            }
            case DriveRaw: {
                auto converted = msg.AsDriveRaw();
                
                break;
            }
            case ComputerRequest: {
                auto converted = msg.AsRequest();

                uint8_t tempSize = 0;
                char* tempData[16];

                // we need to send a message back to the computer. we are only responsible for 2 responses:
              

                // StormMessage response = StormMessage(converted.ID, Address::computer, tempSize, tempData);
                // bus.SendResponse(response);

                break;
            }
            default:
                // message doesn't concern us, don't do anything
                break;
        }
    }

    // any sort of other periodic functions go here

    // ===== debug LEDs =====
}