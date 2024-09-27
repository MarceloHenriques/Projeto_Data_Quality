# Bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cores
color_palette = sns.color_palette("dark")
plot_style = sns.set_style("darkgrid")

class DataQuality:
    def __init__ (self, csv_file):
        self.arquivo = csv_file
        self.df = pd.read_csv(f"./{csv_file}")
        self.lista_numericas = list(self.df.select_dtypes(include=np.number).columns)
        self.lista_categoricas = list(self.df.select_dtypes(exclude=np.number).columns)
        self.__valores_categoricos = 20
    
    
    # Informações do Dataframe
    def informacoes(self):
        self.df.info()
    
    
    # Exibe a contagem dos valores nulos por coluna
    def contagem_nulos(self): 
        nulos = pd.DataFrame(self.df.isnull().sum())
        nulos.columns = ["Nulos Soma"]
        nulos["Nulos %"] = round(100 * nulos["Nulos Soma"] / self.df.shape[0], 2)
        return nulos
    
    
    # Exibindo a contagem dos valores unicos por coluna
    def contagem_unicos(self):
        unicos = pd.DataFrame(self.df.nunique())
        unicos.columns = ["Unicos Soma"]
        unicos["Unicos %"] = round(100 * unicos["Unicos Soma"] / self.df.shape[0], 2)
        return unicos
    
    
    # Analisando as colunas informadas
    def descricao(self, colunas:list = None):
        if colunas == None:
            colunas = self.lista_numericas + self.lista_categoricas
        
        if isinstance(colunas, (int, float, str)):
            if (colunas in self.lista_numericas) or (colunas in self.lista_categoricas):
                colunas = [colunas]
            
            else:
                raise ValueError("O valor informado deve ser o nome de uma das colunas do dataframe, uma lista de valores das colunas, ou não informar argumentos para ver todas as colunas.")
            
        elif not isinstance(colunas, list):
            raise TypeError("O valor informado deve ser o nome de uma das colunas do dataframe, uma lista de valores das colunas, ou não informar argumentos para ver todas as colunas.")
        
        else:
            lista_num = []
            lista_categ = []
            
            for i in colunas:
                if i in self.lista_numericas:
                    lista_num.append(i)
                
                else:
                    lista_categ.append(i)
            
            if len(lista_num) == 0:
                return self.df[lista_categ].describe()
            
            elif len(lista_categ) == 0:
                return self.df[lista_num].describe()
            
            else:       
                return self.df[lista_num].describe(), self.df[lista_categ].describe()
        
        return self.df[colunas].describe()
    
    
    # Analisando as colunas numéricas
    def descricao_numerica(self):
        return self.df[self.lista_numericas].describe()
    
    
    # Analisando as colunas categóricas
    def descricao_categorica(self):
        return self.df[self.lista_categoricas].describe()
    
    
    # Contagem de valores das colunas categóricos
    def contagem_categorica(self) -> list:
        lista_dfs = []
        for i in self.lista_categoricas:
            df_aux = pd.DataFrame(self.df[i].value_counts().reset_index())
            df_aux.columns = [i, "Soma"]
            df_aux["%"] = round(100 * df_aux["Soma"] / self.df.shape[0], 2)
        
        lista_dfs.append(df_aux)
        return lista_dfs
    
    
    # Contagem de valores das colunas numéricas
    def contagem_numerica(self):
        lista_dfs = []
        for i in self.lista_numericas:
            df_aux = pd.DataFrame(self.df[i].value_counts().reset_index())
            df_aux.columns = [i, "Soma"]
            df_aux["%"] = round(100 * df_aux["Soma"] / self.df.shape[0], 2)
            lista_dfs.append(df_aux)
        return lista_dfs
    
    
    # Gráfico de distribuição das variáveis categóricas
    def grafico_dist_categ(self,):
        for coluna in self.lista_categoricas:
            num_valores = self.__valores_categoricos
            tamanho = self.df[coluna].nunique()
            
            if tamanho < num_valores:
                num_valores = tamanho

            elif tamanho > num_valores:
                print(f"A quantidade de valores únicos da coluna: {coluna} é muito grande.")
                print(f"Serão exibidos os {num_valores} valores mais relevantes.")
            
            fig_dinamic =  num_valores/5
            
            if fig_dinamic < 5:
                fig_dinamic = 5
            
            plt.figure(figsize=(10,fig_dinamic))
            sns.set_style(plot_style)
            sns.countplot(y=self.df[coluna], 
                          legend=False, 
                          color = color_palette[0], 
                          order=(pd.Series(self.df[coluna].value_counts(ascending=False).reset_index()[0:num_valores][coluna])))
            plt.title(f"Distribuição de {coluna}")
            plt.tight_layout()
            plt.show()
    
    
    # Gráfico de distribuição das variáveis numéricas
    def grafico_dist_num(self):
        for coluna in self.lista_numericas:
            plt.figure(figsize=(5, 5))
            sns.set_style(plot_style)
            sns.histplot(self.df[coluna], kde=True, color = color_palette[0])
            plt.title(f"Distribuição de {coluna}")
            plt.tight_layout()
            plt.show()
    
    
    # Diagrama de caixa das variáveis numéricas
    def grafico_diagrama_caixa(self):
        count_cores = 0
        for coluna in self.lista_numericas:
            if count_cores > len(color_palette):
                count_cores = 0
            plt.figure(figsize=(2.5,5))
            sns.set_style(plot_style)
            sns.boxplot(self.df[coluna], color = color_palette[count_cores])
            plt.title(f"Boxplot de {coluna}")
            plt.tight_layout()
            plt.show()
            count_cores += 1
    
    
    # Matriz de correlação das variáveis numéricas
    def matriz_correlacao(self):
        matriz_corr = self.df[self.lista_numericas].corr()
        matriz_corr_HM = matriz_corr.stack().reset_index()
        matriz_corr_HM.columns = ["feature_x", "feature_y", "Correlação"]
        matriz_corr_HM["Correlação Absoluta"] = abs(matriz_corr_HM["Correlação"])
        
        plt.figure(figsize=(10,10))
        sns.set_theme(style=plot_style)
        heatm = sns.relplot(data=matriz_corr_HM, 
                            x="feature_x", 
                            y="feature_y", 
                            hue="Correlação", 
                            size="Correlação Absoluta", 
                            palette="coolwarm",
                            hue_norm=(-1,1), 
                            edgecolor=".7", 
                            height=5, 
                            aspect=2, 
                            sizes=(0,500))
        
        heatm.set(xlabel="", ylabel="", )
        heatm.despine(left=True, bottom=True)
        for i in heatm.axes.flat:
            i.set_xticks(i.get_xticks())
            i.set_xticklabels(i.get_xticklabels(), rotation=90)
    
    
    # Relação de pares das variáveis numéricas
    def grafico_relacao_pares(self):
        plt.figure(figsize=(10,10))
        sns.set_theme(style=plot_style)
        sns.set_palette = color_palette
        sns.pairplot(data=self.df[self.lista_numericas])
        plt.show()
    
    
    # Relatório do Dataset
    def relatorio(self) -> None:
        
        print(f"ANÁLISE DO CONJUNTO DE DADOS DO DATAFRAME {self.arquivo}.\n")
        print("Informções Gerais:")
        self.informacoes()
        print("\n")
        
        print(f"REALIZANDO A CONTAGEM DOS VALORES NULOS.\n")
        display(self.contagem_nulos())
        print ("\n")       
        
        print(f"REALIZANDO A CONTAGEM DOS VALORES ÚNICOS.\n")
        display(self.contagem_unicos())
        print("\n") 
        
        if len(self.lista_numericas) >= 1:
            print(f"INFORMAÇÕES DAS COLUNAS NUMÉRICAS.")
            display(self.descricao_numerica())
            print("\n")
        
            print("CONTAGEM DOS VALORES NUMÉRICOS:")
            lista_dfs_num = self.contagem_numerica()
            for df in lista_dfs_num:
                display(df)
            print("\n")
        
            print("DISTRIBUIÇÃO DOS VALORES NUMÉRICOS:")
            self.grafico_dist_num()
            print("\n") 

            print("DIAGRAMA DE CAIXA DOS VALORES NUMÉRICOS:")
            self.grafico_diagrama_caixa()
            print("\n")

            print("RELAÇÃO DE PARES DOS VALORES NUMÉRICOS")
            self.grafico_relacao_pares()
            print("\n")


            print("MATRIZ DE CORRELAÇÃO:")
            if len(self.lista_numericas) >= 2:
                self.matriz_correlacao()
            else:
                print("Não foi possível fazer uma matriz de correlação.")
            print("\n")

        else:
            print("DATASET SEM COLUNAS NUMÉRICAS.")

        if len(self.lista_categoricas) >= 1:
            print(f"INFORMAÇÕES DAS COLUNAS CATEGÓRICAS.")
            display(self.descricao_categorica())
            print ("\n")
        
            print("CONTAGEM DOS VALORES CATEGÓRICOS:")
            lista_dfs_categ = self.contagem_categorica()
            for df in lista_dfs_categ:
                display(df)
            print("\n")
        
            print("DISTRIBUIÇÃO DOS VALORES CATEGÓRICOS:")
            self.grafico_dist_categ()
            print("\n") 
        
        else:
            print("DATASET SEM COLUNAS CATEGÓRICAS.")

    @property
    def valores_categoricos(self):
        return self.__valores_categoricos
    
    @valores_categoricos.setter
    def valores_categoricos(self, novo_valor):
        self.__valores_categoricos = novo_valor