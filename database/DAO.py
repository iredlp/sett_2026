from database.DB_connect import DBConnect
from model.actor import Actor


class DAO:
    @staticmethod
    def getAllMovies():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select * from movie m """

        cursor.execute(query)

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(v_min, v_max):
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            return result

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct  n.*
                from role_mapping rm , names n , movie m, ratings r 
                WHERE rm.category IN ('actor', 'actress') 
                and r.avg_rating between %s and %s
                and m.id =r.movie_id and rm.movie_id =m.id 
                AND n.id = rm.name_id
               """
        cursor.execute(query, (v_min, v_max))

        for row in cursor:
            result.append(Actor(**row))

        cursor.close()
        conn.close()
        return result

    def getFilmPerAttore(v_min, v_max):
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            return result

        cursor = conn.cursor(dictionary=True)
        query = """  SELECT rm.name_id, m.id AS movie_id, m.title, m.year, r.avg_rating
        FROM role_mapping rm, movie m, ratings r
        WHERE rm.movie_id = m.id
        AND m.id = r.movie_id
        AND rm.category IN ('actor', 'actress')
        AND r.avg_rating BETWEEN %s AND %s
        """

        cursor.execute(query, (v_min, v_max))

        for row in cursor:
            result.append((row["name_id"],row["movie_id"], row["title"], row["year"], row["avg_rating"]))

        cursor.close()
        conn.close()
        return result
