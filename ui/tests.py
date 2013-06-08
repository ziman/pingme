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

