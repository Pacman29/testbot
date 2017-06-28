class MessageParser():
    def __init__(self,commands):
        self._commands = commands

    def calculate(self,message):
        for command in self._commands:
            if(message.startswith(command)):
                return {
                    'command': command,
                    'keys': message[len(command):].split()
                }
        return None