from core.firebaseHelper import db


def get_store_by_id(store_id: str):


    doc_ref = db.collection("stores").document(store_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None

def get_stores_by_ids(ids: list) -> list:
    stores = []
    for pid in ids:
        doc = db.collection("stores").document(pid).get()
        if doc.exists:
            stores.append(doc.to_dict())
    return stores