import csv
from okta import UsersClient
from okta.models.user import User
from okta import UserGroupsClient
from okta.models.usergroup import UserGroup
import os
import io
import time
from datetime import date

#Find new users
def compareOldvNew():

    #Set key
    column = 0
    
    #Set secondary key
    secondary_column = 0
    
    #Open CSV files
    master = open('file1.csv', 'rb')
    secondary = open('file2.csv', 'rb')
    results = open('results.csv', 'wb')
    
    #Get header in CSV
    header = master.next()

    #Splitting off the header
    for idx, label in enumerate(header.split(',')):
        if label == "Position ID":
            column = idx
            
    keys = {}
    
    #Sets Employee ID as the key in Master CSV
    for line in master:
        keys.update({line.split(',')[column]:None})
        print keys
    
    #Sets Employee ID as the key in Secondary CSV
    secondary_header = secondary.next()
    for idx, label in enumerate(secondary_header.split(',')):
        if label == 'Position ID':
            secondary_column = idx
            
    #Writes Header to results.csv
    results.write(header)
    
    #Finds the any new users in the latest CSV file
    for line in secondary:
        if line.split(',')[secondary_column] in keys:
            #Do nothing because the ID is in the master
            print "ID exists in master CSV:", line.split(',')[secondary_column]
        else:
            #Key is not in the master. Put whole row in the results
            print "New ID Found:", line.split(',')[secondary_column]
            results.write(line)
    
    #Closes all CSV files
    master.close()
    secondary.close()
    results.close()
    return 
    
#Creates the curl bash file for each new Okta User
def createBashFile():

    with open('results.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        iteration=1
        for row in reader:

            firstName       = (row['First Name'])
            lastName        = (row['Last Name'])
            middleName      = (row['Middle Name'])
            email           = (row['Work Contact: Work Email'])
            title           = (row['Job Title Description'])
            primaryPhone    = (row['Work Contact: Work Phone'])
            city            = (row['Location Description'])
            employeeNumber  = (row['Position ID'])
            department      = (row['Home Department Description'])
            manager         = (row['Reports To Name'])
            positionStatus  = (row['Position Status'])
            termDate        = (row['Termination Date'])
            login           = firstName + "." + lastName + "@companyname.com"
            
            fileName = "createUser" + str(iteration) + ".bash"
            with io.FileIO(fileName, "w") as file:
                f = file.write
                f("curl -v -X POST \\\n")
                f("-H \"Accept: application/json\" \\\n")
                f("-H \"Content-Type: application/json\" \\\n")
                f("-H \"Authorization: SSWS ${API TOKEN}\" \\\n")
                f("-d '{\n")
                f("  \"profile\": {\n")
                f("    \"login\": \"" + login + "\",\n")
                f("    \"firstName\": \"" + firstName + "\",\n")
                f("    \"lastName\": \"" + lastName + "\",\n")
                f("    \"middleName\": \"" + middleName + "\",\n")
                f("    \"email\": \"" + email + "\",\n")
                f("    \"title\": \"" + title + "\",\n")
                f("    \"primaryPhone\": \"" + primaryPhone + "\",\n")
                f("    \"city\": \"" + city + "\",\n")
                f("    \"employeeNumber\": \"" + employeeNumber + "\",\n")
                f("    \"department\": \"" + department + "\",\n")
                f("    \"manager\": \"" + manager + "\"\n")
                f("  }\n")
                f("}' \"https://${ORG}.oktapreview.com/api/v1/users?activate=false\"")
                
            iteration +=1

#Runs the bash file and pushes the new user to Okta via curl
def runBashFile():

    os.system("chmod +x createUser*")
    os.system("for i in createUser*; do bash $i; done")

#Cleans up all the bash files
def cleanup():

    #creates userArchive if it doesn't already exist
    os.system("mkdir -p userArchive")

    #Creates date/time directory under the userArchive
    #Moves createUser* files to that directory
    d = date.fromordinal(730920) # 730920th day after 1. 1. 0001
    currentDate = d.strftime("%d%m%y")
    currentTime = time.strftime("%Ih%Mm%Ss")
    newFolder = "mkdir userArchive/" + currentDate + "_" + currentTime
    mvFiles = "mv createUser* userArchive/" + currentDate + "_" + currentTime
    os.system(newFolder)
    os.system(mvFiles)

compareOldvNew()
createBashFile()
runBashFile()
cleanup()
