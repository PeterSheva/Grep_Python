
import argparse
import sys
import re


def output(line):
    print(line)


def numerated_otput(line, number, non_match=False):
    if(non_match):
        output(str(number + 1) + '-' + line)
    else:
        output(str(number + 1) + ':' + line)


def context(lines, params, reg):
    if(params.context > params.before_context):
        before = params.context
    else:
        before = params.before_context
    if(params.context > params.after_context):
        after = params.context
    else:
        after = params.after_context
    bf = False
    af = False
    indexes = []
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip()
        if bool(reg.search(lines[i])) != params.invert:
            indexes.append(i)
            cur_bf = i - before
            cur_af = i + after
            if(cur_bf < 0): 
                cur_bf = 0
            if(cur_af > len(lines) - 1): 
                cur_af = len(lines) - 1 
            if bf is False is af:
                bf = cur_bf
                af = cur_af
            elif(cur_bf <= af):
                af = cur_af
            else:
                for j in range(bf, af + 1):
                    if(params.line_number):
                        numerated_otput(lines[j], j, j not in indexes)
                    else:
                        output(lines[j])
                    del indexes[:]
                    bf = cur_bf
                    af = cur_af
    if(bf is not False):
        for j in range(bf, af + 1):
            if(params.line_number):
                numerated_otput(lines[j], j, j not in indexes)
            else:
                output(lines[j])

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
    elif(params.context or params.before_context or params.after_context):
        context(lines, params, reg)
    else:
        for number, line in enumerate(lines):
            if bool(reg.search(line)) != params.invert:
                if(params.line_number):
                    numerated_otput(line, number)
                else:
                    output(line)


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
