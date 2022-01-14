from google.protobuf.timestamp_pb2 import Timestamp


class Proto:
    @staticmethod
    def get_current_timestamp():
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        return timestamp
