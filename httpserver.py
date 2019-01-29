from bottle import route, request, response, template, run, error
from patlite import Patlite as p
import time

@route('/patlite')
def index():
    sensors = {
            "red": [p.OFF, p.ON, p.BLINK1, p.BLINK2],
            "yellow": [p.OFF, p.ON, p.BLINK1, p.BLINK2],
            "green": [p.OFF, p.ON, p.BLINK1, p.BLINK2],
            "buzzer": [p.OFF, p.BEEP, p.SHORT, p.LONG, p.TINY],
            }
    params = {}
    params['red'] = request.query.red
    params['yellow'] = request.query.yellow
    params['green'] = request.query.green 
    params['buzzer'] = request.query.buzzer
    params['timeout'] = request.query.timeout
    
    pat = p.get_instance()
    pat.set_dest('192.168.10.1', 10000)

    # change mode
    for name in sensors:
        req_value = int(params[name])
        pat.set_status(name, sensors[name][req_value])
    pat.commit()

    # delay
    if not params['timeout']:
        params['timeout'] = 5
    else:
        params['timeout'] = int(params['timeout'])
    time.sleep(params['timeout'])

    # clear mode
    pat.reset_status()
    pat.commit()

    return 'Success to execute commands'

@error(404)
def error404(error):
    return 'Nothing here, sorry'

@error(500)
def error500(error):
    return 'Internal error, sorry'

run(host='0.0.0.0', port=8080)
