'''

SceTi.py

@summary: Adds scene titles from yWriter's exported "Scene descriptions" file as HTML comments to the pre-processed HTML export file.
OpenOffice shall display these comments e.g. in the Navigator.
This script reads scene titles from "Auto_Descriptions.txt" generated by yWriter (Project-->Export Project-->Scene descriptions).
This script identifies scene beginnings in "Exported Project.html" by the <h6> tag inserted by yW2OO.py postprocessor. 
Exported yWriter scenes must not be empty.
@author: Peter Triesberger
@see: https://github.com/peter88213/yW2OO
@license: The MIT License (https://opensource.org/licenses/mit-license.php)
@copyright: (c) 2019, Peter Triesberger
@return: Exit code 
    0 if no error occurred;
    1 if "Exported Project.html" or "Auto_Descriptions.txt" cannot be read or written;
    2 if "Exported Project.html" is not pre-processed or contains no scene;
    3 if "Exported Project.html" and "Auto_Descriptions.txt" contain different numbers of scenes.
@precondition: The file "Exported Project.html" must exist with r/w access in the working directory. It must be pre-processed by yW2OO.py, i.e. each scene begins with a <H6> formatted paragraph.
@precondition: The File "Auto_Descriptions.txt" must exist in the directory just above the working directory. It must match to "Exported Project.html", i.e the number of sceneTitles must be the same.
@postcondition: The file "Exported Project.html" is modified (see summary).
@since: 2019-10-05
@change: 2019-10-06 v1.1.0 Scene titles are taken from "Auto_Descriptions.txt" instead of "auto_outline.txt". Each scene gets a number.
@change: 2019-10-21 v1.1.1 Refactoring for unit test support.
'''
import sys, re
startMessage = '\nSceTi adding yWriter scene titles to HTML export v1.1.1'

projectFileName = "Exported Project.html" # yWriter default
sceneFileName = "../Auto_Descriptions.txt" # yWriter default

def main():  
    exitcode = 0
    print(startMessage)
    try:     
        message = 'ERROR: Cannot open "'+projectFileName+'".\nPlease export yWriter project as HTML first!\n'
        projectFile = open(projectFileName,'r')
        htmlData = projectFile.readlines()
        projectFile.close()

        message = 'ERROR: Cannot open "'+sceneFileName+'".\nPlease export outline first!\n'
        sceneFile = open(sceneFileName,'r')
        sceneData = sceneFile.readlines()
        sceneFile.close()

    except:
        print(message)
        exitcode = 1
        sys.exit(exitcode)

    else:
        sceneTitles=[]
        sceneMarker = "^ 0"
        chapterNo = -1
        # Counts non-empty lines representing chapter titles.
        # The first line represents the project title and is considered "chapter #0".
        for line in sceneData:
            myMatch = re.search(".+", line.rstrip())
            if myMatch is not None :
                # Line is not empty
                myMatch = re.search(sceneMarker, line)
                if myMatch is None:
                    # Line is not a scene title
                    chapterNo = chapterNo + 1
                else:
                     sceneTitle = re.sub(sceneMarker, str(chapterNo), line)
                     sceneTitles.append("<!-- "+sceneTitle.rstrip()+" -->\n")
        outlineSceneCount = len(sceneTitles)
                
        htmlSceneCount = 0
        projectData=[]
        for line in htmlData:
            if line.count("<H6>") > 0:
                if htmlSceneCount < outlineSceneCount:
                    projectData.append(sceneTitles[htmlSceneCount])
                htmlSceneCount = htmlSceneCount +1
            projectData.append(line)
            
        if htmlSceneCount == 0:
            print('ERROR: "'+projectFileName+'" is not pre-processed or contains no scene.\nPlease run yW2OO.py first!\n')
            exitcode = 2

        elif htmlSceneCount != outlineSceneCount:
            print('ERROR: "'+projectFileName+'" and "'+sceneFileName+'" do not match.\nPlease re-export outline first!\n')
            exitcode = 3

        if exitcode == 0:
            try:   
                projectFile = open(projectFileName,'w')
                projectFile.writelines(projectData)
                projectFile.close()
                print('Added '+str(outlineSceneCount)+' Scene Titles as comments to "'+projectFileName+'".\n')
            except:
                print('ERROR: Cannot write "'+projectFileName+'".\n')
                sys.exit(1)
        else:
            sys.exit(exitcode)



if __name__ == '__main__':
    main()  

