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
import random
import datetime
import crcmod
import struct



# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta
def makepayload(data):
    tamanho = 114

    if len(data) < tamanho:
        payload = data[:]
        data = []
    else:
        payload = data[0:tamanho]
        data = data[tamanho:]

    return data, payload


def crc_from_payload(payload: bytes):
    crc16 = crcmod.mkCrcFun(0x11021, initCrc=0x0000, xorOut=0x0000)
    crc_value = crc16(payload)
    return crc_value.to_bytes(2, byteorder='big')

def makehead(field1, field2, field3, field4, field5, field6, field7, field8,field9,field10):
    header = bytearray([field1, field2, field3, field4, field5, field6, field7, field8,field9,field10])
    header= int.to_bytes(field1,1,byteorder='big') +int.to_bytes(field2,1,byteorder='big')+int.to_bytes(field3,1,byteorder='big')+int.to_bytes(field4,1,byteorder='big')+int.to_bytes(field5,1,byteorder='big')+int.to_bytes(field6,1,byteorder='big')+int.to_bytes(field7,1,byteorder='big')+int.to_bytes(field8,1,byteorder='big')+int.to_bytes(field9,1,byteorder='big')+int.to_bytes(field10,1,byteorder='big')
    return header 


def datagram(head,payload: bytes):
    EOP = b'\xAA\xBB\xCC\xDD'
    return head + payload + EOP

def escreve(status, tp_msg, tamanhototal, IDpacote=0, total_pacotes=0, crc_payload=0):
    tmp = datetime.datetime.now()
    file_name = 'p4/Client/textos/Client5.txt'
    
    with open(file_name, 'a') as file:  # Open the file in append mode ('a')
        if status:
            if tp_msg == 3:
                file.write(f'{tmp}/envio/{tp_msg}/{tamanhototal}/{IDpacote}/{total_pacotes}/{crc_payload}\n')
            else:
                file.write(f'{tmp}/envio/{tp_msg}/{tamanhototal}\n')
        else:
            file.write(f'{tmp}/receb/{tp_msg}/{tamanhototal}\n')
    
    return None

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)



def main():

    print("Iniciou o main")
    #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
    #para declarar esse objeto é o nome da porta.
    com1 = enlace(serialName)
    

    # Ativa comunicacao. Inicia os threads e a comunicação seiral e byte de sacrificio
    com1.enable()
    print("Abriu a comunicação")
    time.sleep(2)
    com1.sendData(b'00')
    print("bit de sacrificio enviado")
    escreve(True,0,0)
    time.sleep(0.5)

    inicio=False
    num_servidor=12

    imageR= "p4\Client\imgs\imagem.jpg"
    img= open(imageR, 'rb').read()
    envio=np.asarray(bytearray(img))

    while inicio==False:
        
        img_size=len(envio)
        print('tamanho do envio---------',img_size)

        num_pacotes=img_size//114
        if img_size % 114 != 0:
            num_pacotes+= 1
        else:
            num_pacotes=num_pacotes

        head=makehead(1,num_servidor,0,num_pacotes,0,1,0,0,0,0)
        datagrama1=datagram(head,b'')
        com1.sendData(datagrama1)
        escreve(True,1,len(datagrama1))
        print("Datagrama do tipo 1 enviado")
        time.sleep(5)

        if com1.rx.getBufferLen() == 0:
            inicio=False
        else:
            rxBuffer,nRx = com1.getData(14)
            
            if rxBuffer[0]==2:
                inicio=True
                print('datagrama do tipo2 recebido')
                escreve(False,rxBuffer[0],14)
            else:
                inicio=False

    cont=1
    desligar=False
    reenvio=False
    erroforc=True
    print('numero de pacotes-----------',num_pacotes)
    while cont <= num_pacotes:
        if desligar == True:
            cont=num_pacotes+1
            com1.disable
            break
        if reenvio ==False:
            envio , payload = makepayload(envio)
            print("payload formado")
        else:
            payload=payload

        if cont==4 and erroforc== True:
            cont=5
            erroforc=False


        crc=crc_from_payload(bytes(payload))
        head= makehead(3,0,0,num_pacotes,cont,len(payload),0,0,0,0)
        print('head+crc----------',head+crc)
        head=head[0:8]
        


        txBuffer= datagram(head+crc,bytes(payload))
        print('tamanho do datagrama',len(txBuffer))
        com1.rx.clearBuffer()
        com1.sendData(txBuffer)


        print(f'datagrama {cont} enviado')
        escreve(True,3,len(txBuffer),cont,num_pacotes,crc)
        tempo_envio1=time.time()
        tempo_envio2=time.time()

        timer1=5
        timer2=20
        
        cyclo=True
        while cyclo==True:
            tempo_atual1=time.time()
            tempo_atual2=time.time()

            if tempo_atual1 - tempo_envio1 >=timer1:
                com1.sendData(txBuffer)
                escreve(True,3,len(txBuffer),cont,num_pacotes,crc)
                tempo_envio1 = tempo_atual1
                print('tempo passou de 5 seg, datagrama reenviado')

            if tempo_atual2 - tempo_envio2 >=timer2:
                head=makehead(5,0,0,0,0,0,0,0,0,0)
                txBuffer= datagram(head,b'')
                com1.sendData(txBuffer)
                escreve(True,5,len(txBuffer))
                print('tempo passou de 20 seg, comunicação encerrada')
                desligar=True
                com1.disable()
                break


            if com1.rx.getBufferLen() != 0:
                rxBuffer,nRx = com1.getData(14)
                escreve(False,rxBuffer[0],14)

                if rxBuffer[0] ==6:
                    print('datagrama do tipo 6 recebido')
                    cont = rxBuffer[6]
                    cyclo=False
                    reenvio=True
                    
                if rxBuffer[0] ==4:
                    reenvio=False
                    print('datagrama do tipo 4 recebido')
                    cont = rxBuffer[7] + 1
                    cyclo=False

                if rxBuffer[0] ==5:
                    print('tempo passou de 20 seg, comunicação encerrada')
                    desligar=True
                    com1.disable()
                    break

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com1.disable()







        
       
        
        
               
        
        
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        
        


        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.

        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        ## txLen = len(txBuffer)
        ##rxBuffer, nRx = com1.getData(txLen)
        ##print("recebeu {} bytes" .format(len(rxBuffer)))
        
        #for i in range(len(rxBuffer)):
            #print("recebeu {}" .format(rxBuffer[i]))

        ##f = open(imageW,'wb')
        ##f.write(rxBuffer)
        ##f.close()
        

            
    
       
        

        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
