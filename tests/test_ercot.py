from pyiso import client_factory
from unittest import TestCase
import pytz
from io import StringIO
from datetime import datetime


class TestERCOT(TestCase):
    def setUp(self):
        self.c = client_factory('ERCOT')

        self.rtm_html = StringIO(u'<html>\n\
<body class="bodyStyle">\n\
<table class="tableStyle" cellpadding="0" cellspacing="0" border="0" bgcolor="#ECECE2">\n\
    <tr>\n\
        <th colspan="5" valign="middle" class="hdr_port" >Real-Time System Conditions</th>\n\
    </tr>\n\
    <tr valign="top">\n\
        <td colspan="5" class="labelClass" valign="middle"><span class="labelValueClass">Last Updated Sep 15 2014 13:50:20 CDT</span></td>\n\
    </tr>\n\
    <tr valign="top">\n\
        <th colspan="5" valign="middle" class="headerClass"><span class="headerValueClass">Frequency</span></th>\n\
    </tr>\n\
    <tr valign="top">\n\
        <td colspan = "4" valign="middle" class="labelClass"><span class="labelValueClass">Current Frequency</span></td>\n\
        <td valign="middle" class="labelClassRight"><span class="labelValueClassBold">59.998</span></td>\n\
    </tr>\n\
    <tr valign="top">\n\
        <td colspan = "4" valign="middle" class="labelClass"><span class="labelValueClass">Instantaneous Time Error</span></td>\n\
        <td valign="middle" class="labelClassRight"><span class="labelValueClassBold">-29.222</span></td>\n\
    </tr>\n\
    <tr valign="top">\n\
        <th colspan="5" valign="middle" class="headerClass"><span class="headerValueClass">Real-Time Data</span></th>\n\
    </tr>\n\
    <tr valign="top">\n\
        <td colspan = "4" valign="middle" class="labelClass"><span class="labelValueClass">Actual System Demand</span></td>\n\
        <td valign="middle" class="labelClassRight"><span class="labelValueClassBold">48681</span></td>\n\
    </tr>\n\
    <tr valign="top">\n\
        <td colspan = "4" valign="middle" class="labelClass"><span class="labelValueClass">Total System Capacity (not including Ancillary Services)</span></td>\n\
        <td valign="middle" class="labelClassRight"><span class="labelValueClassBold">54642</span></td>\n\
    </tr>\n\
    <tr valign="top">\n\
        <td colspan = "4" valign="middle" class="labelClass"><span class="labelValueClass">Total Wind Output</span></td>\n\
        <td valign="middle" class="labelClassRight"><span class="labelValueClassBold">885</span></td>\n\
    </tr>\n\
    <tr valign="top">\n\
        <th colspan = "5" valign="middle" class="headerClass"><span class="headerValueClass">DC Tie Flows</span></th>\n\
    </tr>\n\
            <tr valign="top">\n\
            <td colspan = "3" valign="middle" class="labelClass"><span class="labelValueClass">DC_E (East)</span></td>\n\
            <td colspan = "2" valign="middle" class="labelClassRight"><span class="labelValueClassBold">-543</span></td>\n\
        </tr>\n\
            <tr valign="top">\n\
            <td colspan = "3" valign="middle" class="labelClass"><span class="labelValueClass">DC_L (Laredo VFT)</span></td>\n\
            <td colspan = "2" valign="middle" class="labelClassRight"><span class="labelValueClassBold">0</span></td>\n\
        </tr>\n\
            <tr valign="top">\n\
            <td colspan = "3" valign="middle" class="labelClass"><span class="labelValueClass">DC_N (North)</span></td>\n\
            <td colspan = "2" valign="middle" class="labelClassRight"><span class="labelValueClassBold">0</span></td>\n\
        </tr>\n\
            <tr valign="top">\n\
            <td colspan = "3" valign="middle" class="labelClass"><span class="labelValueClass">DC_R (Railroad)</span></td>\n\
            <td colspan = "2" valign="middle" class="labelClassRight"><span class="labelValueClassBold">0</span></td>\n\
        </tr>\n\
            <tr valign="top">\n\
            <td colspan = "3" valign="middle" class="labelClass"><span class="labelValueClass">DC_S (Eagle Pass)</span></td>\n\
            <td colspan = "2" valign="middle" class="labelClassRight"><span class="labelValueClassBold">5</span></td>\n\
        </tr>\n\
    </table>\n\
</body>\n\
</html>')

    def test_utcify(self):
        ts_str = '05/03/2014 02:00'
        ts = self.c.utcify(ts_str)
        self.assertEqual(ts.year, 2014)
        self.assertEqual(ts.month, 5)
        self.assertEqual(ts.day, 3)
        self.assertEqual(ts.hour, 2+5)
        self.assertEqual(ts.minute, 0)
        self.assertEqual(ts.tzinfo, pytz.utc)

    def test_parse_load(self):
        self.c.handle_options(data='load', latest=True)
        data = self.c.parse_rtm(self.rtm_html)
        self.assertEqual(len(data), 1)
        expected_keys = ['timestamp', 'ba_name', 'load_MW', 'freq', 'market']
        self.assertEqual(sorted(data[0].keys()), sorted(expected_keys))
        self.assertEqual(data[0]['timestamp'], pytz.utc.localize(datetime(2014, 9, 15, 18, 50, 20)))
        self.assertEqual(data[0]['load_MW'], 48681.0)

    def test_parse_genmix(self):
        self.c.handle_options(data='gen', latest=True)
        data = self.c.parse_rtm(self.rtm_html)

        self.assertEqual(len(data), 2)
        expected_keys = ['timestamp', 'ba_name', 'gen_MW', 'fuel_name', 'freq', 'market']
        self.assertEqual(sorted(data[0].keys()), sorted(expected_keys))

        self.assertEqual(data[0]['timestamp'], pytz.utc.localize(datetime(2014, 9, 15, 18, 50, 20)))
        self.assertEqual(data[0]['gen_MW'], 885.0)
        self.assertEqual(data[0]['fuel_name'], 'wind')

        self.assertEqual(data[1]['timestamp'], pytz.utc.localize(datetime(2014, 9, 15, 18, 50, 20)))
        self.assertEqual(data[1]['gen_MW'], 48334.0)
        self.assertEqual(data[1]['fuel_name'], 'nonwind')

    def test_request_report_gen_hrly(self):
        # get data as list of dicts
        df = self.c._request_report('gen_hrly')

        # test for expected data
        self.assertEqual(len(df), 1)
        for key in ['SE_EXE_TIME_DST', 'SE_EXE_TIME', 'SE_MW']:
            self.assertIn(key, df.columns)

    def test_request_report_wind_hrly(self):
        # get data as list of dicts
        df = self.c._request_report('wind_hrly')

        # test for expected data
        self.assertLessEqual(len(df), 96)
        for key in ['DSTFlag', 'ACTUAL_SYSTEM_WIDE', 'HOUR_BEGINNING']:
            self.assertIn(key, df.columns)

    def test_request_report_load_7day(self):
        # get data as list of dicts
        df = self.c._request_report('load_7day')

        # test for expected data
        self.assertEqual(len(df), 8*24)
        for key in ['SystemTotal', 'HourEnding', 'DSTFlag', 'DeliveryDate']:
            self.assertIn(key, df.columns)
