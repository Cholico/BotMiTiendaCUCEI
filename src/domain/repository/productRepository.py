from core.firebaseHelper import db


def get_product_by_id(product_id: str):

    doc_ref = db.collection("products").document(product_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None

def get_products_by_ids(ids: list) -> list:
    products = []
    for pid in ids:
        doc = db.collection("products").document(pid).get()
        if doc.exists:
            products.append(doc.to_dict())
    return products