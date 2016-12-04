from Character import *
from direct.actor.Actor import Actor
from Settings import *
from panda3d.bullet import BulletWorld, BulletPlaneShape, BulletRigidBodyNode, BulletSphereShape

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

    def updatePlayerPosition(self, playerPosition, time):
        vectorToTarget = playerPosition - self.nodePath.getPos()
        vectorFromHome = self.position - self.nodePath.getPos()
        if (vectorToTarget.getZ() < 0.1 and vectorToTarget.length() < SHIELD_ATTACKING_RADIUS and vectorFromHome.length() < SHIELD_MAX_DISTANCE_FROM_HOME):
            self.attack(playerPosition, time);
        elif (vectorFromHome.length > 0):
            self.goBackHome()

    def attack(self, target, time):
        print("Guard Attacking...")
        target.setZ(self.nodePath.getZ())
        # TODO: add turning
        self.nodePath.lookAt(target)

        # Throwing balls at player
        if (time % 2) < 0.01:
            # clean up old balls
            # for ball in self.sphereNodes:
            #     ball.removeAllChildren()
            #     self.world.removeRigidBody(ball)

            vec = target - self.getPosition()
            distance = vec.length()
            self.setPose(SWINGING)
            # throw new ball
            pos = self.getPosition()
            shooting_direction = target - pos
            shooting_direction.normalize()
            print "shotting at: ", shooting_direction
            sphereNode = BulletRigidBodyNode('Ball')
            sphereNode.setMass(1.0)
            sphereNode.addShape(BulletSphereShape(0.2))
            sphere = self.render.attachNewNode(sphereNode)
            pos.setZ(pos.getZ() + 1)
            sphere.setPos(pos)
            smileyFace = self.loader.loadModel("models/smiley")
            smileyFace.setScale(0.2)
            smileyFace.reparentTo(sphere)
            self.world.attachRigidBody(sphereNode)
            sphereNode.applyCentralForce(shooting_direction * 1000)
            self.sphereNodes.append(sphereNode)