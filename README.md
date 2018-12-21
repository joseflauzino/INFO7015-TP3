## Pré-requisitos
- Ubuntu 16.04 LTS (pode funcionar em outras versões, mas não foi testado)
- Python
- Mininet
- Controlador POX (pode ser instalado junto ao Mininet se for passado o parâmetro -a)
- Click Modular Router (modo user-level)
- Biblioteca python Matplotlib
- Git

## Obtendo os códigos
Abra o terminal (recomendávelmente certifique-se de estar em seu diretório home).
Digite
`git clone https://github.com/joseflauzino/INFO7015-TP3.git`

## Antes de Iniciar
É recomendável executar todos os comandos a seguir como super usuário (root)

## Inicializando a Rede
### Executando a topologia do Mininet
Entre no diretório INFO7015-TP3 e digite
`./run`

Se tudo ocorreu bem a rede foi criada e a CLI do Mininet está em execução.

### Executando o controlador POX
Abra outro terminal e entre no diretório INFO7015-TP3.
Copie os arquivos `flow_rules1.json` e `flow_rules1.json` para o diretório pox.
Normalmente ele está em `/home/<seu_usuario>/pox`.
Copie também o arquivo `router.py` para o diretório `/home/<seu_usuario>/pox/pox/forwarding`.
Entre no diretório do POX e digite.
`./pox.py forwarding.router`

O controlador será executado, e instalará as regras do arquivo `flow_rules1.json` no switch 1.
Sua rede deverá estar funcionando no momento.

## Executando os Experimentos
### Observações Importantes
Apesar da maior parte do passos serem feitos por scripts, alguns precisam ser executados manualmente.
Os passos no tópico a seguir são genéricos e devem ser executados para cada cenário.
Os arquivos das capturas de ppacotes devem ser nomeados de acordo com o experimento, pois essa ordem é importante ao gerar a figura.
Eles devem ser nomeados da seguinte forma:

Nome do Arquivo | Nome do Cenário    |
----------------|--------------------|
cap1.txt        | Com VNF (Chrome)   |
cap2.txt        | Sem VNF (Chrome)   |
cap3.txt        | Com VNF (Firefox)  |
cap4.txt        | Sem VNF (Firefox)  |

A ordem de execução é independente, desde que os arquivos sejam nomeados de acordo com a informação acima.
### Configurando o arquivo hosts
Na CLI do Mininet digite `xterm h1` para abrir um terminal do h1.
No terminal do h1 execute `nano /etc/hosts`.
Insira uma linha com o conteúdo `192.168.2.1    info7015.com` (observe que tem um TAB entre as palavras).

### Capturando os pacotes
Na CLI do Mininet digite `xterm h1` para abrir outro terminal do h1.
Nesse terminal do h1 execute `tpcdump -i h1-eth0 port 80 > generate_result/<nome_do_arquivo>` para iniciar a captura de pacotes (não se escreça de inserir corretamente o nome do arquivo de captura atual).

### Abrindo o navegador e acessando a página
Na CLI do Mininet digite `xterm h1` para abrir outro terminal do h1.
Nesse terminal execute `firefox` ou `google-chrome --no-sandbox` dependendo do navegador a ser testado no momento.
No navegador digite `http://info7015.com` e aguarde a página ser carregada por completo.

### Encerrando o experimento
Feche o navegador do h1.
No terminal do h1 executando o tcpdump digite Ctrl+C para encerrar a captura.
Encerre o Mininet com o comando `exit`
Finalize o POX com Ctrl+C.

### Conferindo os arquivos de saída
Entre no diretório `generate_result`e virifique se os arquivos: cap1.txt, cap2.txt, cap3.txt e cap4.txt estão lá dentro.
Caso algum ainda falte, execute o experimento do mesmo.

## Gerando gráfico
Entre no diretório generate_result e execute:
`./run`

Ao término do processamento o resultado estará no arquivo fig3.png.
