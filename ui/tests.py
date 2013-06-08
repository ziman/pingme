import datetime
from django.test import TestCase

from management.commands.receive import parse_timestamp

class TimeParseTests(TestCase):
    def _t(self, numbers, string):
        self.assertEqual(datetime.datetime(*numbers), parse_timestamp(string))
    
    def test_simple_dates(self):
        self._t((2012, 1, 1), '2012-01-01')
        self._t((2012, 1, 1, 12, 35), '2012-01-01-1235')
        self._t((2001, 9, 11, 9, 05), '2001-09-11-0905')
    
    def _ts(self, timestamp, string):
        self._t((timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute), string)
    
    def test_complicated_dates(self):
        self._ts(datetime.datetime.now(), 'now')
        self._ts(datetime.datetime.now() + datetime.timedelta(3), 'now+3-days')
        self._ts(datetime.datetime.now() + datetime.timedelta(5), '5-days')
        
        next_tuesday = datetime.date.today()
        while next_tuesday.weekday() != 1:
            next_tuesday += datetime.timedelta(1)
        ts = datetime.datetime.combine(next_tuesday, datetime.time(17, 4))
        self._ts(ts, '1704-next-tuesday')
        
        ts = datetime.datetime.combine(next_tuesday, datetime.time(16))
        self._ts(ts, '4pm-next-tuesday')
        
        ts = datetime.datetime(datetime.date.today().year, 5, 17)
        self._ts(ts, 'may-17')
