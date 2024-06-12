def product_schema(prods) -> list:
    return [
        {
            "product_id": str(prod[0]),
            "name": prod[1],
            "description": prod[2],
            "company": prod[3],
            "price": prod[4],
            "units": prod[5],
            "subcategory_id": prod[6],
            "created_at": prod[7],
            "updated_at": prod[8],
            "img": prod[9]
        }
        for prod in prods
    ]