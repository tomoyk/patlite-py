import patlite

def main():
    p = patlite.Patlite.get_instance()
    p.set_dest('192.168.0.169', 10000)

    p.RED = p.BLINK1
    p.YELLOW = p.BLINK2
    p.GREEN = p.ON
    p.BUZZER = p.STOP

    p.commit()
    

if __name__ == '__main__':
    main()