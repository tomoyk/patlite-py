import patlite

def main():
    p = patlite.Patlite.get_instance()
    p.set_dest('192.168.0.169', 10000)

    p.RED = p.BLINK2
    p.YELLOW = p.BLINK2
    p.GREEN = p.BLINK1
    p.BUZZER = p.LONG

    p.commit()
    

if __name__ == '__main__':
    main()