# Copy writer.bat to all yWriter projects in [userprofile]\Documents

## Please note:
This toolkit is experimental. **Use it at your own risk**. 
Do not use it, if you are not familiar with the Windows cmd language. 
Do not use it, in case you don't understand the batch code. 

## Function
* Do a recursive search for yWriter projects in your *[userprofile]\Documents* folder.
* Copy *writer.bat* into each yWriter project's *Export* folder
* If needed, remove *writer.bat* from each yWriter project's *Export* folder

## Requirements
* OpenOffice or LibreOffice installation.
* yW2OO installation. **writer.bat** exists in the **yW2OO_vX.X.X** folder. 

## Procedure

### Spread "writer.bat" over all yWriter projects
1. Back up your **[userprofile]\Documents** folder.
2. Move into **yW2OO_vX.X.X\add-on** folder.
3. Run **genCopyWriter.bat** to generate **yW2OO_vX.X.X\copyWriter.bat**.
4. Move into **yW2OO_vX.X.X** folder.
3. Edit **copyWriter.bat** and remove lines containing projects you wish to omit.
4. Run **copyWriter.bat**.

### Remove "writer.bat" from all yWriter projects
1. Back up your **[userprofile]\Documents** folder.
2. Move into **yW2OO_vX.X.X\add-on** folder.
3. Run **genRemoveWriter.bat** to generate **yW2OO_vX.X.X\removeWriter.bat**.
4. Move into **yW2OO_vX.X.X** folder.
3. Edit **removeWriter.bat** and remove lines containing projects you wish to omit.
4. Run **removeWriter.bat**.

