import stomp
import time

conn = stomp.Connection([('localhost', 61613)])
conn.connect('admin', 'admin', wait=True)

for i in range(5):
    message = f"Mensagem {i+1}"
    conn.send(destination='/queue/fila.test', body=message)
    print(f"Enviada: {message}")
    time.sleep(0.5)

conn.disconnect()
