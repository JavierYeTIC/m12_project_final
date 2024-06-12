def product_schema(prod) -> dict:
    return {"product_id": str(prod[0]),
            "name": prod[1],
            "description":prod[2],
            "company":prod[3],
            "price":prod[4],
            "units":prod[5],
            "subcategory_id":prod[6],
            "created_at":prod[7],
            "updated_at":prod[8]
            }
    
def products_schema(prods)->dict:
    return [product_schema(prod) for prod in prods]