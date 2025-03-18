########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv

#################################################################################

## Change to False to disable Sample
SHOW = True


############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')

        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)", ("1", "test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())


######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))

        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "jpatel685"
        return gt_username

    # Part 1.a.i Create Tables [2 points]
    def part_1_a_i(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = "CREATE TABLE MOVIES(ID INTEGER, TITLE TEXT, SCORE REAL);"

        return self.execute_query(connection, part_ai_1_sql)

    def part_1_a_ii(self, connection):
        part_ai_2_sql = "CREATE TABLE MOVIE_CAST(MOVIE_ID INTEGER, CAST_ID INTEGER, CAST_NAME TEXT, BIRTHDAY TEXT, POPULARITY REAL);"

        return self.execute_query(connection, part_ai_2_sql)

    # Part 1.b Import Data [2 points]
    def part_1_b_movies(self, connection, path):
        insert_sql = "INSERT INTO MOVIES VALUES(?, ?, ?)"
        try:
            csv_file = open(path)
            rows = csv.reader(csv_file, delimiter=',')
            for row in rows:
                connection.execute(insert_sql, row)
        except:
            csv_file = open(path, encoding="utf-8")
            rows = csv.reader(csv_file, delimiter=',')
            for row in rows:
                connection.execute(insert_sql, row)

        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    def part_1_b_movie_cast(self, connection, path):
        ############### CREATE IMPORT CODE BELOW ############################

        insert_sql = "INSERT INTO MOVIE_CAST VALUES(?, ?, ?, ?, ?)"
        try:
            csv_file = open(path)
            rows = csv.reader(csv_file, delimiter=',')
            for row in rows:
                connection.execute(insert_sql, row)
        except:
            csv_file = open(path, encoding="utf-8")
            rows = csv.reader(csv_file, delimiter=',')
            for row in rows:
                connection.execute(insert_sql, row)


        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part 1.c Vertical Database Partitioning [5 points]
    def part_1_c(self, connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_1_c_sql = "CREATE TABLE CAST_BIO(CAST_ID INTEGER, CAST_NAME TEXT, BIRTHDAY TEXT, POPULARITY REAL); "


        self.execute_query(connection, part_1_c_sql)

        part_1_c_sql_insert_sql = "INSERT INTO CAST_BIO SELECT DISTINCT CAST_ID, CAST_NAME, BIRTHDAY, POPULARITY FROM MOVIE_CAST"

        self.execute_query(connection, part_1_c_sql_insert_sql)

        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part 2 Create Indexes [1 points]
    def part_2_a(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_2_a_sql = "CREATE INDEX MOVIE_INDEX ON MOVIES(ID)"

        return self.execute_query(connection, part_2_a_sql)

    def part_2_b(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_2_b_sql = "CREATE INDEX CAST_INDEX ON MOVIE_CAST(CAST_ID)"

        return self.execute_query(connection, part_2_b_sql)

    def part_2_c(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_2_c_sql = "CREATE INDEX CAST_BIO_INDEX ON CAST_BIO(CAST_ID)"

        return self.execute_query(connection, part_2_c_sql)

    # Part 3 Calculate a Proportion [3 points]
    def part_3(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_3_sql = """
        SELECT printf('%.2f', c1 * 1.0 / c2 * 100) 
        FROM 
        (SELECT COUNT(1) AS c1 FROM MOVIES WHERE SCORE BETWEEN 7 AND 20) AS T1, 
        (SELECT COUNT(1) AS c2 FROM MOVIES) AS T2;
        """

        cursor = connection.execute(part_3_sql)
        return cursor.fetchall()[0][0]

    # Part 4 Find the Most Prolific Actors [4 points]
    def part_4(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_4 = "SELECT CAST_NAME, COUNT(CAST_NAME) CT FROM MOVIE_CAST GROUP BY CAST_NAME HAVING POPULARITY>10 ORDER BY CT DESC LIMIT 5"
        ######################################################################
        cursor = connection.execute(part_4)
        return cursor.fetchall()

    # Part 5 Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_5(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_5_sql = """
        SELECT TITLE, printf('%.2f', SCORE), COUNT(CAST_ID) AS CT FROM MOVIE_CAST A JOIN MOVIES B ON A.MOVIE_ID=B.ID GROUP BY TITLE ORDER BY SCORE DESC, CT ASC LIMIT 5
        """
        ######################################################################
        cursor = connection.execute(part_5_sql)
        return cursor.fetchall()

    # Part 6 Get High Scoring Actors [4 points]
    def part_6(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_6_sql = """
        SELECT CAST_ID, CAST_NAME, AVERAGE_SCORE FROM (SELECT CAST_ID, CAST_NAME, COUNT(MOVIE_ID) CT, 
        printf('%.2f', avg(SCORE)) AS AVERAGE_SCORE FROM 
        (SELECT * FROM MOVIES WHERE SCORE >= 25) MV JOIN MOVIE_CAST MC ON MV.ID=MC.MOVIE_ID 
        GROUP BY CAST_ID HAVING CT > 2 ORDER BY AVERAGE_SCORE DESC, CAST_NAME ASC LIMIT 10)
        """
        cursor = connection.execute(part_6_sql)
        return cursor.fetchall()

    # Part 7 Creating Views [6 points]
    def part_7(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_7_sql = "CREATE VIEW GOOD_COLLABORATION AS  "\
                        "SELECT A.CAST_ID CAST_MEMBER_ID1, B.CAST_ID CAST_MEMBER_ID2, COUNT(1)" \
                        " AS MOVIE_COUNT, AVG(C.SCORE) AVERAGE_MOVIE_SCORE FROM "\
                        "(SELECT CAST_ID, MOVIE_ID FROM MOVIE_CAST) A JOIN "\
                        "(SELECT CAST_ID, MOVIE_ID FROM MOVIE_CAST) B JOIN "\
                        "(SELECT ID, SCORE FROM MOVIES ) C "\
                        "ON A.MOVIE_ID = B.MOVIE_ID AND A.MOVIE_ID = C.ID AND A.CAST_ID < B.CAST_ID " \
                        "GROUP BY A.CAST_ID, B.CAST_ID HAVING AVERAGE_MOVIE_SCORE >=40 AND MOVIE_COUNT >= 3"
        ######################################################################
        return self.execute_query(connection, part_7_sql)

    def part_8(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_8_sql = """SELECT CAST_ID, CAST_NAME, 
        printf('%.2f', AVG(AVERAGE_MOVIE_SCORE)) AS COLLABORATION_SCORE FROM 
        (SELECT CAST_MEMBER_ID1 AS CAST_ID, CAST_NAME, AVERAGE_MOVIE_SCORE FROM 
        GOOD_COLLABORATION E
        JOIN CAST_BIO F ON E.CAST_MEMBER_ID1=F.CAST_ID 
        UNION 
        SELECT CAST_MEMBER_ID2 AS CAST_ID, CAST_NAME, AVERAGE_MOVIE_SCORE FROM 
        GOOD_COLLABORATION G 
        JOIN CAST_BIO B ON G.CAST_MEMBER_ID2=B.CAST_ID) 
        GROUP BY CAST_ID ORDER BY COLLABORATION_SCORE DESC, CAST_NAME ASC LIMIT 5
        """
        ######################################################################
        cursor = connection.execute(part_8_sql)
        return cursor.fetchall()
        ######################################################################

    # Part 9 FTS [4 points]
    def part_9_a(self, connection, path):
        # Insert data into the table
        part_9_a = "CREATE VIRTUAL TABLE MOVIE_OVERVIEW USING FTS3(ID INTEGER, OVERVIEW TEXT)"
        ######################################################################
        connection.execute(part_9_a)
        ############### CREATE IMPORT CODE BELOW ############################
        insert_sql = "INSERT INTO MOVIE_OVERVIEW VALUES(?, ?)"
        try:
            csv_file = open(path)
            rows = csv.reader(csv_file, delimiter=',')
            for row in rows:
                connection.execute(insert_sql, row)
        except:
            csv_file = open(path, encoding="utf-8")
            rows = csv.reader(csv_file, delimiter=',')
            for row in rows:
                connection.execute(insert_sql, row)
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part 9.b Count Movies Matching the Word "fight"
    def part_9_b(self, connection):
        # Query to count movies where the OVERVIEW contains the word 'fight'
        part_9_b_sql = """
        SELECT COUNT(DISTINCT ID) 
        FROM MOVIE_OVERVIEW 
        WHERE OVERVIEW MATCH 'fight';
        """
        cursor = connection.execute(part_9_b_sql)
        return cursor.fetchall()[0][0]

    # Part 9.c Count Movies Matching "space NEAR/5 program"
    def part_9_c(self, connection):
        # Query to count movies where 'space' is within 5 words of 'program'
        part_9_c_sql = """
        SELECT COUNT(DISTINCT ID) 
        FROM MOVIE_OVERVIEW 
        WHERE OVERVIEW MATCH 'space NEAR/5 program';
        """
        cursor = connection.execute(part_9_c_sql)
        return cursor.fetchall()[0][0]



if __name__ == "__main__":

    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except Exception as e:
        print("Error in Table Drops")
        print(e)

    try:
        print('\033[32m' + "part 1.a.i: " + '\033[m' + str(db.part_1_a_i(conn)))
        print('\033[32m' + "part 1.a.ii: " + '\033[m' + str(db.part_1_a_ii(conn)))
    except Exception as e:
        print("Error in Part 1.a")
        print(e)

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_1_b_movies(conn, "data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(
            db.part_1_b_movie_cast(conn, "data/movie_cast.csv")))
    except Exception as e:
        print("Error in part 1.b")
        print(e)

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_1_c(conn)))
    except Exception as e:
        print("Error in part 1.c")
        print(e)

    try:
        print('\033[32m' + "part 2.a: " + '\033[m' + db.part_2_a(conn))
        print('\033[32m' + "part 2.b: " + '\033[m' + db.part_2_b(conn))
        print('\033[32m' + "part 2.c: " + '\033[m' + db.part_2_c(conn))
    except Exception as e:
        print("Error in part 2")
        print(e)

    try:
        print('\033[32m' + "part 3: " + '\033[m' + str(db.part_3(conn)))
    except Exception as e:
        print("Error in part 3")
        print(e)

    try:
        print('\033[32m' + "part 4: " + '\033[m')
        for line in db.part_4(conn):
            print(line[0], line[1])
    except Exception as e:
        print("Error in part 4")
        print(e)

    try:
        print('\033[32m' + "part 5: " + '\033[m')
        for line in db.part_5(conn):
            print(line[0], line[1], line[2])
    except Exception as e:
        print("Error in part 5")
        print(e)

    try:
        print('\033[32m' + "part 6: " + '\033[m')
        for line in db.part_6(conn):
            print(line[0], line[1], line[2])
    except Exception as e:
        print("Error in part 6")
        print(e)

    try:
        print('\033[32m' + "part 7: " + '\033[m' + str(db.part_7(conn)))
        print("\033[32mRow count for good_collaboration view:\033[m",
              conn.execute("select count(*) from good_collaboration").fetchall()[0][0])
        print('\033[32m' + "part 8: " + '\033[m')
        for line in db.part_8(conn):
            print(line[0], line[1], line[2])
    except Exception as e:
        print("Error in part 7 and/or 8")
        print(e)

    try:
        print('\033[32m' + "part 9.a: " + '\033[m' + str(db.part_9_a(conn, "data/movie_overview.csv")))
        print('\033[32m' + "Count 9.b: " + '\033[m' + str(db.part_9_b(conn)))
        print('\033[32m' + "Count 9.c: " + '\033[m' + str(db.part_9_c(conn)))
    except Exception as e:
        print("Error in part 9")
        print(e)

    conn.close()
    #################################################################################
    #################################################################################

