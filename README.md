# Análise de dados para mapeamento e erradicação de doenças entre animais de rua 

## Setor de Aplicação 
O projeto visa auxiliar ONGs e prefeituras no mapeamento de animais em situação de rua, 
doentes ou em situações de mal tratos, permitindo a tais entidades encontrar e tratar suas 
doenças, realizar castrações e encontrar lares afetuosos para aqueles animais vulneráveis 
ao meio em que vivem.  

## Objetivos 
O objetivo principal é mapear de forma gráfica, com base em latitude e longitude, locais 
onde encontram-se animais em situações de vulnerabilidade, sejam em situações de rua 
ou de mal tratos em lares pouco afetuosos.  
Para alcançar tal objetivo, é necessário criar uma aplicação com acesso via navegador, em 
nuvem, para que usuários anônimos possam informar, comentar e registrar locais, espécies 
e situações que demandam cuidados veterinários ou sociais.  




## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

Consulte **[Implantação](#-implanta%C3%A7%C3%A3o)** para saber como implantar o projeto.

### 📋 Pré-requisitos

O projeto foi desenvolvido em Python, tanto para back-and quanto para front-end, usando as bibliotecas Dash e Plotly para geração dos gráficos, mapas e KPIs, Pandas para tratamento de dados, Numpy para operações matemáticas e CSS e HTML para implementação de algumas partes visuais.

O banco de dados foi desenvolvido em MySQL e integrado à aplicação através da biblioteca Sqlalchemy.

Para dar seguimento ao projeto, é necessário ter os seguintes serviços ou aplicações instaladas na máquina Servidor:

SQL Server;
MySQL Workbench 8.0 ou outro SGBD (sistema gerenciador de banco de dados) de sua preferência. 
VS Code ou outro de sua preferência. 	
Python 3.11.9 (pode precisar de ajustes no código se for usada outra versão do Python)


### 🔧 Instalação

O primeiro passo é catalogar os bairros da cidade e coletar suas informações de latitude e longitude.
Depois, implementar um banco de dados e criar as tabelas e seus relacionamentos.

Neste projeto, nomeei o banco de dados como harpia_animais, mas o nome pode ser qualquer um de sua preferência (lembre-se de ajustar no código)

Criar tabela bairro:
```
CREATE TABLE `bairro` (
  `idbairro` int(11) NOT NULL AUTO_INCREMENT,
  `nomebairro` varchar(45) NOT NULL,
  `latitude` varchar(45) NOT NULL,
  `longitude` varchar(45) NOT NULL,
  PRIMARY KEY (`idbairro`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1
```

Criar tabela cidade:
```
CREATE TABLE `cidade` (
  `idcidade` int(11) NOT NULL AUTO_INCREMENT,
  `nomecidade` varchar(45) NOT NULL,
  PRIMARY KEY (`idcidade`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1
```

Criar tabela grupoanimal:
```
CREATE TABLE `grupoanimal` (
  `idgrupoanimal` int(11) NOT NULL AUTO_INCREMENT,
  `nomegrupoanimal` varchar(45) NOT NULL,
  PRIMARY KEY (`idgrupoanimal`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1
```

Criar tabela gruposituacao:
```
CREATE TABLE `gruposituacao` (
  `idgruposituacao` int(11) NOT NULL AUTO_INCREMENT,
  `nomegruposituacao` varchar(45) NOT NULL,
  PRIMARY KEY (`idgruposituacao`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1
```

Criar tabela racaanimal:
```
CREATE TABLE `racaanimal` (
  `idracaanimal` int(11) NOT NULL AUTO_INCREMENT,
  `nomeracaanimal` varchar(45) NOT NULL,
  `idgrupoanimal` int(11) NOT NULL,
  PRIMARY KEY (`idracaanimal`),
  KEY `idgrupoanimal_idx` (`idgrupoanimal`),
  CONSTRAINT `idgrupoanimal` FOREIGN KEY (`idgrupoanimal`) REFERENCES `grupoanimal` (`idgrupoanimal`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1
```

Criar tabela situacaoanimal:
```
CREATE TABLE `situacaoanimal` (
  `idsituacaoanimal` int(11) NOT NULL AUTO_INCREMENT,
  `nomesituacaoanimal` varchar(45) NOT NULL,
  `idgruposituacao` int(11) NOT NULL,
  PRIMARY KEY (`idsituacaoanimal`),
  KEY `idgruposituacao_idx` (`idgruposituacao`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1
```

Criar tabela ocorrencia:
```
CREATE TABLE `ocorrencia` (
  `idocorrencia` int(11) NOT NULL AUTO_INCREMENT,
  `idracaanimal` int(11) NOT NULL,
  `idsituacaoanimal` int(11) NOT NULL,
  `dataocorrencia` date NOT NULL,
  `dataresolucao` date DEFAULT NULL,
  `situacao` int(11) NOT NULL DEFAULT '0',
  `idcidade` int(11) NOT NULL DEFAULT '1',
  `idbairro` int(11) NOT NULL,
  `nomerua` varchar(45) NOT NULL,
  `observacao` longtext,
  `idgrupoanimal` int(11) NOT NULL,
  PRIMARY KEY (`idocorrencia`),
  KEY `idracaanimal_idx` (`idracaanimal`),
  KEY `idsituacao_idx` (`idsituacaoanimal`),
  KEY `idcidade_idx` (`idcidade`),
  KEY `idbairro_idx` (`idbairro`),
  KEY `idgrupoanimal_idx` (`idgrupoanimal`),
  CONSTRAINT `idbairro` FOREIGN KEY (`idbairro`) REFERENCES `bairro` (`idbairro`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idcidade` FOREIGN KEY (`idcidade`) REFERENCES `cidade` (`idcidade`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idracaanimal` FOREIGN KEY (`idracaanimal`) REFERENCES `racaanimal` (`idracaanimal`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idsituacaoanimal` FOREIGN KEY (`idsituacaoanimal`) REFERENCES `situacaoanimal` (`idsituacaoanimal`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1
```
## Configuração do Python

Após a criação do banco de dados, precisamos intalar as bibliotecas do Python. 
Você pode ou não criar um ambiente virtual, não traterei o assunto aqui. 

Abra um terminal e instale as bibliotecas abaixo:
```
pip install pandas
pip install numpy
pip install dash
pip install plotly
pip install plotly.express
pip install plotly.graph_objects
pip install dash_bootstrap_components
pip install dash_bootstrap_templates
pip install sqlalchemy
pip install locale
pip install datetime
```

## 📦 Implantação

Uma vez que o banco de dados e as bibliotecas Python estejam instaladas, é necessário criar um diretório raiz e adicionar os itens conforme esquema abaixo:

Raiz do projeto:
```
Pasta assets
Pasta Pages
Arquivo Python com nome  "index.py"
Arquivo Readme
```
Pasta assets:
```
Arquivo de imagem em formato PNG com nome "logo.png"
Arquivo CSS com nome "style.css"
```
Pasta Pages:
```
Arquivo Python com nome "dados.py" 
Arquivo Python com nome "dashboard.py" 
Arquivo Python com nome "ocorrencias.py" 
```
Para executar o aplicativo, basta executar o arquivo "index.py" via terminal. 

Nas linhas de código abaixo, é possível definir no host, se o app poderá ser acesso por todos os terminais da rede (host='0.0.0.0'), ou apenas pelo servidor (host='127.0.0.1').
Se o parâmetro debug for = True, a aplicação web mostrará em tempo real se existem falhas conforme os códigos são salvos. Se estiver como False, esse debug não acontecerá. 

if __name__=='__main__':
    app.run_server(host='0.0.0.0', port=8052, debug=True)    

## ✒️ Autores


* **Lucas Rosa Pinto** - [desenvolvedor](https://github.com/BenKefa)
* **Abraão Rogério da Costa Farias** - [desenvolvedor]

## 📄 Licença

Este projeto é livre para melhorias e seu uso, desde que acadêmico.
