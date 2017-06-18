# -*- coding: utf-8 -*-


class Time:
    def __init__(self, h=0, m=0, s=0, ms=0):
        s += ms // 1000
        m += s // 60
        h += m // 60
        self.ms = ms % 1000
        self.s = s % 60
        self.m = m % 60
        self.h = h

    def __repr__(self):
        r = ""
        if self.ms != 0:
            r += str(self.ms) + ' milliseconds'
        if self.s != 0:
            r = str(self.s) + ' seconds ' + r
        if self.m != 0:
            r = str(self.m) + ' minutes ' + r
        if self.h != 0:
            r = str(self.h) + ' hours ' + r

        return 'Time(' + r + ')'

    def __add__(self, other):
        if isinstance(other, Time):
            return Time(self.h + other.h, self.m + other.m, self.s + other.s, self.ms + other.ms)
        else:
            return Time(self.h, self.m, self.s + other, self.ms)

    def __iadd__(self, other):
        return self + other

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Time):
            return Time(ms=self.to_milliseconds() - other.to_milliseconds())
        else:
            return Time(ms=self.to_milliseconds() - other * 1000)

    def __isub__(self, other):
        return self - other

    def __rsub__(self, other):
        if isinstance(other, Time):
            return Time(ms=other.to_milliseconds() - self.to_milliseconds())
        else:
            return Time(ms=other * 1000 - self.to_milliseconds())

    def __gt__(self, other):
        return self.to_milliseconds() > other.to_milliseconds()

    def __ge__(self, other):
        return self.to_milliseconds() >= other.to_milliseconds()

    def to_minutes(self):
        return self.h * 60 + self.m # + self.s / 60 + self.ms / 60000

    def to_seconds(self):
        return self.to_minutes() * 60 + self.s

    def to_milliseconds(self):
        return self.to_seconds() * 1000 + self.ms
