#pragma once
#include <stdint.h>

// stolen from https://stackoverflow.com/a/60881515/13722141
int16_t byte_to_int16(char* data) {
    unsigned value = data[0] | ((unsigned)data[1] << 8);
    if (value & 0x8000)
        return -(int)(~value) - 1;
    else
        return value;
}

//TODO: document
uint16_t byte_to_uint16(char* data) {
    uint16_t value = data[0] | (data[1] << 8);
    
    return value;
}

/**
 * Unique number indicating who the message is for.
 * Only the computer (#1) can send messages on its own initiative.
 * If more boards are created, add them after the "Cannon" board.
 * The special address number 0 indicates the message is for all boards.
 */
enum Address {
    all = 0,
    computer = 1,
    traversal = 2,
    cannon = 3,
    none = 4,
};

/**
 * The unique message ID of the message.
 * See the STORM 2027 Serial Specification for which messages carry what data
 */
enum Message { //TODO: rename me?
    // protocol messages
    ComputerRequestMsg = 10;
    HeartbeatMsg = 11;
    ConfigurationCmd = 12;
    ConfigurationCompleteMsg = 13;

    // Traversal board messages
    RobotVelocityCmd = 20;
    DriveVelocitiesCmd = 21;
    DriveVoltageCmd = 22;
    DriveRawCmd = 23;
    DriveFeedbackRsp = 24;
    BatteryVoltageRsp = 25;

    ClimberHeightCmd = 26;
    ClimberVelocityCmd = 27;
    ClimberRawCmd = 28;
    ClimberPositionCmd = 29;
    ClimberSensorRsp = 30;
    ClimberStateRsp = 31;

    // Cannon board messages
    ShooterVelocityCmd = 50;
    ShooterRawCmd = 51;
    ShooterPositionCmd = 52;
    ShooterStateRsp = 53;

    IndexerVelocityCmd = 54;
    IndexerRawCmd = 55;
    IndexerFeedCmd = 56;
    IntakeVelocityCmd = 57;
    IntakeFeedCmd = 58;
    IntakeRawCmd = 59;
    IntakeIndexerRsp = 60;

     // this is special and used for testing only
    DebugeMsg = 255;
};

// ========== message typedef struct definitions ==========

// ID 10
typedef struct Request {
    uint8_t ID;
} Request;

// ID 11
typedef struct HeartbeatMsg {
    char b = 0xFF; //TODO FIXME
} HeartbeatMsg;

// ID 12
typedef struct ConfigurationMsg {
    uint8_t type;
    uint8_t ID;
    char value[6]; //TODO this will only actually be as long as the data type requires though??? need to be pointer???
} ConfigurationMsg;

// ID 13
typedef struct ConfigCompleteMsg {
    uint8_t num_configs;
} ConfigCompleteMsg;

// ID 20
typedef struct RobotVelocityCmd {
    int16_t forward_velocity;
    int16_t sideways_velocity;
    int16_t rotational_velocity;
} RobotVelocityCmd;

// ID 21
typedef struct DriveVelocityCmd {
    int16_t front_left_velocity;
    int16_t front_right_velocity;
    int16_t back_left_velocity;
    int16_t back_right_velocity;
} DriveVelocityCmd;

// ID 22
typedef struct DriveVoltageCmd {
    int16_t front_left_voltage;
    int16_t front_right_voltage;
    int16_t back_left_voltage;
    int16_t back_right_voltage;
} DriveVoltageCmd;

// ID 23
typedef struct DriveRawCmd {
    int16_t front_left_raw;
    int16_t front_right_raw;
    int16_t back_left_raw;
    int16_t back_right_raw;
} DriveRawCmd;

// ID 24
typedef struct DriveFeedbackRsp {
    int16_t forward_velocity;
    int16_t sideways_velocity;
    int16_t rotational_velocity;
    int16_t delta_x;
    int16_t delta_y;
    int16_t delta_theta;
} DriveFeedbackRsp;

// ID 25
typedef struct BatteryVoltageRsp {
    uint8_t voltage;
} BatteryVoltageRsp;

// ID 26
typedef struct ClimberHeightCmd {
    uint8_t height;
} ClimberHeightCmd;

// ID 27
typedef struct ClimberVelocityCmd {
    //FIXME message not fully defined yet
    int16_t climber_one_velocity;
    int16_t climber_two_velocity;
} ClimberVelocityCmd;

// ID 28
typedef struct ClimberRawCmd {
    int16_t climber_one_raw;
    int16_t climber_two_raw;
} ClimberRawCmd;

// ID 29
typedef struct ClimberPositionCmd {
    uint8_t servo_one_position;
    uint8_t servo_two_position;
} ClimberPositionCmd;

// ID 30
typedef struct ClimberSensorRsp {
    bool climber_sensor;
} ClimberSensorRsp;

// ID 31
typedef struct ClimberStateRsp {
    int16_t climber_one_velocity;
    int16_t climber_two_velocity;
    uint8_t climber_height;
    uint8_t servo_one_position;
    uint8_t servo_two_position;
    bool climber_sensor;
} ClimberStateRsp;

