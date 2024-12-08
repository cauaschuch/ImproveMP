from mp_api.client import MPRester
import math
import numpy as np
from decimal import Decimal
import os
import subprocess

class Improve_MP:
    """
    Classe para gerenciar compostos provenientes do Materials Project (MP) e criar objetos que armazenam
    informações relevantes

    Attributes:
        compostos (list): Lista de todos os compostos criados por esta classe

    Methods:
        criar_composto(composto, chave, simetria=''):
            Cria um objeto Improve_MP com base nas informações de um composto do Materials Project obtidos através da API.
    """

    compostos = []
    chave = None

    def __init__(self,nome,sistema_cristalino,mpid,estrutura,space_group):
        """
        Cria um novo composto.

        Args:
            name (str): nome do composto com sua estequiometria
            crystal_system (str): sistema cristalino, ex: cúbico, hexagonal etc
            mpid (str): ID do Materials Project
            structure (Structure): posições atômicas, ângulos e parâmetros de rede estão nesse arg
            space_group (int): número de 0-230
        """
        self.nome=nome
        self.mpid=mpid
        self.estrutura=estrutura
        self.space_group = space_group
        self.sistema_cristalino = sistema_cristalino
        if self not in Improve_MP.compostos:
            Improve_MP.compostos.append(self)
        
    def __str__(self):
        return f'{self.nome} |  {self.sistema_cristalino} #{self.space_group}'
    
    def __repr__(self):
        return f"{self.nome}"
    
    def __eq__(self, other):
        if isinstance(other, Improve_MP):
            return self.nome == other.nome
        return False

    @classmethod
    def minha_chave(cls, key):
        cls.chave = key

    @classmethod
    def criar_composto(cls,composto,simetria=''):
        """Busca as informações do composto desejado com base em dados extraídos da mp_api.

        Args:
            composto (str): fórmula química em string (`ex: Fe2O3; NaCl; ... `) ou elementos presentes no material separados por `"-"` (`ex: Fe-C; W-Re; Nb-Ru; ... ´).
            
            simetria (str): (opcional) fornecer o sistema cristalino (` 'Triclinic', 'Monoclinic', 'Orthorhombic', 'Tetragonal', 'Trigonal', 'Hexagonal','Cubic' `)

        Returns:
            if composto = fórmula, simetria:
                tuple:
                - nome (str): fórmula química do composto fornecido
                - sistema_cristalino (str): simetria fornecida
                - mpids (list): id do mateiral (mp-api)
                - estrutura (str): dados sobre a posição dos átomos na cela unitária
                - internacional (str): ITA number
            
            elif composto = fórmula:
                tuple:
                - nome (str): fórmula química do composto fornecido
                - sistema_cristalino (str): simetria mais estável
                - mpids (list): id do mateiral (mp-api)
                - estrutura (str): dados sobre a posição dos átomos na cela unitária
                - internacional (str): ITA number
            
            else composto = elementos:
                tuple:
                - nome (str)
                - sistema_cristalino (str)
                - mpids (list)
                - estrutura (str)
                - internacional (str)

        """
        key = cls.chave
        with MPRester(key) as mpr:
                sistemas = ['Triclinic', 'Monoclinic', 'Orthorhombic', 'Tetragonal', 'Trigonal', 'Hexagonal','Cubic']
                if '-' not in composto:
                    if simetria in sistemas:
                        docs = mpr.materials.summary.search(formula=composto,crystal_system=simetria)
                        mpids = [doc.material_id for doc in docs]
                        mpids = mpids[0] 

                    else:
                        docs = mpr.materials.summary.search(formula=composto)
                        mpids = [doc.material_id for doc in docs]
                        mpids = mpids[0]
                        print ('\n !!!  simetria não especificada  !!!  \n')   
                    estrutura = mpr.get_structure_by_material_id(mpids)     
                    dados = mpr.materials.get_data_by_id(mpids)
                    sistema_cristalino = dados.symmetry.crystal_system      
                    internacional = dados.symmetry.number
                    nome = dados.formula_pretty
                    #Improve_MP(composto,sistema_cristalino,mpids,estrutura,internacional)
                    print('>>>Composto criado<<<')
                    return cls(nome, sistema_cristalino, mpids, estrutura, internacional)
                else:
                            docs =  mpr.materials.summary.search(chemsys=composto)
                            mpids = [doc.material_id for doc in docs]
                            for i in range(len(mpids)):
                                estrutura = mpr.get_structure_by_material_id(mpids[i])  
                                dados = mpr.materials.get_data_by_id(mpids[i])
                                sistema_cristalino = dados.symmetry.crystal_system   
                                internacional = dados.symmetry.number
                                nome = dados.formula_pretty
                                Improve_MP(nome,sistema_cristalino,mpids[i],estrutura,internacional)

                            print('>>>Compostos criados ***acesse pela lista Improve_MP.compostos<<<')


    @staticmethod
    def extrair_parametros_rede(filename):
        """
        Extrai parâmetros de rede e informações sobre o material desejado de um arquivo de texto
        obtido do Materials Project.

        Args:
            filename (str): Caminho para o arquivo de texto que contém os dados dos parâmetros de rede e posições atômicas.

        Returns:
            tuple: Uma tupla contendo:
                - a (float): Comprimento da aresta `a` da célula unitária.
                - b (float): Comprimento da aresta `b` da célula unitária.
                - c (float): Comprimento da aresta `c` da célula unitária.
                - alpha (float): Ângulo entre as arestas `b` e `c` (em graus).
                - beta (float): Ângulo entre as arestas `a` e `c` (em graus).
                - gamma (float): Ângulo entre as arestas `a` e `b` (em graus).
                - nat (int): Número total de átomos na célula unitária.
                - tipos_atomicos (set): Conjunto contendo os tipos de átomos únicos presentes no material.
                - vetores (list): Lista contendo as posições e tipos dos átomos, onde cada elemento é uma lista no formato 
                  `[tipo_atomo, x, y, z]` com as coordenadas `x`, `y`, `z`.
                - prefix (str): Nome do composto.

        Raises:
            FileNotFoundError: Se o arquivo especificado não for encontrado.
        """
        try:
            with open(filename, 'r') as file:
                text = file.read()
        except FileNotFoundError:
            print(f"Erro: O arquivo '{filename}' não foi encontrado.")
            return None
        lines = text.split('\n')
        a, b, c = None, None, None
        alpha, beta, gamma = None, None, None

        parts = lines[2].split(':')
        a, b, c = map(float, parts[1].split())

        parts = lines[3].split(':')
        alpha, beta, gamma = map(float, parts[1].split())

        nat = int(lines[-1].split()[0])+1
        vetores = []

        prefix = lines[1].split()[-1]

        for line in lines[8:]:
            line = line.split()
            vetores.append([line[1],float(line[2]),float(line[3]),float(line[4])])
        tipos_atomicos = set()

        for vetor in vetores:
            tipos_atomicos.add(vetor[0])

        return a, b, c, alpha, beta, gamma,nat,tipos_atomicos,vetores, prefix
    @staticmethod
    def calculo_parametros_lattice(a, b, c, alpha, beta, gamma):
        """Cálcula parametros necessários para a criação do CELL_PARAMETERS.

        Args:
            a (float): Largura do paralelepípedo.
            b (float): Comprimento do paralelepípedo.
            c (float): Altura do paralelepípedo.
            alpha (float): Ângulo entre as arestas b e c do paralelepípedo.
            beta (float): Ângulo entre as arestas a e c do paralelepípedo.
            gamma (float): Ângulo entre as arestas a e b do paralelepípedo.

    
        Returns:
            tuple: Uma tupla contendo os seguintes valores calculados:
                - ar (float): Largura do paralelepípedo no espaço reciproco.
                - cgr (float): Cosseno do ângulo gamma no espaço reciproco.
                - sgr (float): Seno do ângulo gamma no espaço reciproco.
                - cb (float): Cosseno do ângulo beta.
                - sa (float): Seno do ângulo alpha.
                - ca (float): Cosseno do ângulo alpha.

        Raises:
            ValueError: Caso os valores dos ângulos fornecidos resultem em um valor de volume inválido (zero ou negativo).
        """
        alpha = math.radians(alpha)
        beta = math.radians(beta)
        gamma = math.radians(gamma)

        ca = math.cos(alpha)
        cb = math.cos(beta)
        cg = math.cos(gamma)
        sa = math.sin(alpha)
        sb = math.sin(beta)

        V = a * b * c * np.sqrt(1 - ca**2 - cb**2 - cg**2 + 2 * ca * cb * cg)
        if V <= 0:
            raise ValueError("Volume inválido.")

        ar = (b * c * sa) / V

        cgr = (ca * cb - cg) / (sa * sb)
        sgr = math.sqrt(1 - cgr**2)

        return ar,cgr,sgr,cb,sa,ca
    
    @staticmethod
    def massa_atomica(elemento):
        """Encontra a massa atômica de um Elemento.

        Args:
            elemento (str): Nome do elemento.

        Returns:
            float: Massa atomica do elemento.

        Raises:
            ValueError: Caso o elemento não esteja no dicionário.
        """
        elemento_massa = {
            "H": 1.00784,
            "He": 4.002602,
            "Li": 6.938,
            "Be": 9.0121831,
            "B": 10.806,
            "C": 12.011,
            "N": 14.0067,
            "O": 15.999,
            "F": 18.998403163,
            "Ne": 20.1797,
            "Na": 22.98976928,
            "Mg": 24.305,
            "Al": 26.9815385,
            "Si": 28.085,
            "P": 30.973761998,
            "S": 32.06,
            "Cl": 35.45,
            "Ar": 39.948,
            "K": 39.0983,
            "Ca": 40.078,
            "Sc": 44.955908,
            "Ti": 47.867,
            "V": 50.9415,
            "Cr": 51.9961,
            "Mn": 54.938044,
            "Fe": 55.845,
            "Co": 58.933194,
            "Ni": 58.6934,
            "Cu": 63.546,
            "Zn": 65.38,
            "Ga": 69.723,
            "Ge": 72.63,
            "As": 74.921595,
            "Se": 78.971,
            "Br": 79.904,
            "Kr": 83.798,
            "Rb": 85.4678,
            "Sr": 87.62,
            "Y": 88.90584,
            "Zr": 91.224,
            "Nb": 92.90637,
            "Mo": 95.95,
            "Tc": 98.0,
            "Ru": 101.07,
            "Rh": 102.90550,
            "Pd": 106.42,
            "Ag": 107.8682,
            "Cd": 112.414,
            "In": 114.818,
            "Sn": 118.710,
            "Sb": 121.760,
            "Te": 127.60,
            "I": 126.90447,
            "Xe": 131.293,
            "Cs": 132.90545196,
            "Ba": 137.327,
            "La": 138.90547,
            "Ce": 140.116,
            "Pr": 140.90766,
            "Nd": 144.242,
            "Pm": 145.0,
            "Sm": 150.36,
            "Eu": 151.964,
            "Gd": 157.25,
            "Tb": 158.92535,
            "Dy": 162.500,
            "Ho": 164.93033,
            "Er": 167.259,
            "Tm": 168.93422,
            "Yb": 173.045,
            "Lu": 174.9668,
            "Hf": 178.49,
            "Ta": 180.94788,
            "W": 183.84,
            "Re": 186.207,
            "Os": 190.23,
            "Ir": 192.217,
            "Pt": 195.084,
            "Au": 196.966569,
            "Hg": 200.592,
            "Tl": 204.38,
            "Pb": 207.2,
            "Bi": 208.98040,
            "Th": 232.0377,
            "Pa": 231.03588,
            "U": 238.02891
        }
        if elemento not in elemento_massa:
            raise ValueError("Não há esse elemento no nosso banco de dados.")
        return elemento_massa[elemento]
    
    def qe_input(self):
        """
        essa função cria um arquivo de texto ".in" no formato do quantum espresso

        Description:
            esse método cria um arquivo (.in) para o Quantum ESPRESSO (QE) a partir da estrutura
            do material;o arquivo contém informações de parâmetros de rede, espécies atômicas, posições 
            atômicas e kpoints, incompletos, restando ao usuário completá-los após a geração

        Steps:
            1. extrai parâmetros de rede e dados atômicos da estrutura do material
            2. calcula os parâmetros de rede padrão e matrizes de transformação
            3. formata as seções: CELL_PARAMETERS, ATOMIC_SPECIES, ATOMIC_POSITIONS e K_POINTS
            4. escreve os dados formatados em um arquivo de entrada para o QE

        Returns:
            não retorna valores > O arquivo `.in` é salvo no diretório de trabalho atual, apenas um aviso é dado
            pelo terminal quando finalizado

        Output:
            um arquivo `.in` para o Quantum ESPRESSO com o nome `<nome_do_material>.in`
    
        File Format:
            - CONTROL: Contém informações gerais, como o `prefix`.
            - SYSTEM: Informações sobre a rede e o número de átomos/tipos.
            - CELL_PARAMETERS: Vetores de rede em angstroms.
            - ATOMIC_SPECIES: Massas atômicas e pseudopotenciais.
            - ATOMIC_POSITIONS: Posições atômicas no cristal.
            - K_POINTS: Geração automática de pontos-k.
        """

        current_dir = os.getcwd()
        tmp_path = os.path.join(current_dir, 'tmp')

        with open(tmp_path, 'w') as file:
            file.write(str(self.estrutura))

        a, b, c, alpha, beta, gamma, nat, tipos_atomicos, vetores, prefix = Improve_MP.extrair_parametros_rede(tmp_path)
        ar,cgr,sgr,cb,sa,ca = Improve_MP.calculo_parametros_lattice(a, b, c, alpha, beta, gamma)
        diag = np.identity(3)
        stdbase = np.array([[1.0 / ar, -cgr / sgr / ar, cb * a], [0.0, b * sa, b * ca], [0.0, 0.0, c]],dtype=float,)
        base = np.dot(stdbase, diag)

        output_path = os.path.join(current_dir, f'{self.nome}.in')
        with open(output_path, 'w') as file: 
            file.write(f"&CONTROL\nprefix = '{prefix}'\n/\n&SYSTEM\nibrav = 0\nnat = {nat}\nntyp = {len(tipos_atomicos)}\n/\n&ELECTRONS\n/\n")
            file.write("CELL_PARAMETERS angstrom\n")
            for vetor in base:
                v_1 = Decimal(vetor[0]).quantize(Decimal('0.00000000'))
                v_2 = Decimal(vetor[1]).quantize(Decimal('0.00000000'))
                v_3 = Decimal(vetor[2]).quantize(Decimal('0.00000000'))
                file.write(f"   {v_1:>10.8f}  {v_2:>10.8f}  {v_3:>10.8f}\n")
            file.write(f'ATOMIC_SPECIES\n')
            for elemento in tipos_atomicos:
                file.write(f'     {elemento} {Improve_MP.massa_atomica(elemento)} {elemento}_pseudo\n')
            file.write('ATOMIC_POSITIONS {crystal}\n')
            for vetor in vetores:
                v_1 = Decimal(vetor[1]).quantize(Decimal('0.00000000'))
                v_2 = Decimal(vetor[2]).quantize(Decimal('0.00000000'))
                v_3 = Decimal(vetor[3]).quantize(Decimal('0.00000000'))
                file.write(f' {vetor[0]} {v_1:>10.8f}  {v_2:>10.8f}  {v_3:>10.8f}\n')
            file.write('K_POINTS automatic')
        print(f'>>>Seu input {self.nome}.in está pronto<<<')

    @classmethod
    def novas_car(cls,composto):
        """
    Adquire características adicionais de um composto do Materials Project (MP) com base no interesse do usuário.

    Este método interage com a API do Materials Project para buscar características específicas de um composto,
    identificadas pelo atributo `mpid` da instância passada. O usuário pode especificar quais características
    deseja obter, e o método verifica se essas informações estão disponíveis no banco de dados do MP.

    Args:
        composto (Improve_MP): Objeto da classe `Improve_MP` contendo o `mpid` do composto.

    Interação do Usuário:
        - O usuário será solicitado a inserir o nome de uma característica do composto, que deve estar listada
          em `mpr.materials.summary.available_fields`.
        - O loop continuará até que o usuário digite 'end', indicando que não deseja adicionar mais características.
        """

        key = cls.chave
        with MPRester(key) as mpr:
            docs = mpr.materials.summary.search(material_ids=composto.mpid)
            jr=docs[0]

            print(mpr.materials.summary.available_fields)
            l=[]
            m=[]
            s=input('Qual Caracteristica do Composto você teria interesse?')

            while s != 'end':
                l= l + [f'jr.{s}']
                m=m +[f'{s}']
                s=input('Tem alguma outra caracteristica que gostaria de adquirir?')
        
            for n in range(len(l)):
                if f'{eval(l[n])}' == 'None':
                    print(f'{m[n]}= Não há tal caracteristica no Material Project para este composto')
                else:
                    print(f'{m[n]}= {eval(l[n])}')
        
    def xcrysden(composto):
        """
        não deve haver um caminho improprio para arquivo .in, por exemplo /home/usuaria/pasta python/composto.in é um caminho improprio,
        já /home/usuaria/pasta_python/composto.in é um caminho funcional.

        """

        comando=f'xcrysden --pwi {composto.nome}.in'
        subprocess.run(comando,shell=True)