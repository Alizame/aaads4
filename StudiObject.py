class StudiObject:

    def __init__(self, name, matr):
        self.name = name
        self.matr = matr

    def __repr__(self):
        return "Student({}, {})".format(self.matr, self.name)

    def get_name(self):
        return self.name

    def get_matr(self):
        return self.matr

    def set_name(self, name):
        self.name = name

    def set_matr(self, matr):
        self.matr = matr
