from panda3d.core import Vec3, Point3

stageFilePath = "models/Ground2/Ground2.egg"

# boxSize, pos, name, modelPath, numberOfEnemy
Stages = [(Vec3(15, 15, 0.2), Vec3(-63, -63, 9), 'Stage1', stageFilePath, 0, 2),
          (Vec3(15, 15, 0.2), Vec3(-63, -63, 9), 'Stage1', stageFilePath, 0, 2),
          (Vec3(15, 5, 0.2), Vec3(-29, -50, 10), 'Stage2', stageFilePath, 0, 2),
          (Vec3(3, 15, 0.2), Vec3(-20, -25, 11), 'Stage3', stageFilePath, 0, 2),
          (Vec3(3, 7, 0.2), Vec3(-12, -25, 12.5), 'Stage4', stageFilePath, 0, 2),
          (Vec3(7, 7, 0.2), Vec3(-10, -10, 14), 'Stage5', stageFilePath, 0, 2),
          (Vec3(2, 15, 0.2), Vec3(-0, 10, 15.5), 'Stage6', stageFilePath, 0, 1),
          (Vec3(2, 2, 0.2), Vec3(5, 10, 17), 'Stage7', stageFilePath, 0, 1),
          (Vec3(1.0, 12, 0.2), Vec3(17, 22, 18), 'Stage8', stageFilePath, -45, 1),
          (Vec3(0.85, 12, 0.2), Vec3(29, 41, 19), 'Stage9', stageFilePath, 0, 1),
          (Vec3(0.7, 12, 0.2), Vec3(40, 62, 20), 'Stage8', stageFilePath, -45, 1),
          (Vec3(0.55, 12, 0.2), Vec3(52, 80, 21), 'Stage9', stageFilePath, 0, 0),
          (Vec3(0.40, 12, 0.2), Vec3(62, 80, 22), 'Stage10', stageFilePath, 45, 0),
          (Vec3(0.40, 100, 0.2), Vec3(72, 20, 23), 'Stage11', stageFilePath, 0, 0),
          (Vec3(0.40, 120, 0.2), Vec3(0, 0, 24), 'Stage12', stageFilePath, 45, 0)]