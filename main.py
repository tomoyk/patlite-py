import patlite

def main():
    p = patlite.Patlite.get_instance()
    p.set_dest('192.168.0.169', 10000)

    p.set_status("red", p.ON)
    p.set_status("yellow", p.BLINK1)
    p.set_status("green", p.BLINK2)
    p.set_status("buzzer", p.OFF)
    p.commit()
    
    ''' Reset
    p.clear
    p.commit()
    '''


if __name__ == '__main__':
    main()