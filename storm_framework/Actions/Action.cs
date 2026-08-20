
namespace storm.Actions;

//TODO: document this
// basically we're copying WPILib's command-based framework (sometimes called the 'new command' framework)
public abstract class Action
{
    // is called when Action is first scheduled
    public abstract void Start();
    
    // is called after Start, and every loop iteration after that until it ends
    public abstract void Run();
    
    // is called after Run, if IsDone() returns true
    public void End()
    {
        // don't force people to implement this method
    }

    // is checked every iteration to determine if the command should be End()-ed or not
    public abstract bool IsDone();
}