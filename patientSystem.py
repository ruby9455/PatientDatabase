import datetime
import time
import os
import random
from typing import List
from collections import defaultdict

class Patient:
    totalPatient = 0
    def __init__(self,name:str,sex:str,dob:str):
        self.name = name
        self.sex = sex
        self.dob = dob
        self.group = None
        self.id = Patient.totalPatient + 1
        Patient.totalPatient += 1
    
    def getName(self):
        return self.name
    
    def getSex(self):
        return self.sex

    def getDOB(self):
        return self.dob

    def getPID(self):
        return self.id

    def setName(self,name: str):
        self.name = name

    def setSex(self,sex: str):
        self.sex = sex
    
    def setDOB(self,dob: str):
        self.dob

class PatientNode:
    def __init__(self,patient: Patient):
        self.patient = patient
        self.next = None
        self.prev = None
    
    def getPatient(self) -> Patient:
        return self.patient
    
    def setPatient(self,patient: Patient):
        self.patient = patient

class PatientDatabase:
    def __init__(self):
        self.head = None
        self.numNode = 0
        self.database = defaultdict() # patientID : PatientNode
        self.nameDatabase = defaultdict() # patientName : patientID
    
    def getNumPatient(self):
        return self.numNode
    
    def addPatientDatabase(self,patient: Patient):
        self.numNode += 1
        pid = patient.getPID()
        new = PatientNode(patient)
        self.database[pid] = new
        self.nameDatabase[patient.getName().upper()] = pid
        if self.head == None:
            self.head = new
        else:
            curr = self.head
            # traverse to the end of the list
            while curr.next != None:
                curr = curr.next
            new.prev = curr
            curr.next = new
        print(patient.getName(),"is added to database")
    
    def delPatientDatabase(self,pid):
        # edge case: empty database
        if not self.numNode:
            print("The database is empty")

        # edge case: pid not in database
        if pid not in self.database:
            print("Patient ID",pid,"is not found in database")

        if pid in self.database:
            node = self.database[pid] # PatientNode
            prevNode = nxtNode = None

            # remove the first node
            if node.prev:
                prevNode = node.prev
            # remove the last node
            if node.next:
                nxtNode = node.next

            # handle 4 cases
            # 1. if both nodes are found
            if prevNode and nxtNode:
                prevNode.next = nxtNode
                nxtNode.prev = prevNode
            # 2. if only 1 patient in database, (both nodes are none)
            elif not prevNode and not nxtNode:
                self.head = None
            # 3. if only nxtNode is found (remove first node)
            elif not prevNode:
                self.head = nxtNode
            # 4. if only prevNode is found (remove last node)
            else:
                prevNode.next = None
            self.numNode -= 1
            print("Patient ID",node.getPatient().getPID(),"is removed from database")

    def searchByID(self):
        pid = int(input("Enter Patient ID: "))
        if pid in self.database:
            self.printNode(self.database[pid])
        else:
            print("Patient ID ",pid,"is not in the database.")

    def searchByName(self):
        name = input("Enter Patient Name: ")
        if name.upper() in self.nameDatabase:
            self.printNode(self.database[self.nameDatabase[name.upper()]])
        else:
            print("Patient ",name,"is not in the database.")

    def printList(self):
        if self.head == None:
            print("The database is empty")
        else:
            curr = self.head
            while curr:
                self.printNode(curr)
                curr = curr.next
    
    def printNode(self,node:PatientNode):
        patient = node.getPatient()
        output = "Patient ID: " + str(patient.getPID()) + "\n"
        output += "Name: " + patient.getName() + "\n"
        output += "Sex: " + patient.getSex() + "\n"
        output += "Date of birth: " + patient.getDOB() + "\n"
        print(output)

    def checkDuplicate(self,name,sex,dob) -> bool:
        if name in self.nameDatabase:
            sexDatabase = self.database[self.nameDatabase[name.upper()]].getPatient().getSex()
            dobDatabase = self.database[self.nameDatabase[name.upper()]].getPatient().getDOB()
            if sexDatabase == sex and dobDatabase == dob:
                print(name,"is already in the database")
                return True
        return False

