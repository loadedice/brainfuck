#!/usr/bin/env python3

from sys import stderr, stdin, argv
from ctypes import c_ubyte

def bf_parse(program, strict=False):
    """
    Takes a brainfuck string, if strict == True checks that it's all valid brainfuck
    returns a dictionary to help deal with jumping around in the program

    I had other ideas about how to do this, but this was the easist to do
    and I think it's kinda nice but also not very efficent in terms of memory useage

    If you can't tell I'm just playing by ear here and things are probably not very good.
    """

    stack = []
    jump_dict = {}

    for position, symbol in enumerate(program):
        if symbol == '[':
            stack.append(position)
        elif symbol == ']':
            destination = stack.pop()
            # Because we may need to jump back up to the '[' to check the condition to see if we need to jump out
            # This could probably be done with a stack in the bf_eval function. Oh well.
            jump_dict[position] = destination
            jump_dict[destination] = position
        elif strict and symbol not in "><+-.,":
            raise SyntaxError("`{s}` at {p} is not a valid brainfuck symbol".format(s=symbol, p=position))

    return jump_dict

def bf_eval(program, memory_size=30000):
    """
    Takes brainfuck string and evaluates it.

    each cell is fixed at being 8 bits
    memory_size defines how many cells there are in memory
    """

    jump_dict = bf_parse(program)
    data = [c_ubyte(0) for _ in range(memory_size)] # Memory
    data_pointer = 0 # index in the memory
    program_counter = 0 # index in the program

    while program_counter < len(program):
        symbol = program[program_counter]

        # Because Python lets you index arrays with negative indecies...
        if 0 > data_pointer or 0 > program_counter:
            raise IndexError("Index out of bounds")

        if symbol == '>':
            data_pointer += 1
        elif symbol == '<':
            data_pointer -= 1
        elif symbol == '+':
            data[data_pointer].value += 1
        elif symbol == '-':
            data[data_pointer].value -= 1
        elif symbol == '.':
            print(chr(data[data_pointer].value), end='')
        elif symbol == ',':
           char = stdin.read(1)
           # If we read nothing then quit.
           if char == '':
               break
           data[data_pointer] = c_ubyte(ord(char))
        elif symbol == '[':
            # If it is false then
            if not data[data_pointer]:
                program_counter = jump_dict[program_counter]
        elif symbol == ']':
            program_counter = jump_dict[program_counter]
            continue

        program_counter += 1
    print()

def main():
    if len(argv) > 2:
        print("Usage: {} [path to file]".format(argv[0]), file=stderr)
        return
    elif len(argv) == 2:
        with open(argv[1], 'r') as f:
            program = f.read().strip()
    else:
        program = input("Enter the brainfuck pogram: ")

    bf_eval(program)

if __name__ == '__main__':
    main()
