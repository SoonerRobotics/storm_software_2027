
namespace storm.Hardware;

public abstract class Interface
{
    // ???
    // what does this even have? like a reader and writer thread?
    // some locks? some data types it stores? idk if we can really abstract this away a whole bunch...

    public abstract void Periodic();
}