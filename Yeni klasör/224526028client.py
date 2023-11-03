from socket import * 
from threading import *
from tkinter import *
from datetime import datetime
from tkinter import filedialog

client = socket(AF_INET, SOCK_STREAM)

ip = "10.100.5.98"
port = 3333

client.connect((ip, port))

ekran = Tk()

ekran.title("Bilgisayar")

message = Text(ekran, width=30)
message.grid(row =0, column=0, padx=15, pady=15,)

metin_gir = Entry(ekran, width=50)
metin_gir.insert(0, "Bağlanan Kişi*")
metin_gir.grid(row=1,column=0,
                 padx=20,pady=20,
                 )


metin_gir.focus() 
metin_gir.selection_range(0, END)

def mesaj_gonder():
    istemci_mesaji = metin_gir.get()
    now = datetime.now()
    message.insert(END, '\n' + 'Sen :'+ istemci_mesaji)
    client.send(istemci_mesaji.encode('utf8'))
    metin_gir.delete(0, END)
    
def dosya_gonder():
    açık_web = filedialog.askopenfilename()
    client.send(açık_web.encode('utf8'))

    with open(açık_web, 'wp') as file:
        for data in file:
            client.send(data)
    print(f"{açık_web} dosyası başarıyla gönderildi.")
    
btn_metin_gonder = Button(ekran, text="Gönder", width=30, command=mesaj_gonder)
btn_metin_gonder.grid(row=2, column=0, pady=10,padx=10)


btn_dosya_gonder = Button(ekran, text="Dosya Gönder", width=30, command=dosya_gonder)
btn_dosya_gonder.grid(row=3, column=0, pady=10, padx=10)
    
def gelen_msaj_kontrol():
    while True:
        server_msg = client.recv(1024).decode('utf8')
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        message.insert(END, '\n'+ server_msg+' Tarih: '+ timestamp)
        
        
ekran.bind('<Return>', lambda event=None: btn_metin_gonder.invoke())
recv_kontrol = Thread(target=gelen_msaj_kontrol)
recv_kontrol.daemon = True
recv_kontrol.start()

ekran.mainloop()
