import pygame, sys
from pygame.locals import *
from os import path
import math
import util
import json


initialState = {
    'window': {
        'width': 900,
        'height': 900
    }
}


  

class Action:
    """
    an action is something that takes the current state and returns the new state
    this should not modify the existing state but copy/replace the whole state object
    if a scope is provided then the dispatcher will pass the indicated portion to the action
    and replace it with the result
    """
    def __init__(self, name: str, mutator, scope = ''):
        self.__mutator = mutator
        self.name = name
        self.scope = scope

    def apply(self, state: object = {}, data = {}):
        return self.__mutator(state, data)


class Listener:
    """
    this class provides subscribers a way to manage their own subscription
    without directly modifying the publisher
    """
    def __init__(self, handler = lambda x: x):
        self.listening = False
        self.destroyed = False
        self.handler = handler

    def on(self):
        self.listening = True

    def off(self):
        self.listening = False

    def remove(self):
        self.listening = False
        self.destroyed = True

class Publisher:
    def __init__(self):
        self.__subscriptions = {
            'change:state': []
        }
    def subscribe(self, name: str, handler = lambda x: x) -> Listener:
            """
            subscribe to a named event, this could certainly be more robust with streams/hooks
            """
            if not (name in self.__subscriptions):
                self.__subscriptions[name] = []
            listener = Listener(handler)
            self.__subscriptions[name].append(listener)
            return listener

    def emit(self, name = '', data = {}):
        if name in self.__subscriptions:
            # remove destroyed listeners
            for subscription in self.__subscriptions.values():
                subscription = list(filter(lambda l: not l.destroyed, subscription))

            for listener in self.__subscriptions[name]:
                if listener.listening:
                    listener.handler(data)
                
            # 'all' top level subscription
            # for listener in self.__subscriptions['all']:
            #     if listener.listening:
            #         listener.handler(data)

    def purge(self, names = []):
        for name in names:
            if name in self.__subscriptions:
                del self.__subscriptions[name]





        

    

class State:
    def __init__(self, initialState = initialState, publisher:Publisher = {}, actions = {}):
        self.__state = initialState
        self.__actions = {}
        self.publisher = publisher
        for action in actions:
            self.__actions[action.name] = action

        # replay logged actions
        if ('-r' in sys.argv):
          self.log_file = open(path.join(util.current_directory, 'action_log.fancy'), 'r')
          self.log_actions = False
        else:
          self.log_file = open(path.join(util.current_directory, 'action_log.fancy'), 'w')
          self.log_file.truncate()
          self.log_actions = True
    
    def get(self, path: str):
        return util.get(path, self.__state)

    def __set(self, path: str, value):
        if path == '':
            self.__state = value
            return
        util.path_set(path, value, self.__state)

    def replay_actions(self):
      if not self.log_actions:
        print('replay')
        for action in self.log_file.readlines():
          self.dispatch(*json.loads(action.strip()))

    def dispatch(self, name: str, data = {}):
        """
        dispatch a named action with the provided data, does nothing if the action does not exist
        listener triggers after the action is complete
        no support for async actions
        """
        print(name, data)
        if name in self.__actions:
            action = self.__actions[name]
            new_state = action.apply(self.__state, data)
            if new_state == None: return
            # if new state is the same as the old state, do nothing (don't trigger update)
            # also if an action returns None, do nothing and dont check if anything has changed
            # if(action.scope and self.get(action.scope) == new_state): return
            self.__set(action.scope, new_state)
            #save the action to log
            if self.log_actions:
              self.log_file.write(json.dumps([name, data]) + '\n')
            self.publisher.emit('change:state', {'scope': action.scope})


            

    

    def register(self, name: str, mutator = lambda x, y: x, scope: str = ''):
        """
        register a named action so that the model knows how to update
        this could be wrapped in a model class but that's unecessary complexity atm
        """
        self.__actions[name] = Action(name, mutator, scope)


    def unsafe_get_state(self):
        return self.__state

    
class EventName:
    hover = 'hover'
    click = 'click'


class Game:
    """
    base class to interface with pygame and manage the game lifecycle
    """
    def __init__(self, state: State, publisher: Publisher):
        self.state = state
        pygame.init()
        window = state.get('window')
        self.publisher = publisher
        self.running = True
        self.screen = pygame.display.set_mode((window['width'], window['height']))
        self.updated = False

        #this could obviously be more efficient
        self.state_change_listener = publisher.subscribe('change:state', lambda scope: self.update())
        self.state_change_listener.on()

    def draw(self):
        pygame.display.update()
        pygame.display.flip()

    def update(self):
        if not self.should_update(): return
        self.draw()

    def consume_events(self):
        for event in pygame.event.get():
            self.publisher.emit(event.type, event)

    def should_update(self):
        return True






        
    




