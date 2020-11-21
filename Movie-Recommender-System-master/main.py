import numpy as np
import pandas as pd
from flask import Flask, render_template, request
df_2=pd.read_csv('data.csv')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
cv=CountVectorizer()
count_matrix_df_2=cv.fit_transform(df_2['sum'])
cos_sim_2=cosine_similarity(count_matrix_df_2)
indexes=pd.Series(data=df_2.index,index=df_2['name']).drop_duplicates()


def rcmd(title,cos_sim_2=cos_sim_2):
    if title not in df_2['name'].unique():
        return("sry this is not present in our database")

    else:
        index=indexes[title]
        cos_score=list(enumerate(cos_sim_2[index]))
        sorted_score=sorted(cos_score,key=lambda x:x[1],reverse=True)
        sorted_score=sorted_score[1:11]
        l = []
        for i in range(len(sorted_score)):
            a = sorted_score[i][0]
            l.append( df_2['name'][a])
        return l
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/recommend")
def recommend():
    movie = request.args.get('movie')
    r = rcmd(movie)
    movie = movie.upper()
    if type(r)==type('string'):
        return render_template('recommend.html',movie=movie,r=r,t='s')
    else:
        return render_template('recommend.html',movie=movie,r=r,t='l')



if __name__ == '__main__':
    app.run()