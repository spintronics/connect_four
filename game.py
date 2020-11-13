import pygame, sys
from pygame.locals import *
from os import path
import math


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

    def apply(self, state: object, data = {}):
        return self.__mutator(state, data)


class Listener:
    """
    this class provides subscribers a way to manage their own subscription
    without directly modifying the publisher
    """
    def __init__(self, handler):
        self.listening = False
        self.destroyed = False
        self.handler = handler

    def on(self):
        self.listening = True

    def off(self):
        self.listening = False

    def remove(self):
        self.destroyed = True


def mutator(state: object, data: object = {}):
    """
    return a new object if possible
    """
    return state

    

class State:
    def __init__(self, initialState = initialState, actions: [Action] = []):
        self.__state = initialState
        self.__subscriptions = {
            'all': []
        }
        self.__actions = {}
        for action in actions:
            self.__actions[action.name] = action
    
    def get(self, path: str):
        """
        . seperated lensing
        state.get('a.b.c') = state.__state['a']['b']['c']
        will retrun None if a key is encountered that doesn't exist
        """
        keys = [key for key in path.split('.') if key]
        target = self.__state
        for key in keys:
            # this doesn't accomodate lists
            if key in target:
                target = target[key]
            else:
                target = None
                break
        return target

    def __set(self, path: str, value):
        keys = [key for key in path.split('.') if key]
        if not (len(keys)):
            self.__state = value
            return
        target = self.__state
        for key in keys[:-1]:
            if key in target:
                target = target[key]
            else:
                target = None
                break
        if target:
            target[keys[-1]] = value

    def subscribe(self, name: str, handler):
        """
        subscribe to a named event, this could certainly be more robust with streams/hooks
        """
        if not (name in self.__subscriptions):
            self.__subscriptions[name] = []
        listener = Listener(handler)
        self.__subscriptions[name].append(listener)
        return listener

    def dispatch(self, name: str, data = {}):
        """
        dispatch a named action with the provided data, does nothing if the action does not exist
        listener triggers after the action is complete
        no support for async actions
        """
        if name in self.__actions:
            action = self.__actions[name]
            new_state = action.apply(self.__state, data)
            self.__set(action.scope, new_state)

            if name in self.__subscriptions:
                self.__subscriptions = [
                    listener for listener in self.__subscriptions[name]
                    if not listener.destroyed
                ]
                for listener in self.__subscriptions[name]:
                    if listener.listening:
                        listener.handler()
                # 'all' top level subscription
                for listener in self.__subscriptions['all']:
                    if listener.listening:
                        listener.handler()

    def register(self, name: str, mutator: mutator = mutator, scope: str = ''):
        """
        register a named action so that the model knows how to update
        this could be wrapped in a model class but that's unecessary complexity atm
        """
        self.__actions[name] = Action(name, mutator, scope)


    def unsafe_get_state(self):
        return self.__state

    

        
    
            


class Game:
    def __init__(self, state: State):
        self.state = state
        pygame.init()
        window = state.get('window')
        self.screen = pygame.display.set_mode((window['width'], window['height']))

        #this could obviously be more efficient
        state.subscribe('all', self.draw)

    def draw(self):
        pygame.display.update()
        pygame.display.flip()

    def update(self):
        self.draw()

        
    




