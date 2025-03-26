# import pandas as pd

# def leer_hojas_excel(file_path):
#     hojas = pd.read_excel(file_path, sheet_name=None)
#     for nombre_hoja, df in hojas.items():
#         print(f"Hoja: {nombre_hoja}")
#         print(df.head(50))  # Imprime las primeras 50 filas de cada DataFrame
#     return hojas

# # Ejemplo de uso
# if __name__ == "__main__":
#     file_path = 'publicadores.xlsx'
#     hojas = leer_hojas_excel(file_path)

import pandas as pd

def leer_hojas_excel(file_path):
    return pd.read_excel(file_path, sheet_name=None)