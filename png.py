from transitions.extensions import GraphMachine
from functools import partial


class Model:

    def clear_state(self, deep=False, force=False):
        print("Clearing state ...")
        return True


model = Model()
machine = GraphMachine(model=model,
    states=[
        'initial',
        'input_search',
        'intro',
        'lists',
        'listen',
        'end',
        #
        'chat',
        'chat2',
    ],
    transitions=[
        #music mode
        {'trigger': 'advance', 'source': 'user', 'dest': 'initial', 'conditions': 'is_going_to_initial'},
        {'trigger': 'advance', 'source': 'initial', 'dest': 'input_search', 'conditions': 'is_going_to_input_search'},
        {'trigger': 'advance', 'source': 'input_search', 'dest': 'intro', 'conditions': 'is_going_to_intro'},
        {'trigger': 'advance', 'source': 'input_search', 'dest': 'lists', 'conditions': 'is_going_to_lists'},
        {'trigger': 'advance', 'source': 'input_search', 'dest': 'listen', 'conditions': 'is_going_to_listen'},
        {'trigger': 'advance', 'source': 'intro', 'dest': 'end', 'conditions': 'is_going_to_end'},
        {'trigger': 'advance', 'source': 'lists', 'dest': 'end', 'conditions': 'is_going_to_end'},
        {'trigger': 'advance', 'source': 'listen', 'dest': 'end', 'conditions': 'is_going_to_end'},
        {'trigger': 'advance', 'source': 'end', 'dest': 'end', 'conditions': 'is_going_to_end'},
        #chat mode
        {'trigger': 'advance', 'source': 'initial', 'dest': 'chat', 'conditions': 'is_going_to_chat'},
        {'trigger': 'advance', 'source': 'chat', 'dest': 'chat2', 'conditions': 'is_going_to_chat2'},
        {'trigger': 'advance', 'source': 'chat2', 'dest': 'chat2', 'conditions': 'is_going_to_chat2'},
        {'trigger': 'advance', 'source': 'chat2', 'dest': 'initial', 'conditions': 'is_going_to_chatEnd'},
        #
        {'trigger': 'advance', 'source': 'intro', 'dest': 'input_search', 'conditions': 'is_going_to_input_search'},
    
        {
            'trigger': 'go_back',
            'source': [
                'initial',
                'input_search',
                'intro',
                'lists',
                'listen',
                'end',
                #
                'chat',
                'chat2',
            ],
            'dest': 'initial'
        },
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


model.get_graph().draw('my_state_diagram.png', prog='dot')