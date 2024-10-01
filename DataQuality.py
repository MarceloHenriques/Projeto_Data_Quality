# Bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

# Cores
color_palette = sns.color_palette("dark")
plot_style = sns.set_style("darkgrid")

class DataQuality:
    def __init__ (self, csv_file: str) -> None:
        self.arquivo = csv_file
        self.df = pd.read_csv(f"./{csv_file}")
        self.lista_numericas = list(self.df.select_dtypes(include=np.number).columns)
        self.lista_categoricas = list(self.df.select_dtypes(exclude=np.number).columns)
        self.__valores_categoricos = 20
        self.__head_tail = 5
    
    
    # Informações do Dataframe
    def informacoes(self) -> pd.DataFrame:
        info = pd.DataFrame(data=self.df.dtypes).reset_index()
        info.columns = ["Colunas", "Tipo de Dados"]
        info["Nulos Soma"] = info["Colunas"].map(self.df.isnull().sum())
        info["Nulos %"] = round(100 * info["Nulos Soma"] / self.df.shape[0], 2)
        
        info["Unicos Soma"] = info["Colunas"].map(self.df.nunique())
        info["Unicos Soma"] = info["Colunas"].map(self.df.nunique())
        info["Unicos %"] = round(100 * info["Unicos Soma"] / self.df.shape[0], 2)
        return(info)
    
    
    # Linhas duplicadas
    def duplicadas(self) -> pd.DataFrame:
        duplicadas_totais = self.df[self.df.duplicated(keep=False)].sort_values([self.df.columns[0]])
        return duplicadas_totais
    
    
    # Analisando as colunas numéricas
    def descricao_numerica(self) -> pd.DataFrame:
        return self.df[self.lista_numericas].describe()
    

    # Contagem de valores das colunas numéricas
    def contagem_numerica(self) -> list:
        lista_dfs = []
        for i in self.lista_numericas:
            df_aux = pd.DataFrame(self.df[i].value_counts().reset_index())
            df_aux.columns = [i, "Soma"]
            df_aux["%"] = round(100 * df_aux["Soma"] / self.df.shape[0], 2)
            lista_dfs.append(df_aux)
        return lista_dfs
    
    
    # Gráfico de distribuição das variáveis numéricas
    def grafico_dist_num(self, coluna:str) -> None:
        plt.figure(figsize=(5, 5))
        sns.set_style(plot_style)
        sns.histplot(self.df[coluna], kde=True, color = color_palette[0])
        plt.title(f"Distribuição de '{coluna}'")
        plt.tight_layout()
        plt.show()
    
    
    # Diagrama de caixa das variáveis numéricas
    def grafico_diagrama_caixa(self, coluna:str) -> None:
        plt.figure(figsize=(2.5,5))
        sns.set_style(plot_style)
        sns.boxplot(self.df[coluna], color = color_palette[0])
        plt.title(f"Boxplot de '{coluna}'")
        plt.tight_layout()
        plt.show()
    
    
    # Matriz de correlação das variáveis numéricas
    def matriz_correlacao(self) -> None:
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
        plt.show()
    
    
    # Relação de pares das variáveis numéricas
    def grafico_relacao_pares(self) -> None:
        plt.figure(figsize=(10,10))
        sns.set_theme(style=plot_style)
        sns.set_palette = color_palette
        sns.pairplot(data=self.df[self.lista_numericas])
        plt.show()
    
    
    # Analisando as colunas categóricas
    def descricao_categorica(self) -> pd.DataFrame:
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
    
    
    # Gráfico de distribuição das variáveis categóricas
    def grafico_dist_categ(self, coluna:str) -> None:
        num_valores = self.__valores_categoricos
        tamanho = self.df[coluna].nunique()
        
        if tamanho < num_valores:
            num_valores = tamanho
        
        elif tamanho > num_valores:
            print(f"A quantidade de valores únicos da coluna '{coluna}' é muito grande.")
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
    
    
    # Relatório do Dataset
    def relatorio(self) -> None:
        
        print(f"ANÁLISE DO CONJUNTO DE DADOS DO DATAFRAME {self.arquivo}.\n")
        print("INFORMAÇÕES GERAIS:\n")
        
        print(f"Tamanho do Dataset:\n{self.df.shape[0]} linhas;\n{self.df.shape[1]} colunas;\n")
        display(self.informacoes())
        print("\n")
        
        print(f"Exibindo as {self.__head_tail} primeiras linhas:\n")
        display(self.df.head(self.__head_tail))
        print("\n")
        
        print(f"Exibindo as {self.__head_tail} últimas linhas:\n")
        display(self.df.tail(self.__head_tail))
        print("\n")
        
        print("Colunas duplicadas no Dataset:\n")
        df_duplicada = self.duplicadas()
        if df_duplicada.shape[0] == 0:
            print(f"O Dataset não possui linhas duplicadas.\n")
            print("\n")
        else:
            print(f"O Dataset possui {df_duplicada.shape[0]} linhas duplicadas.")
            print(f"As linhas duplicadas correspondem a {round(100 * df_duplicada.shape[0] / self.df.shape[0], 2)}% do Dataset.\n")
            display(df_duplicada.head(self.__head_tail))
            print("\n")
            display(df_duplicada.tail(self.__head_tail))
            print("\n")
        
        if len(self.lista_numericas) >= 1:
            print(f"INFORMAÇÕES DAS COLUNAS NUMÉRICAS.\n")

            print(f"O Dataset possui as seguintes colunas numéricas: {self.lista_numericas}.\n")
            print("\n")

            print(f"Estatística descritiva das colunas numéricas:\n")
            display(self.descricao_numerica())
            print("\n")
            
            print("DISTRIBUIÇÃO DOS VALORES NUMÉRICOS:\n")

            lista_dfs_num = self.contagem_numerica()
            for df in lista_dfs_num:
                print(f"Análise da coluna '{df.columns[0]}'\n")
                display(df)
                print("\n")
                if df["Soma"].nunique() == 1:
                    print(f"A coluna '{df.columns[0]}' possui apenas valores únicos.\n")
                    print("\n")
                else:
                    self.grafico_dist_num(df.columns[0])
                    print("\n")
                    self.grafico_diagrama_caixa(df.columns[0])
                    print("\n")
            
            print("RELAÇÃO DE PARES DOS VALORES NUMÉRICOS:\n")

            self.grafico_relacao_pares()
            print("\n")
            
            print("MATRIZ DE CORRELAÇÃO:\n")

            if len(self.lista_numericas) >= 2:
                self.matriz_correlacao()
            else:
                print("Não foi possível fazer uma matriz de correlação.\n")
            print("\n")

        else:
            print("DATASET SEM COLUNAS NUMÉRICAS.\n")

        if len(self.lista_categoricas) >= 1:
            print(f"INFORMAÇÕES DAS COLUNAS CATEGÓRICAS.\n")

            print(f"O Dataset possui as seguintes colunas categóricas: {self.lista_categoricas}.\n")
            print("\n")
            
            print(f"Maiores frequências das colunas categóricas:\n")
            display(self.descricao_categorica())
            print ("\n")
        
            print("DISTRIBUIÇÃO DOS VALORES CATEGÓRICOS:\n")

            lista_dfs_categ = self.contagem_categorica()
            for df in lista_dfs_categ:
                print(f"Análise da coluna '{df.columns[0]}'\n")
                display(df)
                if df["Soma"].nunique() == 1:
                    print(f"A coluna '{df.columns[0]}' possui apenas valores únicos.\n")
                else:
                    self.grafico_dist_categ(df.columns[0])
            print("\n")
        
        else:
            print("DATASET SEM COLUNAS CATEGÓRICAS.\n")

    @property
    def valores_categoricos(self):
        return self.__valores_categoricos
    
    @valores_categoricos.setter
    def valores_categoricos(self, novo_valor):
        self.__valores_categoricos = novo_valor
    
    @property
    def valores_head_tail(self):
        return self.__valores_head_tail
    
    @valores_head_tail.setter
    def valores_head_tail(self, novo_valor):
        self.__valores_head_tail = novo_valor