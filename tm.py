import argparse
import re


def get_ir(state, tape, head):
    ir = []
    for index, char in enumerate(tape):
        if index == head:
            ir.append('[{}]'.format(state))
        ir.append(char)
    return ''.join(ir)


def left(tape, head, symbol):
    tape[head] = symbol
    if head == 0:
        tape.insert(0, 'B')
    else:
        head -= 1
    return head


def right(tape, head, symbol):
    tape[head] = symbol
    head += 1
    if head == len(tape):
        tape.append('B')
    return head


def store(table, state, symbol, transition):
    if state in table:
        if symbol in table[state]:
            raise ValueError(
                'transition: {} was already present'.format(transition))
        else:
            table[state][symbol] = transition
    else:
        table[state] = {symbol: transition}


def crash(state, tape, head):
    raise SystemExit(
        'Undefined transition: {} on {}'.format(state, tape[head]))


def main():
    parser = argparse.ArgumentParser(description='A Turing Machine')
    parser.add_argument('program_path', type=str, help='the program to be run')
    parser.add_argument('input_string', type=str, help='the input string')
    args = parser.parse_args()

    program = open(args.program_path, 'r')

    comment = re.compile('//')

    instructions = {}   # the transition table

    for line in program.readlines():
        line = line.lstrip()
        res = comment.search(line)
        if res:
            line = line[:res.start()].rstrip()
        line = line.split(' ')
        if len(line) != 5:
            continue
        store(instructions, line[0], line[1], (line[2], line[3], line[4]))

    tape = [sym for sym in args.input_string.lower()]
    state = '0'
    head = 0
    count = 0

    print('Begin in state: {}'.format(get_ir(state, tape, head)))

    while state != 'f':
        transition = None
        try:
            transition = instructions[state][tape[head]]
        except KeyError:
            crash(state, tape, head)
        if not transition:
            crash(state, tape, head)
        if transition[2] == 'R':
            head = right(tape, head, transition[1])
            state = transition[0]
        elif transition[2] == 'L':
            head = left(tape, head, transition[1])
            state = transition[0]
        count += 1
        print('t={}: {}'.format(count, get_ir(state, tape, head)))

    print('Halted in accepting state.')


if __name__ == "__main__":
    main()
