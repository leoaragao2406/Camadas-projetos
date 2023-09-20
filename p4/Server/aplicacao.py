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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


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
        
        rxBuffer, nRx = com1.getData(1)
        print('rxBuffer ======>', rxBuffer)
        if rxBuffer == b'0':
            com1.sendData(b'00')
            com1.rx.clearBuffer()
            time.sleep(1)
            print("Handshake")

        last_id = 0
        running = True
        eop_size = 3
        payload = bytearray()
        total = 1
        erro = 0

        while running:
            rxBuffer, nRx = com1.getData(12)
            pack_id = int.from_bytes(rxBuffer[0:4], byteorder ='big')
            total_packs = int.from_bytes(rxBuffer[4:8], byteorder= 'big')
            payload_size = int.from_bytes(rxBuffer[8:12], byteorder= 'big')


            print("ID ====>", pack_id, "LAST ====>", last_id)
            print("Total:", total_packs)
            print("Payload size:",payload_size)

            rxBuffer, nrx = com1.getData(payload_size+eop_size)
            print("rxBuffer =====>", rxBuffer,"\n")
            rec_payload = rxBuffer[:payload_size]
            rec_eop = rxBuffer[payload_size:]


            ver = True
            
            if len(rxBuffer)-3 != (payload_size):
                print("ERRO: TAMANHO PAYLOAD diferente do esperado")
                ver = False
                erro+=1
                com1.disable()


            if pack_id != (last_id + 1):
                print("ERRO: ID diferente do esperado")
                ver = False
                erro+=1
                com1.disable()
            else:
                last_id +=1


            if rec_eop != b'\xff\xff\xff':
                print("ERRO: TAMANHO PAYLOAD diferente do esperado")
                ver = False
                com1.disable()

            if ver == True:
                payload += rec_payload
                if total_packs == total:
                    print("Todos os Pacotes foram Recebidos")
                    print(payload)
                    print(type(payload))

            

            txBuffer = pack_id.to_bytes(12, 'big') + b'00' + rec_eop
            com1.sendData(txBuffer)

            total +=1

            if len(rec_payload) < 50:
                running = False

    
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
    

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
