import pandas as pd

class student:

    def __init__(self, first: str, last: str):
        self.first = first
        self.last = last

class consumer:
    
    def __init__(self, name: str) -> None:
        self.name = name
        self._students = []
    
    def read_data(self, data: pd.DataFrame):
        for _, row in data.iterrows():
            try:
                if row["Last name, First name"].count(','):
                    names = row["Last name, First name"].split(',')
                    stud = student(names[1], names[0])
                    self._students.append(stud)
                else:
                    names = row["Last name, First name"].split()
                    self._students.append(student(names[0], names[1]))
            except AttributeError:
                pass
    
    def students(self) -> pd.DataFrame:
       data = [ [student.first, student.last] for student in self._students]
       return pd.DataFrame(data, columns=['First', 'Last'])


    