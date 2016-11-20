from Guard import *
from Shield import *
from Player import *
from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletWorld
from panda3d.core import *
from Settings import *

class GameScene(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.level = 1

        self.setupScene()
        self.addCharacters()

    def setupScene(self):
        # Set Scene Background Color
        base.setBackgroundColor(0.1, 0.1, 0.8, 1)
        base.setFrameRateMeter(True)
        # TODO: remove this Add Camera
        self.cameraHeight = 50
        # Add Physics to GameScene
        self.addPhysicsWorld()
        # Add lightings to GameScene
        self.addLights()
        # Load Game Map
        self.loadMap()

    def addCharacters(self):
        self.addPlayer()
        self.addShield()
        self.addGuard()

# ==========    Functions setting up GameScene
    def loadMap(self):
        self.addSky()
        self.addGround()
        self.addWalls()
        self.addStages()
        self.addSpings()

    def addPhysicsWorld(self):
        # Create Physics World
        self.world = BulletWorld()
        # Add Gravity towards ground
        self.world.setGravity(Vec3(0, 0, -9.81))

    def addLights(self):
        # Add Lights
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        alightNP = render.attachNewNode(alight)
        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(1, 1, -1))
        dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        dlightNP = render.attachNewNode(dlight)
        self.render.clearLight()
        self.render.setLight(alightNP)
        self.render.setLight(dlightNP)

    def addSky(self):
        self.blue_sky_sphere = self.loader.loadModel(
            "models/blue_sky_sphere/blue_sky_sphere.egg")
        self.blue_sky_sphere.reparentTo(self.render)
        self.blue_sky_sphere.setScale(0.04, 0.04, 0.04)
        self.blue_sky_sphere.setPos(0, 0, 0)

    def addGround(self):
        self.garden = self.loader.loadModel(
            "models/garden/garden.egg")
        self.garden.reparentTo(self.render)
        self.garden.setScale(2, 2, 2)
        self.garden.setPos(0, 0, 0)
        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
        floorNP = self.render.attachNewNode(BulletRigidBodyNode('Ground'))
        floorNP.node().addShape(shape)
        floorNP.setPos(0, 0, 0)
        floorNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(floorNP.node())

    def addWalls(self):
        def addWall(size, posX, posY):
            shape = BulletBoxShape(size)
            wallNP = self.render.attachNewNode(BulletRigidBodyNode('wall'))
            wallNP.node().addShape(shape)
            wallNP.setPos(posX, posY, size.getZ())
            wallNP.setCollideMask(BitMask32.allOn())
            if (posY is 0):
                left = -(size.getY())
                right = -left
                pos = left - 5
                while pos <= right:
                    wallModel = loader.loadModel('models/fence.egg')
                    wallModel.reparentTo(wallNP)
                    wallModel.setPos(0, pos, -(size.getZ()))
                    wallModel.setScale(1, 1, 1)
                    wallModel.setH(90)
                    pos += 13.5
            else:
                left = -(size.getX())
                right = -left
                pos = left - 5
                while pos <= right:
                    wallModel = loader.loadModel('models/fence.egg')
                    wallModel.reparentTo(wallNP)
                    wallModel.setPos(pos, 0, -(size.getZ()))
                    wallModel.setScale(1, 1, 1)
                    pos += 13.5
            self.world.attachRigidBody(wallNP.node())

        addWall(Vec3(1, 90, 5), 80, 0)
        addWall(Vec3(1, 90, 5), -80, 0)
        addWall(Vec3(100, 1, 5), 0, 100)
        addWall(Vec3(100, 1, 5), 0, -100)

    def addStages(self):
        for stage in STAGE_POS_LIST:
            boxSize = stage[0]
            pos = stage[1]
            name = stage[2]
            # create a BodyNode and attach to render become a NodePath
            objNP = self.render.attachNewNode(BulletRigidBodyNode(name))
            # attach the BodyNode inside the NodePath to physics world
            self.world.attachRigidBody(objNP.node())

            # set the properties of the NodePath
            #   - shape
            shape = BulletBoxShape(boxSize)
            objNP.node().addShape(shape)
            #   - position
            objNP.setPos(pos.getX(), pos.getY(), pos.getZ())
            #   - collideMask
            objNP.setCollideMask(BitMask32.allOn())
            #   - model
            objModel = self.loader.loadModel(
                "models/brick-cube/brick.egg")
            objModel.setScale(boxSize.getX() * 2, boxSize.getY()
                              * 2, boxSize.getZ() * 2)
            objModel.setPos(0, 0, boxSize.getZ() / -1)
            objModel.reparentTo(objNP)
            #   - texture
            ts = TextureStage.getDefault()
            texture = objModel.getTexture()
            objModel.setTexOffset(ts, -0.5, -0.5)
            objModel.setTexScale(ts,
                                 boxSize.getX() / 2.0,
                                 boxSize.getY() / 2.0,
                                 boxSize.getZ() / 2.0)

    def addSpings(self):
        # TODO: remove springs
        springs = []
        for pos in SPRING_LIST:
            print "add spring #{} at: {}".format(len(springs), pos)
            shape = BulletBoxShape(Vec3(0.3, 0.3, 0.8))
            node = BulletGhostNode('Spring' + str(len(springs)))
            node.addShape(shape)
            springNP = self.render.attachNewNode(node)
            springNP.setCollideMask(BitMask32.allOff())
            springNP.setPos(pos.getX(), pos.getY(), pos.getZ() + 3.4)
            modelNP = loader.loadModel('models/spring/spring.egg')
            modelNP.reparentTo(springNP)
            modelNP.setScale(1, 1, 1)
            modelNP.setPos(0, 0, -1)
            self.world.attachGhost(node)
            springs.append(springNP)


# ==========    Functions add Characters into GameScene
    def addPlayer(self):
        shield = Player(self.world, self.render, "Bricker", PLAYER_POSITIONS[self.level])

    def addShield(self):
        counter = 0
        for position in SHIELD_POSITIONS:
            player = Shield(self.world, self.render, "Shield_{}".format(counter), position)
            counter+=1

    def addGuard(self):
        counter = 0
        for position in GUARD_POSITIONS:
            guard = Guard(self.world, self.render, "Guard_{}".format(counter), position)
            counter+=1


