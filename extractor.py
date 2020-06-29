import csv
import sys
import datetime
import subprocess

def readCsvFile(fileName):
    with open(fileName, 'r') as readFile:
        reader = csv.reader(readFile)
        rows = list(reader)
        if len(rows) > 0:
            return rows
        else:
            return None


def popRow(row):
    row.pop(26)
    row.pop(25)
    row.pop(22)
    row.pop(21)
    row.pop(20)
    row.pop(19)
    row.pop(18)
    row.pop(17)
    row.pop(16)
    row.pop(15)
    row.pop(14)
    row.pop(11)
    row.pop(10)
    row.pop(7)
    row.pop(6)
    row.pop(4)
    row.pop(3)
    return row


def runFirebaseScripts(appName, fileName, fileFormat):
    subprocess.call(["firebase", "login"])
    subprocess.call(["firebase", "projects:list"])
    subprocess.call(["firebase", "use", appName])
    subprocess.call(["firebase", "auth:export", fileName, "--format=" + fileFormat])
    subprocess.call(["firebase", "logout"])


def printHelp():
        print('Firebase auth data extractor\n')
        print('Name')
        print('\tFire auth data extractor - a fast firebase email extractor\n')
        print('Synopsis\n')
        print('\tpython extractor.py [--app-name] [--file] [--help] [--output-file]\n')
        print('Description\n')
        print('\t Firebase auth data extractor is a fast extractor of firebase auth data which may help you to generate your user\'s email in the firebase platform.\n')
        print('Options')
        print('\t--app-name')
        print('\t\tApp name in your firebase project \n')
        print('\t--file')
        print('\t\tFile that will be processed\n')
        print('\t--output-file')
        print('\t\tFile that will be the storage of the processed file\n')


if __name__ == "__main__":
    arguments = sys.argv
    i = 0
    appName = None
    fileName = None
    fileFormat = "csv"
    isHelp = False
    outputFileName = None
    outputFileNameHeaders = ['UID', 'Email', 'Email Verified', 'Name', 'Google Email', 'Google Display Name', 'Facebook Email', 'Facebook Display Name', 'User Creation Time', 'Last Sign-In Time']
    
    
    for argument in arguments:
        if argument == "--file":
            try:
                fileName = arguments[i+1]
            except:
                fileName = None


        if argument == "--app-name":
            try:
                appName = arguments[i+1]
            except:
                appName = None
        
        
        if argument == "--output-file":
            try:
                outputFileName = arguments[i+1]
            except:
                outputFileName = None

       
        if argument == "--help":
            isHelp = True


        i += 1


    if i <= 1 or isHelp or fileName is None or outputFileName is None or appName is None:
        printHelp()
    else:
        runFirebaseScripts(appName, fileName, fileFormat)

        if fileName is not None and outputFileName is not None:
            print('preparing to read the file')
            rows = readCsvFile(fileName)
            print('already read file')
            if rows is not None:
                if outputFileName is not None:
                    print('preparing to write to ' + fileName )
                    with open(outputFileName, 'w') as writeFile:
                        writer = csv.writer(writeFile)
                        writer.writerow(outputFileNameHeaders)
                        for row in rows:
                            newRow = popRow(row)

                            if newRow[8] is not None and newRow[8] != '':
                                newRow[8] = datetime.datetime.fromtimestamp(long(newRow[8])/1000).strftime('%Y-%m-%d %H:%M:%S')
                            else:
                                pass


                            if newRow[9] is not None and newRow[9] != '':
                                newRow[9] = datetime.datetime.fromtimestamp(long(newRow[9])/1000).strftime('%Y-%m-%d %H:%M:%S')
                            else:
                                pass


                            writer.writerow(newRow)
                        print('wrote to file')            
                else:
                    print("you don't have output file name declared")
            else:
                print('file cannot be opened or nothing to read')
