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

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

comando1 = bytes([0x04, 0X00, 0X00, 0X00, 0X00]) 
comando2 = bytes([0x04, 0X00, 0X00, 0XBB, 0X00])
comando3 = bytes([0x03, 0XBB, 0X00, 0X00]) 
comando4 = bytes([0x03, 0X00, 0XBB, 0X00]) 
comando5 = bytes([0x03, 0X00, 0X00, 0XBB]) 
comando6 = bytes([0x02, 0X00, 0XAA])
comando7 = bytes([0x02, 0XBB, 0X00]) 
comando8 = bytes([0x01, 0X00])
comando9 = bytes([0x01, 0XBB])

lista=[comando1,comando2,comando3,comando4,comando5,comando6,comando7,comando8,comando9]

x=random.randint(10,30)
print(x)

def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral e byte de sacrificio
        com1.enable()
        time.sleep(2)
        com1.sendData(b'00')
        time.sleep(1)

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        


        
        #txBuffer = imagem em bytes!
        i=1
        print("transmissão vai começar")
        while i < x:
            n_comando = random.randint(0,8)
            comando = lista[n_comando]

            print("Meu comando tem {0} bytes".format(len(comando)))

            com1.sendData(np.asarray(comando))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            time.sleep(0.5)
            txSize = com1.tx.getStatus()
            i+=1

        #bit final
        print("envio do ultimo bit")
        txBuffer = bytes([0x01, 0xFF])
        com1.sendData(np.asarray(txBuffer))
        time.sleep(1)
        print("bit final enviado")
        time.sleep(5)


        if com1.rx.getBufferLen() == 0:
            print('Time Out')
            print("Comunicação encerrada")
            print("-------------------------")
            com1.disable()

        rxBuffer, nRx = com1.getData(2)

        if (i) != int.from_bytes(rxBuffer, "little"):
            print('numero de comandos errado!')
            exit()  
            
        else:
            print('SUCESSO,recebi o numero certo de comandos!')
            print(int.from_bytes(rxBuffer, "little"))

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
        

            
    
       
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
