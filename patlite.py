import socket

class Patlite:

    HOST = '192.168.0.169'
    PORT = 10000

    # light
    OFF = b'\x00'
    ON = b'\x01'
    BLINK1 = b'\x02' # ----____----____
    BLINK2 = b'\x03' # -_-_____-_-_____

    # buzzer
    STOP = b'\x00'  
    SHORT = b'\x01' # --__--__--__--__
    LONG = b'\x02'  # ----____----____
    TINY = b'\x03'  # -_-_____-_-_____
    START = b'\x04' # ----------------

    '''
    シングルトーンパターンで設計
    http://www.denzow.me/entry/2018/01/28/171416
    '''
    _unique_instance = None

    def __new__(self):
        raise NotImplementedError('not permitted')

    # 内部からのインスタンス作成用
    @classmethod
    def __internal_new__(cls):
        return super().__new__(cls)

    @classmethod
    def get_instance(cls):
        if not cls._unique_instance:
            cls._unique_instance = cls.__internal_new__()
        
        return cls._unique_instance
        
    def commit(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            # s.sendall(b'\x57\xc0\x2d\x9b\xdb\x93')
            s.sendall(b'\x58\x58\x53\x00\x00\x06' + b'\x03\x02\x01\x00\x00\x00')
            data = s.recv(1024)
            print('Received', repr(data))

