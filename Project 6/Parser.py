class Parser:
    def __init__(self, file_name):
        with open(file_name, "r") as file:
            self.lines = file.readlines()

        self.commands = self._clean_lines()
        self.current_command = ""
        self.current_index = -1

    def _clean_lines(self):
        cleaned = []
        for line in self.lines:
            line = line.split("//")[0].strip()  # Remove comments and whitespace
            if line:
                cleaned.append(line)
        return cleaned

    def has_more_commands(self):
        return self.current_index + 1 < len(self.commands)

    def advance(self):
        self.current_index += 1
        self.current_command = self.commands[self.current_index]

    def instruction_type(self):
        if self.current_command.startswith("@"):
            return "A"
        elif self.current_command.startswith("("):
            return "L"
        else:
            return "C"

    def symbol(self):
        if self.instruction_type() == "A":
            return self.current_command[1:]
        elif self.instruction_type() == "L":
            return self.current_command[1:-1]

    def dest(self):
        if "=" in self.current_command:
            return self.current_command.split("=")[0]
        return ""

    def comp(self):
        command = self.current_command
        if "=" in command:
            command = command.split("=")[1]
        if ";" in command:
            command = command.split(";")[0]
        return command

    def jump(self):
        if ";" in self.current_command:
            return self.current_command.split(";")[1]
        return ""

    def reset(self):
        self.current_command = ""
        self.current_index = -1
