
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def obter_frequencias(numero):
    # Dicionário DTMF com listas
    dtmf_dict = {
        "1":(697, 1209),
        "2":(697, 1336),
        "3":(697, 1477),
        "A":(697, 1633),
        "4":(770, 1209),
        "5":(770, 1336),
        "6":(770, 1477),
        "B":(770, 1633),
        "7":(852, 1209),
        "8":(852, 1336),
        "9":(852, 1477),
        "C":(852, 1633),
        "X":(941, 1209),
        "0":(941, 1336),
        "#":(941, 1477),
        "D":(941, 1633),
    }

    # Verifica se o número está no dicionário
    if numero in dtmf_dict:
        return dtmf_dict[numero]
    else:
        return None 
    
def gerar_senoides(frequencias, duracao, taxa_amostragem):
    tempo = np.arange(0, duracao, 1/taxa_amostragem)

    # Gera as duas senoides
    sinal1 = 1*np.sin(2 * np.pi * frequencias[0] * tempo)
    sinal2 = 1*np.sin(2 * np.pi * frequencias[1] * tempo)

    # Soma as senoides para obter o sinal final
    sinal_final = sinal1 + sinal2

    return tempo, sinal_final



def main():
    print("Inicializando encoder")
    print("Aguardando usuário")
    signal = signalMeu()
    fs=44100
    NUM= input("escolha um numero de 0 a 9: ")
    f = obter_frequencias(NUM)
    print("frequencias relacionadas a tecla escolhida:",f)

    tempo,sinal_final = gerar_senoides(f,5,fs)
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    sd.play(sinal_final, fs)
    
    # Exibe gráficos
    t=np.linspace(0, len(sinal_final),400)
    plt.plot(t, sinal_final[0:400])
    plt.title('Sinal DTMF para a tecla pressionada')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')

    signal.plotFFT(sinal_final, fs)

    plt.tight_layout()  # Garante que os subplots não se sobreponham
    plt.show()
    # aguarda fim do audio
    
    sd.wait()
    
    

if __name__ == "__main__":
    main()
