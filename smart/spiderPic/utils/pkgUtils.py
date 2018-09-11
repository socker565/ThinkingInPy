import _md5
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
    if not os.path.isfile(path):
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


def get_md5_name(url):
    f_str = url.encode("utf-8")
    md5 = _md5
    m = md5.md5(f_str)
    r = md5.MD5Type.hexdigest(m)
    return r

# testPath()
# res = (get_md5_name(
#     "http://imglf6.nosdn0.126.net/img/eHJBeHlSUFlxWXpoT2Juc1ZCZTMrQnBVcnhVeFZIZThGa0JSTWFxZ29OcEZyY0JDb2JEYXRBPT0.jpg?imageView&thumbnail=1680x0&quality=96&stripmeta=0&type=jpg"))
# print(get_md5_name(res))
