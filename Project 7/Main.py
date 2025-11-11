import sys
from Parser import Parser
from CodeWriter import CodeWriter

def main():

    input_file = sys.argv[1]
    output_file = input_file.replace(".vm", ".asm")

    parser = Parser(input_file)
    code_writer = CodeWriter(output_file)

    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()

        if command_type == "C_ARITHMETIC":
            code_writer.write_arithmetic(parser.arg1())
        elif command_type in {"C_PUSH", "C_POP"}:
            code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())

    code_writer.close()

if __name__ == "__main__":
    main()
