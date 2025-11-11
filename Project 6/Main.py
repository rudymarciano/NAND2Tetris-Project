import sys
from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable

def HackAssembler():
    # Get file name from command line arguments
    file_name = sys.argv[1]
    output_name = file_name.replace(".asm", ".hack")

    parser = Parser(file_name)
    code = Code()
    symbols = SymbolTable()

    # First pass: Build the symbol table with labels
    rom_address = 0
    while parser.has_more_commands():
        parser.advance()
        if parser.instruction_type() == "L":
            symbols.add_entry(parser.symbol(), rom_address)
        else:
            rom_address += 1

    # Second pass: Translate instructions to binary
    parser.reset()  # Reset parser for second pass
    next_ram_address = 16  # Start allocating RAM addresses at 16
    binary_instructions = []

    while parser.has_more_commands():
        parser.advance()

        if parser.instruction_type() == "A":
            symbol = parser.symbol()
            if symbol.isdigit():
                address = int(symbol)
            else:
                if not symbols.contains(symbol):
                    symbols.add_entry(symbol, next_ram_address)
                    next_ram_address += 1
                address = symbols.get_address(symbol)
            binary_instructions.append(f"{address:016b}")

        elif parser.instruction_type() == "C":
            comp = code.comp(parser.comp())
            dest = code.dest(parser.dest())
            jump = code.jump(parser.jump())
            binary_instructions.append(f"111{comp}{dest}{jump}")

    # Write output to file
    with open(output_name, "w") as output_file:
        output_file.write("\n".join(binary_instructions))

if __name__ == "__main__":
    HackAssembler()
