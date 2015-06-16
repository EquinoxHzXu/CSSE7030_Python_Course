class Student(object):
    """A university student"""
    def __init__(self, name, student_no, degree):
        """Create a student with a name.

        Constructor: Student(str)
        """
        self._name = name
        self._student_no = student_no
        self._degree = degree

    def get_name(self):
        """Returns the name of the student

        Student.get_name() -> str

        """
        return self._name

    def get_student_no(self):
        return self._student_no

    def get_degree(self):
        return self._degree

    def get_first_name(self):
        return self.get_name().split(' ')[0]

    def get_last_name(self):
        return self.get_name().split(' ')[-1]

    def get_email(self):
        first = self.get_first_name()
        last = self.get_last_name()
        #return (first.lower() + '.' +last +'@uq.net.au')
        return "[0].[1]@uq.edu.au".format(first.lower(), last.lower())

    def __str__(self):
        return (self._name + ' (' + self.get_email() + ', ' + str(self._student_no) + ', ' + self._degree + ')')
        #return "[0] ({1}, {2}, {3})".format(self.get_name(), ..........)
    
    def __repr__(self):
        return ('Student(' + "\'" + self._name + "\'," + str(self._student_no) + "\'," + self._degree + "\')")

def check_students(students):

        
                
        

                

            
