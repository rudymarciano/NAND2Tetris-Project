
class Parser:
    def __init__(self,file_path) -> None:
        self.file = file_path
        self.current_instruction = None
        self.lines = self.file.readlines()
        self.current_line = 0

    def hasMoreLines(self) -> bool:
        return self.current_line < len(self.lines)

    def advance(self) -> None:
        while self.hasMoreLines():
            line = self.lines[self.current_line].strip()
            self.current_line += 1
            if line and not line.startswith("//"):
                self.current_instruction = line.split("//")[0].strip()
                break

    def commandType(self) -> str:
        arithmetic_commands = {"add", "sub", "and", "or", "eq", "gt", "lt", "neg", "not"}
        command=self.current_instruction.split(" ")[0]
        if command in arithmetic_commands:
            return "C_ARITHMETIC"
        elif command == "push":
            return "C_PUSH"
        elif command == "pop":
            return "C_POP"
        elif command == "label":
            return "C_LABEL"
        elif command == "goto":
            return "C_GOTO"
        elif command == "if-goto":
            return "C_IF"
        elif command == "function":
            return "C_FUNCTION"
        elif command == "call":
            return "C_CALL"
        elif command == "return":
            return "C_RETURN"

    def arg1(self) -> str:
        command = self.current_instruction
        if self.commandType() == "C_RETURN":
            pass
        if self.commandType() == "C_ARITHMETIC":
            return command
        else:
            return command.split()[1]



    def arg2(self):
        command = self.current_instruction.split()[2]
        return int(command)








