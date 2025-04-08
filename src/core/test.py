
from core.firebaseHelper import db

productos = [
    {
        "id": "prod001",
        "name": "Pizza Margarita",
        "description": "Deliciosa pizza con salsa de tomate, mozzarella y albahaca fresca.",
        "image": "https://example.com/images/pizza_margarita.jpg",
        "price": 150,
        "quantity": 25,
        "store": {"id": "store001", "name": "La Cava Italiana"},
        "category": ["Italiana", "Pizza"],
        "discount": {
            "id": "disc001", "percentage": 10,
            "startDate": "2025-02-20T00:00:00Z", "endDate": "2025-02-28T23:59:59Z"
        },
        "rating": 4.5, "totalRating": 150, "totalReviews": 45,
        "paginationKey": "page1",
        "createdAt": "2025-02-15T12:00:00Z", "updatedAt": "2025-02-20T10:00:00Z"
    },
    {
        "id": "prod002",
        "name": "Sushi Roll Dragón",
        "description": "Anguila, aguacate y salsa teriyaki.",
        "image": "https://example.com/images/sushi_dragon.jpg",
        "price": 200,
        "quantity": 12,
        "store": {"id": "store002", "name": "Sushi Zen"},
        "category": ["Japonesa", "Sushi"],
        "discount": {
            "id": "disc002", "percentage": 15,
            "startDate": "2025-03-01T00:00:00Z", "endDate": "2025-03-10T23:59:59Z"
        },
        "rating": 4.7, "totalRating": 180, "totalReviews": 50,
        "paginationKey": "page1",
        "createdAt": "2025-02-18T12:00:00Z", "updatedAt": "2025-03-01T10:00:00Z"
    },
    {
        "id": "prod003",
        "name": "Bife de Chorizo",
        "description": "Corte argentino con chimichurri.",
        "image": "https://example.com/images/bife_chorizo.jpg",
        "price": 320,
        "quantity": 8,
        "store": {"id": "store003", "name": "Asador Argentino"},
        "category": ["Argentina", "Carnes"],
        "discount": {
            "id": "disc003", "percentage": 20,
            "startDate": "2025-02-25T00:00:00Z", "endDate": "2025-03-05T23:59:59Z"
        },
        "rating": 4.8, "totalRating": 220, "totalReviews": 60,
        "paginationKey": "page1",
        "createdAt": "2025-02-20T12:00:00Z", "updatedAt": "2025-03-01T10:00:00Z"
    },
    {
        "id": "prod004",
        "name": "Tortilla Española",
        "description": "Papas, huevos y cebolla caramelizada.",
        "image": "https://example.com/images/tortilla_espanola.jpg",
        "price": 90,
        "quantity": 30,
        "store": {"id": "store004", "name": "Bodega Española"},
        "category": ["Española", "Tapas"],
        "discount": {
            "id": "disc004", "percentage": 5,
            "startDate": "2025-03-01T00:00:00Z", "endDate": "2025-03-07T23:59:59Z"
        },
        "rating": 4.6, "totalRating": 140, "totalReviews": 40,
        "paginationKey": "page1",
        "createdAt": "2025-02-22T12:00:00Z", "updatedAt": "2025-03-01T10:00:00Z"
    },
    {
        "id": "prod005",
        "name": "Tacos al Pastor",
        "description": "Cerdo marinado y piña con salsa verde.",
        "image": "https://example.com/images/tacos_al_pastor.jpg",
        "price": 80,
        "quantity": 18,
        "store": {"id": "store005", "name": "Tacos y Salsas"},
        "category": ["Mexicana", "Tacos"],
        "discount": {
            "id": "disc005", "percentage": 12,
            "startDate": "2025-03-02T00:00:00Z", "endDate": "2025-03-12T23:59:59Z"
        },
        "rating": 4.5, "totalRating": 160, "totalReviews": 55,
        "paginationKey": "page1",
        "createdAt": "2025-02-25T12:00:00Z", "updatedAt": "2025-03-02T10:00:00Z"
    },
    {
        "id": "prod006",
        "name": "Fajitas de Pollo",
        "description": "Fajitas servidas con tortillas y guacamole.",
        "image": "https://example.com/images/fajitas.jpg",
        "price": 180,
        "quantity": 22,
        "store": {"id": "store006", "name": "La Parrilla Mexicana"},
        "category": ["Mexicana", "Parrilla"],
        "discount": {
            "id": "disc006", "percentage": 10,
            "startDate": "2025-03-05T00:00:00Z", "endDate": "2025-03-15T23:59:59Z"
        },
        "rating": 4.6, "totalRating": 160, "totalReviews": 50,
        "paginationKey": "page2",
        "createdAt": "2025-02-28T12:00:00Z", "updatedAt": "2025-03-05T10:00:00Z"
    },
    {
        "id": "prod007",
        "name": "Croissant de Almendra",
        "description": "Crujiente croissant relleno de crema de almendra.",
        "image": "https://example.com/images/croissant.jpg",
        "price": 60,
        "quantity": 40,
        "store": {"id": "store007", "name": "Café de París"},
        "category": ["Francesa", "Repostería"],
        "discount": {
            "id": "disc007", "percentage": 5,
            "startDate": "2025-03-01T00:00:00Z", "endDate": "2025-03-10T23:59:59Z"
        },
        "rating": 4.7, "totalRating": 180, "totalReviews": 55,
        "paginationKey": "page2",
        "createdAt": "2025-02-28T08:00:00Z", "updatedAt": "2025-03-01T10:00:00Z"
    },
    {
        "id": "prod008",
        "name": "Hamburguesa BBQ",
        "description": "Carne a la parrilla con salsa BBQ y cebolla caramelizada.",
        "image": "https://example.com/images/burger_bbq.jpg",
        "price": 220,
        "quantity": 15,
        "store": {"id": "store008", "name": "Burger House"},
        "category": ["Americana", "Hamburguesas"],
        "discount": {
            "id": "disc008", "percentage": 15,
            "startDate": "2025-03-01T00:00:00Z", "endDate": "2025-03-07T23:59:59Z"
        },
        "rating": 4.5, "totalRating": 170, "totalReviews": 60,
        "paginationKey": "page2",
        "createdAt": "2025-02-25T12:00:00Z", "updatedAt": "2025-03-01T10:00:00Z"
    },
    {
        "id": "prod009",
        "name": "Pollo Tikka Masala",
        "description": "Pollo marinado con especias y salsa cremosa.",
        "image": "https://example.com/images/tikka_masala.jpg",
        "price": 250,
        "quantity": 10,
        "store": {"id": "store009", "name": "India Palace"},
        "category": ["India", "Curry"],
        "discount": {
            "id": "disc009", "percentage": 20,
            "startDate": "2025-03-01T00:00:00Z", "endDate": "2025-03-10T23:59:59Z"
        },
        "rating": 4.8, "totalRating": 200, "totalReviews": 70,
        "paginationKey": "page2",
        "createdAt": "2025-02-26T12:00:00Z", "updatedAt": "2025-03-01T10:00:00Z"
    },
    {
        "id": "prod010",
        "name": "Ensalada Vegana",
        "description": "Quinoa, espinacas, frutos secos y vinagreta balsámica.",
        "image": "https://example.com/images/ensalada_vegana.jpg",
        "price": 120,
        "quantity": 35,
        "store": {"id": "store010", "name": "Veggie Delight"},
        "category": ["Vegana", "Saludable"],
        "discount": {
            "id": "disc010", "percentage": 8,
            "startDate": "2025-03-01T00:00:00Z", "endDate": "2025-03-08T23:59:59Z"
        },
        "rating": 4.7, "totalRating": 190, "totalReviews": 65,
        "paginationKey": "page2",
        "createdAt": "2025-02-27T12:00:00Z", "updatedAt": "2025-03-01T10:00:00Z"
    }
]


