# -*- coding: utf-8 -*-
# Importa o módulo tkinter como tk
import tkinter as tk
# Importa a função messagebox do módulo tkinter
from tkinter import messagebox

# classe connect
class ConnectFour:
    # Define o método de inicialização da classe ConnectFour
    def __init__(self, root):
        # Inicializa o atributo root da instância
        self.root = root
        # Define o título da janela como "Jogo da velha"
        self.root.title("Jogo da Velha")
         # Define o jogador atual como 'X'
        self.jogador = 'X'
        # Cria uma matriz 7x7 para representar o tabuleiro do jogo
        self.tabuleiro = [['' for _ in range(7)] for _ in range(7)]
        # Inicializa uma lista vazia para armazenar os botões do jogo
        self.botoes = []
        # Define a dificuldade inicial como 'Fácil'
        self.dificuldade = 'Fácil'
        # Cria uma variável do tipo StringVar() do tkinter
        self.variavel_dificuldade = tk.StringVar()
        # Define o valor inicial da variável de dificuldade como 'Fácil'
        self.variavel_dificuldade.set('Fácil')
        # Chama o método para criar o tabuleiro do jogo
        self.criar_tabuleiro()
        # Chama o método para criar o seletor de dificuldade do jogo
        self.criar_seletor_dificuldade()
        # Cache para armazenar as jogadas pré-computadas
        self.precompute = {}
        # Limite de profundidade para o algoritmo minimax, para otimizar 
        self.limite_profundidade = 3
# Define o método para criar o tabuleiro do jogo
    def criar_tabuleiro(self):
        # Loop sobre as linhas do tabuleiro
        for i in range(7):
# Inicializa uma lista vazia para representar uma linha do tabuleiro
            linha = []
            # Loop sobre as colunas do tabuleiro
            for j in range(7):
# Cria um botão tkinter com texto vazio, fonte Arial de tamanho 20, largura de 3 caracteres e altura de 1 caractere
                botao = tk.Button(self.root, text='', font=('Arial', '20'), width=3, height=1,
                # Cria um botão na posição (i, j) do tabuleiro e associa a função clique_botao a ele
                                  command=lambda linha=i, coluna=j: self.clique_botao(linha, coluna))
                # Posiciona o botão na janela do tkinter
                botao.grid(row=i, column=j, padx=5, pady=5)
                # Adiciona o botão à linha atual
                linha.append(botao)
                # Adiciona a linha à lista de botões do tabuleiro
            self.botoes.append(linha)
# Define o método para criar o seletor de dificuldade do jogo
    def criar_seletor_dificuldade(self):
        # Cria um rótulo para indicar o nível de dificuldade
        label_dificuldade = tk.Label(self.root, text="Nível de Dificuldade:")
        # Posiciona o rótulo na janela tkinter
        label_dificuldade.grid(row=7, column=0, columnspan=2)
        # Cria um botão de seleção para a dificuldade fácil
        botao_facil = tk.Radiobutton(self.root, text="Fácil", variable=self.variavel_dificuldade, value='Fácil')
        # Posiciona o botão de seleção na janela tkinter
        botao_facil.grid(row=7, column=3)
        # Cria um botão de seleção para a dificuldade difícil
        botao_dificil = tk.Radiobutton(self.root, text="Difícil", variable=self.variavel_dificuldade, value='Difícil')
        # Posiciona o botão de seleção na janela tkinter
        botao_dificil.grid(row=7, column=5)
        
# Define o método para tratar o clique em um botão do tabuleiro
    def clique_botao(self, linha, coluna):
        # Verifica se a célula clicada está vazia
        if self.tabuleiro[linha][coluna] == '':
            # Atualiza o tabuleiro com a marca do jogador atual
            self.tabuleiro[linha][coluna] = self.jogador
            # Atualiza a representação visual do tabuleiro na interface
            self.desenhar_tabuleiro()
            # Verifica se há um vencedor após o último movimento
            vencedor = self.verificar_vencedor()
            # Se houver um vencedor
            if vencedor:
                # Exibe uma mensagem indicando o vencedor
                messagebox.showinfo("Fim do Jogo", f"{vencedor} venceu!")
                # Reinicia o jogo
                self.reiniciar_jogo()
                # Se não houver um vencedor
            else:
                # Alterna para o próximo jogador
                self.jogador = 'O' if self.jogador == 'X' else 'X'
                # Se for a vez da IA jogar
                if self.jogador == 'O':
                    # Se a dificuldade for fácil
                    if self.variavel_dificuldade.get() == 'Fácil':
                        # Executa o movimento da IA fácil
                        self.movimento_ia_facil()
                        # Se a dificuldade for difícil
                    else:
                        # Obtém a linha e coluna da jogada calculada pela função alfabeta
                        linha, coluna = self.alfabeta()
                        # Realiza a jogada da IA na posição calculada
                        self.tabuleiro[linha][coluna] = 'O'
                        # Atualiza a representação visual do tabuleiro
                        self.desenhar_tabuleiro()
                        # Verifica se há um vencedor após a jogada da IA
                        vencedor = self.verificar_vencedor()
                        # Se houver um vencedor
                        if vencedor:
                            # Exibe uma mensagem de fim de jogo com o vencedor
                            messagebox.showinfo("Fim do Jogo", f"{vencedor} venceu!")
                            # Reinicia o jogo
                            self.reiniciar_jogo()
                            # Se não houver um vencedor
                        else:
                            # Alterna para o próximo jogador (jogador humano)
                            self.jogador = 'X'
                            