class PatientSystem:
    sysDatabase = PatientDatabase()
    def __init__(self):
        _menuOption = [1, 2, 3, 4, 5, 0]
        _continue = True
        p1 = Patient("RUBY","F","1990-06-13")
        p2 = Patient("KRY","F","1993-09-17")
        p3 = Patient("CANDY","F","1963-08-31")
        self.sysDatabase.addPatientDatabase(p1)
        self.sysDatabase.addPatientDatabase(p2)
        self.sysDatabase.addPatientDatabase(p3)
        while _continue:
            os.system("cls" if os.name == "nt" else "clear")
            self.displayMenu()
            _option = self.getOption(_menuOption)
            if _option != None and _option != -1:
                _continue = self.performTask(_option)
            else:
                if _option == None:
                    print(":: It is not a number, please try again  ::" + "\n")
                else:
                    print(":: Invalid option, please select again   ::" + "\n")
                self.displayTryAgain()
            
    def displayHeader(self, toPrint: bool):
        output = "\n\n\n"
        output += "===========================================" + "\n"
        output += ":: Patient Management System             ::" + "\n"
        output += "===========================================" + "\n"
        if toPrint:
            print(output)
        return output

    def displayMenu(self):
        output = self.displayHeader(False)
        output += ":: Options:                              ::" + "\n"
        output += ":: 1. Add Patient                        ::" + "\n"
        output += ":: 2. Delete Patient                     ::" + "\n"
        output += ":: 3. Search Patient by Name             ::" + "\n"
        output += ":: 4. Search Patient by ID               ::" + "\n"
        # output += ":: 5. Randomization                      ::" + "\n"
        output += ":: 5. Print Patient List                 ::" + "\n"
        output += ":: 0. Exit                               ::" + "\n"
        output += "===========================================" + "\n"
        print(output)
        
    def displayTryAgain(self):
        os.system("cls" if os.name == "nt" else "clear")
        output = self.displayHeader(False)
        output += ":: Your input is invalid, please select  ::" + "\n"
        output += ":: a valid option.                       ::" + "\n"
        output += "===========================================" + "\n"
        print(output)
        self.displayWaitInput()

    def displayWaitInput(self):
        output = "\n\n\n"
        output += "::      Press enter key to continue      ::"+ "\n"
        output += "==========================================="
        print(output)
        input()

    def displayExitMessage(self):
        self.countDownSec(5)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Thank you!")
    
    def getOption(self,optionAvail:List[int]):
        _input = input(":: Your option: ")
        try:
            if _input.isdigit():
                _input = int(_input)
                return _input if _input in optionAvail else -1
            else:
                raise ValueError
        except ValueError:
            return None
    
    def countDownSec(self,t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:2d}'.format(secs)
            print("Screen will now be cleared in"+timer, end=" seconds\r")
            time.sleep(1)
            t -= 1

    def validateDate(self,dob):
        try:
            if dob != datetime.datetime.strptime(dob,"%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            return True
        except ValueError:
            return False

    def addPatient(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        name = input("Please enter the name: ")
        
        sex = input("Please enter the sex (M/F): ")
        while sex.upper() != "M" and sex.upper() != "F":
            sex = input("Please enter the sex (M/F): ")
        dob = input("Please enter the date of birth (YYYY-MM-DD): ")
        while not self.validateDate(dob):
            dob = input("Please enter the date of birth (YYYY-MM-DD): ")

        # check for duplicate name, dob and sex
        if not self.sysDatabase.checkDuplicate(name.upper(),sex.upper(),dob):
            newPatient = Patient(name.upper(),sex.upper(),dob)
            self.sysDatabase.addPatientDatabase(newPatient)
        self.displayWaitInput()

    def delPatient(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        pid = int(input("Enter patient ID to be deleted: "))
        self.sysDatabase.delPatientDatabase(pid)
        self.displayWaitInput()

    def searchDatabaseByName(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.sysDatabase.searchByName()
        self.displayWaitInput()

    def searchDatabaseByPID(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.sysDatabase.searchByID()
        self.displayWaitInput()
    
    def printDatabase(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.sysDatabase.printList()
        self.displayWaitInput()

    def performTask(self,_option):
        os.system('cls' if os.name == 'nt' else 'clear')
        if _option == 1:
            self.addPatient()
        if _option == 2:
            self.delPatient()
        if _option == 3:
            self.searchDatabaseByName()
        if _option == 4:
            self.searchDatabaseByPID()
        # if _option == 5:
        #     self.randomization()
        if _option == 5:
            self.printDatabase()
        if _option == 0:
            self.displayExitMessage()
            exit()
        return True

ps = PatientSystem()