// ID 50
typedef struct ShooterVelocityCmd {
    uint16_t shooter_velocity;
} ShooterVelocityCmd;

// ID 51
typedef struct ShooterRawCmd {
    uint16_t shooter_raw;
} ShooterRawCmd;

// ID 52
typedef struct ShooterPositionCmd {
    int16_t turret_angle;
    uint8_t hood_angle;
} ShooterPositionCmd;

// ID 53
typedef struct ShooterStateRsp {
    int16_t shooter_velocity;
    int16_t turret_angle;
    uint8_t hood_angle;
} ShooterStateRsp;

// ID 54
typedef struct IndexerVelocityCmd {
    int16_t indexer_velocity;
} IndexerVelocityCmd;

// ID 55
typedef struct IndexerRawCmd {
    int16_t indexer_raw;
} IndexerRawCmd;

// ID 56
typedef struct IndexerFeedCmd {
    uint8_t num_cannonballs;
} IndexerFeedCmd;

// ID 57
typedef struct IntakeVelocityCmd {
    int16_t intake_velocity;
} IntakeVelocityCmd;

// ID 58
typedef struct IntakeFeedCmd {
    uint8_t num_cannonballs;
} IntakeFeedCmd;

// ID 59
typedef struct IntakeRawCmd {
    int16_t intake_raw;
} IntakeRawCmd;

// ID 60
typedef struct IntakeIndexerRsp {
    int16_t intake_velocity;
    int16_t indexer_velocity;
    char ir_sensor_states;
    uint8_t shot_count;
    uint8_t collected_count;
} IntakeIndexerRsp;

// ID 255
typedef struct DebugeMsg {
    char[16] data; //TODO FIXME???
} DebugeMsg;


// ================================================
// ===     end message struct definitions       ===
// ================================================


/**
 * TODO: document
 */
class StormMessage {
public:
    Message type;
    Address address;
    uint8_t size;
    char DATA[16];

    /**
     * TODO: document
     */
    StormMessage() {
        //FIXME this is like, bad, no?
        this->type = Message::None;
        this->address = Address::all;
        this->size = 0;
    }

    /**
    * TODO: document
    */
    StormMessage(Message type, Address address, uint8_t size, char* data) {
        this->type = type;
        this->address = address;
        this->size = size;

        //TODO: check to see if this makes a legal message and if not, idk do something
        
        for (uint8_t i = 0; i < size; i++) {
            DATA[i] = data[i];
        }
    }

    /**
    * TODO: document
    */
    ~StormMessage() {
        //TODO
    }

    // message conversion methods
    Request AsRequest() {
        Request msg;

        msg.ID = this->DATA[0];

        return msg; 
    }

    HeartbeatMsg AsHeartbeat() {
        HeartbeatMsg msg;

        // no meaningful data bytes

        return msg;
    }

    ConfigurationMsg AsConfiguration() {
        ConfigurationMsg msg;

        msg.ID = static_cast<uint8_t>(DATA[0]);
        
        //TODO: data type and whatnot

        return msg;
    }

    ConfigCompleteMsg AsConfigurationComplete() {
        ConfigCompleteMsg msg;

        // no meaningful data bytes

        return msg;
    }

    RobotVelocityCmd AsRobotVelocity() {
        RobotVelocityCmd cmd;

        cmd.forward_velocity = byte_to_int16(DATA);
        cmd.sideways_velocity = byte_to_int16(DATA + 2);
        cmd.rotational_velocity = byte_to_int16(DATA + 4);

        return cmd;
    }

    DriveVelocityCmd AsDriveVelocity() {
        DriveVelocityCmd cmd;

        cmd.front_left_velocity = byte_to_int16(DATA);
        cmd.front_right_velocity = byte_to_int16(DATA + 2);
        cmd.back_left_velocity = byte_to_int16(DATA + 4);
        cmd.back_right_velocity = byte_to_int16(DATA + 6);

        return cmd;
    }

    DriveVoltageCmd AsDriveVoltage() {
        DriveVoltageCmd cmd;

        cmd.front_left_voltage = byte_to_int16(DATA);
        cmd.front_right_voltage = byte_to_int16(DATA + 2);
        cmd.back_left_voltage = byte_to_int16(DATA + 4);
        cmd.back_right_voltage = byte_to_int16(DATA + 6);

        return cmd;
    }

    DriveRawCmd AsDriveRaw() {
        DriveRawCmd cmd;

        cmd.front_left_raw = byte_to_int16(DATA);
        cmd.front_right_raw = byte_to_int16(DATA + 2);
        cmd.back_left_raw = byte_to_int16(DATA + 4);
        cmd.back_right_raw = byte_to_int16(DATA + 6);

        return cmd;
    }

    DriveFeedbackRsp AsDriveFeedback() {
        DriveFeedbackRsp rsp;

        rsp.forward_velocity = byte_to_int16(DATA);
        rsp.sideways_velocity = byte_to_int16(DATA + 2);
        rsp.rotational_velocity = byte_to_int16(DATA + 4);
        rsp.delta_x = byte_to_int16(DATA + 6);
        rsp.delta_y = byte_to_int16(DATA + 8);
        rsp.delta_theta = byte_to_int16(DATA + 10);

        return rsp;
    }

