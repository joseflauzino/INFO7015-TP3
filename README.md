## Pré-requisitos
- Ubuntu 16.04 LTS (pode funcionar em outras versões, mas não foi testado)
- Python
- Mininet
- Controlador POX (pode ser instalado junto ao Mininet se for passado o parâmetro -a)
- Click Modular Router (modo user-level)
- Biblioteca python Matplotlib
- Git

## Obtendo os códigos
Abra o terminal (recomendávelmente certifique-se de estar em seu diretório home)
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
Copie os arquivos `flow_rules1.json` e `flow_rules1.json` para o diretório pox
Normalmente ele está em `/home/<seu_usuario>/pox`
Copie também o arquivo `router.py` para o diretório `/home/<seu_usuario>/pox/pox/forwarding`
Entre no diretório do POX e digite.
`./pox.py forwarding.router`

O controlador será executado, e instalará as regras do arquivo `flow_rules1.json` no switch 1.
Sua rede deverá estar funcionando no momento.

## Executando os Experimentos

## Gerando gráfico
Entre no diretório generate_result e execute:
`./run`

Ao término do processamento o resultado estara no arquivo fig3.png.
