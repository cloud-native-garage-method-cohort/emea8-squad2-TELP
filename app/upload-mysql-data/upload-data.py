import pymysql
import csv

mydb = pymysql.connect(user='testuser', passwd='Password123!', host='mysql', database='sampledb')

mycursor = mydb.cursor()

mycursor.execute("DROP TABLE IF EXISTS sampledb.movie_predictions;")
mycursor.execute("CREATE TABLE sampledb.movie_predictions (name VARCHAR(255), userId INT, rec_1 VARCHAR(255), rec_2 VARCHAR(255), rec_3 VARCHAR(255), rec_4 VARCHAR(255), rec_5 VARCHAR(255), rec_6 VARCHAR(255), rec_7 VARCHAR(255), rec_8 VARCHAR(255), rec_9 VARCHAR(255), rec_10 VARCHAR(255), oldrank_1 VARCHAR(255), oldrank_2 VARCHAR(255), oldrank_3 VARCHAR(255))")

file = open('initial-predicted-results.csv')
csv_data = csv.reader(file)

skipHeader = True
for row in csv_data:
    if skipHeader:
        skipHeader = False
        continue

    sql = "INSERT INTO movie_predictions (name,userId,rec_1,rec_2,rec_3,rec_4,rec_5,rec_6,rec_7,rec_8,rec_9,rec_10,oldrank_1,oldrank_2,oldrank_3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, row)

mydb.commit()
