import pygame
from pygame.locals import *
import math
from game import EventName, Publisher
from threading import Timer

ComponentContext = {
    'screen': {},
    'position': (0,0)
}



class Component:
    name = 'Component'
    """
    base class for components that includes the most common properties and behaviors
    todo: implement UpdatingComponent
    """
    def __init__(
        self, children = [], context = ComponentContext,
        width = 0, height = 0, margin = 0, padding = 0,
        position = [0,0], name = '', ref = None, expanded = False,
        absolute = False
    ):
        """
        component context will not be delegated to children until after it's parent
        is initialized. so don't use context variables in init of children classes
        """
        self._absolute = False
        self._explicit_width = width
        self._explicit_height = height
        self.context = context
        self.children = children
        self.width = width
        self.height = height
        self.margin = margin
        self.padding = padding
        self.position = position
        self.expanded = expanded
        self._name = f'{self.name}({name})'



        if ref:
            ref(self)

    def set_height(self, height = 0):
        """
        explicitly set height in component props overrides and assignment (from parent)
        """
        self.height = self._explicit_height or height

    def set_width(self, width = 0):
        self.width = self._explicit_width or width

    def set_position(self, position = [0,0]):
        if not self._absolute:
            self.position = position


    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.position[0],
            self.position[1],
            self.width,
            self.height
        )

    def resize_children(self):
        """
        because components are nested, the sizing/placing must happen recursively
        once the top of the component tree is reached. this may limit the amount of nesting
        that can occur. i'm sure this can be optimized. if it's slow, look here.

        """
        for child in self.children:
            if not child: continue
            child.set_height(self.height)
            child.set_width(self.width)
            child.set_position(self.position.copy())
            if self.padding:
                child.height -= self.padding * 2
                child.width -= self.padding * 2
                child.position[0] += self.padding
                child.position[1] += self.padding
            child.resize_children()
        
        return self

    def propagate_context(self):
        """
        pass the context down recursively to children unless another context barrier is reached
        potentially extend with the new context if possible
        """
        for child in self.children:
            if not child: continue
            if not isinstance(child, ContextProvider):
                child.context = self.context
                child.propagate_context()

    

    def draw_children(self):
        if self.children:
            for child in self.children:
                if not child: continue
                child.draw()


    def draw(self):
        self.draw_children()
        return self

class ContextProvider(Component):
    name = 'ContextProvider'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.propagate_context()

class Image(Component):
    name = 'Image'
    image_cache = {}

    def __init__(self, file: str = '', **kwargs):
        super().__init__(**kwargs)

        if not(file in self.image_cache):
            self.image_cache[file] = pygame.image.load(file)

        self.image = self.image_cache[file]
        self.boundary = self.image.get_rect()

    def draw(self):
        scaled_image = pygame.transform.scale(
            self.image,
            (
                math.floor(self.width),
                math.floor(self.height)
            )
        )
        self.context['screen'].blit(scaled_image, dest = self.position)
        return self

        

class Row(Component):
    name = 'Row'
    def __init__(
        self, gutter: int = 0, direction = 'right', **kwargs
    ):
        super().__init__(**kwargs)
        self.direction = direction
        self.gutter = gutter
        self.count = len(self.children)

    def draw(self):
        offset = 0
        direction = 'width' if self.direction == 'right' else 'height'
        direction_length = getattr(self, direction)
        adjusted_length = direction_length - self.gutter * (len(self.children) - 1)
        child_length = adjusted_length / len(self.children)

        for child in self.children:
            # empty children are skipped but still take up space
            if child:
                if self.direction == 'right':
                    child.set_height(self.height)
                    child.set_width(child_length)
                else:
                    child.set_width(self.width)
                    child.set_height(child_length)

                child.position = [
                    self.position[0] + (offset if self.direction == 'right' else 0),
                    self.position[1] + (offset if self.direction == 'down' else 0)
                ]

                child.resize_children()
                child.draw()

            offset += child_length + self.gutter

        return self

