class Course (object):
    def __init__(self, name, grade, comment):
        self.courseName = name
        self.courseGrade = grade.upper()
        self.term = []
        self.comment = comment
    #getCourseName
    #Purpose: gets the name of the course
    #Parameters: none
    #Return: courseName - string
    def getCourseName(self):
        return self.courseName

    # getCourseGrade
    # Purpose: gets the grade of the course
    # Parameters: none
    # Return: courseGrade - string
    def getCourseGrade(self):
        return self.courseGrade

    #getTerm
    #Purpose: gets the term the course is active in
    #Parameters: none
    #Return:
    def getTerm(self):
        return self.term

    #setTerm
    #Purpose: allows user to set the term for the course
    #Parameters:
    #Return:
    def setTerm(self, newTerm):
        self.term.append(newTerm)

    #getComment
    #Purpose: access comment for this course
    #Parameters: none
    #Return: comment - string
    def getComment(self):
        return self.comment

    #setComment
    #Purpose: assigns new comment for course
    #Parameters: newComment - string
    #Return: none
    def setComment(self, newComment):
        self.comment = newComment

    #setGrade
    #Purpose: allows user to assign a new grade for a course
    #Parameters: newGrade - string
    #Return - none
    def setGrade(self, newGrade):
        if newGrade.upper() == self.courseGrade: #checks if same grade was entered
            print("You entered the same grade.")
        else:
            self.courseGrade = newGrade.upper()
            print("The grade for ", self.courseName, " has been changed to ", self.courseGrade)

if __name__ == "__main__":
    print("This is a module and is meant to be imported.")