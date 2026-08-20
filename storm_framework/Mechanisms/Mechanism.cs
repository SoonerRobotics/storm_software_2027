
namespace storm.Mechanisms;

public abstract class Mechanism
{
    //TODO: what the heck is a mechanism? just a subsystem? what does it do?
    // do we want to have default Actions? or like, default, robot-state-based Actions?
    // that kinda makes sense, or maybe we just schedule default commands in the RobotContainer-equivalent class we write?
    // no that doesn't make sense.

    public abstract void Periodic();
}