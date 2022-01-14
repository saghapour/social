from .errors import ErrorsFa, ErrorsEn


class Messages:
    @staticmethod
    def get_record_exist_error():
        return ErrorsEn.RecordExist.value

    @staticmethod
    def get_success_message():
        return "Operation done successfully"
