'''

SceTi.py

@summary: Adds scene titles from yWriter's exported "Outline" file as HTML comments to the pre-processed HTML export file.
OpenOffice shall display these comments e.g. in the Navigator.
This script reads scene titles from "auto_outline.txt" generated by yWriter (Project-->Export Project-->Outline).
This script identifies scene beginnings in "Exported Project.html" by the <h6> tag inserted by yW2OO.py postprocessor. 
@author: Peter Triesberger
@see: https://github.com/peter88213/yW2OO
@license: The MIT License (https://opensource.org/licenses/mit-license.php)
@copyright: (c) 2019, Peter Triesberger
@return: Exit code 
    0 if no error occurred;
    1 if "Exported Project.html" or "auto_outline.txt" cannot be read or written;
    2 if "Exported Project.html" is not pre-processed or contains no scene;
    3 if "Exported Project.html" and "auto_outline.txt" contain different numbers of scenes.
@precondition: The file "Exported Project.html" must exist with r/w access in the working directory. It must be pre-processed by yW2OO.py, i.e. each scene begins with a <H6> formatted paragraph.
@precondition: The File "auto_outline.txt" must exist in the directory just above the working directory. It must match to "Exported Project.html", i.e the number of SceneTitles must be the same.
@postcondition: The file "Exported Project.html" is modified (see summary).
@since: 2019-10-05
@version: v1.0.0
'''
import sys
startMessage = '\nSceTi adding yWriter scene titles to HTML export v1.0.0'

HTMLfileName = "Exported Project.html" # yWriter default
SceneFileName = "../auto_outline.txt" # yWriter default

if __name__ == '__main__':
    exitcode = 0
    print(startMessage)
    try:     
        message = 'ERROR: Cannot open "'+HTMLfileName+'".\nPlease export yWriter project as HTML first!\n'
        HTMLfile = open(HTMLfileName,'r')
        HTMLdata = HTMLfile.readlines()
        HTMLfile.close()

        message = 'ERROR: Cannot open "'+SceneFileName+'".\nPlease export outline first!\n'
        SceneFile = open(SceneFileName,'r')
        SceneData = SceneFile.readlines()
        SceneFile.close()

    except:
        print(message)
        exitcode = 1
        sys.exit(exitcode)

    else:
        SceneTitles=[]
        for line in SceneData:
            if line.count("[scene]") > 0:
                SceneTitles.append("<!-- "+line.rstrip()+" -->\n")
        OutlineSceneCount = len(SceneTitles)
                
        HTMLsceneCount = 0
        ProjectData=[]
        for line in HTMLdata:
            if line.count("<H6>") > 0:
                if HTMLsceneCount < OutlineSceneCount:
                    ProjectData.append(SceneTitles[HTMLsceneCount])
                HTMLsceneCount = HTMLsceneCount +1
            ProjectData.append(line)
            
        if HTMLsceneCount == 0:
            print('ERROR: "'+HTMLfileName+'" is not pre-processed or contains no scene.\nPlease run yW2OO.py first!\n')
            exitcode = 2

        elif HTMLsceneCount != OutlineSceneCount:
            print('ERROR: "'+HTMLfileName+'" and "'+SceneFileName+'" do not match.\nPlease re-export outline first!\n')
            exitcode = 3

        if exitcode == 0:
            try:   
                message = 'ERROR: Cannot write "'+HTMLfileName+'".\n'
                HTMLfile = open(HTMLfileName,'w')
                HTMLfile.writelines(ProjectData)
                HTMLfile.close()
                print('Added '+str(OutlineSceneCount)+' Scene Titles as comments to "'+HTMLfileName+'".\n')
            except:
                print(message)
                exitcode = 1
                
        sys.exit(exitcode)
