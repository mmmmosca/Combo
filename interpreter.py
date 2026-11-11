"""
COMMANDS:
l r u d a b c n() ()

l/r = moves pointer
u/d = increments/decrements current cell
a/b = output/input (like brainfuck)
c = output number
n() = repeats instructions inside them n times
() = loops until current cell is 0
"""


import sys


def tokenize(code):
    tokens = []
    l = len(code)
    i = 0

    while i < l:
        c = code[i]

        if c.isdigit():
            j = i
            while j < l and code[j].isdigit():
                j += 1

            tokens.append(int(code[i:j]))
            i = j
            continue
        elif c == "l":
            tokens.append("LEFT")
        elif c == "r":
            tokens.append("RIGHT")
        elif c == "u":
            tokens.append("UP")
        elif c == "d":
            tokens.append("DOWN")
        elif c == "a":
            tokens.append("A")
        elif c == "b":
            tokens.append("B")
        elif c == "c":
            tokens.append("C")
        elif c == "(":
            tokens.append("LPAREN")
        elif c == ")":
            tokens.append("RPAREN")

        i += 1

    return tokens


def eval(tokens, tape, state):
    l = len(tokens)
    i = 0

    while i < l:
        token = tokens[i]
        next_token = tokens[i + 1] if i + 1 < l else None

        if isinstance(token, int) and next_token == "LPAREN":
            loop_inst = []
            n = token
            j = i + 2

            while j < l and tokens[j] != "RPAREN":
                loop_inst.append(tokens[j])
                j += 1

            while n > 0:
                eval(loop_inst, tape, state)
                n -= 1

            i = j + 1
            continue

        elif token == "LPAREN":
            loop_inst = []
            j = i + 1

            while j < l and tokens[j] != "RPAREN":
                loop_inst.append(tokens[j])
                j += 1

            while tape[state["ptr"]] != 0:
                eval(loop_inst, tape, state)

            i = j + 1
            continue

        elif token == "RIGHT":
            state["ptr"] += 1
            if state["ptr"] > 254:
                state["ptr"] = 0
        elif token == "LEFT":
            state["ptr"] -= 1
            if state["ptr"] < 0:
                state["ptr"] = 254
        elif token == "UP":
            tape[state["ptr"]] += 1
        elif token == "DOWN":
            tape[state["ptr"]] -= 1
        elif token == "A":
            print(chr(tape[state["ptr"]]), end="")
        elif token == "C":
            print(tape[state["ptr"]], end="")
        elif token == "B":
            line = input()

            for c in line:
                tape[state["ptr"]] = ord(c)
                state["ptr"] += 1
                if state["ptr"] > 254:
                    state["ptr"] = 0

        i += 1


with open(sys.argv[1], "r") as code:

    code = code.readlines()
    tape = [0] * 255
    state = {"ptr": 0}

    tokens = []
    for line in code:
        tokens += tokenize(line)

    eval(tokens, tape, state)

    try:
        if sys.argv[2] == "--debug":
            print(f"tape: {tape}")
            print(f"pointer: {state["ptr"]}")
    except IndexError:
        pass
