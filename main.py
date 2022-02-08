#Student Roster program with GUI
#Purpose: allows user to create and manage a student record with names, courses and grades
#Shalva Rishe
#December 31, 2021

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import Student
import Roster
import Course
import pickle

class Application(Frame): #make gui into class
    contents = []
    roster = Roster.Roster(contents) #create a roster object with an empty list
    studentList=[] #class variable of all student for the whole program
    from os.path import exists as file_exists
    if (file_exists("roster1.dat")): #check if data file exists
        binaryFile = open("roster1.dat", "rb")
        roster = pickle.load(binaryFile)  # take all contents of the file and put them into the roster object
        binaryFile.close()
        for student in roster.getRoster():
            studentList.append(student.getStudentName()) #add all students saved in the student list

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.createWidgets()

    #createWidgets
    #Purpose: creates the initial buttons for the menu and calls all helper methods
    #Parameters: none
    #Return: none
    def createWidgets(self):
        self.welcomeText = ttk.Label(self, text = "Welcome to the WITS Student Roster Program!")
        self.welcomeText.grid(row = 0, column = 1)
        self.endButton = ttk.Button(self, text = "Click here to end the program", command = self.endProgram)
        self.endButton.grid(row = 1, column = 1)
        Label(self, text = "Select what you would like to do").grid(row = 2, column = 1)
        ttk.Button(self, text = "Import a text file of names", command = self.namesFromFile).grid(row = 3, column = 0)
        ttk.Button(self, text = "Add a student", command = self.getNames).grid(row = 3, column = 1)
        ttk.Button(self, text="Add courses", command=self.addCourses).grid(row = 3, column = 2)
        ttk.Button(self, text="Add grades", command=self.addGrades).grid(row=4, column=0)
        ttk.Button(self, text="View your entire record", command=self.printRoster).grid(row=4, column=1)
        ttk.Button(self, text="Search your roster", command=self.searchRoster).grid(row=4, column=2)
        ttk.Button(self, text="Create a report card", command=self.createReportCard).grid(row =5, column=0)
        ttk.Button(self, text="Create a transcript", command = self.createTranscript).grid(row=5, column=2)

    #namesFromFile
    #Purpose: allows user to import a text file of names and adds them to the program
    #Parameters: none
    #Return: none
    def namesFromFile(self):
        fileName = simpledialog.askstring("File Name", "What is the name of your file? Include the .txt extension")
        #checks if file exists
        from os.path import exists as file_exists
        if not (file_exists(fileName)):
            messagebox.showerror("Error!", "That file does not exist")
        else:
            #takes all the names in the file and adds each one to the roster as a Student object
            namesFile = open(fileName, "r")
            namesInFile = namesFile.readlines()
            messagebox.showinfo("Imported", "Your file has been imported.")
            for line in namesInFile:
                line = line.strip()
                if line in Application.studentList:
                    messagebox.showinfo("Info", line+" is already in your record and will not be added.")
                else:
                    Application.studentList.append(line)
                    myCourses = []
                    myStudent = Student.Student(line, myCourses, 0)
                    Application.roster.getRoster().append(myStudent)
                    studentID = simpledialog.askinteger("Student ID", "Enter student ID number for "+myStudent.getStudentName())
                    myStudent.setStudentID(studentID)

    #getNames
    #Purpose: takes user input from dialog box and adds each name to the roster as a Student object
    #Parameters: none
    #Return: none
    def getNames(self):
        name = simpledialog.askstring("Entry", "Enter name")
        if name is None: #if the user pressed cancel instead of ok
            messagebox.showerror("Error", "No name was entered")
        else:
            if name in Application.studentList:
                messagebox.showerror("Error", name + " is already in your record and will not be added.")
            else:
                Application.studentList.append(name)
                courseList = []
                studentID = simpledialog.askinteger("Student ID", "Enter student ID number")
                newStudent = Student.Student(name, courseList, studentID)
                Application.roster.getRoster().append(newStudent)

    #addCoursees
    #Purpose: allows user to input courses for the student of their choice
    #Parameters: none
    #Return: none
    def addCourses(self):
        self.addCoursesLbl = Label(self, text="Add courses:")
        self.addCoursesLbl.grid(row = 6, column =1)
        self.chooseCourseLbl = Label(self, text="Choose student from dropdown")
        self.chooseCourseLbl.grid(row=7, column=0)
        self.firstClicked = StringVar()
        self.firstClicked.set("(Choose student)") #if there are no students in the list it will say this
        self.studentMenu = OptionMenu(self, self.firstClicked, *Application.studentList) #creates dropdown menu of all the students
        self.studentMenu.grid(row=7, column=1)
        #user chooses the student they want to add courses to
        self.chooseStudentBtn = ttk.Button(self, text = "Choose", command = self.inputCourse)
        self.chooseStudentBtn.grid(row=7, column=2)

    #inputCourse
    #Purpose: called when user chooses the student they want to add courses to, gets name of course in dialog box
    #Parameters: none
    #Return: none
    def inputCourse(self):
        course = simpledialog.askstring("Entry", "Enter course name")
        if course is None: #if user pressed cancel instead of ok
            messagebox.showerror("Error", "No course was entered")
        else:
            studentName = self.firstClicked.get()  #choice from dropdown menu of students
            self.studentObj = Application.roster.getStudent(studentName) #finds the student object of that student
            courseExists = False
            for studentCourse in self.studentObj.getCourses(): #checks if student is already in the course entered
                if course == studentCourse.getCourseName():
                    messagebox.showerror("Error", studentName + " is already enrolled in "+ course+ " and it won't be added.")
                    courseExists = True
                    break
            if not courseExists: #if the student isn't registered, will create a new Course object for that student with an empty string for grade
                self.courseObj = Course.Course(course, "", "No comment",)
                self.studentObj.getCourses().append(self.courseObj) #adds the course to that student's course list
        self.chooseSemLbl = Label(self, text="Select all semesters that apply")
        self.chooseSemLbl.grid()
        self.semesterFall = BooleanVar()
        self.checkFall = Checkbutton(self, text="Fall", variable=self.semesterFall, command=self.addSemester)
        self.checkFall.grid()
        self.semesterSpring = BooleanVar()
        self.checkSpring = Checkbutton(self, text="Spring", variable=self.semesterSpring, command=self.addSemester)
        self.checkSpring.grid()
        self.bothSemesters = BooleanVar()
        self.checkBoth = Checkbutton(self, text="Both", variable = self.bothSemesters, command = self.addSemester)
        self.checkBoth.grid()

    #addSemester
    #Purpose: helper method to input course that allows user to choose which semester the course is offered in
    #Parameters: none
    #Return: none
    def addSemester(self):
        if self.semesterFall.get():
            self.courseObj.setTerm("Fall")
        if self.semesterSpring.get():
            self.courseObj.setTerm("Spring")
        if self.bothSemesters.get():
            self.courseObj.setTerm("Fall")
            self.courseObj.setTerm("Spring")
        messagebox.showinfo("Added", "Course added")
        self.addCoursesLbl.destroy()
        self.chooseCourseLbl.destroy()
        self.studentMenu.destroy()
        self.chooseStudentBtn.destroy()
        self.chooseSemLbl.destroy()
        self.checkFall.destroy()
        self.checkSpring.destroy()
        self.checkBoth.destroy()
        
    #addGrades
    #Purpose: allows user to enter a grade for the student and course of their choice
    #Parameters: none
    #Return: none
    def addGrades(self):
        self.addGradesLbl = Label(self, text="Add grades:")
        self.addGradesLbl.grid(row=8, column=1)
        self.chooseStdforGrdLbl = Label(self, text="Choose a student and course from the dropdown")
        self.chooseStdforGrdLbl.grid(row=9, column=1, columnspan=2)
        self.secondClicked = StringVar()
        self.secondClicked.set("(Choose student)")
        #creates a dropdown menu of all students for user to choose from
        self.studentMenu = OptionMenu(self, self.secondClicked, *Application.studentList)
        self.studentMenu.grid(row=10, column=0)
        self.chooseStdforGrdBtn = ttk.Button(self, text="Choose", command=self.getCourseChoice)
        self.chooseStdforGrdBtn.grid(row=10, column=1, sticky=W)

    #getCourseChoice
    #Purpose: gives user course options of the student they chose in addGrades function
    #Paramters: none
    #Return: none
    def getCourseChoice(self):
        studentName = self.secondClicked.get() #choice of student from dropdown
        studentObj = Application.roster.getStudent(studentName) #Student object of that name chosen
        studentCourses = studentObj.getCourses() #list of that student's courses
        if not studentCourses:
            messagebox.showerror("No courses", "The student you selected is not registered in any courses.")
        else:
            courseOptions = []
            self.courseClicked = StringVar()
            self.courseClicked.set("(Choose course)")
            for course in studentCourses:
                courseOptions.append(course.getCourseName()) #makes list of all course names from that student's courses
            self.courseMenu = OptionMenu(self, self.courseClicked, *courseOptions) #puts all courses into dropdown menu
            self.courseMenu.grid(row=10, column=1, sticky=E)
            self.chooseCourseBtn = ttk.Button(self, text="Choose", command=self.inputGrade)
            self.chooseCourseBtn.grid(row=10, column=2, sticky=W)

    #inputGrade
    #Purpose: takes user input from dialog box of the grade for the course the user chose
    #Parameters: none
    #Return: none
    def inputGrade(self):
        grade = simpledialog.askstring("Entry","Enter grade")
        if grade is None or grade=="": #if user pressed cancel instead of ok
            messagebox.showerror("Error", "No grade was entered.")
        else:
            studentName = self.secondClicked.get() #name they chose from dropdown
            studentObj = Application.roster.getStudent(studentName) #Student object of that name
            courseObj = studentObj.getCourse(self.courseClicked.get()) #course object of course they chose from second dropdown
            courseObj.setGrade(grade) #puts grade in for the course they chose
            addComments = messagebox.askyesno("Add comments", "Would you like to add a comment for this course?")
            if addComments:
                comment = simpledialog.askstring("Comment",
                                                 "Enter a brief comment for " + studentObj.getStudentName() + " for " + courseObj.getCourseName())
                if comment is None:
                    messagebox.showerror("Error", "No comment was entered")
                else:
                    courseObj.setComment(comment)
            messagebox.showinfo("Grade Set", "Grade and comments have been added")
        self.addGradesLbl.destroy()
        self.chooseStdforGrdLbl.destroy()
        self.studentMenu.destroy()
        self.chooseStdforGrdBtn.destroy()
        self.courseMenu.destroy()
        self.chooseCourseBtn.destroy()

    #printRoster
    #Purpose: displays all contents of the roster in a messagebox
    #Parameters: none
    #Return: none
    def printRoster(self):
        printStr = ""
        for student in Application.roster.getRoster(): #iterates thru the roster and adds each student with their courses and grades to the printStr
            name = student.getStudentName()
            if name is None:
                messagebox.showerror("Error", "No students are saved in your roster")
            else:
                printStr += "\n----------------\n" + student.getStudentName()
            for course in student.getCourses():
                courseName = course.getCourseName()
                courseGrade = course.getCourseGrade()
                if courseName is None or courseGrade is None:
                    messagebox.showinfo("Info", "None")
                else:
                    printStr += "\n" + course.getCourseName() + ": " + course.getCourseGrade() + "\n"
        messagebox.showinfo("Students", printStr)

    #searchRoster
    #Purpose: allows user to choose a student and course and see the grade
    #Parameters: none
    #Return: none
    def searchRoster(self):
        self.searchRosterLbl = Label(self, text="Search your roster. ")
        self.searchRosterLbl.grid()
        self.chooseStudentSearchLbl = Label(self, text="Choose a student and course from the dropdown to view the grade.")
        self.chooseStudentSearchLbl.grid(row=13, column=1, columnspan=2)
        self.searchNameClick = StringVar()
        self.searchNameClick.set("(Choose student)")
        self.studentMenu = OptionMenu(self, self.searchNameClick, *Application.studentList) #dropdown menu of names
        self.studentMenu.grid(row=14, column=0)
        self.chooseStdSearchBtn = ttk.Button(self, text="Choose", command=self.chooseCourse)
        self.chooseStdSearchBtn.grid(row=14, column=1, sticky=W)

    #chooseCourse
    #Purpose: gives a dropdown menu of courses for the selected student
    #Parameters: none
    #Return: none
    def chooseCourse(self):
        studentName = self.searchNameClick.get() #name chosen from dropdown
        studentObj = Application.roster.getStudent(studentName) #Student object of that name
        studentCourses = studentObj.getCourses() #list of courses for that student
        if not studentCourses: #if the student isn't registered in any courses
            messagebox.showerror("No courses", "The student you selected is not registered in any courses.")
        else:
            courseOptions = []
            self.searchCourseClick = StringVar()
            self.searchCourseClick.set("(Choose course)")
            for course in studentCourses:
                courseOptions.append(course.getCourseName()) #makes list of courses for that student
            self.courseMenu = OptionMenu(self, self.searchCourseClick, *courseOptions)
            self.courseMenu.grid(row=14, column=1, sticky=E)
            self.chooseCourseSearchBtn = ttk.Button(self, text="Choose", command=self.displayGrade)
            self.chooseCourseSearchBtn.grid(row=14, column=2, sticky=W)

    #displayGrade
    #Purpose: shows the grade for the selected student and course
    #Parameters: none
    #Return: none
    def displayGrade(self):
        studentObj = Application.roster.getStudent(self.searchNameClick.get()) #Student object of name chosen
        courseObj = studentObj.getCourse(self.searchCourseClick.get()) #Course object of course chosen
        grade = courseObj.getCourseGrade()
        strOutput= self.searchNameClick.get() + "'s grade in " + self.searchCourseClick.get() + " is " + grade
        messagebox.showinfo("Grade", strOutput) #displays grade of course chosen
        self.searchRosterLbl.destroy()
        self.chooseStudentSearchLbl.destroy()
        self.studentMenu.destroy()
        self.chooseStdSearchBtn.destroy()
        self.courseMenu.destroy()
        self.chooseCourseSearchBtn.destroy()

    #createReportCard
    #Purpose: allows user to create a report card for a specific student and semester
    #Paramerters: none
    #Return: none
    def createReportCard(self):
        self.createRCLbl = Label(self, text="Create report card")
        self.createRCLbl.grid(row=7, column=0)
        self.studentClicked = StringVar()
        self.studentClicked.set("(Choose Student)")
        self.studentMenu = OptionMenu(self, self.studentClicked, *Application.studentList)  # creates dropdown menu of all the students
        self.studentMenu.grid(row=7, column=1)
        # user chooses the student they want to create report card for
        self.chooseStudentBtn = ttk.Button(self, text="Choose", command=self.chooseTerm)
        self.chooseStudentBtn.grid(row=7, column=2)

    #sendChoice
    #Purpose: helper method for createReportCard that allows user to choose semester they want report card for
    #Parameters: none
    #Return: none
    def chooseTerm(self):
        #creates 2 checkboxes, Fall and Spring for user to choose to create report card for
        self.semesterFall = BooleanVar()
        self.checkFall = Checkbutton(self, text="Fall", variable=self.semesterFall, command=self.createRC)
        self.checkFall.grid()
        self.semesterSpring = BooleanVar()
        self.checkSpring = Checkbutton(self, text="Spring", variable=self.semesterSpring, command=self.createRC)
        self.checkSpring.grid()

    #createRC
    #Purpose: helper method for createReportCard that writes information to textfile
    #Parameters: none
    #Return: none
    def createRC(self):
        self.studentChosen = self.studentClicked.get()
        studentObj = Application.roster.getStudent(self.studentChosen)
        studentName = studentObj.getStudentName()
        term = ""
        #takes the checkbox that was selected
        if self.semesterFall.get():
            term = "Fall"
        if self.semesterSpring.get():
            term = "Spring"
        fileName = studentName +"_" + term + "_Report_Card.txt" #distinct file name
        rcFile = open(fileName, "w")
        #write information to readable file
        rcFile.write("Name: "+studentName+"\n")
        rcFile.write("Student ID # " + str(studentObj.getStudentID())+"\n")
        rcFile.write("Term: "+term+"\n")
        rcFile.write("=============================\n")
        for course in studentObj.getCourses():
            if term in course.getTerm():  #if the course is enrolled for the term of the report card being created will add it
                rcFile.write(course.getCourseName() + ": "+ course.getCourseGrade()+"\n")
                if course.getComment() != "No comment": #if there's a comment for the course will add it
                    rcFile.write("Teacher comments: " + course.getComment()+"\n")
                rcFile.write("---------------------------\n")
        rcFile.close()
        messagebox.showinfo("Success!", "Report card file created. You can locate it in the same folder as this program.")
        self.createRCLbl.destroy()
        self.studentMenu.destroy()
        self.chooseStudentBtn.destroy()
        self.checkFall.destroy()
        self.checkSpring.destroy()

    #createTranscript
    #Purpose: allows user to choose a student to create a transcript for
    #Parameters: none
    #Return: none
    def createTranscript(self):
        self.createTrnLbl = Label(self, text="Create transcript")
        self.createTrnLbl.grid(row=7, column=0)
        self.studentClicked = StringVar()
        self.studentClicked.set("(Choose Student)")
        self.studentMenu = OptionMenu(self, self.studentClicked, *Application.studentList)  # creates dropdown menu of all the students
        self.studentMenu.grid(row=7, column=1)
        # user chooses the student they want to create transcript for
        self.chooseStudentBtn = ttk.Button(self, text="Choose", command=self.makeTrn)
        self.chooseStudentBtn.grid(row=7, column=2)

    #makeTrn
    #Purpose: helper method to createTranscript that writes transcript to file
    #Parameters: none
    #Return: none
    def makeTrn(self):
        self.studentChosen = self.studentClicked.get()
        studentObj = Application.roster.getStudent(self.studentChosen)
        studentName = studentObj.getStudentName()
        fileName = studentName + "_Transcript.txt" #distinct file name for transcript
        transcriptFile = open(fileName, "w")
        # put information onto file in readable format
        transcriptFile.write("Name: "+studentName + "\n")
        transcriptFile.write("Student ID # "+str(studentObj.getStudentID())+"\n")
        transcriptFile.write("GPA: "+str(studentObj.calculateGPA())+"\n")
        transcriptFile.write("=======================\n")
        for course in studentObj.getCourses():
            transcriptFile.write(course.getCourseName()+": "+course.getCourseGrade()+"\n")
            transcriptFile.write("---------------------\n")
        transcriptFile.close()
        messagebox.showinfo("Success!", "Transcript file created. You can locate it in the same folder as this program.")
        self.createTrnLbl.destroy()
        self.studentMenu.destroy()
        self.chooseStudentBtn.destroy()

    #endProgram
    #Purpose: allows user to save changes and exit
    #Paramters: none
    #Return: none
    def endProgram(self):
        save = messagebox.askyesno("Save", "Would you like to save your changes?")
        if save: #if the user chose yes
            binaryRoster = open("roster1.dat", "wb")  # update binary file with current roster so next time used it will have all new info
            pickle.dump(Application.roster, binaryRoster)
            binaryRoster.close()
            root.destroy()
        else:
            root.destroy()


#main
#creates the Application object with its frame
root = Tk()
root.title("WITS Roster Program")
root.geometry("600x500")
app = Application(root)
root.mainloop()