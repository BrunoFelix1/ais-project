import stomp
import time

conn = stomp.Connection([('localhost', 61613)])
conn.connect('admin', 'admin', wait=True)

for i in range(5):
    message = f"Mensagem automática {i+1}"
    conn.send(destination='/queue/fila.test', body=message)
    print(f"Enviada: {message}")
    time.sleep(0.5)

while True:
    user_message = input("Digite uma mensagem (ou 'sair' para encerrar): ")
    if user_message.lower() == "sair":
        break
    conn.send(destination='/queue/fila.test', body=user_message)
    print(f"Enviada: {user_message}")

conn.disconnect()
