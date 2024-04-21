import tkinter as tk # Importa o módulo tkinter como tk
from tkinter import messagebox # Importa a função messagebox do módulo tkinter

class ConnectFour:
    # Define o método de inicialização da classe ConnectFour
    def __init__(self, root): 
        # Inicializa o atributo root da instância
        self.root = root 
        # Define o título da janela como "Jogo da velha"
        self.root.title("Jogo da velha") 
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
        self.precompute = {}  # Cache para armazenar as jogadas pré-computadas
        self.limite_profundidade = 3  # Limite de profundidade para o algoritmo minimax

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
        botao_facil.grid(row=7, column=2)
        # Cria um botão de seleção para a dificuldade difícil
        botao_dificil = tk.Radiobutton(self.root, text="Difícil", variable=self.variavel_dificuldade, value='Difícil')
        # Posiciona o botão de seleção na janela tkinter
        botao_dificil.grid(row=7, column=3)
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
                         # Executa o movimento da IA difícil
                        self.movimento_ia_dificil()
# Define o método para atualizar a representação visual do tabuleiro na interface
    def desenhar_tabuleiro(self):
        # Loop pelas linhas do tabuleiro
        for i in range(7):
            # Loop pelas colunas do tabuleiro
            for j in range(7):
         # Atualiza o texto do botão correspondente com o conteúdo da célula do tabuleiro
                self.botoes[i][j]['text'] = self.tabuleiro[i][j]
 # Define o método para verificar se há um vencedor no jogo
    def verificar_vencedor(self):
        # Loop pelas linhas do tabuleiro
        for i in range(7):
            # Loop pelas colunas do tabuleiro
            for j in range(7):
                 # Verifica se a célula atual não está vazia
                if self.tabuleiro[i][j] != '':
                    # Verifica se há uma sequência de quatro peças iguais na horizontal
                    if j <= 3 and self.tabuleiro[i][j] == self.tabuleiro[i][j+1] == self.tabuleiro[i][j+2] == self.tabuleiro[i][j+3]:
                       # Retorna o jogador vencedor
                        return self.tabuleiro[i][j]
                     # Verifica se há uma sequência de quatro peças iguais na vertical
                    if i <= 3 and self.tabuleiro[i][j] == self.tabuleiro[i+1][j] == self.tabuleiro[i+2][j] == self.tabuleiro[i+3][j]:
                        # Retorna o jogador vencedor
                        return self.tabuleiro[i][j]
                    # Verifica se há uma sequência de quatro peças iguais na diagonal principal
                    if i <= 3 and j <= 3 and self.tabuleiro[i][j] == self.tabuleiro[i+1][j+1] == self.tabuleiro[i+2][j+2] == self.tabuleiro[i+3][j+3]:
                        # Retorna o jogador vencedor
                        return self.tabuleiro[i][j]
                    # Verifica se há uma sequência de quatro peças iguais na diagonal secundária
                    if i <= 3 and j >= 3 and self.tabuleiro[i][j] == self.tabuleiro[i+1][j-1] == self.tabuleiro[i+2][j-2] == self.tabuleiro[i+3][j-3]:
                       # Retorna o jogador vencedor
                        return self.tabuleiro[i][j]
                    # Retorna None se não houver um vencedor
        return None
 # Define o método para realizar o movimento da IA na dificuldade fácil
    def movimento_ia_facil(self):
        # Loop pelas linhas do tabuleiro
        for i in range(7):
            # Loop pelas colunas do tabuleiro
            for j in range(7):
                # Verifica se a célula está vazia
                if self.tabuleiro[i][j] == '':
                     # Marca a célula como 'O' (movimento da IA)
                    self.tabuleiro[i][j] = 'O'
                    # Atualiza a representação visual do tabuleiro na interface
                    self.desenhar_tabuleiro()
                    # Verifica se há um vencedor após o movimento da IA
                    vencedor = self.verificar_vencedor()
                    # Se houver um vencedor
                    if vencedor:
                         # Exibe uma mensagem indicando o vencedor
                        messagebox.showinfo("Fim do Jogo", f"{vencedor} : venceu!")
                        # Reinicia o jogo
                        self.reiniciar_jogo()
                        # Retorna para encerrar o método
                        return
                    # Se não houver um vencedor
                    else:
                        # Define o próximo jogador como 'X'
                        self.jogador = 'X'
                        # Retorna para encerrar o método
                        return
 # Define o método para realizar o movimento da IA na dificuldade difícil
    def movimento_ia_dificil(self):
        # Verifica se a jogada está pré-computada
        if self.precompute.get(tuple(map(tuple, self.tabuleiro))):
            # Obtém a jogada pré-computada
            linha, coluna = self.precompute[tuple(map(tuple, self.tabuleiro))]
            #Use else para especificar um bloco
        else:
            # Inicializa a melhor pontuação como menos infinito
            melhor_pontuacao = float('-inf')
             # Inicializa a melhor jogada como nula
            melhor_jogada = None
            # Loop pelas linhas do tabuleiro
            for i in range(7):
                # Loop pelas colunas do tabuleiro
                for j in range(7):
                    # Verifica se a célula está vazia
                    if self.tabuleiro[i][j] == '':
                        # Marca a célula como 'O' (movimento da IA)
                        self.tabuleiro[i][j] = 'O'
                        # Calcula a pontuação para o movimento atual
                        pontuacao = self.minimax(0, False, float('-inf'), float('inf'))
                        # Desfaz o movimento da IA
                        self.tabuleiro[i][j] = ''
                         # Verifica se a pontuação atual é melhor que a melhor pontuação encontrada até o momento
                        if pontuacao > melhor_pontuacao:
                            # Atualiza a melhor pontuação
                            melhor_pontuacao = pontuacao
                            # Atualiza a melhor jogada
                            melhor_jogada = (i, j)
                            # Obtém a linha e coluna da melhor jogada
            linha, coluna = melhor_jogada
             # Armazena a jogada pré-computada
             #Uma tuple (tupla) em Python é uma estrutura de dados ordenada tupla = (1, 2, 3, 4, 5)
            #A função map() em Python aplica uma função (como uma lista, tupla, etc.)
            self.precompute[tuple(map(tuple, self.tabuleiro))] = (linha, coluna)
        # Realiza o movimento da IA no tabuleiro
        self.tabuleiro[linha][coluna] = 'O'
        # Atualiza a representação visual do tabuleiro na interface
        self.desenhar_tabuleiro()
        # Verifica se há um vencedor após o movimento da IA
        vencedor = self.verificar_vencedor()
        # Se houver um vencedor
        if vencedor:
            # Exibe uma mensagem indicando o vencedor
            messagebox.showinfo("Fim do Jogo", f"{vencedor} : venceu!")
            # Reinicia o jogo
            self.reiniciar_jogo()
            #Use else para especificar 
        else:
            # Define o próximo jogador como 'X'
            self.jogador = 'X'
    #dica a profundidade atual na árvore de busca. É usada para limitar a profundidade da recursão.
    #self: Este parâmetro sugere que a função é um método dentro de uma classe
    def minimax(self, profundidade, eh_jogador_maximizando, alfa, beta):
        # Verifica se há um vencedor
        vencedor = self.verificar_vencedor()
        #vencedor for = 0 
        if vencedor == 'O':
            # Se 'O' vencer, retorna 1
            return 1
        #vencedor for = X 
        elif vencedor == 'X':
            # Se 'O' vencer, retorna -1
            return -1
        # Se houver empate ou a profundidade máxima for atingida, retorna 0
        elif vencedor == 'Empate' or profundidade == self.limite_profundidade:
            #retorn 0
            return 0
        #jogada maxim
        if eh_jogador_maximizando:
            # Inicializa a melhor pontuação para o jogador maximizador
            melhor_pontuacao = float('-inf')
            # Loop pelas linhas do tabuleiro 
            for i in range(7):
                # Loop pelas colunas do tabuleiro
                for j in range(7):
                    # Se a célula estiver vazia
                    if self.tabuleiro[i][j] == '':
                        # Coloca 'O' na célula
                        self.tabuleiro[i][j] = 'O'
                        # Chama recursivamente o minimax para o jogador minimizador
                        pontuacao = self.minimax(profundidade + 1, False, alfa, beta)
                         # Desfaz a jogada
                        self.tabuleiro[i][j] = ''
                        # Atualiza a melhor pontuação
                        melhor_pontuacao = max(melhor_pontuacao, pontuacao)
                        # Atualiza o valor de alfa
                        alfa = max(alfa, pontuacao)
                         # Realiza poda se necessário
                        if beta <= alfa:
                            #parar
                            break
                        # Retorna a melhor pontuação para o jogador maximizador
            return melhor_pontuacao
        #se nao
        else:
            # Inicializa a pior pontuação para o jogador minimizador
            pior_pontuacao = float('inf')
            # Loop pelas linhas do tabuleiro 
            for i in range(7):
                # Loop pelas colunas do tabuleiro
                for j in range(7):
                    # Se a célula estiver vazia
                    if self.tabuleiro[i][j] == '':
                        # Coloca 'X' na célula
                        self.tabuleiro[i][j] = 'X'
                        # Chama recursivamente o minimax para o jogador maximizador
        #profundidade em 1, indicando que estamos indo para o próximo nível na árvore de jogadas.
                        pontuacao = self.minimax(profundidade + 1, True, alfa, beta)
                        # Desfaz a jogada
                        self.tabuleiro[i][j] = ''
                        # Atualiza a pior pontuação
                        pior_pontuacao = min(pior_pontuacao, pontuacao)
                        # Atualiza o valor de beta
                        beta = min(beta, pontuacao)
                        # Realiza poda se necessário
                        if beta <= alfa:
                            #parar
                            break
                        # Retorna a pior pontuação para o jogador minimizador
            return pior_pontuacao
    # Método para reiniciar o jogo
    def reiniciar_jogo(self):
        # Define o jogador inicial como 'X'
        self.jogador = 'X'
        # Cria um tabuleiro vazio com 7 linhas e 7 colunas
        self.tabuleiro = [['' for _ in range(7)] for _ in range(7)]
        # Desenha o tabuleiro inicial
        self.desenhar_tabuleiro()
        
# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    # Cria uma instância do Tkinter
    root = tk.Tk()
    # Inicializa o jogo Connect Four passando a instância do Tkinter
    jogo = ConnectFour(root)
    # Inicia o loop principal do Tkinter
    root.mainloop()
