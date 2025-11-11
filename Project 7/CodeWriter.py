class CodeWriter:
    def __init__(self, output_file):
        self.file = open(output_file, "w")
        self.label_counter = 0             # Counter for generating unique labels

    def writeInit(self):
        # Writes the Hack assembly code that initializes the VM
        self.file.write("@256\nD=A\n@SP\nM=D\n")
        self.write_call("Sys.init", 0)

    def writeLabel(self, label: str):
        # Writes the Hack assembly code that sets a label
        self.file.write(f"({label})\n")

    def writeGoto(self, label: str):
        # Writes the Hack assembly code that jumps to the specified label
        self.file.write(f"@{label}\n0;JMP\n")

    def writeIf(self, label: str):
        # Writes the Hack assembly code that jumps to the specified label if the top of the stack is not zero
        self.file.write("@SP\nAM=M-1\nD=M\n")
        self.file.write(f"@{label}\nD;JNE\n")

    def setFileName(self, file_name: str):
        self.fileName = file_name

    def write_arithmetic(self, command):
        # Dictionary mapping arithmetic commands to their corresponding Hack code
        operations = {
            "add": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=M+D\n",
            "sub": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=M-D\n",
            "neg": "@SP\nA=M-1\nM=-M\n",
            "not": "@SP\nA=M-1\nM=!M\n",
            "and": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=M&D\n",
            "or": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=M|D\n",
            "eq": self._write_comparison("JEQ"),
            "gt": self._write_comparison("JGT"),
            "lt": self._write_comparison("JLT"),
        }
        self.file.write(operations[command])

    def _write_comparison(self, jump_type):
        # Generates unique labels for comparison commands
        label_true = f"TRUE{self.label_counter}"
        label_end = f"END{self.label_counter}"
        self.label_counter += 1
        return (
            "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\n"
            f"@{label_true}\nD;{jump_type}\n"
            "@SP\nA=M-1\nM=0\n"
            f"@{label_end}\n0;JMP\n"
            f"({label_true})\n@SP\nA=M-1\nM=-1\n"
            f"({label_end})\n"
        )

    def write_push_pop(self, command_type, segment, index):
        # Generates Hack code for push and pop commands
        if command_type == "C_PUSH":
            if segment == "constant":
                self.file.write(f"@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif command_type == "C_POP":
            if segment == "local":
                self.file.write(
                    f"@{index}\nD=A\n@LCL\nD=M+D\n@R13\nM=D\n"
                    "@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
                )

    def close(self):
        # Closes the output file
        self.file.close()
