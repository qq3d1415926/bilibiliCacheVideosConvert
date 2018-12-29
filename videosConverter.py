import os
import json
import shutil

repeat = 0
fatherDir = None
targetDir = None

def getSubDir():
    global repeat
    global fatherDir
    fatherDir = input("把缓存视频的父文件夹路径粘贴到这儿: >> ")
    if os.path.isdir(fatherDir):
        return os.listdir(fatherDir)
    else:
        repeat += 1
        if repeat > 2:
            return None
        print("不是文件夹哦！请仔细一点.")
        getSubDir()

def checkSubDirs(dirs):
    if len(dirs) == 0:
        return False
    else:
        numOfDirs = 0
        for ele in dirs:
            if ele.isdigit():
                numOfDirs += 1
            else:
                numOfDirs -= 1
        if numOfDirs == len(dirs):
            return True
        else:
            return False

def createTargetDir(fatherDir):
    myDir = input("输入你要存放的目录哟骚年: >> ")
    if myDir == None or myDir == '' or not os.path.isdir(myDir):
        print("输入的是什么狗屁东东嘛！我只好用默认路径了……")
        return os.path.dirname(fatherDir)
    else:
        return myDir

def everyDir(aDir):
    global targetDir
    entryFileUrl = None
    # mainDirUrl = None
    entryFile = None
    entryJsonObj = None
    oldFile = None
    if os.path.isdir(aDir):
        gsDirs = os.listdir(aDir)
        gsDirs = [aDir + "\\" + s for s in gsDirs]
        for ele in gsDirs:
            if os.path.isfile(ele):
                if ele[-10:] == 'entry.json':
                    entryFileUrl = ele
            # elif os.path.isdir(ele):
            #     mainDirUrl = ele
            else:
                pass

        try:
            entryFile = open(entryFileUrl, 'r', encoding = 'utf-8')
            entryJsonObj = json.loads(entryFile.read())
        except:
            print("文件\"{}\"操作失败！".format(entryFileUrl))
        finally:
            entryFile.close()

        titleDir = entryJsonObj['title']
        itemDir = targetDir + "\\" + titleDir
        if titleDir not in os.listdir(targetDir):
            os.mkdir(itemDir)
        else:
            pass
        typeTagUrl = entryJsonObj['type_tag']
        pageName = entryJsonObj['page_data']['page']
        partName = entryJsonObj['page_data']['part']
        newFile = itemDir + "\\" + str(pageName) + "-" + partName + ".flv"
        for item in os.listdir(aDir + "\\" + typeTagUrl):
            if item[-4:] == '.blv':
                oldFile = aDir + "\\" + typeTagUrl + "\\" + item
            else:
                pass
        if os.path.isfile(oldFile) and newFile not in os.listdir(itemDir):
            print("正在转换{}……".format(pageName + "-" + partName))
            shutil.copyfile(oldFile, newFile)
        else:
            pass
    else:
        print("\"{}\"不是一个目录哦！".format(aDir))


if __name__ == '__main__':
    subDirs = getSubDir()
    targetDir = createTargetDir(fatherDir)
    if checkSubDirs(subDirs):
        subDirs.sort(key = lambda s : int(s))
        subDirs = [fatherDir + '\\' + s for s in subDirs]
        print("正在转换哦，请坐和放宽0^_^0………………")
        for ele in subDirs:
            everyDir(ele)
        print("转换完成啦！我好棒棒哦，快夸我！")
    else:
        print("目录里面好像混入了什么奇怪的东西？好好检查一下哦！")
