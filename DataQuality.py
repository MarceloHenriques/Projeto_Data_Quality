# Bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cores
color_palette = sns.set_palette("dark")
plot_style = sns.set_style("darkgrid")

class DataQuality:
    def __init__ (self, csv_file):
        self.arquivo = csv_file
        self.df = pd.read_csv(f"./{csv_file}")
        self.lista_numericas = list(self.df.select_dtypes(include=np.number).columns)
        self.lista_categoricas = list(self.df.select_dtypes(exclude=np.number).columns)


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
    def descricao_personalizada(self, colunas:list = None):
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


    # Contagem de valores categóricos
    def contagem_categorica(self) -> list:
        lista_dfs = []
        for i in self.lista_categoricas:
            df_aux = pd.DataFrame(self.df[i].value_counts().reset_index())
            df_aux.columns = [i, "Soma"]
            df_aux["%"] = round(100 * df_aux["Soma"] / self.df.shape[0], 2)

            lista_dfs.append(df_aux)
        return lista_dfs


    def contagem_numerica(self):
        lista_dfs = []
        for i in self.lista_numericas:
            df_aux = pd.DataFrame(self.df[i].value_counts().reset_index())
            df_aux.columns = [i, "Soma"]
            df_aux["%"] = round(100 * df_aux["Soma"] / self.df.shape[0], 2)
            lista_dfs.append(df_aux)
        return lista_dfs


    def grafico_dist_categ(self):
        plt.figure(figsize=(20,10))
        for coluna in self.lista_categoricas:
            sns.set_style(plot_style)
            sns.countplot(y=self.df[coluna], legend=False, color= color_palette)
            plt.title(f"Distribuição de {coluna}")
            plt.show()
            #TODO vincular tamanho com quantidade de nomes unicos


    def grafico_dist_num(self):
        plt.figure(figsize=(20,10))
        for coluna in self.lista_numericas:
            sns.set_style(plot_style)
            sns.histplot(self.df[coluna], kde=True, color = color_palette)
            plt.title(f"Distribuição de {coluna}")
            plt.show()


    def grafico_diagrama_caixa(self):
        print("Boxplot das Colunas Numéricas:")
        plt.figure(figsize=(5,10))
        count_cores = 0
        for coluna in self.lista_numericas:
            if count_cores > len(sns.color_palette()):
                count_cores = 0
            sns.set_style(plot_style)
            sns.boxplot(self.df[coluna], color = color_palette[count_cores])
            plt.title(f"Boxplot de {coluna}")
            plt.show()
            count_cores += 1


    def matriz_correlacao(self):
        matriz_corr = self.df[self.lista_numericas].corr()
        matriz_corr_HM = matriz_corr.stack().reset_index()
        matriz_corr_HM.columns = ["feature_x", "feature_y", "Correlação"]
        matriz_corr_HM["Correlação Absoluta"] = abs(matriz_corr_HM["Correlação"])

        print("Matriz de Correlação:")
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



    #TODO Pairplot
    #def grafico_relacao_pares(self):
            #print("Relaçao de Pares:")
            #plt.figure(figsize=(10,10))
            #sns.pairplot()



    #TODO Relatório
    def relatorio(self) -> None:
        print (f"ANÁLISE DO CONJUNTO DE DADOS DO DATAFRAME {self.arquivo}.\n")
        print ("Informções Gerais:")
        self.informacoes()
        print ("\n")
        

        print (f"REALIZANDO A CONTAGEM DOS VALORES NULOS.\n")
        display (self.contagem_nulos())
        print ("\n")       
        
        print (f"REALIZANDO A CONTAGEM DOS VALORES ÚNICOS.\n")
        display (self.contagem_unicos())
        print ("\n") 
        
        print (f"INFORMAÇÕES DAS COLUNAS NUMERICAS.")
        display (self.descricao_numerica())
        print ("\n")    
        print ("CONTAGEM DOS VALORES NUMERICOS:")
        display (self.contagem_numerica())
        print ("\n")  
        print ("INFORMAÇÕES GRÁFICAS:")
        display (self.grafico_dist_num())
        print ("\n") 
        
        print (f"INFORMAÇÕES DAS COLUNAS CATEGORICAS.")
        display (self.descricao_categorica())
        print ("\n") 
        print ("CONTAGEM DOS VALORES CATEGORICOS:")
        display (self.contagem_categorica())
        print ("\n")
        print ("INFORMAÇÕES GRÁFICAS:")
        display(self.grafico_dist_categ())
        print ("\n") 
        
        
        
        