class Column(Row):
    name = 'Column'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.direction = 'down'


class Wrapper(Component):
    def __init__(self, component: Component = None):
        super().__init__()
        self.children = [component]



        


def with_events(
    component, name = '', publisher = {},
    **kwargs
):
    class WithEvents(Wrapper):
        def __init__(self, component = component, publisher: Publisher = {}, id=0, **kwargs):
            super().__init__(component)
            self.name = f'WithEvents({name})'
            self.events = kwargs
            self.publisher = publisher
            self.listeners = {}
            self.id = id
            self.bind_events()

        def bind_events(self):

            # wrap handlers with pygame event logic and bind
            # need to implement a way to destroy these listeners on cleanup
            for name, handler in self.events.items():
                if name.startswith('on_'):
                    name = name.split('_')[1]
                    if name == EventName.hover:
                        self.listeners[name] = self.publisher.subscribe(pygame.MOUSEMOTION, self.hover(handler))

                    if name == EventName.click:
                        self.listeners[name] = self.publisher.subscribe(pygame.MOUSEBUTTONUP, self.click(handler))

            for listener in self.listeners.values():
                listener.on()


            
        def click(self, handler):
            def listener(event):
                if self.get_rect().collidepoint(pygame.mouse.get_pos()):
                    return handler(event, self)
            return listener


        def hover(self, handler):
            def listener(event):
                if self.get_rect().collidepoint(pygame.mouse.get_pos()):
                    return handler(event, self)
            
            return listener


        def get_rect(self) -> pygame.Rect:
            return pygame.Rect(
                self.position[0],
                self.position[1],
                self.width,
                self.height
            )
    
    return WithEvents(component, publisher, **kwargs)






# unsized items share the remaining space
class Expanded(Row):
    name = 'Expanded'
    def draw(self):
        direction = 'width' if self.direction == 'right' else 'height'
        direction_length = getattr(self, direction)
        adjusted_length = direction_length - self.gutter * (len(self.children) - 1)

        #use some other method to detect the sized children
        sized_children = []
        unsized_children = []

        for child in self.children:
            if child.expanded:
                unsized_children.append(child)
            else:
                sized_children.append(child)

        #implement percentages
        #catch the case where children are larger than parent
        remaining_space = adjusted_length - sum([getattr(c, direction) for c in sized_children])

        expanded_children_length = remaining_space / len(unsized_children)

        for child in unsized_children:
            if child:
                if self.direction == 'right':
                    child.set_width(expanded_children_length)
                else:
                    child.set_height(expanded_children_length)

        offset = 0

        for child in self.children:
            if child:
                if self.direction == 'right':
                    child.set_height(self.height)
                else:
                    child.set_width(self.width)

                child.position = [
                    self.position[0] + (offset if self.direction == 'right' else 0),
                    self.position[1] + (offset if self.direction == 'down' else 0)
                ]

                child.resize_children()
                child.draw()

            offset += getattr(child, direction) + self.gutter



class Shape(Component):
    def __init__(self, color = (0,0,0), **kwargs):
        super().__init__(**kwargs)
        self.color = color

        
class Rectangle(Shape):
    def draw(self):
        pygame.draw.rect(self.context['screen'], self.color, self.get_rect())
        # calling this so that children get drawn
        super().draw()
        return self

class Ellipse(Shape):
    def __init__(self, radius = 0, **kwargs):
        super().__init__(**kwargs)
    
    def draw(self):
        pygame.draw.ellipse(self.context['screen'], self.color, self.get_rect())
        super().draw()
        return self

class Circle(Shape):
    def __init__(self, radius=0, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius

    def draw(self):
        rect = self.get_rect()
        pygame.draw.circle(self.context['screen'], self.color, rect.center, rect.width / 2)
        super().draw()
        return self


        
