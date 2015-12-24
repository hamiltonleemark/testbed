#!/usr/bin/python

import os
import sys

BUILD_COUNT=2000
SUITE_COUNT=5
TEST_COUNT=2

args = {"product": "product1"}

def run(cmd):
    print cmd
    rtc = os.system(cmd)
    if rtc != 0:
        raise ValueError('"%s failed %d"' % (cmd, rtc))

run("./bin/tbd product add %(product)s branch1" % args)
run("./bin/tbd product add %(product)s branch2" % args)

run("./bin/tbd product testplan add %(product)s branch1 default" % args)
run("./bin/tbd product testplan add %(product)s branch2 default" % args)


for buildid in range(0, BUILD_COUNT):
    args["build"] = "build%d" % buildid
    run("./bin/tbd build add %(product)s branch1 %(build)s" % args)
    run("./bin/tbd build add %(product)s branch2 %(build)s" % args)

##
# Create testplan
for suite_item in range(0, SUITE_COUNT):
    args["order"] = str(suite_item)
    args["testsuite"] = "testsuite%d" % suite_item

    run("./bin/tbd testplan add %(testsuite)s" % args)
run("./bin/tbd testplan pack")

for suite_item in range(0, SUITE_COUNT):
    args["order"] = str(suite_item)
    run("./bin/tbd testplan key add %(order)s key1 value1.1" % args)
    run("./bin/tbd testplan key add %(order)s key2 value2.1" % args)
    for test_item in range(0, TEST_COUNT):
        args["test"] = "test%d.%d" % (suite_item, test_item)
        run("./bin/tbd testplan test add %(order)s %(test)s" % args)
# Add testplan keys
#

for buildid in range(0, BUILD_COUNT):
    for suite_item in range(0, SUITE_COUNT):
        args["order"] = str(suite_item)
        args["testsuite"] = "testsuite%d" % suite_item
        args["build"] = "build%d" % buildid

        for test_item in range(0, TEST_COUNT):
            args["test"] = "test%d.%d" % (suite_item, test_item)
            print "adding result %(testsuite)s %(test)s" % args
            run("./bin/tbd result set %(product)s branch1 %(build)s "
                "%(testsuite)s %(test)s pass key1=value1.1 key2=value2.1" % args)
