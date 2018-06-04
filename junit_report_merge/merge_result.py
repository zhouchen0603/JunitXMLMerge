from junitparser import TestCase, TestSuite, JUnitXml, Skipped, Error, Failure
import os
import random
import argparse

def get_case(testsuite, testcase):
    for case in testsuite._elem.getchildren():
        _testcase = TestCase.fromelem(case)
        if _testcase.classname == testcase.classname and _testcase.name == testcase.name and _testcase._elem.attrib['file'] == testcase._elem.attrib['file']:
            return _testcase
    return None

def main():
    out_file_path = '/Users/zzhou/helmut/test1/utils/merged_result_%d.xml' % random.randint(0,10000000)
    in_path ='/Users/zzhou/helmut/test1/'

    parser = argparse.ArgumentParser()
    parser.add_argument('--in', help='path')
    parser.add_argument('--out', help='full path with filename')
    parser.add_argument('--delete', help='delete the file(--out) before merge', default=False, type=type(True))

    #parser.print_help()
    args = parser.parse_args()
    try:
        out_file_path = vars(args)['out']
        in_path = vars(args)['in']
        delete = vars(args)['delete']
    except Exception as e:
        # print args
        # print e
        parser.print_help()

    if out_file_path == None or in_path == None:
        parser.print_help()

    if not os.path.exists(in_path):
        raise Exception("Can't find the path: in=%s" %in_path)

    files_to_merge = []
    for root, dirs, files in os.walk(in_path):
        for file in files:
            if file.endswith('.xml'):
                files_to_merge.append(os.path.join(root,file))

    if len(files_to_merge) <= 1:
        print("Can't find XML to merge. Must more than 1 xml file. %s" % str(files_to_merge))
        return
    else:
        print("Found below files to merge: %s" % str(files_to_merge))

    # handle duplicate entries
    testsuite = TestSuite()
    for file in files_to_merge:
        try:
            xml = JUnitXml.fromfile(file)
        except:
            print("Warning: found unsupported xml: %s" % file)
            continue
        for case in xml._elem.getchildren():
            testcase = TestCase.fromelem(case)
            _testcase = get_case(testsuite, testcase)
            if _testcase == None:
                testsuite.add_testcase(testcase)
            else:
                if _testcase.result and _testcase.result._tag == Failure._tag:
                    testsuite.remove_testcase(_testcase)
                    testsuite.add_testcase(testcase)
        if delete:
            os.remove(file)
            print ("File removed after merge. %s" % file)

    time = 0
    skips = 0
    failures = 0
    errors = 0
    tests = 0

    # add properties
    for case in testsuite._elem.getchildren():
        testcase = TestCase.fromelem(case)
        tests += 1
        time += testcase.time
        if not hasattr(testcase.result, '_tag'):
            continue
        if testcase.result._tag == Failure._tag:
            failures += 1
        elif testcase.result._tag == Skipped._tag:
            skips += 1
        elif testcase.result._tag == Error._tag:
            errors += 1

    testsuite.errors = errors
    testsuite.tests = tests
    testsuite.time = time
    testsuite.skipped = skips
    testsuite.failures = failures
    testsuite.name = 'pytest'

    if os.path.exists(out_file_path):
        os.remove(out_file_path)
    testsuite.write(out_file_path)
    if os.path.exists(out_file_path):
        print("File created successfaully. %s" % out_file_path)


if __name__=="__main__":
    main()