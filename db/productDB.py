from db import clientPS

from model.Product import Product as Product

import json

from typing import List

import csv

from fastapi import UploadFile

from datetime import datetime

import pandas as pd

def consulta():
    
    try:
        conn = clientPS.client()
        
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM PRODUCT")
        
        data= cur.fetchall()
        
    except Exception as e:
        print(f"ERRORRRRR: {e}")
        
    finally:    
        conn.close()
    
    return data


def consultaiD(id:int):

    conn = clientPS.client()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.product WHERE product_id = %s", (id,))
    product = cur.fetchone()
    conn.close()
    if product:
        return {
            "product_id": product[0],
            "name": product[1],
            "description": product[2],
            "company": product[3],
            "price": product[4],
            "units": product[5],
            "subcategory_id": product[6],
            "created_at": product[7],
            "updated_at": product[8],
            "img": product[9]
        }
    return None

def inserta(prod: Product):
    try:
        conn = clientPS.client()
        
        cur = conn.cursor()
        
        cur.execute("""INSERT INTO public.product (
                            product_id, name, img, description, company, price, units, subcategory_id, created_at, updated_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )""", (
                            prod.product_id, prod.name, prod.img, prod.description, prod.company,
                            prod.price, prod.units, prod.subcategory_id, prod.created_at, prod.updated_at
                        ))
        
        conn.commit()

    except Exception as e:
        print(f"ERRORRRRR: {e}")
        
    finally:    
        conn.close()
    
def edit(product_id: int, prod: Product) -> bool:
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        cur.execute("""
            UPDATE public.product
            SET name = %s, description = %s, company = %s, price = %s, units = %s, subcategory_id = %s, updated_at = %s ,img = %s
            WHERE product_id = %s
        """, (prod.name, prod.description, prod.company, prod.price, prod.units, prod.subcategory_id, prod.updated_at, prod.img, product_id))
        conn.commit()
        cur.close()
        conn.close()
        return cur.rowcount > 0
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    

def borrar(id):
    try:
        conn = clientPS.client()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM PRODUCT WHERE product_id = {id}")
        conn.commit()
        
        if cur.rowcount == 0:
            return False  # No rows affected, product not found
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False  # Return False if an error occurs
        
    finally:
        conn.close()
    
    return True  # Return True if the product was successfully deleted


def productAll():
    try:
        # Establiment de connexió amb la base de dades.
        conn = clientPS.client()
        
        # Creació d'un objecte cursor per executar consultes SQL.
        cur = conn.cursor()
        
        # Execució de la consulta SQL per recuperar tots els productes amb informació rellevant.
        cur.execute("""
            SELECT c.name AS category_name, 
                   sc.name AS subcategory_name, 
                   p.name AS product_name, 
                   p.company AS product_brand, 
                   p.price
            FROM Product p
            INNER JOIN Subcategory sc ON p.subcategory_id = sc.subcategory_id
            INNER JOIN Category c ON sc.category_id = c.category_id
            """)
        
        # Obtenció de les dades recuperades de la consulta.
        data = cur.fetchall()
    
    except Exception as e:
        # Captura d'errors i impressió del missatge d'error.
        print(f"ERROR: {e}")
        return None
    
    finally:
        # Tancament de la connexió a la base de dades.
        conn.close()

    # Creació de la llista de productes i formatatge de les dades en un diccionari.
    products_list = []
    for row in data:
        # Check if the length of the row is as expected
        if len(row) >= 5:
            product_dict = {
                'Nom_Categoria': row[0],
                'Nom_Subcategoria': row[1],
                'Nom_Producte': row[2],
                'Marca_Producte': row[3],
                'Preu': float(row[4])
            }
            products_list.append(product_dict)

    # Returning the list of dictionaries directly, not converting it to JSON here.
    return products_list

# Funció per importar una categoria a la base de dades.
def impCategoria(category_id, name):
    try: 
        # Establiment de connexió amb la base de dades.
        conn = clientPS.client()
        
        # Creació d'un objecte cursor per executar consultes SQL.
        cur = conn.cursor()
        
        # Obtenció de l'hora actual per a la data.
        tiempo_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cur.execute(f"""SELECT * FROM category WHERE category_id={category_id};""")
        
        # Comprovació si la categoria ja existeix i actualització o inserció de la mateixa.
        if(cur.fetchone() is not None):
            cur.execute(f"""UPDATE category
                        SET category_id={category_id}, name='{name}', updated_at='{tiempo_actual}'
	                    WHERE category_id={category_id};""")
        else:
            cur.execute(f"INSERT INTO category (category_id, name, created_at, updated_at) VALUES ({category_id}, '{name}', '{tiempo_actual}', '{tiempo_actual}')")
        
        # Confirmació dels canvis fets a la base de dades.
        conn.commit()
        
    except Exception as e:
        # Captura d'errors i impressió del missatge d'error.
        print(f'Error conexió {e}')
        
    finally:
        # Tancament de la connexió a la base de dades.
        conn.close()

