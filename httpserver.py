from bottle import route, request, response, template, run
from patlite import Patlite as p

@route('/patlite')
def index():
    sensors = {
            "red": [p.OFF, p.ON, p.BLINK1, p.BLINK2],
            "yellow": [p.OFF, p.ON, p.BLINK1, p.BLINK2],
            "green": [p.OFF, p.ON, p.BLINK1, p.BLINK2],
            "buzzer": [p.STOP, p.START, p.SHORT, p.LONG, p.TINY],
            }
    params = {}
    params['red'] = request.query.red # 0,1,2...
    params['yellow'] = request.query.yellow # 0,1,2...
    params['green'] = request.query.green
    params['buzzer'] = request.query.buzzer
    params['timeout'] = request.query.timeout
    
    pat = p.get_instance()
    pat.set_dest('192.168.5.100', 10000)
    '''
    sensors2 = {
            "red": pat.RED,
            "yellow": pat.YELLOW,
            "green": pat.GREEN,
            "buzzer": pat.BUZZER,
            }

    for k,v in sensors2.items():
        sensors[k][int(params[k])]

    '''
    pat.RED = sensors['red'][int(params['red'])]
    pat.YELLOW = sensors['yellow'][int(params['yellow'])]
    pat.GREEN = sensors['green'][int(params['green'])]
    pat.BUZZER = sensors['buzzer'][int(params['buzzer'])]
    # for k,v in params.items():
    #     print(k, sensors[k][int(v)])
    pat.commit()

    return template('<b>Hello World</b>!')

run(host='localhost', port=8080)
