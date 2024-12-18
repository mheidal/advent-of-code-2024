from utils import utils

def run_computer(instructions: list[int], registers: tuple[int, int, int], *, allow_jump: bool = True) -> list[int]:
    a, b, c = registers
    iptr = 0
    out = []
    while iptr < len(instructions):
        operation, operand = instructions[iptr:iptr+2]
        if operation in [1, 3] or operand <= 3:
            val = operand
        elif operand == 4:
            val = a
        elif operand == 5:
            val = b
        elif operand == 6:
            val = c
        else:
            raise ValueError(f"Invalid operation, operand pair: {operation, operand}")

        jumped = False
        match operation:
            case 0:
                a = int(a / (2 ** val))
            case 1:
                b = b ^ val
            case 2:
                b = val % 8
            case 3:
                if not allow_jump:
                    return out
                else:
                    if a != 0:
                        jumped = True
                        iptr = val
            case 4:
                b = b ^ c
            case 5:
                out.append(val % 8)
            case 6:
                b = int(a / (2 ** val))
            case 7:
                c = int(a / (2 ** val))
        if not jumped:
            iptr += 2
    return out


def part_1():
    with open("inputs/day17.txt", "r") as f:
        numbers = utils.ints(f.read())
    a, b, c = numbers[:3]
    instructions = numbers[3:]
    return ",".join([str(o) for o in run_computer(instructions, (a, b, c), allow_jump=True)])


def part_2():
    with open("inputs/day17.txt", "r") as f:
        instructions = utils.ints(f.read())[3:]

    # The input program is a loop and outputs once per loop. Once per loop, it divides A by 8 and truncates the result.
    # Every output is dependent on a 3-bit chunk of the value in A, as well as all more-significant bits of A.
    # The most significant 3 bits are used to generate the last output.
    # The most significant 6 bits are used to generate the second-to-last output, and so on.
    # So we check which 3-bit values (values less than 8) could be concatenated to the value in A (starting A out at 0)
    #     to generate each output, going from last output to first.
    # We check this by recursively trying new values for A and running the computer for one loop (until it outputs once)
    #     and checking if that output matches the part of the program we were trying to generate.
    # Notably, the values of B and C at the end of one loop have no impact on the next loop, so we can ignore them and 
    #     simply set them to 0, 0 at the beginning of each check.
    def recursively_try_3_bits(instruction_index: int = len(instructions) - 1, A: int = 0) -> int | None:
        if instruction_index < 0:
            return A
        A *= 8
        valid_octals = [
            a for a in range(8)
            if run_computer(instructions, (A + a, 0, 0), allow_jump=False)[0] == instructions[instruction_index]
        ]
        for valid_octal in valid_octals:
            if (result := recursively_try_3_bits(instruction_index - 1, A + valid_octal)) is not None:
                return result
        return None

    return recursively_try_3_bits()
