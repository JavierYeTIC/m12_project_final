def product_schema(prods) -> list:
    return [
        {
            "nom_categoria": prod.get('Nom_Categoria'),
            "nom_subcategoria": prod.get('Nom_Subcategoria'),
            "nom_product": prod.get('Nom_Producte'),
            "company": prod.get('Marca_Producte'),
            "price": prod.get('Preu'),
        }
        for prod in prods
    ]