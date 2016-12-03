from Character import *
from direct.actor.Actor import Actor
from Settings import *

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
                                  'walk': 'models/Actors/lego/Shield/Shield-walk.egg'
                              })
        Character.__init__(self, world, render, name, animator, position, STANDING)
        self.pushSound = base.loader.loadSfx("sounds/push.wav")
        self.position = position

    def updatePlayerPosition(self, playerPosition):
        vectorToTarget = playerPosition - self.nodePath.getPos()
        vectorFromOrigin = self.position - self.nodePath.getPos()
        if (vectorToTarget.length() < SHIELD_ATTACKING_RADIUS and vectorFromOrigin.length() < SHIELD_MAX_DISTANCEToTarget_FROM_HOME):
            self.attack(playerPosition);
        elif (vectorFromOrigin.length > 0):
            self.goBackHome()

    def attack(self, target):
        print("Attacking...")
        vectorToTarget = target - self.nodePath.getPos()
        target.setZ(self.nodePath.getZ())
        # TODO: add turning
        self.nodePath.lookAt(target)

        distanceToTarget = vectorToTarget.length()
        heightDelta = vectorToTarget.getZ()
        if (distanceToTarget < SHIELD_ATTACKING_RADIUS) and (abs(heightDelta) < 0.1):
            if not self.isWalking():
                self.setPose(RUNNING)

        if not self.isAttacking() and distanceToTarget < SHIELD_ATTACKING_RADIUS:
            self.setPose(ATTACKING)
            self.pushSound.play()
            if distanceToTarget > SHIELD_ATTACKING_RADIUS and not self.isAttacking():
                self.nodePath.node().setLinearMovement(Vec3(0, TYPE_1_ENEMY_MOVING_SPEED, 0), True)
            else:
                self.nodePath.node().setLinearMovement(Vec3(0, 0, 0), True)
                self.pushed = True
                self.pushedDirection = vectorToTarget
                vectorToTarget.normalize()
        else:
            if self.isWalking():
                self.setPose(STANDING)
        self.nodePath.node().setLinearMovement(Vec3(0, SHIELD_MOVING_SPEED, 0), True)