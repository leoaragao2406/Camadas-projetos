#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

import crcmod
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

# Escolha um polinômio CRC (por exemplo, CRC-16)

def crc_from_payload(payload: bytes):
    crc16 = crcmod.mkCrcFun(0x11021, initCrc=0x0000, xorOut=0x0000)
    crc_value = crc16(payload)
    return crc_value.to_bytes(2, byteorder='big')


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


def datagrama_make(head,payload: bytes):
    EOP = b'\xAA\xBB\xCC\xDD'
    return head + payload + EOP

def main():

    print("Iniciou o main")
    imageR= "p4/imgs/img.png"
    log1= "p4/logs/Serv1.txt"
    log2 = "p4/logs/Serv2.txt"
    log3 = "p4/logs/Serv3.txt"
    log4 = "p4/logs/Serv4.txt"
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
        head = com1.getData(10)[0]
        
        now = datetime.now()
        buffer_len = com1.rx.getBufferLen()
        string = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second} /receb/ type: {head[0]}/ Size: {buffer_len} \n"
        str_list.append(string)
        pack_type = head[0]
        s_id = head[1]
        
        if pack_type== 1 and s_id == server_id:
            ocioso = False
            time.sleep(1)
        else:
            time.sleep(1)

    
    now = datetime.now()
    tx_head = makehead(2,0,0,0,0,0,0,0,0,0)
    txBuffer = datagrama_make(tx_head, b'')
    com1.sendData(txBuffer)
    tx_len = com1.tx.getBufferLen()
    string = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second} /envio/ type: {tx_head[0]}/ Size: {tx_len} \n"
    str_list.append(string)

    counter = 1
    numPckg = head[3]
    EOP =  b'\xaa\xbb\xcc\xdd'
    timer1_env = time.time()
    timer2_env = time.time()
    com1.rx.clearBuffer()
    payload = bytearray()

    while counter <= numPckg:
        time.sleep(1)
        tempo=time.time()
        if com1.rx.getBufferLen() >= 10:
            timer1_env = time.time()
            timer2_env = time.time()
            message, nrx = com1.getData(com1.rx.getBufferLen())
            head = message[0:10]
            m_type = head[0]
            now = datetime.now()
            print("full message", [n for n in message])

            __payload = message[10:-4]
            crc_calculado = crc_from_payload(__payload)
            
            if m_type == 3 and head[-2:] == crc_calculado:
                string = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second} /receb/ type: {head[0]}/ Size: {len(message)}/ pacote recebido: {head[4]}/ total de pacotes {head[3]} CRC: {head[-2:]} \n"
                str_list.append(string) 
                print("CRC IGUAL", [n for n in crc_calculado], [n for n in head[-2:]])
                if head[4] == counter and (len(message)-14) == head[5] and message[-4:] == EOP:
                    payload += message[10:-4]
                    tx_head = makehead(4,0,0,0,0,0,0,counter,0,0)
                    datagram = datagrama_make(tx_head, b'')
                    com1.sendData(datagram)
                    counter+=1
                else:
                    tx_head = makehead(6,0,0,0,0,0,counter,0,0,0)
                    datagram = datagrama_make(tx_head, b'')
                    com1.sendData(datagram)
            
                now = datetime.now()
                tx_len = len(datagram)
                string = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second} /envio/ type: {tx_head[0]}/ Size: {tx_len} \n"
                str_list.append(string)
            
            

            elif m_type == 3 and crc_calculado != head[-2:]:
                print("CRC DIFERENTE", [n for n in crc_calculado], [n for n in head[-2:]])
                print("-------------------------")
                print("Comunicação encerrada")
                print("-------------------------")
                com1.disable()
                exit()

            else:
                string = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second} /receb/ type: {head[0]}/ Size: {com1.rx.getBufferLen()} \n"
                str_list.append(string) 


        else:
            if time.time()-timer2_env> 20:
                    print("TIMER DE 20") 
                    tx_head = makehead(5,0,0,0,0,0,0,0,0,0)
                    datagram = datagrama_make(tx_head, b'')
                    com1.sendData(datagram)
                    now = datetime.now()
                    tx_len = len(datagram)
                    string = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second} /envio /type: {tx_head[0]}/ Size: {tx_len} \n"
                    str_list.append(string)
                    break
            
            elif time.time()-timer1_env> 2:
                    print("TIMER 2")
                    tx_head = makehead(4,0,0,0,0,0,0,counter,0,0)
                    datagram = datagrama_make(tx_head, b'')
                    com1.sendData(datagram)
                    timer1_env = time.time()

                    now = datetime.now()
                    tx_len = len(datagram)
                    string = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second} /envio /type: {tx_head[0]}/ Size: {tx_len} \n"
                    str_list.append(string)



                
                
    f = open(log4, 'w')     
    for str in str_list:
        f.write(str)
    f.close()
        

    f = open(imageR,'wb')
    f.write(payload)
    f.close()
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com1.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
