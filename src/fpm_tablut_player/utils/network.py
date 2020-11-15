import struct

###

class NetworkUtils:

    @staticmethod
    def is_value_sent(bytes_sent: int, expected_bytes_sent: int):
        return bytes_sent == expected_bytes_sent

    @staticmethod
    def integer_request(integer: int):
        return struct.pack('>i', integer)


    @staticmethod
    def string_request(string):
        return string.encode('utf-8')
