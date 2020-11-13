import pygame
from pygame.locals import *
import math

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
        position = [0,0], name = '', ref = None
    ):
        """
        component context will not be delegated to children until after it's parent
        is initialized. so don't use context variables in init of children classes
        """
        self.context = context
        self.children = children
        self.width = width
        self.height = height
        self.margin = margin
        self.padding = padding
        self.position = position
        self._name = f'{self.name}({name})'

        if ref:
            ref.set(self)

            


    def resize_children(self):
        """
        because components are nested, the sizing/placing must happen recursively
        once the top of the component tree is reached. this may limit the amount of nesting
        that can occur. i'm sure this can be optimized. if it's slow, look here.

        """
        for child in self.children:
            child.height = self.height
            child.width = self.width
            child.position = self.position.copy()
            if self.padding:
                child.height -= self.padding * 2
                child.width -= self.padding * 2
                child.position[0] += self.padding
                child.position[1] += self.padding
            child.resize_children()
        
        return self

    def _propagate_context(self):
        """
        pass the context down recursively to children unless another context barrier is reached
        potentially extend with the new context if possible
        """
        for child in self.children:
            if not isinstance(child, ContextProvider):
                child.context = self.context
                child._propagate_context()

    

    def draw_children(self):
        if self.children:
            for child in self.children:
                child.draw()


    def draw(self):
        self.draw_children()
        return self

class ContextProvider(Component):
    name = 'ContextProvider'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._propagate_context()

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
        direction_length = self.width if self.direction == 'right' else self.height
        adjusted_length = direction_length - self.gutter * (len(self.children) - 1)
        child_length = adjusted_length / len(self.children)

        for child in self.children:
            if self.direction == 'right':
                child.height = self.height
                child.width = child_length
            else:
                child.width = self.width
                child.height = child_length

            child.position = (
                self.position[0] + (offset if self.direction == 'right' else 0),
                self.position[1] + (offset if self.direction == 'down' else 0)
            )

            child.draw()

            offset += child_length + self.gutter

        return self

class Column(Row):
    name = 'Column'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.direction = 'down'


# unsized items share the remaining space
# class Expanded(Row):
#     name = 'Expanded'
#     def draw(self):
#         direction_length = self.width if self.direction == 'right' else self.height
#         adjusted_length = direction_length - self.gutter * (len(self.children) - 1)




        
