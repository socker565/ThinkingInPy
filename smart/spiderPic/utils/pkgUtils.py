import os


def getDir(level):
    paths = ".."
    number = level - -1
    if number < 1:
        for i in range(number, 0):
            paths += "/.."
        return os.path.abspath(os.path.join(os.getcwd(), paths))
    return os.getcwd()


def makeDir(dir):
    if os.path.isdir(dir):
        pass
    else:
        os.mkdir(dir)


def getLevelPath(level, sonPath):
    levelPath = getDir(level)
    path = os.path.join("", levelPath + sonPath)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def getSysPath(sonPath, params):
    home_path = os.path.expanduser('~')
    path = os.path.join(home_path, sonPath, params)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def testPath():
    path1 = getLevelPath(-2, '\\download\\meinv\\')
    print(path1)
    pPath = getDir(-2) + '\\download\\'
    makeDir(pPath)
    cPath = pPath + "meinv\\"
    makeDir(cPath)
    print(cPath)

# testPath()
