import Student
import Course

class Roster(object):
    def __init__(self, roster):
        self.roster = roster

    #getRoster
    #Purpose: gets the contents of roster
    #Parameters: none
    #Return: roster - list
    def getRoster(self):
        return self.roster

    #getStudent
    #Purpose: gets a student object from the roster
    #Parameters: student - string
    #Return: name - Student object
    def getStudent(self, student):
        for name in self.roster:
            if name.getStudentName() == student:
                return name

    #studentCheck
    #Purpose: checks if a student exists in the roster
    #Parameters: student - string
    #Return - boolean value
    def studentCheck(self, student):
        for name in self.roster:
            if name.getStudentName() == student:
                return True
        return False

    #printRoster
    #Purpose: prints out the roster neatly
    #Parameters: none
    #Return: none
    def printRoster(self):
        for student in self.roster:
            print(student.getStudentName())
            for course in student.getCourses():
                print(course.getCourseName() + ": " + course.getCourseGrade())
            print("-----------------------------")

    #checkIfEmpty
    #Purpose: checks if there is anything in the roster
    #Parameters: none
    #Return: boolean value
    def checkIfEmpty(self):
        if not self.roster:
            return True
        return False

if __name__ == "__main__":
    print("This is a module and is meant to be imported.")