# ISH CLOCK version 1.02 - based on old javascipt from 1998-2001!
# Python conversion 25/04/2021

from datetime import datetime
from random import randint

def ish(*args):
    ish = IshTime()
    return ish.now


class IshTime():
    def __init__(self, time=None, width=40):
        """
        A class to represent a text-based telling of the time, for example:

            It is about twenty-five minutes to eleven in the morning.

        Attributes:

        now :
            The ish time at the time of creation

        time: str
            The ish time at the time specified

        Methods:

        then(time)
            The ish time at a specified time, datetime object,
            a string such as "11:20", or "13:20:12", or "0744"
            or an int such as 1, 222, etc.

        random()
            Returns a reandom ish time

        """
        self.now = self.time = self.ish(0, 0, 0)
        self.long = "It is about twenty-five minutes to eleven in the morning."
        if time:
            self.time = self.then(time)

    def random(self):
        return self.ish(randint(0, 24), randint(0, 60), randint(0, 60))

    def then(self, time):
        if type(time) == datetime:
            then = self.ish(time.hour, time.minute, time.second)
        else:
            t = []
            if type(time) == int:
                time = f'{time:04}'
            if type(time) == str:
                if ':' in time:
                    time = time.split(':')
                elif len(time) >= 4:
                    t = [time[0:2], time[2:4]]
                    if len(time) > 4:
                        t.append(time[4:])
            time = t
            if isinstance(time, (list, tuple)):
                h = m = s = 0
                if len(time) > 0:
                    h = time[0]
                if len(time) > 1:
                    m = time[1]
                if len(time) > 2:
                    s = time[2]
                then = self.ish(h, m, s)
            else:
                try:
                    then = self.ish(h, m, s)
                except:
                    then = "IshTime not known."
        return then

    def number(self, x):
        try:
            return ('one', 'two', 'three', 'four', 'five', 'six',
                    'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve')[x - 1]
        except:
            return x

    def bittime(self, m):
        m = int(m)
        if m <= 7 or m > 53:
            m = "five minutes"
        elif m <= 12 or m > 48:
            m = "ten minutes"
        elif m <= 17 or m > 43:
            m = "quarter"
        elif m <= 23 or m > 38:
            m = "twenty minutes"
        elif m <= 28 or m > 33:
            m = "twenty-five minutes"
        return m  # default

    def ishtime(self, h, m):
        foo = ''
        h = self.number(h)
        m = int(m)
        if m <= 3 or m > 57:
            return h + " o'clock"
        elif m <= 33 and m > 28:
            return "half past " + h
        elif m < 30:
            foo = "past"
        else:
            foo = "to"
        m = self.bittime(m)
        return m + " " + foo + " " + h

    def daytime(self, h):
        h = int(h)
        if not h or h > 21:
            return "at night"
        elif h < 12:
            return "in the morning"
        elif (h <= 17):
            return "in the afternoon"
        return "in the evening"  #   default

    def ish(self, h=0, m=0, s=0):
        if not h and not m:
            ct = datetime.now()
            h = ct.hour
            m = ct.minute
            s = ct.second

            # if (not s) s = 0
        z = self.daytime(h)
        h = int(h)
        m = int(m)
        h = h % 12  # fix to 12 hour clock
        if (m > 57 and s > 30): m += 1  # round seconds
        if (m > 60): m = 0  # round up minutes
        if (m > 33): h += 1  # round up hours
        if (h > 12): h = 1  # the clock turns round...
        if (h == 0): h = 12
        return (f"It is about {self.ishtime(h, m)} {z}.")

def main():
    ish = IshTime()
    print(ish.now)
    # print("Then:",ish.then(3434))
    # print("Random:",ish.random())

if __name__ == "__main__":
    main()