# Funció per importar una subcategoria a la base de dades.
def impSubcategory(subcategory_id, name, category_id):
    try:
        # Establiment de connexió amb la base de dades.
        conn = clientPS.client()
        
        # Creació d'un objecte cursor per executar consultes SQL.
        cur = conn.cursor()
        
        # Obtenció de l'hora actual per a la data.
        tiempo_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')       
        
        cur.execute(f"""SELECT * FROM subcategory WHERE subcategory_id={subcategory_id};""")
        
        # Comprovació si la subcategoria ja existeix i actualització o inserció de la mateixa.
        if(cur.fetchone() is not None):
            cur.execute(f"""UPDATE subcategory
                        SET subcategory_id={subcategory_id}, name='{name}', category_id={category_id}, updated_at='{tiempo_actual}'
	                    WHERE category_id={category_id};""")
        else:
            cur.execute(f"INSERT INTO subcategory (subcategory_id, name, category_id, created_at, updated_at) VALUES ({subcategory_id}, '{name}', {category_id}, '{tiempo_actual}', '{tiempo_actual}')")
        
        # Confirmació dels canvis fets a la base de dades.
        conn.commit()
        
    except Exception as e:
        # Captura d'errors i impressió del missatge d'error.
        print(f'Erroe conexió {e}')
        
    finally:
        # Tancament de la connexió a la base de dades.
        conn

# Función para crear o actualizar un producto desde un archivo CSV.
def crearProducteCSV(product_id, name, description, company, price, units, subcategory_id):
    try:
        # Establecer conexión con la base de datos.
        conn = clientPS.client()
        
        # Crear un cursor para ejecutar consultas SQL.
        cur = conn.cursor()
        
        # Obtener la fecha y hora actual en el formato especificado.
        tiempo_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cur.execute(f"""SELECT * FROM product WHERE product_id={product_id};""")
        
        # Comprobar si el producto ya existe y actualizar o insertar según corresponda.
        if(cur.fetchone() is not None):
            cur.execute(f"""UPDATE product
                        SET product_id={product_id}, name='{name}', description='{description}', company='{company}', price={price}, units={units} , subcategory_id={subcategory_id}, updated_at='{tiempo_actual}'
	                    WHERE product_id={product_id};""")
        else:
            cur.execute(f"INSERT INTO product (product_id, name, description, company, price, units, subcategory_id, created_at, updated_at) VALUES ({product_id}, '{name}', '{description}', '{company}', {price}, {units}, {subcategory_id}, '{tiempo_actual}', '{tiempo_actual}')")
        
        # Confirmar los cambios en la base de datos.
        conn.commit()
        
    except Exception as e:
        # Capturar errores e imprimir el mensaje de error.
        print(f'Error de conexión: {e}')
        
    finally:
        # Cerrar la conexión a la base de datos.
        conn.close()

# Función para cargar datos masivos desde un archivo CSV.
def pujarCSV(fitcherCSV): 
    try:
        # Establecer conexión con la base de datos.
        conn = clientPS.client()
        
        # Leer el archivo CSV especificado.
        df = pd.read_csv(fitcherCSV.file, header=0 )
        
        # Iterar sobre cada fila del DataFrame y procesar los datos.
        for index, row in df.iterrows():
            fila = row.to_dict()
            
            # Importar la categoría y la subcategoría si no existen.
            impCategoria(fila["id_categoria"], fila["nom_categoria"])
            impSubcategory(fila["id_subcategoria"], fila["nom_subcategoria"], fila["id_categoria"])
            
            # Crear o actualizar el producto en la base de datos.
            crearProducteCSV(fila["id_producto"], fila["nom_producto"], fila["descripcion_producto"], fila["companyia"], fila["precio"], fila["unidades"], fila["id_subcategoria"])

        # Confirmar la carga masiva de datos.
        conn.commit()
        return "Has subido el fitcher correte"
    
    except Exception as e:
        # Capturar errores e imprimir el mensaje de error.
        return f"Error al cargar datos masivos: {e}"
        
    finally:
        # Cerrar la conexión a la base de datos.
        conn.close()