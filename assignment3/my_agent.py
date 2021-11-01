from collections import deque
import argparse
import json


class State(object):
    def Execute(self):
        pass

    def Transition(self):
        pass


class Zero(State):
    def __init__(self):
        self.state = "zero"

    def Execute(self):
        print("confess")


class Confess(State):
    def __init__(self):
        self.state = "confess"

    def Execute(self):
        print("confess")

    # used for testing
    def Transition(self):
        print("transitioned to confess")


class Silent(State):
    def __init__(self):
        self.state = "silent"

    def Execute(self):
        print("silent")

    # used this for testing
    def Transition(self):
        print("transitioned to silent")


# dont want to initialize initial state in the state machine to offer myself more flexibility of when i start FSM
# what if i receive arguments from script that doesnt iterate from 1-100 continuously, rather, it terminates after every
# iteration.
class StateMachine(object):
    def __init__(self):
        self.states = {}
        self.currentState = None
        self.transitions = {}
        self.mood = self.LoadJson()  # deque(["silent"], maxlen=5) * 5

    # sets state and runs the state
    def setState(self, to_state):
        self.currentState = self.states[to_state]
        if self.currentState.state != "zero":
            self.mood.appendleft(to_state)
            decisions = {'last_opponent_move': self.toJsonSerializable(self.mood)}
            with open('decisions.json', 'w') as file:  # self.mood.appendleft(to_state)
                json.dump(decisions, file)

    def Execute(self):
        # ex. if zero.state is "zero"
        if self.currentState.state == "zero":
            self.currentState.Execute()
        else:
            if self.mood.count("silent") >= 4 and self.currentState.state == "silent":
                self.Transition("toConfess")
                self.currentState.Execute()

            elif self.mood.count("silent") >= 4 and self.currentState.state == "confess":
                self.Transition("toSilent")
                self.currentState.Execute()
            # case: curState: silent & self.mood.count("silent") < 4
            elif self.currentState.state == "silent":
                self.currentState.Execute()
            # case: curState: confess & self.mood.count("silent") < 4
            else:
                self.currentState.Execute()

    def Transition(self, to_state):
        # print("transitioning...")
        self.currentState = self.transitions[to_state]
        # self.currentState.Transition()

    # loads json object to dictionary string. method call to convert "last_opponent_move" key value to deque()
    def LoadJson(self):
        with open("decisions.json", "r") as read_file:
            vi_deque = json.load(read_file)
        return self.toJsonDeserialize(vi_deque["last_opponent_move"])

    # "Object of type deque is not JSON serializable, so i converted to list"
    def toJsonSerializable(self, list):
        new_list = []
        for i in list:
            new_list.append(i)
        return new_list

    # converting from list to deque() so im able to use maxlen queue
    def toJsonDeserialize(self, list):
        queue = deque(list, maxlen=5)
        return queue


if __name__ == "__main__":
    # initializing states and transitions
    game = StateMachine()
    game.states["zero"] = Zero()
    game.states["silent"] = Silent()
    game.states["confess"] = Confess()
    game.transitions["toSilent"] = Silent()
    game.transitions["toConfess"] = Confess()

    # receiving commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', help='called when new game')
    parser.add_argument('--iterations', help='number of iterations in game')
    parser.add_argument('--last_opponent_move', help='last opponent move')

    args = parser.parse_args()
    
    elif args.init != None:
        sys.exit()

    else:
        game.setState(args.last_opponent_move)
        game.execute()
    
    
    
