class SQL:
    PERSONS_ID = """SELECT DISTINCT
        id,
        modified
        FROM content.person
        WHERE modified > %(date)s
        ORDER BY modified
        LIMIT 100;
        """

    GENRES_ID = """SELECT DISTINCT
        id,
        modified
        FROM content.genre
        WHERE modified > %(date)s
        ORDER BY modified
        LIMIT 100;
        """

    PERSONS_FILMWORK_ID = """SELECT DISTINCT
        fw.id,
        fw.modified
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        WHERE pfw.person_id IN %(id)s
        ORDER BY fw.modified;
        """

    GENRES_FILMWORK_ID = """SELECT DISTINCT
        fw.id,
        fw.modified
        FROM content.film_work fw
        LEFT JOIN content.genre_film_work pfw ON pfw.film_work_id = fw.id
        WHERE pfw.genre_id IN %(id)s
        ORDER BY fw.modified;
        """

    FILMWORK_ID = """SELECT DISTINCT
        id,
        modified
        FROM content.film_work
        WHERE modified > %(date)s
        ORDER BY modified
        LIMIT 100;
        """

    FILMWORK = """SELECT
        fw.id,
        fw.rating as imdb_rating,
        g.name as genre,
        fw.title,
        fw.description,
        fw.modified,
        ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'director') AS director,
        ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor') AS actors_names,
        ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer') AS writers_names,
        JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
        JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers
        FROM content.film_work fw
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        WHERE fw.id in %(id)s
        GROUP BY fw.id, g.name
        ORDER BY fw.id;
        """
