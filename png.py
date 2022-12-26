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
        'lyrics',
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
        {'trigger': 'advance', 'source': 'intro', 'dest': 'initial', 'conditions': 'is_going_to_initial'},
        {'trigger': 'advance', 'source': 'lists', 'dest': 'initial', 'conditions': 'is_going_to_initial'},
        {'trigger': 'advance', 'source': 'listen', 'dest': 'initial', 'conditions': 'is_going_to_initial'},
        #{'trigger': 'advance', 'source': 'end', 'dest': 'initial', 'conditions': 'is_going_to_initial'},
        #chat mode
        {'trigger': 'advance', 'source': 'initial', 'dest': 'chat', 'conditions': 'is_going_to_chat'},
        {'trigger': 'advance', 'source': 'chat', 'dest': 'chat2', 'conditions': 'is_going_to_chat2'},
        {'trigger': 'advance', 'source': 'chat2', 'dest': 'chat2', 'conditions': 'is_going_to_chat2'},
        {'trigger': 'advance', 'source': 'chat2', 'dest': 'initial', 'conditions': 'is_going_to_chatEnd'},
        #
        {'trigger': 'advance', 'source': 'intro', 'dest': 'input_search', 'conditions': 'is_going_to_input_search'},
        #lyrics
        {'trigger': 'advance', 'source': 'initial', 'dest': 'lyrics', 'conditions': 'is_going_to_lyrics'},
        {'trigger': 'advance', 'source': 'lyrics', 'dest': 'initial', 'conditions': 'is_going_to_initial'},
        {
            'trigger': 'go_back',
            'source': [
                'initial',
                'input_search',
                'intro',
                'lists',
                'listen',
                'lyrics',
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