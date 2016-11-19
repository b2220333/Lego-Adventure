from Character import *
from direct.actor.Actor import Actor
from Settings import *

# Members:
#   controllerNode
#   nodePath
#   animator
#   pose
class Player(Character):
    def __init__(self, world, render, name):
        animator = Actor('models/Actors/lego/Bricker/Bricker3.egg',
                             {
                                 'fallbackGetup': 'models/Actors/lego/Bricker/Bricker-FallbackGetup.egg',
                                 'fallforwardGetup': 'models/Actors/lego/Bricker/Bricker-FallforwardGetup.egg',
                                 'fireball': 'models/Actors/lego/Bricker/Bricker-fireball.egg',
                                 'jump': 'models/Actors/lego/Bricker/Bricker-jump.egg',
                                 'punching': 'models/Actors/lego/Bricker/Bricker-punching.egg',
                                 'run': 'models/Actors/lego/Bricker/Bricker-run.egg',
                                 'superpunch': 'models/Actors/lego/Bricker/Bricker-superpunch.egg',
                                 'walk': 'models/Actors/lego/Bricker/Bricker-walk.egg'
                             })
        Character.__init__(self, world, render, name, animator, STANDING)