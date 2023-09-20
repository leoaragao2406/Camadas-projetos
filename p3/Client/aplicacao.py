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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta
def makepayload(data):
    tamanho = 50

    if len(data) < tamanho:
        payload = data[:]
        data = []
    else:
        payload = data[0:tamanho]
        data = data[tamanho:]

    return data, payload


def datagram(packet: int, total_number_of_packets: int, payload: bytes):
    payload_size = len(payload)
    head = packet.to_bytes(4, 'big') + total_number_of_packets.to_bytes(4, 'big') + payload_size.to_bytes(4, 'big')
    EOP = b'\xff\xff\xff'
    
    
    return head + payload + EOP

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
    time.sleep(2)
    com1.sendData(b'00')
    print('enviou handshake' )
    time.sleep(5)
    cyclo=True
    m=0
    while cyclo==True:
        if m==2:
            com1.sendData(b'00')
            print("bit de sacrificio enviado")
            time.sleep(2)
            com1.sendData(b'00')
            print('enviou handshake' )
            cyclo=False

        if com1.rx.getBufferLen() == 0:
            resposta = input("Servidor inativo. Tentar novamente? S/N: ").strip().upper()

            if resposta == 'S':
                com1.sendData(b'00')
                time.sleep(5)
                m+=1
                
            elif resposta == 'N':
                print("Comunicação encerrada")
                print("-------------------------")
                com1.disable()
                break
            else:
                print("Resposta inválida. Por favor, digite 'S' para Sim ou 'N' para Não.")
        else:
            rxBuffer,nRx = com1.getData(1)
            if rxBuffer== b'0':
                print('handshake finalizado')
                cyclo= False
            else:
                print("não recebi o que foi combinado")
                break
            


    #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
    print('inicio do envio do datagrama')

    imageR= "p3\Client\imgs\img.png"

    img= open(imageR, 'rb').read()
    envio=np.asarray(bytearray(img))

    img_size=len(envio)
    print("tamanho do envio")
    print(img_size)

    num_pacotes=img_size//50
    
    
    if img_size % 50 != 0:
        num_pacotes+= 1
    else:
        num_pacotes=num_pacotes
    print("num pacotes")
    print(num_pacotes)
    i=0

    while i < num_pacotes:
        envio,payload = makepayload(envio)
        print("payload formado")

        txBuffer=datagram(i+1,int(num_pacotes),bytes(payload))
        print("datagrama formado")
        com1.rx.clearBuffer()
        com1.sendData(txBuffer)

        print(f'pacote de numero {i+1} enviado')
        time.sleep(1)

        rxBuffer, nRx = com1.getData(16)
        msg_received=rxBuffer[12]
        if msg_received == b'0':
                print('pacote recebido pelo servidor')
        

        if len(payload)==0:
            break
            
        i+=1

    # Encerra comunicação
    print("envio completado")
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
