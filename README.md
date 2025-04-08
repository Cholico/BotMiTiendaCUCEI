# Proyecto de Chatbot Recomendador

Este proyecto implementa un chatbot diseñado para responder preguntas relacionadas con productos y tiendas, utilizando recomendaciones basadas en embeddings y FAISS (Facebook AI Similarity Search). El bot puede procesar preguntas sobre productos, categorías, tiendas y más, proporcionando respuestas relevantes usando Firestore como base de datos.

## Funcionalidades

- **Respuestas a consultas sobre productos:** El bot recomienda productos basados en preguntas sobre precio, categorías y otros filtros.
- **Recomendaciones de tiendas:** Proporciona información sobre tiendas disponibles y sus características.
- **Embeddings y similitudes:** Utiliza embeddings generados por el modelo `SentenceTransformer` para identificar consultas similares y mejorar la precisión de las respuestas.
- **Manejo de saludos:** El bot reconoce saludos comunes y responde de forma amistosa y personalizada.

## Estructura del Proyecto

├── src │ ├── controllers # Lógica para manejar las rutas de la API │ ├── core # Funciones y clases base, incluyendo el modelo de embeddings │ ├── data │ │ ├── model # Modelos de datos, como productos y tiendas │ │ └── service # Servicios de acceso a la base de datos (Firestore) │ ├── domain │ │ ├── model # Clases de dominio, como productos y tiendas │ │ └── repository # Repositorios para interactuar con la base de datos │ ├── routes # Rutas de la API, incluidas las consultas y recomendaciones │ ├── embeddings # Archivos y lógica para manejar los embeddings y FAISS │ └── main.py # Archivo principal para inicializar el servidor └── requirements.txt # Dependencias del proyecto

markdown
Copiar
Editar

## Tecnologías Utilizadas

- **Python:** Lenguaje principal para el desarrollo del bot.
- **FastAPI:** Framework para construir la API que sirve como backend para el chatbot.
- **Firestore:** Base de datos NoSQL de Firebase para almacenar información sobre productos y tiendas.
- **FAISS:** Biblioteca de Facebook para realizar búsquedas de similitud en embeddings.
- **SentenceTransformer:** Modelo de transformadores para generar embeddings a partir de texto.

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/usuario/chatbot-recomendador.git
   cd chatbot-recomendador
Instalar las dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
Configurar Firestore: Asegúrate de tener un proyecto de Firebase y de configurar las credenciales de Firestore siguiendo las instrucciones de Firebase.

Cargar los embeddings: Al iniciar el servidor, se cargará el modelo de embeddings utilizando SentenceTransformer. No es necesario hacerlo manualmente.

Ejecutar el servidor:

bash
Copiar
Editar
uvicorn src.main:app --reload
El servidor estará corriendo en http://127.0.0.1:8000.

Uso
Consultas de ejemplo
El bot responderá a preguntas como:

"¿Tienes pizzas?" → El bot buscará productos similares a pizzas.

"Recomiéndame algo barato." → El bot recomendará productos dentro de un rango de precios bajo.

"¿Dónde puedo comprar sushi?" → El bot proporcionará información sobre tiendas que venden sushi.

Rutas disponibles
POST /query
Procesa una consulta del usuario y responde con una recomendación (producto o tienda).

GET /products/{product_id}/similar
Devuelve productos similares a uno dado, basándose en su ID y usando FAISS.

Contribuciones
Las contribuciones son bienvenidas. Si tienes alguna sugerencia o mejoras, por favor, abre un issue o envía un pull request.

Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
