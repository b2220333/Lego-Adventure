# Panda3d Library
from direct.actor.Actor import Actor
# My Game Classes
from Character import *
from Settings import *

# Members:
#   controllerNode
#   nodePath
#   animator
#   pose
class Guard(Character):
    def __init__(self, world, render, name, position):
        animator = Actor('models/Actors/lego/SecurityGuard/SecurityGuard.egg',
                              {
                                  'fallbackGetup': 'models/Actors/lego/SecurityGuard/SecurityGuard-fallbackGetup.egg',
                                  'fallforwardGetup': 'models/Actors/lego/SecurityGuard/SecurityGuard-fallforwardGetup.egg',
                                  'firegun': 'models/Actors/lego/SecurityGuard/SecurityGuard-firegun.egg',
                                  'jump': 'models/Actors/lego/SecurityGuard/SecurityGuard-jump.egg',
                                  'run': 'models/Actors/lego/SecurityGuard/SecurityGuard-run.egg',
                                  'attack': 'models/Actors/lego/SecurityGuard/SecurityGuard-swing.egg',
                                  'walk': 'models/Actors/lego/SecurityGuard/SecurityGuard-walk.egg'
                              })
        Character.__init__(self, world, render, name, animator, position, STANDING)
        self.pushSound = base.loader.loadSfx("sounds/push.wav")
        self.position = position
        self.time = 1.0

    def saveShootingTime(self, time):
        self.time = time

    def getShootingTime(self):
        return self.time