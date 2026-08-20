
using System.Collections;

namespace storm.Actions;

public class ParallelActionGroup : Action
{
    // hold parallel actions
    private List<Action> m_actions;
    private int m_index = -1;

    public ParallelActionGroup(List<Action> actions)
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
        //TODO: we should start all of them, right...? am I stupid? I think I am yes
        //FIXME
        m_actions[m_index].Start();
    }

    public override void Run()
    {
        // we need to run all of them
        m_actions[m_index].Run();
    }


    public override bool IsDone()
    {
        //TODO we need to check all of them
        throw new NotImplementedException();
    }
}