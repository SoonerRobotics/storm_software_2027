#pragma once
#include <memory>
#include <stdlib_noniso.h>

#include "StormMessage.hpp"


// configuration parameters -- throw these in a struct?
int16_t linear_velocity_scaler = 3000; // ID 11
int16_t rotational_velocity_scaler = 3500; // ID 12
int16_t motor_velocity_scaler = 100; // ID 13 RENAME because we will have other motors one day
int16_t motor_voltage_scaler = 2500; // ID 14
uint8_t battery_voltage_scaler = 18; // ID 15


class StormBus {
public:
    /**
     * TODO: document
     */
    StormBus(Address address, SerialUART* serial, int txPin, int rxPin, int builtin_led_pin, bool useRS485 = true) {
        this->address = address;
        
        this->serialObj = serial;
        
        this->txEnablePin = txPin;
        this->rxEnablePin = rxPin;
        this->BUILTIN_LED_PIN = builtin_led_pin;

        this->useRS485 = useRS485;
    }

    ~StormBus() {
        this->serialObj->end();

        //TODO: anything else here?
    }

    /**
     * TODO: document
     */
    bool Init() {
        this->serialObj->begin(BAUD_RATE);

        pinMode(this->rxEnablePin, OUTPUT);
        pinMode(this->txEnablePin, OUTPUT);

        if (address > Address::computer) {
            // enable receiving messages
            digitalWrite(this->rxEnablePin, LOW);
        }
        
        // indicate that we connecteds
        digitalWrite(this->BUILTIN_LED_PIN, HIGH);

        return true;
    }

    /**
     * TODO: document
     */
    //TODO: rename this to uint8_t GetMessage() and have it return the address
    // or alternatively name it like PollForMessage() or TryReceiveMessage() or something
    bool HasMessage() {
        Address tempAddress;
        Message tempType;
        uint8_t tempSize;
        char tempDATA[16];

        if (this->isTransmitting) {
            return false;
        }
        
        //TODO: do we need to enable receive pin here?

        // minimum message size, according to spec, is 6 bytes
        if (this->serialObj->available() < this->MIN_MSG_SIZE) {
            return false;
        }
        
        // check for start byte (0xAA)
        bool foundMsg = false;
        while (this->serialObj->peek() != -1) {
            if (this->serialObj->read() == this->START_BYTE) {
                foundMsg = true;
                break;
            }
        }

        if (!foundMsg) {
            return false;
        }

        //FIXME: I don't think we need all these peek() calls, like, we already checked serial.available()

        // next byte is address
        if (this->serialObj->peek() != -1) {
            tempAddress = static_cast<Address>(this->serialObj->read());

            // handle broadcast messages (like heartbeat)
            if (tempAddress == Address::all) {
                //TODO handle heartbeat

                return false; // ???
            } else if (tempAddress != this->address) {
                return false;
            }
        }

        // next byte is type
        if (this->serialObj->peek() != -1) {
            tempType = static_cast<Message>(this->serialObj->read());
        }

        // next byte is size
        if (this->serialObj->peek() != -1) {
            tempSize = static_cast<uint8_t>(this->serialObj->read());

            // maximum message size is 16 according to the spec
            if (tempSize < 0 || tempSize > this->MAX_MSG_SIZE) {
                return false;
            }
        }

        // next SIZE bytes are data
        for (int i = 0; i < tempSize; i++) {
            tempDATA[i] = this->serialObj->read();
        }

        // read stop byte
        if (this->serialObj->peek() != -1) {
            if (this->serialObj->read() != this->END_BYTE) {
                return false;
            }
        }

        //FIXME this will conflict with like, the address variable we should do something
        this->address = tempAddress;
        this->size = tempSize;
        this->type = tempType;

        // transfer DATA too
        for (int i = 0; i < this->size; i++) {
            DATA[i] = tempDATA[i];
        }

        // if we made it this far, we have a message
        digitalWrite(this->BUILTIN_LED_PIN, this->debugBlink ? HIGH : LOW);
        this->debugBlink = !this->debugBlink;

        return true;
    }

    /**
     * Get a StormMessage object.
     * Once you've identified that there's a message for you (via HasMessage()),
     * use this to get the message object.
     * then check the message's type/ID to see which one it is,
     * then use the various msg.AsMessgeType() functions to get a struct.
     * alternatively you can work with the raw DATA[] array, if you know what you're doing.
     */
    StormMessage GetMessage() {
        // create the message object from the stored information
        StormMessage msg = StormMessage(this->type, this->address, this->size, this->DATA);

        return msg;
    }

    /**
     * Send a response back to the robot's computer.
     * Use this function to SEND messages FROM your board.
     */
    bool SendResponse(StormMessage msg) {
        // start transmission
        this->isTransmitting = true;
        digitalWrite(this->txEnablePin, HIGH);
        delayMicroseconds(50);

        // write start byte
        this->serialObj->write(this->START_BYTE);

        // write address (always computer for a response)
        this->serialObj->write(msg.address);

        // write message ID
        this->serialObj->write(msg.type);

        // write size
        this->serialObj->write(msg.size);

        // finally write the data
        for (int i = 0; i < msg.size; i++) {
            this->serialObj->write(msg.DATA[i]);
        }

        // write end byte
        this->serialObj->write(this->END_BYTE);

        // wait for entire buffer to send
        this->serialObj->flush();

        delayMicroseconds(50);
        digitalWrite(this->txEnablePin, LOW);
        this->isTransmitting = false;

        return true; // return true on success
    }

private:
    // === protocol definitions ===
    const char START_BYTE = 0xAA;
    Address address = Address::all;
    uint8_t size = 255;
    Message type = Message::None;
    char DATA[16]; //FIXME ???
    const char END_BYTE = 0x55;
    const unsigned int BAUD_RATE = 115200;

    const uint8_t MAX_DATA_SIZE = 12;
    const uint8_t MIN_DATA_SIZE = 1;
    const uint8_t MAX_MSG_SIZE = 16;
    const uint8_t MIN_MSG_SIZE = 6;
    // ============================

    // pins
    bool useRS485 = true; // disable when testing over USB serial
    SerialUART* serialObj;
    int txPin = 0;
    int rxPin = 0;
    int txEnablePin = 0;
    int rxEnablePin = 0;
    bool isTransmitting = false;
    int BUILTIN_LED_PIN = 25; // default on Pico 2
    bool debugBlink = false;
};