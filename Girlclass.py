#this class represents the user of the telegram bot
#Sorry for naming, no sexism or other forms of descrimination intended
#Be aware that methods, named in snake_case should be used to work with attrs of this object
#method _fromtuple is used to create an object out of tuple, given by sqlite3

class Girl:

    def __init__(self, userid = '', takepill = False, mustpill = False, numinc = 0):
        self.userid = userid #stores the telegramuserid in string.
        self.takepill = takepill #stores a boolean. If a girl has taken a pill, set to "true"
        self.mustpill = mustpill #stores a boolean. States if today is the day when the pill should be taken
        self.numinc = numinc #stores an integer. Represents days of the cicle

    def fromtuple(self, tuple):
        self.userid = tuple[0]
        self.takepill = tuple[1]
        self.mustpill = tuple[2]
        self.numinc = tuple[3]
        return self

    def set_userid(self, user_id):
        self.userid = user_id
        return self.userid

    def set_takepill(self, take_pill):
        self.takepill = take_pill
        return self.takepill

    def set_mustpill(self, must_pill):
        self.mustpill = must_pill
        return self.mustpill

    def set_mustpill_from_numinc(self):
        if self.numinc <= 21:
            self.mustpill = True
        elif self.numinc <= 28:
            self.mustpill = False
        elif self.numinc > 28:
            self.mustpill = True
            self.numinc = 1
        return self.mustpill, self.numinc

    def set_numinc(self, num):
        self.numinc = num
        return self.numinc

    def get_userid(self):
        return self.userid

    def get_takepill(self):
        return self.takepill

    def get_mustpill(self):
        return self.mustpill
    def get_numinc(self):
        return self.numinc



    def add_numinc(self, number):
        self.numinc = self.numinc + number
        return self.numinc

    def __str__(self):
        return "This is a Girl object with userid = " + self.userid


