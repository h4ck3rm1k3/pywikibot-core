import re
class WbTime(object):
    """ A Wikibase time representation"""

    PRECISION = {'1000000000': 0, '100000000': 1, '10000000': 2, '1000000': 3, '100000': 4, '10000': 5, 'millenia': 6, 'century': 7, 'decade': 8, 'year': 9, 'month': 10, 'day': 11, 'hour': 12, 'minute': 13, 'second': 14}
    FORMATSTR = '{0:+012d}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}Z'

    def __init__(self, year=None, month=None, day=None, hour=None, minute=None, second=None, precision=None, before=0, after=0, timezone=0, calendarmodel='http://www.wikidata.org/entity/Q1985727'):
        """ Creates a new WbTime object. The precision can be set by the Wikibase int value (0-14) or by a human readable string, e.g., 'hour'. If no precision is given, it is set according to the given time units."""
        if year is None:
            raise ValueError('no year given')
        self.precision = WbTime.PRECISION['second']
        if second is None:
            self.precision = WbTime.PRECISION['minute']
            second = 0
        if minute is None:
            self.precision = WbTime.PRECISION['hour']
            minute = 0
        if hour is None:
            self.precision = WbTime.PRECISION['day']
            hour = 0
        if day is None:
            self.precision = WbTime.PRECISION['month']
            day = 1
        if month is None:
            self.precision = WbTime.PRECISION['year']
            month = 1
        self.year = int(year)
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.after = after
        self.before = before
        self.timezone = timezone
        self.calendarmodel = calendarmodel

        # if precision is given it overwrites the autodetection above
        if precision is not None:
            if isinstance(precision, int):
                self.precision = precision
            elif precision in WbTime.PRECISION:
                self.precision = WbTime.PRECISION[precision]
            else:
                raise ValueError('Invalid precision: "%s"' % precision)

    @staticmethod
    def fromTimestr(datetimestr, precision=14, before=0, after=0, timezone=0, calendarmodel='http://www.wikidata.org/entity/Q1985727'):
        match = re.match('([-+]?\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)Z', datetimestr)
        if not match:
            raise ValueError("Invalid format: '%s'" % datetimestr)
        t = match.groups()
        return WbTime(int(t[0]), int(t[1]), int(t[2]), int(t[3]), int(t[4]), int(t[5]), precision, before, after, timezone, calendarmodel)

    def toWikibase(self):
        """
        Function which converts the data to a JSON object
        for the Wikibase API.
        """
        json = {'time': WbTime.FORMATSTR.format(self.year, self.month, self.day,
                self.hour, self.minute, self.second),
                'precision': self.precision,
                'after': self.after,
                'before': self.before,
                'timezone': self.timezone,
                'calendarmodel': self.calendarmodel
                }
        return json

    @staticmethod
    def fromWikibase(ts):
        return WbTime.fromTimestr(ts['time'], ts['precision'], ts['before'], ts['after'], ts['timezone'], ts['calendarmodel'])

    def __str__(self):
        return str(self.toWikibase())

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "WbTime(year=%(year)d, month=%(month)d, day=%(day)d, " \
            "hour=%(hour)d, minute=%(minute)d, second=%(second)d, " \
            "precision=%(precision)d, before=%(before)d, after=%(after)d, " \
            "timezone=%(timezone)d, calendarmodel='%(calendarmodel)s')" % self.__dict__

