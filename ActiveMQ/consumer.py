import stomp

class Listener(stomp.ConnectionListener):
    def on_message(self, frame):
        print('Recebida:', frame.body)

conn = stomp.Connection([('localhost', 61613)])
conn.set_listener('', Listener())
conn.connect('admin', 'admin', wait=True)

conn.subscribe(destination='/queue/fila.test', id=1, ack='auto')

print("Aguardando mensagens... (CTRL+C para sair)")

import time
while True:
    time.sleep(1)
