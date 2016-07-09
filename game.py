# LIHAO LIN Created on 07/08/2016 All right reserved
from direct.showbase.ShowBase import ShowBase


class LegoAdventure(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setupLights()

    def setupLights(self):
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


game = LegoAdventure()
game.run()
