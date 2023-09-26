#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
from datetime import datetime

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)
str_list = []
def makepayload(data):
    tamanho = 50

    if len(data) < tamanho:
        payload = data[:]
        data = []
    else:
        payload = data[0:tamanho]
        data = data[tamanho:]

    return data, payload

def makehead(field0, field1, field2, field3, field4, field5, field6, field7, field8, field9):
    header = bytearray([field0,field1, field2, field3, field4, field5, field6, field7, field8, field9])
    return header


def datagram(head,payload: bytes):
    EOP = b'\xAA\xBB\xCC\xDD'
    return head + payload + EOP

def main():
    try:
        print("Iniciou o main")
        imageR= "p3/imgs/img.png"
        com1 = enlace(serialName)
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print("Abriu a comunicação")
        print("Esperando byte sacrificio")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(1)
        print("Byte sacrificado")
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        
        ocioso = True
        server_id = 12

        while ocioso:
            rxBuffer, nrx = com1.getData(9)
            EOP = com1.getData(com1.rx.getBufferLen())[0][-4:]
            now = datetime.now()
            buffer_len = com1.rx.getBufferLen()
            string = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second} /receb/type: {head[0]}Size: {buffer_len}\n"
            str_list.append(string)
            if int.from_bytes(rxBuffer[0]) == 1 and int.from_bytes(rxBuffer[1]) == server_id:
                ocioso = False
                time.sleep(1)
            else:
                time.sleep(1)

        #ocioso == False
        now = datetime.now()
        tx_head = makehead(2,0,0,0,0,0,0,0,0,0)
        txBuffer = datagram(tx_head, None)
        com1.sendData(txBuffer)
        tx_len = com1.tx.getBufferLen()
        string = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second} /envio/type: {tx_head[0]}/MessageSize: {tx_len}\n"
        str_list.append(string)

        counter = 1
        rxBuffer, nrx = com1.getData(14)
        numPckg = rxBuffer[3]
        com1.rx.clearBuffer()
        EOP =  b'\xaa\xbb\xcc\xdd'

        while counter <= numPckg:
            timer1 = time.time()
            timer2 = time.time()
            buffer_len = com1.rx.getBufferLen() 
            if buffer_len >= 9:
                message = com1.getData(buffer_len)[0]
                head = message[0:9]
                m_type = message[0]
                now = datetime.now()
                string = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second} /receb/type: {head[0]}/Size: {buffer_len}/Packet number: {head[4]}/Total of packages {head[3]}/PayloadCRC: \n"
                str_list.append(string)
                if m_type == 3:
                    if head[4] == counter and (len(message)-14) == head[5] and head[-4:] == EOP and (counter-1) == head[7] :
                        tx_head = makehead(4,0,0,0,0,0,0,counter-1,0,0)
                        datagram = datagram(tx_head, None)
                        com1.sendData(datagram)
                        counter+=1
                    else:
                        tx_head = makehead(6,0,0,0,0,0,counter,0,0,0)
                        datagram = datagram(tx_head, None)
                        com1.sendData(datagram)
                
                    now = datetime.now()
                    tx_len = len(datagram)
                    string = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second} /receb/type: {tx_head[0]}/Size: {tx_len}"
                    str_list.append(string)
                    
                else:
                    time.sleep(1)
                    if timer2> 20:
                        ocioso = True
                        tx_head = makehead(5,0,0,0,0,0,0,0,0,0)
                        datagram = datagram(tx_head, None)
                        com1.sendData(datagram)
                        com1.disable()

                    else:
                        if timer1> 2:
                            tx_head = makehead(4,0,0,0,0,0,0,counter,0,0)
                            datagram = datagram(tx_head, None)
                            com1.sendData(datagram)
                            timer1 = time.time()

                    now = datetime.now()
                    tx_len = len(datagram)
                    string = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second} /receb/type: {tx_head[0]}/Size: {tx_len}"
                    str_list.append(string)
                
                

        print(str_list)


    
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
    


    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com1.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
