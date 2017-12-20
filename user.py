
class User:
    def __init__(self, id, fname, lname, email, password):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password

    def getId(self):
        return self.id

    def getName(self):
        return self.fname+" "+self.lname

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password