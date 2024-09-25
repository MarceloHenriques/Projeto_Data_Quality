import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataQuality:
    def __init__ (self, csv_file):
        self.df = pd.read_csv(f"./{csv_file}")
        self.lista_numericas = ["S.NO", "Current Rank", "Previous Year Rank", "Year", "earnings ($ million)"] #TODO ALTERAR
        self.lista_categoricas = ["Name", "Nationality", "Sport"] #TODO ALTERAR
        #iteração para adicionar nas listas #TODO


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
                print("Variáveis Numéricas:")
                display(self.df[lista_num].describe())

                print(f"Variáveis Categóricas:")
                display(self.df[lista_categ].describe())
                        
                return self.df[lista_num].describe(), self.df[lista_categ].describe()
    
        return self.df[colunas].describe()
    

    # Analisando as colunas numéricas
    def descricao_numerica(self):
        return self.df[self.lista_numericas].describe()
    

    # Analisando as colunas categóricas
    def descricao_categorica(self):
        return self.df[self.lista_categoricas].describe()


    ############
    #TODO contagem personalizada
    ############

    # Contagem de valores categóricos
    def contagem_categorica(self):
        lista_dfs = []
        for i in self.lista_categoricas:
            df_aux = pd.DataFrame(self.df[i].value_counts().reset_index())
            print(f"Coluna: {i}")
            display(df_aux)
            lista_dfs.append(df_aux)
        return lista_dfs
    
    def contagem_numerica(self):
        lista_dfs = []
        for i in self.lista_numericas:
            df_aux = pd.DataFrame(self.df[i].value_counts().reset_index())
            print(f"Coluna: {i}")
            display(df_aux)
            lista_dfs.append(df_aux)
        return lista_dfs


    # Exibe a contagem dos valores nulos por coluna
    def contagem_nulos(self): 
        nulos = pd.DataFrame(self.df.isnull().sum())
        nulos.columns = ["Nulos"]
        return nulos
        
    

    # Exibindo a contagem dos valores unicos por coluna
    def contagem_unicos(self):
        unicos = pd.DataFrame(self.df.nunique())
        unicos.columns = ["Unicos"]
        return unicos
