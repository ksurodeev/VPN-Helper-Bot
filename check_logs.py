from command import Command


class Check_Logs(Command):
    def __init__(self, container_id):
        self.container_id = container_id
        self.container = super().ConnectToContainer(self.container_id)

    def Execute(self) -> str:
        for each in self.container.logs():
            print(str(each, 'utf-8'))
