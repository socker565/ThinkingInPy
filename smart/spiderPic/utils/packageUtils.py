import os


def getDir(level):
    if (level == -1):
        return os.path.abspath(os.path.join(os.getcwd(), ".."))
    elif (level == -2):
        return os.path.abspath(os.path.join(os.getcwd(), "../.."))
    return os.getcwd()


def makeDir(dir):
    if os.path.isdir(dir):
        pass
    else:
        os.mkdir(dir)

