from statemachine import State

class customState(State):
    def __init__(self, name, value=None, initial=False):
        # type: (Text, Optional[V], bool) -> None
        self.name = name
        self.value = value
        self._initial = initial
        self.identifier = None  # type: Optional[Text]
        self.transitions = []  # type: List[Transition]
        self.test = []
        