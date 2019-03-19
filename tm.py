import argparse
import re

parser = argparse.ArgumentParser(description='A Turing Machine')
parser.add_argument('program_path', type=str, help='the program to be run')
parser.add_argument('input_string', type=str, help='the input string')
args = parser.parse_args()

program = open(args.program_path, 'r')

comment = re.compile('//')
instructions = []
for line in program.readlines():
    line = line.lstrip()
    res = comment.search(line)
    if res:
        line = line[:res.start()].rstrip()
    line = line.split(' ')
    if len(line) != 5:
        raise ValueError('bad instruction length: {}'.format(len(line)))
    instructions.append((line[0], line[1], line[2], line[3], line[4]))


def print_IR(count, state, tape, head):
    ir = []
    for index, char in enumerate(tape):
        if index == head:
            ir.append('[{}]'.format(state))
        ir.append(char)
    print(count+': '+''.join(ir))


def left(tape, head, symbol):
    tape[head] = symbol
    if head == 0:
        tape.insert(0, 'B')
    else:
        head -= 1


def right(tape, head, symbol):
    tape[head] = symbol
    head += 1
    if head == len(tape):
        tape.append('B')


def main():
    tape = args.input_string.lower().split('')
    state = '0'
    head = 0
    count = 0

    while state.lower() != 'f':
        print_IR()
        defined = False
        for i in instructions:
            if i[0].lower() == state:
                if i[1].lower() == tape[head]:
                    if i[4].lower() == 'l':
                        left(i[2], i[3])
                        state = i[3]
                    else:
                        right(i[2], i[3])
                        state = i[3]
                    defined = True
                    break
        if not defined:
            raise ValueError('Undefined transition')
        count += 1

    print_IR()