#funçao desenha tabuleiro 
    def desenhar_tabuleiro(self):
        # Percorre todas as linhas do tabuleiro
        for i in range(7):
             # Percorre todas as colunas do tabuleiro
            for j in range(7):
# Atualiza o texto do botão na posição (i, j) com o conteúdo da célula correspondente do tabuleiro
                self.botoes[i][j]['text'] = self.tabuleiro[i][j]
#funçao verificar o vencedor
    def verificar_vencedor(self):
        # Loop pelas linhas do tabuleiro
        for i in range(7):
            # Loop pelas colunas do tabuleiro
            for j in range(7):
                # Verifica se a célula não está vazia
                if self.tabuleiro[i][j] != '':
                    # Verifica se há uma sequência de quatro peças iguais na horizontal
                    if j <= 3 and self.tabuleiro[i][j] == self.tabuleiro[i][j+1] == self.tabuleiro[i][j+2] == self.tabuleiro[i][j+3]:
                        # Retorna o jogador que venceu
                        return self.tabuleiro[i][j]
                    # Verifica se há uma sequência de quatro peças iguais na vertical
                    if i <= 3 and self.tabuleiro[i][j] == self.tabuleiro[i+1][j] == self.tabuleiro[i+2][j] == self.tabuleiro[i+3][j]:
                       # Retorna o jogador que venceu
                        return self.tabuleiro[i][j]
                    # Verifica se há uma sequência de quatro peças iguais na diagonal principal
                    if i <= 3 and j <= 3 and self.tabuleiro[i][j] == self.tabuleiro[i+1][j+1] == self.tabuleiro[i+2][j+2] == self.tabuleiro[i+3][j+3]:
                       # Retorna o jogador que venceu
                        return self.tabuleiro[i][j]
                    # Verifica se há uma sequência de quatro peças iguais na diagonal secundária
                    if i <= 3 and j >= 3 and self.tabuleiro[i][j] == self.tabuleiro[i+1][j-1] == self.tabuleiro[i+2][j-2] == self.tabuleiro[i+3][j-3]:
                       # Retorna o jogador que venceu
                        return self.tabuleiro[i][j]
                    # Retorna None se não houver um vencedor
        return None
#funçao movimento facil
    def movimento_ia_facil(self):
        # Percorre todas as linhas do tabuleiro
        for i in range(7):
            # Percorre todas as colunas do tabuleiro
            for j in range(7):
                # Verifica se a célula está vazia
                if self.tabuleiro[i][j] == '':
                    # Marca a célula com 'O' (movimento da IA)
                    self.tabuleiro[i][j] = 'O'
                    # Atualiza a representação visual do tabuleiro
                    self.desenhar_tabuleiro()
                    # Verifica se há um vencedor após o movimento da IA
                    vencedor = self.verificar_vencedor()
                    # Se houver um vencedor
                    if vencedor:
                        # Exibe uma mensagem indicando o vencedor
                        messagebox.showinfo("Fim do Jogo", f"{vencedor} venceu!")
                        # Reinicia o jogo
                        self.reiniciar_jogo()
                        # Retorna para encerrar a função
                        return
                    #se não 
                    else:
                        # Alterna para o próximo jogador (jogador humano)
                        self.jogador = 'X'
                        # Retorna para encerrar a função
                        return
    # funçao alfa beta
    def alfabeta(self):
        # Inicializa a melhor pontuação como menos infinito
        melhor_pontuacao = float('-inf')
        # Inicializa a melhor jogada como nula
        melhor_jogada = None
         # Inicializa alfa como menos infinito
        alfa = float('-inf')
        # Inicializa beta como infinito
        beta = float('inf')
 # Loop pelas linhas do tabuleiro
        for i in range(7):
            # Loop pelas colunas do tabuleiro
            for j in range(7):
                # Verifica se a célula está vazia
                if self.tabuleiro[i][j] == '':
                    # Marca a célula com 'O' (movimento da IA)
                    self.tabuleiro[i][j] = 'O'
                    # Calcula a pontuação para o movimento atual usando o algoritmo minimax
                    pontuacao = self.minimax(0, False, alfa, beta)
                    # Desfaz a jogada
                    self.tabuleiro[i][j] = ''
