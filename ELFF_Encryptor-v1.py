import numpy as np
import os
import glob
import time

from numpy.f2py.crackfortran import currentfilename

#.elff ->eoin's locked file format
errorEncountered = False
CurrentName = "ELFF_Encryptor-v1.py" #Update to make this more Dynamic

print(r" ______           _                _            _   ______ _ _         _____           _                 ")
print(r"|  ____( )       | |              | |          | | |  ____(_) |       / ____|         | |                ")
print(r"| |__   _   ___  | |     ___   ___| | _____  __| | | |__   _| | ___  | (___  _   _ ___| |_ ___ _ __ ___  ")
print(r"|  __| | | / __| | |    / _ \ / __| |/ / _ \/ _` | |  __| | | |/ _ \  \___ \| | | / __| __/ _ \ '_ ` _ \ ")
print(r"| |____| | \__ \ | |___| (_) | (__|   <  __/ (_| | | |    | | |  __/  ____) | |_| \__ \ ||  __/ | | | | |")
print(r"|______| | |___/ |______\___/ \___|_|\_\___|\__,_| |_|    |_|_|\___| |_____/ \__, |___/\__\___|_| |_| |_|")
print(r"      _/ |                                                                    __/ |                      ")
print(r"     |__/                                                                    |___/                       ")

while(True):
    while(True):
        type = int(input("What kind of file are you going to work with?\n"
                         "1: Image (decrypted to .png)\n"
                         "2: Video (decrypted to .mp4)\n"
                         "3: Audio (decrypted to .wav)\n"
                         "4: Text (decrypted to .txt)\n"
                         "------------------------->"))
        if(type == 1 or type == 2 or type == 3 or type == 4):
            print("\n\n")
            break
        else:
            print("Invalid Input.")

    while(True):
        mode = int(input("Encrypting? (1) or Decrypting? (2)\n"
                         "------------------------->"))
        if(mode == 1 or mode == 2):
            break

    if(mode == 1 or mode == 2):
        print("\n\n\n"
              "------*VERY IMPORTANT NOTICE!*------\n"
              "i:   If you forget your access code, you will permanently lose all access to your files. (You will need it to decrypt them)\n"
              "ii:  Save your code or make sure it is written down somewhere\n"
              "iii:  I am not responsible for lost files (Though I've made sure that doesn't happen)\n"
              "iv:  This programs encrypts all files in the folder its in of the selected type (images, audio, ect)\n"
              "v:   So, Double check what files you're encrypting!\n"
              "vi:  If you have any issues or suggestions, please email me at TrilomorphSoftware@gmail.com or DM me on discord (@ejcman)\n\n")

        while(True):
            try:
                seed = int(input("Enter your access code: ")) #The Seed for the Random Number Generator
                break  # exit the loop if conversion succeeds
            except ValueError:
                print("Invalid input. Please enter numbers only.")
        rng = np.random.default_rng(seed)

        def removeExtension(filename): #Removes the file extension from the file
            return os.path.splitext(filename)[0]

        def makeHexArray(): #Creates the array of all hex bytes, Length = 256
            characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']  # Hex characters 0-f
            i = 0
            allHexBytes = []
            while (i < len(characters)):
                j = 0
                while (j < len(characters)):
                    allHexBytes.append(characters[i] + characters[j])
                    j = j + 1
                i = i + 1
            return allHexBytes

        def getAllFiles(mode,type):
            current_directory = current_directory = os.getcwd() #Gets the current directory
            if(mode == 1):
                if(type == 1):
                    filesExtensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff', '*.tif', '*.webp', '*.svg']
                elif(type == 2):
                    filesExtensions = ['*.mp4']
                elif (type == 3):
                    filesExtensions = ['*.mp3','*.wav']
                elif (type == 4):
                    filesExtensions = ['*.txt','*.py','*.java','*.html','*.js','*.css','*.vue']
            elif(mode == 2):
                if (type == 1):
                    filesExtensions = ['*.elffI']
                elif (type == 2):
                    filesExtensions = ['*.elffV']
                elif (type == 3):
                    filesExtensions = ['*.elffA']
                elif (type == 4):
                    filesExtensions = ['*.elffT']
            i = 0; files = []  # Saves all files with supported extensions
            while (i < len(filesExtensions)):
                files = files + glob.glob(os.path.join(current_directory, filesExtensions[i]))
                i=i+1
            return files

        def makeHexMap(arr1,arr2): #Makes the Hex map from two arrays (arr1 = ['ab'], arr2 = ['rt'] ---> ab=rt)
            i = 0
            while (i < 100000):
                positions = rng.integers(0, len(arr2), 2, dtype='int64')  # Rolls 1d6
                char1 = arr2[positions[0]]
                char2 = arr2[positions[1]]
                arr2[positions[1]] = char1
                arr2[positions[0]] = char2
                i = i + 1
            hexMap = {arr1[i]: arr2[i] for i in range(len(arr1))}
            return hexMap

        files = getAllFiles(mode,type)
        allHexBytes = makeHexArray()
        shuffledBytes = allHexBytes.copy()
        hexMap = makeHexMap(allHexBytes, shuffledBytes)
        if(mode == 2):
            reversedMap = {v: k for k, v in hexMap.items()}
            hexMap = reversedMap

        #Loop through the list of files and read them
        counter = 0
        if(len(files)!=0):
            fileNames = [os.path.basename(f) for f in files]
            for file in files:
                if(fileNames[counter] == CurrentName):
                    print("Skipping "+CurrentName+"!")
                    continue
                if(mode == 1):
                    print("Encrypting "+fileNames[counter]+"...")
                elif(mode == 2):
                    print("Decrypting " + fileNames[counter] + "...")
                else:
                    print("Error!")
                with open(file, 'rb') as f:
                    image_data = f.read()
                    hex_str = image_data.hex()

                converted_str = ''.join(hexMap[hex_str[i:i + 2]] for i in range(0, len(hex_str), 2))
                binary_data = bytes.fromhex(converted_str)
                filename = removeExtension(file)
                if(mode == 1):
                    match type:
                        case 1:
                            output = filename+".elffI"
                        case 2:
                            output = filename+".elffV"
                        case 3:
                            output = filename+".elffA"
                        case 4:
                            output = filename+".elffT"
                        case _:
                            print("Error!!! Invalid Type")
                            errorEncountered = True
                    if(errorEncountered == False):
                        with open(output, 'wb') as file:
                            file.write(binary_data)
                            os.remove(fileNames[counter])
                elif(mode == 2):
                    match type:
                        case 1:
                            output = filename+".png"
                        case 2:
                            output = filename+".mp4"
                        case 3:
                            output = filename+".wav"
                        case 4:
                            output = filename+".txt"
                        case _:
                            print("Error!!! Invalid Type")
                            errorEncountered = True
                    if (errorEncountered == False):
                        with open(output, 'wb') as file:
                            file.write(binary_data)

                counter = counter + 1
    else:
        print("Invalid Input")

    print("Task Completed!")
    time.sleep(2)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n")