class TaskStatusOnTaskNotFound(Exception):
    """Exceção personalizada para informar que o status da tarefa não foi encontrado na tarefa."""
    def __init__(self, message="Status da tarefa não encontrado ou incompleto."):
        self.message = message
        super().__init__(self.message)