from socket import *
from threading import *


clients = []
names = []

def clientThread(client):
    bilgisayar = True
    while True:
        try:
            message = client.recv(1024).decode('utf8')
            if bilgisayar:
                names.append(message)
                print(message, 'Bağlandı')
                bilgisayar = False
            for c in clients:
                if c != client:
                    index = clients.index(client)
                    name = names[index]
                    c.send((name + ':' + message).encode('utf8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            name = names[index]
            names.remove(name)
            print(name+ 'Ayrıldı')
            break
        


def file_transfer_thread(client):
    try:
        açık_web = client.recv(1024).decode('utf8')
        print(f"Alınacak Dosya Adı: {açık_web}")
        with open(açık_web, 'web programlama') as file:
            while True:
                data = client.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"{açık-web} dosyası başarıyla alındı.")
    except:
        print("Dosya transferi sırasında bağlantı koptu.")
        
        
        
server = socket(AF_INET, SOCK_STREAM)
ip = "10.100.5.98"
port = 3333
server.bind((ip, port))
server.listen()
print('Server Beklemede')


while True:
    client, adress = server.accept()
    clients.append(client)
    print('Bağlantı Yapıldı', adress[0] + ':' + str(adress[1]))
    file_transfer_thread = Thread(target=file_transfer_thread, args=(client,))
    file_transfer_thread.start()
    thread = Thread(target = clientThread, args=(client,))
    thread.start()