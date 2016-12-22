# Panda3d Library
from direct.actor.Actor import Actor
from Settings import *
# My Game Classes
from Character import *
# Members:
#   controllerNode
#   nodePath
#   animator
#   pose
class Shield(Character):
    def __init__(self, world, render, name, position):
        animator = Actor('models/Actors/lego/Shield/Shield.egg',
                              {
                                  'FallbackGetup': 'models/Actors/lego/Shield/Shield-FallbackGetup.egg',
                                  'FallforwardGetup': 'models/Actors/lego/Shield/Shield-FallforwardGetup.egg',
                                  'jump': 'models/Actors/lego/Shield/Shield-jump.egg',
                                  'attack': 'models/Actors/lego/Shield/Shield-punch.egg',
                                  'run': 'models/Actors/lego/Shield/Shield-walk.egg'
                              })
        Character.__init__(self, world, render, name, animator, position, STANDING)
        self.pushSound = base.loader.loadSfx("sounds/push.wav")
        self.position = position