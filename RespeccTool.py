import xml.etree.ElementTree as ET
import subprocess
import os
import glob
import shutil

characters = ["Sebille", "The Red Prince", "Lohse"]

# Set profile name and user's home
#profile = os.path.splitext(os.path.basename(sys.argv[0]))[0]
profileName = 'UgoBUONSugo'
userPath = os.environ['USERPROFILE']
excTool = '.\\divine.exe'
if not os.path.exists(excTool):
    excTool = input("divine.exe path: ")

save_dir = f'{userPath}\\Documents\\Larian Studios\\Divinity Original Sin 2\\PlayerProfiles\\{profileName}\\Savegames\\Story\\'
if not os.path.exists(save_dir):
    save_dir = input("Enter the path to your save folder (e.g. C:\\Users\\<username>\\Documents\\Larian Studios\\Divinity Original Sin\\PlayerProfiles\\<profile>\\Savegames\\Story\\): ")
    if not save_dir.endswith('\\'):
        save_dir += '\\'
latest_save = max(glob.glob(save_dir + '*'), key=os.path.getmtime)

save_name = os.path.basename(latest_save)
save = f'{latest_save}\\{save_name}.lsv'

temp_path = os.path.abspath('.\\Temp')
subprocess.run([excTool, '-s', save, '-d', temp_path, '-a', 'extract-package'])

f = temp_path + '\\globals'
lsf = f + '.lsf'
lsx = f + '.lsx'

#Run converter tool
subprocess.run(['.\\divine.exe', '-s', lsf, '-d', lsx, '-a', 'convert-resource'])

#Create a parse tree from the "globals.lsx" file
tree = ET.parse(lsx)
root = tree.getroot()

#For every character find and delete their <node> Element, which define their non-default features
for c in characters:
    nodeParent = root.find(".//node[@id = 'PlayerCustomData']/attribute[@id = 'Name'][@value = '" + c + "']../..")
    if nodeParent is None:
        continue
    nodeParent.remove(nodeParent.find(".//node[@id = 'PlayerCustomData']/attribute[@id = 'Name'][@value = '" + c + "'].."))

#Overwrite the original save file
tree.write(lsx, encoding='utf-8', xml_declaration=True)

subprocess.run([excTool, '-s', lsx, '-d', lsf, '-a', 'convert-resource'])
os.remove(lsx)

subprocess.run([excTool, '-s', temp_path, '-d', save, '-a', 'create-package'])
shutil.rmtree(f'{temp_path}')