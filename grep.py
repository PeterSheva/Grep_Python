import argparse
import sys
import re
from collections import deque


def output(line):
    print(line)


def numerated_otput(line, number, non_match=False):
    if(non_match):
        output(str(number) + '-' + line)
    else:
        output(str(number) + ':' + line)


def context(lines, params, reg):
    if(params.context > params.before_context):
        before = params.context
    else:
        before = params.before_context
    if(params.context > params.after_context):
        after = params.context
    else:
        after = params.after_context
        
    buf = deque(lines, before)
    after_print = 0
    i = 0

    for line in lines:
        i += 1
        line = line.rstrip()
        if bool(reg.search(line)) != params.invert:
            after_print = after
            for k in range(len(buf)):
                show_line = buf.popleft()
                if(params.line_number):
                    numerated_otput(show_line[1], show_line[0], show_line[2])
                else:
                    output(show_line[1])
            if(params.line_number):
                numerated_otput(line, i)
            else:
                output(line)
        elif(after_print != 0):
            if(params.line_number):
                numerated_otput(line, i, True)
            else:
                output(line)
            after_print -= 1
        else:
            buf.append((i, line, True))


def grep(lines, params):
    reg = params.pattern.replace('?', '.').replace('*', '.*')
    if(params.ignore_case):
        reg = re.compile(reg,re.IGNORECASE)
    else:
        reg = re.compile(reg)

    if(params.count):
        counter = 0
        for line in lines:
            if bool(reg.search(line)) != params.invert:
                counter += 1
        output(str(counter))
    else:
        context(lines, params, reg)

                    
def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
