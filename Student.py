import Course

class Student(object):
    def __init__(self, name, courses, studentID):
        self.studentName = name
        self.coursesEnrolled = courses
        self.studentID = studentID
        self.gpa = 0.0

    #getStudentName
    #Purpose: allows user to access student's name
    #Parameters: none
    #Return: studentName - string
    def getStudentName(self):
        return self.studentName

    #getCourses
    #Purpose: allows user to access courses the student is enrolled in
    #Parameters: none
    #Return: coursesEnrolled - list of course objects
    def getCourses(self):
        return self.coursesEnrolled

    #getStudentID
    #Purpose: allows user to access student's ID number
    #Parameters: none
    #Return: studentID - int
    def getStudentID(self):
        return self.studentID

    #setStudentID
    #Purpose: allows user to assign student's ID number
    #Parameter: newID - int
    #Return: none
    def setStudentID(self, newID):
        self.studentID = newID


    #checkCourse
    #Purpose: checks if student is enrolled in specific course
    #Parameters: newCourse - string
    #Return: boolean value
    def checkCourse(self, newCourse):
        for course in self.coursesEnrolled: #checking if student already enrolled in course
            if newCourse == course.getCourseName():
                return True
        return False

    #getCourse
    #Purpose: gives user course requested
    #Parameters: courseName - string
    #Return: course - Course object
    def getCourse(self, courseName):
        for course in self.coursesEnrolled:
            if course.getCourseName() == courseName:
                return course

    #calculateGPA
    #Purpose: calculate's a student's GPA based on their grades and courses they're enrolled in
    #Parameters: none
    #Return: if student isn't enrolled in courses, returns "N/A"
    #         otherwise returns gpa - double
    def calculateGPA(self):
        totalCourses = len(self.coursesEnrolled)
        if totalCourses == 0:
            return "N/A"
        totalPoints = 0
        for course in self.coursesEnrolled:
            courseGrade = course.getCourseGrade()
            if courseGrade == "A":
                totalPoints += 4
            elif courseGrade == "B":
                totalPoints += 3
            elif courseGrade == "C":
                totalPoints += 2
            elif courseGrade == "D":
                totalPoints += 1
        self.gpa = totalPoints/totalCourses
        self.gpa = round(self.gpa, 2)
        return self.gpa

    #getGPA
    #Purpose: allows user to access student's gpa
    #Parameters: none
    #Return: gpa - double
    def getGPA(self):
        return self.gpa

if __name__ == "__main__":
    print("This is a module and is meant to be imported.")
