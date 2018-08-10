import os


def printPath(flag):
    pathLike = ""
    if flag == 1:
        pathLike = ".."
    elif flag == 2:
        pathLike = "../.."
    path = os.path.abspath(os.path.join(os.getcwd(), pathLike))
    print(path)


def testPath():
    printPath(0)
    printPath(1)
    printPath(2)


testPath()