tiendas = [
  {
      "id": "store001",
      "name": "La Cava Italiana",
      "description": "Auténticos sabores de Italia con pastas, pizzas y vinos seleccionados.",
      "email": "contacto@lacavaitaliana.com",
      "phoneNumber": "+34 612 345 678",
      "rating": 4.7,
      "totalRating": 980,
      "totalReviews": 230,
      "startTime": "12:00",
      "endTime": "23:00"
    },
    {
      "id": "store002",
      "name": "Sushi Zen",
      "description": "Experiencia japonesa con sushi fresco y ramen casero.",
      "email": "reservas@sushizen.com",
      "phoneNumber": "+34 613 456 789",
      "rating": 4.6,
      "totalRating": 750,
      "totalReviews": 200,
      "startTime": "13:00",
      "endTime": "22:00"
    },
    {
      "id": "store003",
      "name": "Asador Argentino",
      "description": "Cortes premium y empanadas artesanales.",
      "email": "contacto@asadorargentino.com",
      "phoneNumber": "+34 614 567 890",
      "rating": 4.8,
      "totalRating": 1200,
      "totalReviews": 280,
      "startTime": "12:30",
      "endTime": "23:30"
    },
    {
      "id": "store004",
      "name": "Bodega Española",
      "description": "Tapas y vinos de las mejores regiones de España.",
      "email": "contacto@bodegaespanola.com",
      "phoneNumber": "+34 633 321 654",
      "rating": 4.8,
      "totalRating": 1200,
      "totalReviews": 280,
      "startTime": "13:00",
      "endTime": "23:30"
    },
    {
      "id": "store005",
      "name": "Tacos y Salsas",
      "description": "Tacos auténticos y salsas picantes caseras.",
      "email": "contacto@tacosysalsas.com",
      "phoneNumber": "+34 615 678 901",
      "rating": 4.5,
      "totalRating": 900,
      "totalReviews": 210,
      "startTime": "13:00",
      "endTime": "22:30"
  },
  {
      "id": "store006",
      "name": "La Parrilla Mexicana",
      "description": "Auténticos antojitos mexicanos y parrilladas.",
      "email": "contacto@laparrillamex.com",
      "phoneNumber": "+34 616 789 012",
      "rating": 4.7,
      "totalRating": 1050,
      "totalReviews": 250,
      "startTime": "12:00",
      "endTime": "23:00"
  },
  {
      "id": "store007",
      "name": "Café de París",
      "description": "Repostería francesa y café gourmet.",
      "email": "contacto@cafedeparis.com",
      "phoneNumber": "+34 617 890 123",
      "rating": 4.6,
      "totalRating": 980,
      "totalReviews": 240,
      "startTime": "08:00",
      "endTime": "20:00"
    },
    {
      "id": "store008",
      "name": "Burger House",
      "description": "Hamburguesas artesanales y papas fritas.",
      "email": "contacto@burgerhouse.com",
      "phoneNumber": "+34 618 901 234",
      "rating": 4.5,
      "totalRating": 1100,
      "totalReviews": 260,
      "startTime": "12:00",
      "endTime": "22:00"
    },
    {
      "id": "store009",
      "name": "India Palace",
      "description": "Curry, tikka masala y más platos tradicionales.",
      "email": "contacto@indiapalace.com",
      "phoneNumber": "+34 619 012 345",
      "rating": 4.8,
      "totalRating": 1300,
      "totalReviews": 300,
      "startTime": "13:00",
      "endTime": "22:30"
    },
    {
      "id": "store010",
      "name": "Veggie Delight",
      "description": "Comida saludable y opciones veganas.",
      "email": "contacto@veggiedelight.com",
      "phoneNumber": "+34 620 123 456",
      "rating": 4.7,
      "totalRating": 900,
      "totalReviews": 220,
      "startTime": "11:00",
      "endTime": "21:00"
    }
]


def insertar_productos():
    for producto in productos:
        doc_ref = db.collection('products').document(producto['id'])
        doc_ref.set(producto)


def insertar_tiendas():
    for tienda in tiendas:
        doc_ref = db.collection('stores').document(tienda['id'])
        doc_ref.set(tienda)


def main():
    insertar_productos()
    insertar_tiendas()


if __name__ == "__main__":
    main()