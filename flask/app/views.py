#This file contains all the routes for our application. 
#This will tell Flask what to display on which path.

from app import app,db
from flask import render_template,request
from elasticsearch import Elasticsearch, helpers

es= Elasticsearch()
es.indices.delete(index='ted', ignore=[400, 404])

num1=1
num2=1
for content in db.find():
    content.pop('_id')
    if content['con_type']=='ted':
        es.index(index="ted", doc_type='video', id=num1, body=content)
        num1+=1
    else:
        es.index(index="vocal", doc_type='article', id=num2, body=content)
        num2+=1
es.indices.refresh(index="ted")
es.indices.refresh(index="vocal")

@app.route('/')
def hello():
    return render_template('main.html')

@app.route('/ted_videos',methods=['GET', 'POST'])
def ted_videos():
    res=es.search(
        index="ted",
        body={
            "from": 0,
            "size": 100,
            "query": {
                "match_all":{}
            }
        }
    )
    return render_template('ted.html',res=res)

@app.route('/vocal_articles',methods=['GET', 'POST'])
def vocal_articles():
    res=es.search(
        index="vocal",
        body={
            "from": 0,
            "size": 100,
            "query": {
                "match_all":{}
            }
        }
    )
    return render_template('vocal.html',res=res)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search/results',methods=['POST'])
def search_request():
    search_term=request.form['input']
    try:
        res_ted = es.search(
            index="ted", 
            body={
                    "from": 0,
                    "size": 100,
                    "query": {
                        "multi_match" : { 
                            "query": search_term, 
                            "fields": ["title","keywords","author","description"]
                        }
                    }
            }
        )
        res_vocal = es.search(
            index="vocal", 
            body={
                    "from": 0,
                    "size": 100,
                    "query": {
                        "multi_match" : { 
                            "query": search_term, 
                            "fields": ["title","keywords","author","description"]
                        }
                    }
            }
        )

        return render_template('results.html', res_ted=res_ted, res_vocal=res_vocal, term=search_term)
    except:
        flash("ERROR: Can't find any ElasticSearch servers.")
        return redirect('/search')

@app.route('/search/results/<uploadDate>',methods=['POST'])
def search_detail():
    con=es.search(
            index="ted", 
             body={"query": {"multi_match" : { "query": uploadDate, "fields": ["title","keywords","author","description"]}}}
    )
    return render_template('detail.html',content=con)