import os
import re

SEARCH_PATH=os.environ["HOME"] + "/.local/share/applications"
ICONS_PATH=os.environ["HOME"] + "/.local/share/icons"
EXPECTED_PREFIX="chrome"

if "CRF_SEARCH_PATH" in os.environ:
    SEARCH_PATH = os.environ["CRF_SEARCH_PATH"]

if "CRF_ICONS_PATH" in os.environ:
    ICONS_PATH = os.environ["CRF_ICONS_PATH"]

if "CRF_EXPECTED_PREFIX" in os.environ:
    EXPECTED_PREFIX = os.environ["CRF_EXPECTED_PREFIX"]

def run():
    print("Searching for chrome apps")
    work = {}
    for files in os.listdir(SEARCH_PATH):
        if files.startswith(EXPECTED_PREFIX):
            fileName = files.split(".")[0]
            minRes = -1
            minResFile = ""
            for root, dirs, ff in os.walk(ICONS_PATH):
                for file in ff:
                    if file.startswith(fileName):
                        z = re.search(r'\/(\d+)x(\d+)\/?', root)
                        if z:
                            res = int(z.groups(1)[0])
                            if res > minRes:
                                minRes = res
                                minResFile = root + "/" + file
                        else:
                            res = 0
                            if res > minRes:
                                minRes = res
                                minResFile = root + "/" + file
            work[files] = minResFile

    print("Found " + str(len(work)) + " apps")
    if "CRF_AUTOMATE" in os.environ:
        process(work)
    else:
        print("Let's go over each file one by one and confirm which you want to alter.")
        newwork = {}
        for key in work:
            consented = False
            with open(SEARCH_PATH + "/" + key, 'r') as f:
                data = f.read()
                name = ""
                z = re.search(r'Name=(.+)\n', data)
                if z:
                    name = z.groups(1)[0]
                else:
                    name = key
                
                print("Would you like to replace the icon for " + key + " (" + name + ") with " + work[key] + " (Y/n)?")
                consent = input()
                if consent.lower() == "y":
                    consented = True
                else:
                    consented = False
            if consented:
                newwork[key] = work[key]

        process(newwork)
    print("Done. If you're a KDE user, run this command: kbuildsycoca5 --noincremental")

    
def process(data):    
    print("Processing " + str(len(data)) + " apps")
    for key in data:
        fileContent = ""
        with open(SEARCH_PATH + "/" + key, 'r') as f:
            fileContent = f.read()
            fileContent = re.sub(r'Icon=.+\n', "Icon=" + data[key] + "\n", fileContent)
        with open(SEARCH_PATH + "/" + key, 'w') as f:
            f.write(fileContent)
    

            
if "CRF_AUTOMATE" in os.environ:
    run()
else:
    print("Current configuration:")
    print("SEARCH_PATH: " + SEARCH_PATH)
    print("ICONS_PATH: " + ICONS_PATH)
    print("EXPECTED_PREFIX: " + EXPECTED_PREFIX)
    print("If you'd like to change these, or not be prompted again, use the following env vars:")
    print("CRF_SEARCH_PATH, CRF_ICONS_PATH, CRF_EXPECTED_PREFIX, CRF_AUTOMATE")
    print("Is this configuration correct? (y/n)")
    answer = input()
    if answer.lower() == "y":
        run()
    else:
        print("Exiting")

