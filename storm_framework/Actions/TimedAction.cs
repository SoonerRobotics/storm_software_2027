
namespace storm.Actions;

public class TimedAction : Action
{
    //FIXME need be ulong?
    private long m_timeout = -1;
    private long m_starttime = -1;

    //TODO: document. like, is this in seconds? milliseconds? nanoseconds ???
    public TimedAction(long timeout)
    {
        if (timeout < 0)
        {
            throw new ArgumentOutOfRangeException("timeout", "timeout must be positive!");
        }
        m_timeout = timeout;
        m_starttime = -1;
    }

    public override void Start()
    {
        m_starttime = DateTime.Now.Ticks;
    }

    public override void Run()
    {
        // don't actually need to do anything.
    }

    public override bool IsDone()
    {
        return (DateTime.Now.Ticks - m_starttime) > m_timeout;
    }
}