    BatteryVoltageRsp AsBatteryVoltage() {
        BatteryVoltageRsp rsp;
        
        rsp.voltage = static_cast<uint8_t>(DATA[0]);

        return rsp;
    }

    ClimberHeightCmd AsClimberHeightCmd() {
        ClimberHeightCmd cmd;

        cmd.height = static_cast<uint8_t>(DATA[0]);

        return cmd;
    }

    ClimberVelocityCmd AsClimberVelocityCmd() {
        ClimberVelocityCmd cmd;


        cmd.climber_one_velocity = byte_to_int16(DATA);
        cmd.climber_two_velocity = byte_to_int16(DATA + 2);

        return cmd;
    }

    ClimberRawCmd AsClimberRawCmd() {
        ClimberRawCmd cmd;

        cmd.climber_one_raw = byte_to_int16(DATA);
        cmd.climber_two_raw = byte_to_int16(DATA + 2);

        return cmd;
    }

    ClimberPositionCmd AsClimberPositionCmd() {
        ClimberPositionCmd cmd;

        cmd.servo_one_position = static_cast<uint8_t>(DATA[0]);
        cmd.servo_two_position = static_cast<uint8_t>(DATA[1]);

        return cmd;
    }

    ClimberSensorRsp AsClimberSensorRsp() {
        ClimberSensorRsp rsp;

        rsp.climber_sensor = static_cast<bool>(DATA[0]);

        return rsp;
    }

    ClimberStateRsp AsClimberStateRsp() {
        ClimberStateRsp rsp;

        rsp.climber_one_velocity = byte_to_int16(DATA);
        rsp.climber_two_velocity = byte_to_int16(DATA + 2);
        rsp.climber_height = static_cast<uint8_t>(DATA[4]);
        rsp.servo_one_position = static_cast<uint8_t>(DATA[5]);
        rsp.servo_two_position = static_cast<uint8_t>(DATA[6]);
        rsp.climber_sensor = static_cast<bool>(DATA[7]);

        return rspl;
    }

    ShooterVelocityCmd AsShooterVelocityCmd() {
        ShooterVelocityCmd cmd;

        cmd.shooter_velocity = byte_to_uint16(DATA);

        return cmd;
    }

    ShooterRawCmd AsShooterRawCmd() {
        ShooterRawCmd cmd;

        cmd.shooter_raw = byte_to_uint16(DATA);

        return cmd;
    }

    ShooterPositionCmd AsShooterPositionCmd() {
        ShooterPositionCmd cmd;

        cmd.turret_angle = static_cast<uint8_t>(DATA[0]);
        cmd.hood_angle = static_cast<uint8_t>(DATA[1]);

        return cmd;
    }

    ShooterStateRsp AsShooterStateRsp() {
        ShooterStateRsp rsp;
        
        rsp.shooter_velocity = byte_to_int16(DATA);
        rsp.turret_angle = byte_to_int16(DATA + 2);
        rsp.hood_angle = static_cast<uint8_t>(DATA[4]);

        return rsp;
    }

    IndexerVelocityCmd AsIndexerVelocityCmd() {
        IndexerVelocityCmd cmd;

        cmd.indexer_velocity = byte_to_int16(DATA);

        return cmd;
    }

    IndexerRawCmd AsIndexerRawCmd() {
        IndexerRawCmd cmd;
        
        cmd.indexer_raw = byte_to_int16(DATA);

        return cmd;
    }

    IndexerFeedCmd AsIndexerFeedCmd() {
        IndexerFeedCmd cmd;

        cmd.num_cannonballs = static_cast<uint8_t>(DATA[0]);

        return cmd;
    }

    IntakeVelocityCmd AsIntakeVelocityCmd() {
        IntakeVelocityCmd cmd;

        cmd.intake_velocity = byte_to_int16(DATA);

        return cmd;
    }

    IntakeFeedCmd AsIntakeFeedCmd() {
        IntakeFeedCmd cmd;
        
        cmd.num_cannonballs = static_cast<uint8_t>(DATA[0]);

        return cmd;
    }

    IntakeRawCmd AsIntakeRawCmd() {
        IntakeRawCmd cmd;

        cmd.intake_raw = byte_to_int16(DATA);

        return cmd;
    }

    IntakeIndexerRsp AsIntakeIndexerRsp() {
        IntakeIndexerRsp rsp;
        
        rsp.intake_velocity = byte_to_int16(DATA);
        rsp.indexer_velocity = byte_to_int16(DATA + 2);
        rsp.ir_sensor_states = static_cast<char>(DATA[4]);
        rsp.shot_count = static_cast<uint8_t>(DATA[5]);
        rsp.collected_count = static_cast<uint8_t>(DATA[6]);

        return rsp;
    }

    //TODO once we have this figured out, if we even actually need it
    // // ID 255
    // typedef struct DebugeMsg {
    //     char[16] data;
    // } DebugeMsg;
};