from command import Command


class Check_Status(Command):
    def __init__(self, container_id):
        self.container_id = container_id
        self.container = super().ConnectToContainer(self.container_id)
        self.Execute()

    def Execute(self) -> str:
        return self.container.status
