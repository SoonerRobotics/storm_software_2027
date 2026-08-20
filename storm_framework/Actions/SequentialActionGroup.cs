
using System.Collections;

namespace storm.Actions;

//TODO document and everything
public class SequentialActionGroup : Action
{
    // hold parallel actions
    private List<Action> m_actions;
    private int m_index = -1;

    public SequentialActionGroup(List<Action> actions)
    {
        if (actions.Count <= 0)
        {
            throw new ArgumentException("actions list cannot be empty!");
        }

        //FIXME does this need to be like, a deep copy or something?
        m_actions = actions;
    }

    public override void Start()
    {
        if (m_index != -1)
        {
            //TODO: idk error here or something this shouldn't happen
        }

        m_index = 0;
        m_actions[m_index].Start();
    }

    public override void Run()
    {
        //TODO: need to handle like, starting the next action and everything right?
        m_actions[m_index].Run();
    }


    public override bool IsDone()
    {
        //TODO
        throw new NotImplementedException();
    }
}