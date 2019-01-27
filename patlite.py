import socket

class Patlite:
    # dest
    _host = '192.168.10.1'
    _port = 10000

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

    _led = {
        'red': OFF,
        'yellow': OFF,
        'green': OFF,
        'blue': OFF,
        'white': OFF,
    }

    _buzzer = STOP

    _auto_update = True

    '''
    シングルトーンパターンで設計
    http://www.denzow.me/entry/2018/01/28/171416
    '''
    _unique_instance = None

    def __new__(self):
        raise NotImplementedError('[err] not permitted')

    # create instance for internal class
    @classmethod
    def __internal_new__(cls):
        return super().__new__(cls)

    @classmethod
    def get_instance(cls):
        if not cls._unique_instance:
            cls._unique_instance = cls.__internal_new__()
        
        return cls._unique_instance


    def set_dest(self, host, port):
        if not(0 <= port <= 65535):
            raise ValueError("[err] port must be set integer")
        
        self._host = host
        self._port = port


    def set_led(self, led_type, value):
        self._led[led_type] = value
        if self._auto_update:
            self.commit()

    '''
    properties_dict = {
        "RED": 'red', 
        "YELLOW": 'yellow',
        "GREEN": 'green',
        "BLUE": 'blue',
        "WHITE": 'white',
    }
    
    for k_upper,v_lower in properties_dict.items():
        self.__dict__[k_upper] = property(lambda self: self._led[v_lower],
                                          lambda self, value: self.set_led(v_lower, value))
    '''
    RED = property(lambda self: self._led['red'],
                   lambda self, value: self.set_led('red', value))

    YELLOW = property(lambda self: self._led['yellow'],
                      lambda self, value: self.set_led('yellow', value))

    GREEN = property(lambda self: self._led['green'],
                     lambda self, value: self.set_led('green', value))
    

    def set_buzzer(self, value):
        self._buzzer = value

    BUZZER = property(lambda self: self._buzzer,
                      lambda self, value: self.set_buzzer(value))
    

    def commit(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self._host, self._port))
            except OSError as e:
                print("[err] Cannot connect to patlite. Recheck for address or port.")
                return
            
            s.sendall(b'\x58\x58\x53\x00\x00\x06' + self._led['red'] + self._led['yellow'] + self._led['green'] 
                + b'\x00\x00' + self._buzzer)
            data = s.recv(1024)
            print('Received', repr(data))

