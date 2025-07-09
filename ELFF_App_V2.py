#Author, Eoin Corless
#To convert to .exe, use pyinstaller --onefile ELFF_App_V2.py

# I M P O R T S #
import numpy as np
import os
import glob
import time


def makeHeader(string):
    extensionIndex = string.rfind(".") #Finds position of the last . in the file name
    extension = string[extensionIndex+1:] #Moves onto the next char, after the last .
    length = str(len(extension)) #Gets the length of the extension
    hexValue1 = length.encode('utf-8').hex() #Converts the length integer to hex bytes
    hexValue2 = extension.encode('utf-8').hex() #Converts the extension to hex bytes
    header = hexValue1+hexValue2 #Creates the header data
    return header

def decodeHeader(hexStr):
    headerLength = bytes.fromhex(hexStr[:2]).decode('utf-8') #Gets first hexbyte, which encodes length of file extension
    headerLength = int(headerLength)*2 #Number of characters to be converted, since 1 character of ASCII is 2 characters when Hex
    headerStr = hexStr[2:2+headerLength] #Gets file extension in Hex
    extension = bytes.fromhex(headerStr).decode('utf-8') #Gets extension as a string
    return extension

def removeHeader(hexStr):
    headerLength = bytes.fromhex(hexStr[:2]).decode('utf-8')  # Gets first hexbyte, which encodes length of file extension
    headerLength = (int(headerLength)*2)+2  # Number of characters to be converted, since 1 character of ASCII is 2 characters when Hex, +2 from length hexbyte
    hexStr = hexStr[headerLength:]
    return hexStr

#from numpy.f2py.crackfortran import currentfilename

#.elff ->eoin's locked file format
errorEncountered = False
CurrentName = "ELFF_App_V2.py" #Make more dynamic!! Breaks when file is renamed

print(r" ______           _                _            _   ______ _ _         _____           _                 ")
print(r"|  ____( )       | |              | |          | | |  ____(_) |       / ____|         | |                ")
print(r"| |__   _   ___  | |     ___   ___| | _____  __| | | |__   _| | ___  | (___  _   _ ___| |_ ___ _ __ ___  ")
print(r"|  __| | | / __| | |    / _ \ / __| |/ / _ \/ _` | |  __| | | |/ _ \  \___ \| | | / __| __/ _ \ '_ ` _ \ ")
print(r"| |____| | \__ \ | |___| (_) | (__|   <  __/ (_| | | |    | | |  __/  ____) | |_| \__ \ ||  __/ | | | | |")
print(r"|______| | |___/ |______\___/ \___|_|\_\___|\__,_| |_|    |_|_|\___| |_____/ \__, |___/\__\___|_| |_| |_|")
print(r"      _/ |                                                                    __/ |                      ")
print(r"     |__/                                                                    |___/                       ")

while(True):

    while (True):
        mode = int(input("Encrypting? (1) or Decrypting? (2)\n"
                         "------------------------->"))
        if (mode == 1 or mode == 2):
            break
        else:
            print("Invalid Input.")

    if(mode == 1):
        while(True):
            #type is the file category to be encrypted
            type = int(input("What kind of file are you going to work with?\n"
                             "1: Image \n"
                             "2: Video \n"
                             "3: Audio \n"
                             "4: Text \n"
                             "------------------------->"))
            if(type == 1 or type == 2 or type == 3 or type == 4):
                print("\n\n")
                break
            else:
                print("Invalid Input.")

    else:
        type = 1

    if(mode == 1 or mode == 2):
        #Disclaimer
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

        def makeHexArray(): #Creates the array of all hex bytes, (00,01,02...,FF), Length = 256
            characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']  # Hex characters 0-f
            i = 0
            allHexBytes = [] #Saves all 256 hex bytes
            while (i < len(characters)):
                j = 0
                while (j < len(characters)):
                    allHexBytes.append(characters[i] + characters[j])
                    j = j + 1
                i = i + 1
            return allHexBytes

        def getAllFiles(mode,type): #Returns Array of all directory files
            current_directory = current_directory = os.getcwd() #Gets the current directory

            #Sets the types of files that can be encrypted
            if(mode == 1):
                if(type == 1):
                    filesExtensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff', '*.tif', '*.webp', '*.svg']
                elif(type == 2):
                    filesExtensions = ['*.mp4']
                elif (type == 3):
                    filesExtensions = ['*.mp3','*.wav']
                if (type == 4):
                    filesExtensions = ['*.txt','*.java','*.html','*.js','*.css','*.vue']

            elif(mode == 2):
                filesExtensions = ['*.elff'] #.elff is the encrypted file
            i = 0; files = []  #Saves all files with supported extensions
            while (i < len(filesExtensions)):
                files = files + glob.glob(os.path.join(current_directory, filesExtensions[i])) #Files contains all files with valid extensions
                i=i+1
            return files

        def makeHexMap(arr1,arr2): #Makes the Hex map from two arrays (arr1 = ['ab'], arr2 = ['rt'] ---> ab=rt)
            i = 0
            while (i < 100000): #Swaps positions 100000 times
                positions = rng.integers(0, len(arr2), 2, dtype='int64')
                char1 = arr2[positions[0]]
                char2 = arr2[positions[1]]
                arr2[positions[1]] = char1
                arr2[positions[0]] = char2
                i = i + 1
            hexMap = {arr1[i]: arr2[i] for i in range(len(arr1))} #Creates a map of the two hex byte arrays
            return hexMap

        files = getAllFiles(mode,type) #Gets all files of valid extension
        allHexBytes = makeHexArray() #Makes a "standard" hex array (00, 01, 02, ... , FE, FF)
        shuffledBytes = allHexBytes.copy() #Copies the hex byte array
        hexMap = makeHexMap(allHexBytes, shuffledBytes) #Shuffles the 2nd hex byte array
        if(mode == 2): #Reverses the mapping if decrypting (so from shuffled -> standard)
            reversedMap = {v: k for k, v in hexMap.items()}
            hexMap = reversedMap

        #Loop through the list of files
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
                with open(file, 'rb') as f: #Binary read
                    image_data = f.read()
                    hexStr = image_data.hex() #Converts bytes to a hex string

                if(mode == 2):#Decrypting
                    extension = decodeHeader(hexStr) #Decodes the extension header
                    hexStr = removeHeader(hexStr) #Removes Header from hex string

                converted_str = ''.join(hexMap[hexStr[i:i + 2]] for i in range(0, len(hexStr), 2)) #Uses mapping dictionary

                if(mode == 1):#Encrypting
                    header = makeHeader(file) #Creates header data
                    converted_str = header+converted_str #Adds header data to the start of the hex string

                binary_data = bytes.fromhex(converted_str) #Converts hex string into back into binary data
                filename = removeExtension(file) #Removes the file extension from the file
                if(mode == 1):#Encrypting
                    output = filename+".elff" #Adds .elff to the encrypted file, ( eoin's locked file format)
                    with open(output, 'wb') as file:
                        file.write(binary_data) #Creates a file with the current binary data
                        os.remove(fileNames[counter]) #Removes the original unencrypted file
                elif(mode == 2):#Decrypting
                    output = filename + "." + extension #Adds the decoded extension
                    with open(output, 'wb') as file:
                        file.write(binary_data) #Writes the decrypted file (Leaves encypted form in case of incorrect code)

                counter = counter + 1 #Moves onto the next file
    else:
        print("Invalid Input")

    print("Task Completed!")
    time.sleep(2)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n")