from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pymysql

app = Flask(__name__)

def movieExists(movie_name,df):
    if movie_name in df.index:
        return True
    else:
        return False

def find_similar_movie(movie_name,df):
    if movieExists(movie_name,df):
        a_1 = np.array(df.loc[movie_name]).reshape(1, -1)
        score_1 = cosine_similarity(df, a_1).reshape(-1)
        dictDf = {'content': score_1}
        similar = pd.DataFrame(dictDf, index = df.index)
        similar.sort_values('content', ascending = False, inplace = True)
        similar_list = similar.index.tolist()[1:11]
        return similar_list
    else:
        raise ValueError('ERROR: The Movie is not Recognised')

@app.route('/')
def my_form():
    return render_template("home.html")

@app.route('/handleDataExistingUser', methods=['POST'])
def handleDataExistingUser():
    mydb = pymysql.connect(user='testuser', passwd='Password123!', host='mysql', database='sampledb')
    mycursor = mydb.cursor()
    
    firstname = request.form['firstnameval']
    lastname = request.form['lastnameval']
    
    fullname = firstname+' '+lastname
    fullname = fullname.title()
    
    modelval = "1"
    
    mycursor.execute("SELECT * FROM sampledb.movie_predictions WHERE name=%s", (fullname,))

    myresult = mycursor.fetchall()
    
    res_name = 'no user exists by that name'
    if not myresult:
        res_name = 'no user exists by that name'
        
        print("We are using Model: " + modelval)
        return render_template("home.html", error_message="ERROR: User is not recognized")
    else:
        res_name = fullname
        movies = myresult[0]
        print("We are using Model: " + modelval)
        return render_template("results.html", fullname=res_name,
                              movie_rec_1=movies[2],movie_rec_2=movies[3],movie_rec_3=movies[4],movie_rec_4=movies[5],movie_rec_5=movies[6],
                              movie_rec_6=movies[7],movie_rec_7=movies[8],movie_rec_8=movies[9],movie_rec_9=movies[10],movie_rec_10=movies[11])

@app.route('/handleDataNewUser', methods=['POST'])
def handleDataNewUser():
    res_name = 'ERROR'
    try:
        latent_matrix_1_mvp=pd.read_csv('app_csvs/movie-similarity-matrix.csv', index_col=0)
        
        firstname = request.form['firstnameval']
        lastname = request.form['lastnameval']
        movie = request.form['movieval']

        res_name = firstname+' '+lastname
        res_name = res_name.title()

        modelval = "2"

        movies = find_similar_movie(movie,latent_matrix_1_mvp)

        print("We are using Model: " + modelval)
        return render_template("results.html", fullname=res_name,
                                   movie_rec_1=movies[0], movie_rec_2=movies[1], movie_rec_3=movies[2], movie_rec_4=movies[3],movie_rec_5=movies[4],
                                   movie_rec_6=movies[5], movie_rec_7=movies[6], movie_rec_8=movies[7], movie_rec_9=movies[8],movie_rec_10=movies[9])

    except Exception as error:
        print("We are using Model: "+modelval)
        print(str(error))
        return render_template("home.html", error_message=str(error))
    
@app.route('/new/user', methods=['POST'])
def newuser():
    try:
        mydb = pymysql.connect(user='testuser', passwd='Password123!', host='mysql', database='sampledb')
        mycursor = mydb.cursor()

        sql = "INSERT INTO movie_predictions (name,userId,rec_1,rec_2,rec_3,rec_4,rec_5,rec_6,rec_7,rec_8,rec_9,rec_10,oldrank_1,oldrank_2,oldrank_3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        args = (request.json['name'], request.json['userid'], request.json['movie_rec_1'], request.json['movie_rec_2'],
                request.json['movie_rec_3'], request.json['movie_rec_4'], request.json['movie_rec_5'],
                request.json['movie_rec_6'], request.json['movie_rec_7'], request.json['movie_rec_8'],
                request.json['movie_rec_9'], request.json['movie_rec_10'], request.json['old_movie_1'],
                request.json['old_movie_2'], request.json['old_movie_3'])

        mycursor.execute(sql, args)

        mydb.commit()

        return jsonify({'result' : "New user added successfully"})
    
    except Exception as error:
        return jsonify({"ERROR" : "There was an error while adding new user","ERROR MESSAGE" : str(error)})
    
if __name__ == '__main__':
    app.run(host="0.0.0.0")
