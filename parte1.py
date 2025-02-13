from neo4j import GraphDatabase

# Configuración de la conexión
URI = "neo4j+s://55a06213.databases.neo4j.io"
AUTH = ("neo4j", "LLZGdkq6Yxv-jGfijw9nQLKugJ2LjjzVdBUYRidHK4o")

# Lista de usuarios
users = [
    {
        "label": "User",
        "name": "John Smith",
        "userId": "user1",
        "email": "john@example.com"
    },
    {
        "label": "User",
        "name": "Maria García",
        "userId": "user2",
        "email": "maria@example.com"
    },
    {
        "label": "User",
        "name": "David Sainz",
        "userId": "user3",
        "email": "david@example.com"
    },
    {
        "label": "User",
        "name": "Taylor Johnson",
        "userId": "user4",
        "email": "sarah@example.com"
    },
    {
        "label": "User",
        "name": "Alex Leclerc",
        "userId": "user5",
        "email": "alex@example.com"
    }
]

# Lista de películas
movies = [
    {
        "label": "Movie",
        "title": "La La Land",
        "year": 2016
    },
    {
        "label": "Movie",
        "title": "Top Gun: Maverick",
        "year": 2022
    },
    {
        "label": "Movie",
        "title": "Barbie",
        "year": 2023
    },
    {
        "label": "Movie",
        "title": "Spider-Man",
        "year": 2012
    },
    {
        "label": "Movie",
        "title": "The Notebook",
        "year": 2004
    },
    {
        "label": "Movie",
        "title": "Pride & Prejudice",
        "year": 2005
    }
]

class MovieDatabase:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def create_nodes(self, nodes_list):
        """Función para crear nodos en la base de datos"""
        with self.driver.session() as session:
            for node in nodes_list:
                label = node["label"]
                properties = {k: v for k, v in node.items() if k != "label"}
                
                query = f"""
                CREATE (n:{label} $props)
                RETURN n
                """
                session.run(query, props=properties)
                print(f"Created {label} node: {properties.get('name', properties.get('title', 'Unknown'))}")

    def create_relationship(self, start_label, start_key, start_value, 
                          end_label, end_key, end_value, 
                          rel_type, **properties):
        """Función para crear relaciones entre nodos"""
        with self.driver.session() as session:
            query = f"""
            MATCH (a:{start_label} {{{start_key}: $start_value}}),
                  (b:{end_label} {{{end_key}: $end_value}})
            CREATE (a)-[r:{rel_type} $props]->(b)
            RETURN r
            """
            session.run(query, 
                       start_value=start_value,
                       end_value=end_value,
                       props=properties)
            print(f"Created {rel_type} relationship between {start_value} and {end_value}")

    def find_user(self, user_id):
        """Función para encontrar un usuario específico"""
        with self.driver.session() as session:
            query = """
            MATCH (u:User {userId: $user_id})
            RETURN u
            """
            result = session.run(query, user_id=user_id)
            return result.single()

    def find_movie(self, movie_title):
        """Función para encontrar una película específica"""
        with self.driver.session() as session:
            query = """
            MATCH (m:Movie {title: $title})
            RETURN m
            """
            result = session.run(query, title=movie_title)
            return result.single()

    def find_user_ratings(self, user_id):
        """Función para encontrar las calificaciones de un usuario"""
        with self.driver.session() as session:
            query = """
            MATCH (u:User {userId: $user_id})-[r:RATED]->(m:Movie)
            RETURN u, r, m
            """
            result = session.run(query, user_id=user_id)
            return list(result)

def main():
    # Inicializar la base de datos
    db = MovieDatabase(URI, AUTH)
    
    try:
        # Crear nodos
        print("=== CREANDO NODOS ===")
        db.create_nodes(users)
        db.create_nodes(movies)

        # Crear relaciones de rating (actualizadas para incluir las nuevas películas)
        print("\n=== CREANDO RATINGS ===")
        ratings = [
            ("user1", "La La Land", 4.5),
            ("user1", "The Notebook", 5.0),
            ("user2", "Pride & Prejudice", 4.0),
            ("user2", "Spider-Man", 4.8),
            ("user3", "The Notebook", 3.5),
            ("user3", "Pride & Prejudice", 5.0),
            ("user4", "Barbie", 4.2),
            ("user4", "Top Gun: Maverick", 4.7),
            ("user5", "Spider-Man", 4.5),
            ("user5", "La La Land", 3.8)
        ]

        for user_id, movie, rating in ratings:
            db.create_relationship(
                "User", "userId", user_id,
                "Movie", "title", movie,
                "RATED",
                rating=rating
            )

        # Probar funciones de búsqueda
        print("\n=== PRUEBAS DE BÚSQUEDA ===")
        
        # 1. Buscar usuario
        print("\n1. Buscando usuario (user1):")
        user = db.find_user("user1")
        if user:
            print(f"Usuario encontrado: {user['u']['name']}")

        # 2. Buscar película
        print("\n2. Buscando película (The Notebook):")
        movie = db.find_movie("The Notebook")
        if movie:
            print(f"Película encontrada: {movie['m']['title']} ({movie['m']['year']})")

        # 3. Buscar ratings de usuario
        print("\n3. Buscando ratings del usuario 'user1':")
        ratings = db.find_user_ratings("user1")
        for record in ratings:
            print(f"  {record['u']['name']} calificó {record['m']['title']} con {record['r']['rating']}/5.0")

    finally:
        db.close()

if __name__ == "__main__":
    main()