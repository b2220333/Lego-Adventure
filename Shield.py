from Character import *
from direct.actor.Actor import Actor
from Settings import *

# Members:
#   controllerNode
#   nodePath
#   animator
#   pose
class Shield(Character):
    def __init__(self, world, render, name):
        animator = Actor('models/Actors/lego/Shield/Shield.egg',
                              {
                                  'FallbackGetup': 'models/Actors/lego/Shield/Shield-FallbackGetup.egg',
                                  'FallforwardGetup': 'models/Actors/lego/Shield/Shield-FallforwardGetup.egg',
                                  'jump': 'models/Actors/lego/Shield/Shield-jump.egg',
                                  'punch': 'models/Actors/lego/Shield/Shield-punch.egg',
                                  'walk': 'models/Actors/lego/Shield/Shield-walk.egg'
                              })
        Character.__init__(self, world, render, name, animator, STANDING)