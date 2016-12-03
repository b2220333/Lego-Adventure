from Character import *
from direct.actor.Actor import Actor
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
    def updatePlayerPosition(self, playerPosition):
        vectorToTarget = playerPosition - self.nodePath.getPos()
        vectorFromOrigin = self.position - self.nodePath.getPos()
        # print("from origin: " + str(vectorFromOrigin.length()) + ", distance to target:" + str(vectorToTarget.length()))
        # print(type(vectorFromOrigin))
        if (vectorToTarget.length() < SHIELD_ATTACKING_RADIUS and vectorFromOrigin.length() < SHIELD_MAX_DISTANCE_FROM_HOME):
            self.attack(playerPosition);
        elif (vectorFromOrigin.length > 0):
            self.goBackHome()

    def attack(self, target):
        print("Attacking...")
        target.setZ(self.nodePath.getZ())
        vectorToTarget = target - self.nodePath.getPos()
        # TODO: add turning
        self.nodePath.lookAt(target)
        distance = vectorToTarget.length()
        heightDelta = vectorToTarget.getZ()
        if (distance < TYPE_1_ENEMY_ATTACK_RAIUS) and (abs(heightDelta) < 0.1):
            if not self.isWalking():
                self.setPose(RUNNING)

        if not self.isAttacking() and distance < GUARD_ATTACKING_RADIUS:
            self.setPose(ATTACKING)
            self.pushSound.play()
            if distance > GUARD_ATTACKING_RADIUS and not self.isAttacking():
                self.nodePath.node().setLinearMovement(Vec3(0, TYPE_1_ENEMY_MOVING_SPEED, 0), True)
            else:
                self.nodePath.node().setLinearMovement(Vec3(0, 0, 0), True)
                self.pushed = True
                self.pushedDirection = vectorToTarget
                vectorToTarget.normalize()
        else:
            if self.isWalking():
                self.setPose(STANDING)
        self.nodePath.node().setLinearMovement(Vec3(0, GUARD_MOVING_SPEED, 0), True)