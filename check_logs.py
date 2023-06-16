from command import Command

class Check_Logs(Command):
    def __init__(self, container_id):
        self.container_id = container_id
        self.container = Command.ConnectToContainer(self.container_id)

    def execute(self) -> str:
        return self.container.logs(timestamps=True) 
    