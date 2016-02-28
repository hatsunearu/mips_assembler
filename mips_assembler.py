#!/usr/bin/python

import sys


def main():
    if len(sys.argv) < 2:
        print "You must specify the input file."
        return

    filename = sys.argv[1]

    input_file = open(filename, 'r')

    reference_table = dict();
    instructions = list();

    linenum = 0

    with input_file as f:
        for line in f:
            if not line.strip():
                continue

            (instr, label) = parse_line(line)
            instructions.append(instr)
            if label:
                reference_table[label] = linenum

            linenum += 1

    for instr in instructions:
        instr_hex = 0x0;
        if (instr[0] == "add"):
            instr_hex |= 0b000000 << 26
            instr_hex |= instr[2] << 21
            instr_hex |= instr[3] << 16
            instr_hex |= instr[1] << 11
            instr_hex |= 0b00000100000

        elif (instr[0] == "j"):
            linenum = reference_table[instr[1]]
            instr_hex |= 0b000010 << 26
            instr_hex |= linenum

        print format(instr_hex, '08x')



    input_file.close()


def parse_line(line):
    line = line.strip()
    split_colon = line.split(":")
    if len(split_colon) == 2:
        label = split_colon[0]
        line = split_colon[1]
    else:
        label = ""

    line = line.strip().split(" ")
    line = map(lambda x: x.replace(",", ""), line)
    line = map(match_regs, line)

    return (line, label)

def match_regs(s):
    if s[0] == '$':
        nodollar = s[1:]
        return int(nodollar)
    return s

if __name__ == '__main__':
    main()
