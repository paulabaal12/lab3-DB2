from neo4j import GraphDatabase

# Configuración de la conexión
URI = "neo4j+s://55a06213.databases.neo4j.io"
AUTH = ("neo4j", "LLZGdkq6Yxv-jGfijw9nQLKugJ2LjjzVdBUYRidHK4o")

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

def main():
    # Inicializar la base de datos
    db = MovieDatabase(URI, AUTH)
    
    try:
        # Definir listas de nodos
                
        # Lista de actores
        actors = [
            {
                "label": "Actor",
                "name": "Tom Cruise",
                "tmdbld": 500,
                "born": "1962-07-03",
                "died": "N/A",
                "bomln": "Syracuse, New York, USA", 
                "url": "https://www.themoviedb.org/person/500",
                "ibmdbld": 500,
                "bio": "Thomas Cruise Mapother IV es un actor y productor estadounidense, conocido por películas como Top Gun, Mission: Impossible y Jerry Maguire.",
                "poster": "https://link-al-poster.com/cruise.jpg"
            },
            {
                "label": "Actor",
                "name": "Emma Stone",
                "tmdbld": 501,
                "born": "1988-11-06", 
                "died": "N/A",
                "bomln": "Scottsdale, Arizona, USA",
                "url": "https://www.themoviedb.org/person/501",
                "ibmdbld": 501,
                "bio": "Emily Jean Stone es una actriz estadounidense, ganadora del Premio de la Academia por La La Land.",
                "poster": "https://link-al-poster.com/stone.jpg"
            },
            {
                "label": "Actor",
                "name": "Andrew Garfield",
                "tmdbld": 502,
                "born": "1983-08-20",
                "died": "N/A",
                "bomln": "Los Angeles, California, USA",
                "url": "https://www.themoviedb.org/person/502", 
                "ibmdbld": 502,
                "bio": "Andrew Russell Garfield es un actor británico-estadounidense conocido por su papel como Spider-Man.",
                "poster": "https://link-al-poster.com/garfield.jpg"
            },
            {
                "label": "Actor", 
                "name": "Margot Robbie",
                "tmdbld": 503,
                "born": "1990-07-02",
                "died": "N/A",
                "bomln": "Gold Coast, Queensland, Australia",
                "url": "https://www.themoviedb.org/person/503",
                "ibmdbld": 503,
                "bio": "Margot Elise Robbie es una actriz y productora australiana, conocida por películas como Wolf of Wall Street y Barbie.",
                "poster": "https://link-al-poster.com/robbie.jpg"
            },
            {
                "label": "Actor",
                "name": "Chris Evans",
                "tmdbld": 504,
                "born": "1981-06-13",
                "died": "N/A",
                "bomln": "Boston, Massachusetts, USA",
                "url": "https://www.themoviedb.org/person/504",
                "ibmdbld": 504,
                "bio": "Christopher Robert Evans es un actor estadounidense, conocido por interpretar al Capitán América en el Universo Cinematográfico de Marvel.",
                "poster": "https://link-al-poster.com/evans.jpg"
            },
            {
                "label": "Actor",
                "name": "Anne Hathaway",
                "tmdbld": 505,
                "born": "1982-11-12",
                "died": "N/A",
                "bomln": "Brooklyn, New York, USA",
                "url": "https://www.themoviedb.org/person/505",
                "ibmdbld": 505,
                "bio": "Anne Jacqueline Hathaway es una actriz estadounidense, ganadora del Oscar por Les Misérables y conocida por películas como El diablo viste de Prada.",
                "poster": "https://link-al-poster.com/hathaway.jpg"
            }
        ]

       
        # Lista de películas
        movies = [
            {
                "label": "Movie",
                "title": "La La Land",
                "tmdbld": "601",
                "released": "2017-12-09",
                "imdbRating": 8.0,
                "movieId": 313369,
                "year": 2016,
                "imdbld": 3783958,
                "runtime": 128,
                "countries": ["Estados Unidos"],
                "imdbVotes": 500000,
                "url": "https://www.themoviedb.org/movie/313369",
                "revenue": 446100000,
                "plot": "Una aspirante a actriz y un músico de jazz se enamoran mientras persiguen sus sueños en Los Ángeles.",
                "poster": "https://link-al-poster.com/lalaland.jpg",
                "budget": 30000000,
                "languages": ["Inglés"]
            },
            {
                "label": "Movie",
                "title": "Top Gun: Maverick",
                "tmdbld": "602",
                "released": "2022-05-27",
                "imdbRating": 8.3,
                "movieId": 361743,
                "year": 2022,
                "imdbld": 1745960,
                "runtime": 130,
                "countries": ["Estados Unidos"],
                "imdbVotes": 550000,
                "url": "https://www.themoviedb.org/movie/361743",
                "revenue": 1488732821,
                "plot": "Después de más de 30 años, Maverick regresa para entrenar a una nueva generación de pilotos.",
                "poster": "https://link-al-poster.com/topgun.jpg",
                "budget": 170000000,
                "languages": ["Inglés"]
            },
            {
                "label": "Movie", 
                "title": "Barbie",
                "tmdbld": "346698",
                "released": "2023-07-21",
                "imdbRating": 7.3,
                "movieId": 603,
                "year": 2023,
                "imdbld": 1747960,
                "runtime": 114,
                "countries": ["Estados Unidos"],
                "imdbVotes": 450000,
                "url": "https://www.themoviedb.org/movie/346698",
                "revenue": 1437000000,
                "plot": "Barbie y Ken viven en Barbieland hasta que descubren el mundo real.",
                "poster": "https://link-al-poster.com/barbie.jpg",
                "budget": 145000000,
                "languages": ["Inglés"]
            },
            {
                "label": "Movie",
                "title": "The Devil Wears Prada",
                "tmdbld": "350",
                "released": "2006-06-30",
                "imdbRating": 7.6,
                "movieId": 604,
                "year": 2006,
                "imdbld": 796731,
                "runtime": 109,
                "countries": ["Estados Unidos"],
                "imdbVotes": 400000,
                "url": "https://www.themoviedb.org/movie/350",
                "revenue": 326000000,
                "plot": "Una graduada universitaria consigue trabajo como asistente de una poderosa editora de moda.",
                "poster": "https://link-al-poster.com/devilwearsprada.jpg",
                "budget": 35000000,
                "languages": ["Inglés"]
            },
            {
                "label": "Movie",
                "title": "Spider-Man",
                "tmdbld": "605",
                "released": "2012-07-03",
                "imdbRating": 7.0,
                "movieId": 605,
                "year": 2012,
                "imdbld": 1877832,
                "runtime": 136,
                "countries": ["Estados Unidos"],
                "imdbVotes": 550000,
                "url": "https://www.themoviedb.org/movie/605",
                "revenue": 757930663,
                "plot": "Peter Parker desarrolla habilidades similares a las de una araña tras ser mordido por una araña modificada genéticamente.",
                "poster": "https://link-al-poster.com/spiderman.jpg",
                "budget": 230000000,
                "languages": ["Inglés"]
            }
        ]


        genres = [
            {"label": "Genre", "name": "Drama"},
            {"label": "Genre", "name": "Musical"},
            {"label": "Genre", "name": "Action"},
            {"label": "Genre", "name": "Adventure"},
            {"label": "Genre", "name": "Comedy"},
            {"label": "Genre", "name": "Fantasy"}
        ]

        # Crear todos los nodos
        print("=== CREANDO NODOS ===")
        db.create_nodes(actors)
        db.create_nodes(movies)
        db.create_nodes(genres)
        # Crear relaciones actor-película
        print("\n=== CREANDO RELACIONES ACTOR-PELÍCULA ===")
        actor_movie_relations = [
            ("Emma Stone", "La La Land", "Principal"),
            ("Tom Cruise", "Top Gun: Maverick", "Principal"),
            ("Margot Robbie", "Barbie", "Principal"),
            ("Anne Hathaway", "The Devil Wears Prada", "Principal"),
            ("Andrew Garfield", "Spider-Man", "Principal"),
            ("Chris Evans", "Spider-Man", "Secundario")
        ]

        for actor, movie, role in actor_movie_relations:
            db.create_relationship(
            "Actor", "name", actor,
            "Movie", "title", movie,
            "ACTED_IN",
            role=role
            )

        # Crear relaciones película-género
        print("\n=== CREANDO RELACIONES PELÍCULA-GÉNERO ===")
        movie_genre_relations = [
            ("La La Land", "Drama"),
            ("La La Land", "Musical"),
            ("Top Gun: Maverick", "Action"),
            ("Top Gun: Maverick", "Adventure"),
            ("Barbie", "Comedy"),
            ("Barbie", "Fantasy"),
            ("The Devil Wears Prada", "Comedy"),
            ("The Devil Wears Prada", "Drama"),
            ("Spider-Man", "Action"),
            ("Spider-Man", "Adventure"),
            ("Spider-Man", "Fantasy")
        ]

        for movie, genre in movie_genre_relations:
            db.create_relationship(
            "Movie", "title", movie,
            "Genre", "name", genre,
            "IN_GENRE"
            )

        # Crear relaciones de usuarios y ratings (manteniendo las del ejercicio anterior)
        print("\n=== CREANDO RELACIONES DE USUARIOS Y RATINGS ===")
        
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

        # Crear nodos de usuarios
        db.create_nodes(users)

        # Crear relaciones de rating
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

    finally:
        db.close()

if __name__ == "__main__":
    main()