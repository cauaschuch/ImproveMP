
.. figure:: https://github.com/user-attachments/assets/0f7c4b08-f9e2-4172-b355-cf4b955c2d5a

|en|

Conheça a documentação do ImproveMP! MUDOU
=========

ImproveMP é uma biblioteca pensada para auxiliar pesquisadores na
criação de inputs para o software Quantum ESPRESSO, com base no banco de
dados ofertado pelo Materials Project (MP).

Introdução
----------

O programa ImproveMP tem como objetivo facilitar o uso do software
Quantum ESPRESSO, automatizando a transferência de dados como os
parâmetros de rede de diversos materiais do banco de dados Materials
Project (MP) utilizando interfaces de programação de aplicações (APIs).

Instruções
----------

Para instalar a biblioteca, execute o comando abaixo:

.. code:: bash

   pip install ImproveMP

Como usar o programa
~~~~~~~~~~~~~~~~~~~~

**1° Passo:**

Instale a biblioteca

**2° Passo:**

Faça login em sua conta no Materials Project
(https://next-gen.materialsproject.org/api#api-key), clique em APIs no
menu superior e obtenha a sua chave (API Key). É recomendado salvar a
sua chave em algum local de fácil acesso.

**3° Passo:**

Em um novo arquivo, importe a biblioteca:

.. code:: python

   from ImproveMP import Improve_MP

Insira sua chave no comando:

.. code:: python

   Improve_MP.minha_chave(“”)

**Diferentes funcionalidades**

-  Para buscar vários compostos baseado em sua composição, utilize um -
   entre os elementos, no formato “A-B-C-…”:
   ``python     Improve_MP.criar_composto("Mg-Nb-O")     print(Improve_MP.compostos)``
   Nesse exemplo será gerada uma lista de materiais compostos por
   Magnésio, Nióbio e Oxigênio no terminal.

-  Para gerar o input para o Quantum ESPRESSO, primeiro defina uma
   variável para o composto, e depois use Improve_MP.qe_input():
   ``python     a = Improve_MP.criar_composto(“FeO”)     Improve_MP.qe_input(a)``
   Nesse exemplo será gerado um arquivo com todos os inputs referentes
   aos parâmetros de rede do FeO necessários para o Quantum ESPRESSO.

-  Para obter características do material selecionado utilize
   Improve_MP.novas_car() e a variável do material criado:
   ``python     a = Improve_MP.criar_composto(“FeO”)     Improve_MP.novas_car(a)``
   Nesse exemplo aparecerão no terminal quais as características
   existentes e a pergunta “Qual Caracteristica do Composto você teria
   interesse?”.

   Responda no terminal escrevendo a característica.

   Após isso, uma segunda pergunta aparecerá no terminal “Tem alguma
   outra caracteristica que gostaria de adquirir?”



        - Caso a resposta seja **sim**:

            Digite a segunda característica desejada.

        - Caso a resposta seja **não**: 

            Digite end .       

   Após o end, todas as características solicitadas para o composto
   escolhido aparecerão no terminal. Para esse exemplo as
   características serão referentes ao FeO.

Para colaboradores
------------------

O programa foi criado com intuito de uso prório na instituição de ensino
dos criados e tornado público para facilitar o uso do Quantum ESPRESSO
para outros usuários. A princípio não há intenção de fazer mudanças ao
código ou adicionar novas funcionalidades e não foram identificados
defeitos no código que exijam alterações, portanto não há sentido em
colaborações, mas agradecemos o interesse na biblioteca!

.. |en| image:: https://img.shields.io/badge/lang-en-red.svg
   :target: https://github.com/cauaschuch/ImproveMP/blob/main/README.en.md

Contents
--------

.. toctree::

