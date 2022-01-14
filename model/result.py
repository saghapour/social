from typing import Any


class OperationResult:
    def __init__(self):
        self.__has_error = False
        self.__message = ""
        self.__object = None

    def set_error(self, message: str):
        self.__has_error = True
        self.__message = message

    def set_success(self, message: str):
        self.__has_error = False
        self.__message = message

    def set_object(self, obj: Any):
        self.__object = obj

    @property
    def has_error(self) -> bool:
        return self.__has_error

    @property
    def message(self) -> str:
        return self.__message

    @property
    def object(self):
        return self.__object

    @property
    def success(self):
        return not self.__has_error

    @staticmethod
    def get_instance():
        return OperationResult()

    def __str__(self):
        return self.__message


class BatchOperationResult:
    def __init__(self):
        self.__batch_result = []
        self.__has_error = False

    def add_result(self, result: OperationResult):
        self.__has_error |= result.has_error
        self.__batch_result.append(result)

    @property
    def has_error(self):
        return self.__has_error
