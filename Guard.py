from Character import *
from direct.actor.Actor import Actor
from Settings import *

# Members:
#   controllerNode
#   nodePath
#   animator
#   pose
class Guard(Character):
    def __init__(self, world, render, name):
        animator = Actor('models/Actors/lego/SecurityGuard/SecurityGuard.egg',
                              {
                                  'fallbackGetup': 'models/Actors/lego/SecurityGuard/SecurityGuard-fallbackGetup.egg',
                                  'fallforwardGetup': 'models/Actors/lego/SecurityGuard/SecurityGuard-fallforwardGetup.egg',
                                  'firegun': 'models/Actors/lego/SecurityGuard/SecurityGuard-firegun.egg',
                                  'jump': 'models/Actors/lego/SecurityGuard/SecurityGuard-jump.egg',
                                  'run': 'models/Actors/lego/SecurityGuard/SecurityGuard-run.egg',
                                  'swing': 'models/Actors/lego/SecurityGuard/SecurityGuard-swing.egg',
                                  'walk': 'models/Actors/lego/SecurityGuard/SecurityGuard-walk.egg'
                              })
        Character.__init__(self, world, render, name, animator, STANDING)