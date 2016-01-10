#!/usr/bin/python

import os
import sys

BUILD_COUNT=2000
SUITE_COUNT=5
TEST_COUNT=2

##
# db is usually default but can be set to local.

args = {
    "db": "default",
    "product": "product1",
    "tbd": "../../bin/tbd"
    }

def run(cmd):
    print cmd
    rtc = os.system(cmd)
    if rtc != 0:
        raise ValueError('"%s failed %d"' % (cmd, rtc))

run("%(tbd)s -d %(db)s product add %(product)s branch1" % args)
run("%(tbd)s -d %(db)s product add %(product)s branch2" % args)
run("%(tbd)s -d %(db)s product add %(product)s branch3" % args)

run("%(tbd)s -d %(db)s product testplan add %(product)s branch1 default" % args)
run("%(tbd)s -d %(db)s product testplan add %(product)s branch2 default" % args)
run("%(tbd)s -d %(db)s product testplan add %(product)s branch3 default" % args)


##
# Create testplan
for suite_item in range(0, SUITE_COUNT):
    args["order"] = str(suite_item)
    args["testsuite"] = "testsuite%d" % suite_item

    run("%(tbd)s -d %(db)s testplan add %(testsuite)s" % args)
run("%(tbd)s -d %(db)s testplan pack" % args)

for suite_item in range(0, SUITE_COUNT):
    args["order"] = str(suite_item)
    run("%(tbd)s -d %(db)s testplan key add %(order)s key1 value1.1" % args)
    run("%(tbd)s -d %(db)s testplan key add %(order)s key2 value2.1" % args)
    for test_item in range(0, TEST_COUNT):
        args["test"] = "test%d.%d" % (suite_item, test_item)
        run("%(tbd)s -d %(db)s testplan test add %(order)s %(test)s" % args)
# Add testplan keys
#

for buildid in range(0, BUILD_COUNT):
    args["build"] = "build%d" % buildid
    run("%(tbd)s -d %(db)s build add %(product)s branch1 %(build)s" % args)
    run("%(tbd)s -d %(db)s build add %(product)s branch2 %(build)s" % args)

    for suite_item in range(0, SUITE_COUNT):
        args["order"] = str(suite_item)
        args["testsuite"] = "testsuite%d" % suite_item
        args["build"] = "build%d" % buildid

        for test_item in range(0, TEST_COUNT):
            args["test"] = "test%d.%d" % (suite_item, test_item)
            print "adding result %(testsuite)s %(test)s" % args
            run("%(tbd)s -d %(db)s result set %(product)s branch1 %(build)s "
                "%(testsuite)s %(test)s pass key1=value1.1 key2=value2.1" % args)