# Verifica se a pontuação atual é melhor que a melhor pontuação encontrada até o momento
                    if pontuacao > melhor_pontuacao:
                        # Atualiza a melhor pontuação
                        melhor_pontuacao = pontuacao
                        # Atualiza a melhor jogada
                        melhor_jogada = (i, j)
                        # Atualiza alfa com o máximo entre alfa e a pontuação
                    alfa = max(alfa, pontuacao)
                    # Realiza poda se necessário
                    if beta <= alfa:
                        # Sai do loop interno
                        break
# Retorna a melhor jogada encontrada
        return melhor_jogada

    def minimax(self, profundidade, eh_jogador_maximizando, alfa, beta):
        # Verifica se há um vencedor
        vencedor = self.verificar_vencedor()
        # Se 'O' vencer
        if vencedor == 'O':
            #retorna 1
            return 1
        # Se 'X' vencer
        elif vencedor == 'X':
            #retorna -1
            return -1
        # Se houver empate ou a profundidade máxima for atingida, retorna 0
        elif vencedor == 'Empate' or profundidade == self.limite_profundidade:
            #returna 0
            return 0
# Se for a vez do jogador maximizador
        if eh_jogador_maximizando:
            # Inicializa a melhor pontuação como menos infinito
            melhor_pontuacao = float('-inf')
            # Loop pelas linhas do tabuleiro
            for i in range(7):
                # Loop pelas colunas do tabuleiro
                for j in range(7):
                    # Verifica se a célula está vazia
                    if self.tabuleiro[i][j] == '':
                        # Marca a célula com 'O' (movimento da IA)
                        self.tabuleiro[i][j] = 'O'
                        # Chama recursivamente o minimax para o jogador minimizador
                        pontuacao = self.minimax(profundidade + 1, False, alfa, beta)
                        # Desfaz a jogada
                        self.tabuleiro[i][j] = ''
                        # Atualiza a melhor pontuação
#O (max) é uma função embutida do Python que retorna o maior valor entre dois ou mais valores 
                        melhor_pontuacao = max(melhor_pontuacao, pontuacao)
                        # Atualiza alfa com o máximo entre alfa e a pontuação
#O (max) é uma função embutida do Python que retorna o maior valor entre dois ou mais valores 
                        alfa = max(alfa, pontuacao)
                         # Realiza poda se necessário
                        if beta <= alfa:
                            # Sai do loop interno
                            break
             # Retorna a melhor pontuação para o jogador maximizador           
            return melhor_pontuacao
        # Se for a vez do jogador minimizador
        else:
            # Inicializa a pior pontuação como infinito
            pior_pontuacao = float('inf')
            # Loop pelas linhas do tabuleiro
            for i in range(7):
                # Loop pelas colunas do tabuleiro
                for j in range(7):
                    # Verifica se a célula está vazia
                    if self.tabuleiro[i][j] == '':
                        # Marca a célula com 'X' (movimento do jogador humano)
                        self.tabuleiro[i][j] = 'X'
                        # Chama recursivamente o minimax para o jogador maximizador
                        pontuacao = self.minimax(profundidade + 1, True, alfa, beta)
                        # Desfaz a jogada
                        self.tabuleiro[i][j] = ''
                        # Atualiza a pior pontuação
#O (min) é uma função embutida do Python que retorna o menor valor entre dois
                        pior_pontuacao = min(pior_pontuacao, pontuacao)
                        # Atualiza beta com o mínimo entre beta e a pontuação
#O (min) é uma função embutida do Python que retorna o menor valor entre dois
                        beta = min(beta, pontuacao)
                        # Realiza poda se necessário
                        if beta <= alfa:
                            # Sai do loop interno
                            break
                        # Retorna a pior pontuação para o jogador minimizador
            return pior_pontuacao
# função reiniciar jogo
    def reiniciar_jogo(self):
        # Define o jogador inicial como 'X'
        self.jogador = 'X'
        # Cria um tabuleiro vazio com 7 linhas e 7 colunas
        self.tabuleiro = [['' for _ in range(7)] for _ in range(7)]
        # Atualiza a representação visual do tabuleiro na interface
        self.desenhar_tabuleiro()
# main
if __name__ == "__main__":
    # Cria uma instância do Tkinter
    root = tk.Tk()
    # Inicializa o jogo Connect Four passando a instância do Tkinter
    jogo = ConnectFour(root)
     # Inicia o loop principal do Tkinter
    root.mainloop()
