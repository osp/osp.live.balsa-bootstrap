# -*- coding: utf-8 -*-

from bottle import request, Bottle, abort, static_file
app = Bottle()


import chiplotle
from chiplotle import hpgl

import json
import sys
import os

DEBUG = True
DEBUG = False
ROOT_DIR = os.getcwd()
plotter = None

import threading
import Queue




print('ROOT => %s'%(ROOT_DIR,))

try:
    if not DEBUG:
        devices = chiplotle.instantiate_plotters()
        plotter = devices[0]
        
        bl = plotter.margins.hard.bottom_left
        tr = plotter.margins.hard.top_right
        cmd = hpgl.IP([(bl.x,bl.y),(tr.x, tr.y)])
        print cmd
        plotter.write(cmd)
        
except Exception as e:
    print('Could not istantiate plotter: %s'%e)
    if not DEBUG:
        sys.exit()

def draw_on_plotter(x,y):
    cmd = hpgl.PD([(x,y)])
    print cmd
    if not DEBUG:
        try:
            plotter.write(cmd)
        except Exception as e:
            print('Error plotter.write: %s'%(e))
    
queue = Queue.Queue()

def worker():
    while True:
        coord = queue.get()
        ok = False
        try:
            x = int(coord['x'])
            y = int(coord['y'])
            ok = True
        except Exception as e:
            print('Malformed coordinates: %s'%(e))
        if ok:
            draw_on_plotter(x,y)
        queue.task_done()

        
workers = []
for i in range(4):
     t = threading.Thread(target=worker)
     t.daemon = True
     t.start()
     workers.append(t)

@app.route('/')
def index():
    idx = open('base.html')
    idx_html = idx.read()
    idx.close()
    return idx_html

@app.route('/static/<sf>')
def static(sf):
    root = os.path.join(ROOT_DIR,'static')
    print('Looking for %s in %s'%(sf,root))
    return static_file(sf, root=root)

@app.route('/plotter')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    wsock.send(json.dumps({'status':'ready'}))
    while True:
        try:
            message = wsock.receive()
            try:
                coord = json.loads(message)
                if 'scale' in  coord:
                    if not DEBUG:
                        cmd = hpgl.SC([(0,int(coord['w'])),(0, int(coord['h']))])
                        print cmd
                        plotter.write(cmd)
                    else:
                        print hpgl.SC([(0,float(coord['w'])),(0, float(coord['h']))])
                else:
                    #draw_on_plotter(coord['x'], coord['y'])
                    queue.put(coord)
                    
                wsock.send(json.dumps({'status':'ready'}))
                
            except Exception as e:
                wsock.send(json.dumps({'msg':"%s"%e, 'status':'error'}))
        except WebSocketError:
            break

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler, WebSocketError
server = WSGIServer(("127.0.0.1", 8000), app,
                    handler_class=WebSocketHandler)
server.serve_forever()


