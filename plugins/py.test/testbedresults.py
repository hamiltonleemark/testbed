import pytest

def pytest_report_teststatus(report):
    if report.when == "call":
        print "MARK: report_teststatus", report
