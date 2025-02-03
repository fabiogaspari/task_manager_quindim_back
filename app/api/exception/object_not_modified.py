class ObjectNotModified(Exception):
    """Exceção personalizada para informar que o objeto não foi modificado ao tentar atualiza-lo."""
    def __init__(self, message="O Objeto não foi modificado, pois os parametros passados estão iguais aos do registro encontrado."):
        self.message = message
        super().__init__(self.message)