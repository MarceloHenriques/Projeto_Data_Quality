class DataQuality:
    def __init__ (self, csv_file):
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        self.df = pd.read_csv(f"./{csv_file}")
        self.lista_numericas = []
        self.lista_categoricas = []
        
        #iteração para adicionar nas listas
        for coluna in self.df.columns:
            if pd.api.types.is_numeric_dtype (self.df[coluna]): # PD.API.TYPES, CONVERSAR COM O NICOLAS
                self.lista_numericas.append(coluna)# Adicionando na lista se for valor numerico
            else:
                self.lista_categoricas.append(coluna) # Adiciona a lista de valores categorico 

        
    # def analise_numerica(self): # Analisando as colunas numericas
    #     self.separar_features()
    #     return self.df.describe()
    
    # def contagem_nulos(self): # Exibe a contagem dos valores nulos por coluna
    #     return self.df.isnull().sum()
    
    # def contagem_unicos(self): # Exibindo a contagem dos valores unicos por coluna
    #     return self.df.nunique()
    
    # def descricao(self, lista_colunas = self.lista_numericas):
        #df[lista_colunas].describe()