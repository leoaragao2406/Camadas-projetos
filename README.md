# Camadas-projetos
"""
pacote = head + payload + eop
overhead = tamanho_total / payload = (head + payload + eop) / payload

OverHead: len (datagrama) /len (payload)
throughput: taxa de envio e download
baudrate: quantos bits sao transmitidos em 1 segundo

udp: simples (arremesso do bebê)
tcp: handshake e via de mão dupla

CRC: escolher um numero binario para o polinomio do CRC;
ex: 10011 --> ×^4+×+1 ;
como o polinomio acima é de 4 grau, pegue seus dados e adicione 4 zeros no final;
faz uma divisao entre os dados com 4 zeros a mais e o polinomio do CRC, substituindo as subtrações da divisão por um XOR com o polinomio CRC quando o bit mais alto for 1 :
Se o bit mais alto for 0, fazer xor com 00000;
Ao final dessa operação, o resto da divisao é o CRC adiciona esse CRC no final dos dados para que o server recalcule essa divisão com os dados + CRC no final. Se o resultado for 0, não houve erro na transmissão

"""
