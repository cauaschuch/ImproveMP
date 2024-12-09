
![Logo ](https://github.com/user-attachments/assets/0f7c4b08-f9e2-4172-b355-cf4b955c2d5a)

[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](https://github.com/cauaschuch/ImproveMP/blob/main/README.md)

# ImproveMP

ImproveMP is a library designed to assist researchers in creating inputs for the Quantum ESPRESSO software, based on the database offered by the Materials Project (MP).

## Introduction

The ImproveMP program aims to facilitate the use of Quantum ESPRESSO software by automating the transfer of data such as the network parameters of various materials from the Materials Project (MP) database using application programming interfaces (APIs).

**Note:** Since the program was targeted to a Brazilian audience, the arguments for the code and the questions on the terminal are in portuguese, so you might have to use a translator at some points. 

## Instructions

To install the library, run the command below:

```bash
pip install ImproveMP
```

### How to use the program 

**1° Step:** 

Install the library.

**2° Step:**

Log in to your Materials Project account (https://next-gen.materialsproject.org/api#api-key), click on APIs at the top menu and get your API Key.
It is recommended to save your key in an easily accessible location.

**3° Step:**

In a new file, import the library:
```python
from ImproveMP import Improve_MP
```

Insert your key into the command:
```python
Improve_MP.minha_chave(“”)
```
**Different functionalities**

- To search for several compounds based on their composition, use a - between the elements, in the format "A-B-C-...":
    ```python
    Improve_MP.criar_composto("Mg-Nb-O")
    print(Improve_MP.compostos)
    ```
    In this example, a list of materials composed of Magnesium, Niobium and Oxygen will be generated at the terminal.

- To generate the input for Quantum ESPRESSO, first define a variable for the compound, and then use Improve_MP.qe_input():
    ```python
    a = Improve_MP.criar_composto(“FeO”)
    Improve_MP.qe_input(a)
    ```
    In this example, a file will be generated with all the inputs relating to the FeO network parameters necessary for Quantum ESPRESSO.

- To obtain characteristics of the selected material, use Improve_MP.novas_car() and the created material variable:
    ```python
    a = Improve_MP.criar_composto(“FeO”)
    Improve_MP.novas_car(a)
    ```
    In this example, the existing characteristics will appear on the terminal and the question "Qual Caracteristica do Composto você teria interesse?", which translates to "Which characteristic of the compound would you be interested in?".

    Respond in the terminal by writing the characteristic you want.

    After that, a second question will appear on the terminal "Tem alguma outra caracteristica que gostaria de adquirir?", which translates to "Do you have any other characteristics you would like to obtain?"

        - If the answer is **yes**:

            Enter the second desired characteristic.

        - If the answer is **no**:

            Enter end .       

    After end, all requested characteristics for the chosen compound will appear in the terminal. For this example, the characteristics will refer to FeO.


## For collaborators

The program was created with the intention of its own use in the educational institution of the children and made public to facilitate the use of Quantum ESPRESSO for other users. 
In principle, there is no intention to make changes to the code or add new features and no defects have been identified in the code that require changes, so there is no point in collaborations, but we appreciate your interest in the library!
