#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-26 22:13:31 awieser>

import unittest
import os
import sys
import codecs
import time
from common.orgformat import OrgFormat
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))
from common.orgwriter import OrgOutputWriter


class TestOutputWriter(unittest.TestCase):
    def setUp(self):
        # setting tmpfolder to "./tmp"
        self.TMPFOLDER = os.path.normpath(
            os.path.dirname(os.path.abspath(__file__)) + \
                os.path.sep + "tmp") + os.sep
        if not os.path.exists(self.TMPFOLDER):
            os.makedirs(self.TMPFOLDER)

    def test_ouput_to_file(self):
        """
        Simple Test
        """
        test_filename = self.TMPFOLDER + "testfile.org"

        # writing test output
        writer = OrgOutputWriter("short descript", "test-tag", test_filename)
        writer.write("## abc\n")
        writer.writeln("## abc")
        writer.write_comment("abc\n")
        writer.write_commentln("abc")
        writer.write_org_item("begin")
        timestamp = OrgFormat.datetime(time.gmtime(0))
        writer.write_org_subitem(timestamp=timestamp, output="sub")
        writer.write_org_subitem(timestamp=timestamp,
                                 output="sub",
                                 tags=["foo", "bar"])
        writer.close()

        # read and check the file_handler
        file_handler = codecs.open(test_filename, "r", "utf-8")
        data = file_handler.readlines()

        #for d in range(len(data)):
        #   print "self.assertEqual(\n\tdata[%d],\n\t\"%s\")" % \
        #       (d, data[d])

#        self.assertEqual(
#            data[1],
#            "## this file is generated by "...
#        ")
#        self.assertEqual(
#            data[2],
#            "## To add this file to your org-agenda " ...
#        ")
        self.assertEqual(
            data[3],
            "* short descript          :Memacs:test-tag:\n")
        self.assertEqual(
            data[4],
            "## abc\n")
        self.assertEqual(
            data[5],
            "## abc\n")
        self.assertEqual(
            data[6],
            "## abc\n")
        self.assertEqual(
            data[7],
            "## abc\n")
        self.assertEqual(
            data[8],
            "* begin\n")
        self.assertEqual(
            data[9],
            "** <1970-01-01 Thu 00:00> sub\n")
        self.assertEqual(
            data[10],
            "   :PROPERTIES:\n")
        self.assertEqual(
            data[11],
            "   :ID:         da39a3ee5e6b4b0d3255bfef95601890afd80709\n")
        self.assertEqual(
            data[12],
            "   :END:\n")
        self.assertEqual(
            data[13],
            "** <1970-01-01 Thu 00:00> sub\t:foo:bar:\n")
        self.assertEqual(
            data[14],
            "   :PROPERTIES:\n")
        self.assertEqual(
            data[15],
            "   :ID:         da39a3ee5e6b4b0d3255bfef95601890afd80709\n")
        self.assertEqual(
            data[16],
            "   :END:\n")
        #cleaning up
        os.remove(self.TMPFOLDER + "testfile.org")

    def test_utf8(self):
        test_filename = self.TMPFOLDER + "testutf8.org"

        # writing test output
        writer = OrgOutputWriter("short-des", "tag", test_filename)
        writer.write(u"☁☂☃☄★☆☇☈☉☊☋☌☍☎☏☐☑☒☓☔☕☖☗♞♟♠♡♢♣♤♥♦♧♨♩♪♫♬♭♮♯♰♱♲♳♴♵\n")
        writer.close()

        # read and check the file_handler
        file_handler = codecs.open(test_filename, "r", "utf-8")
        input_handler = file_handler.readlines()
        self.assertEqual(input_handler[4],
                         u"☁☂☃☄★☆☇☈☉☊☋☌☍☎☏☐☑☒☓☔☕☖☗♞♟♠♡♢♣♤♥♦♧♨♩♪♫♬♭♮♯♰♱♲♳♴♵\n",
                         "utf-8 failure")

        #cleaning up
        os.remove(self.TMPFOLDER + "testutf8.org")

if __name__ == '__main__':
    unittest.main()
