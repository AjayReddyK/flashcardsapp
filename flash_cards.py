from multiprocessing import synchronize
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy.sql.expression import func, select

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://skfeyedwskfcxn:e334e83faa7f3c1caa038abf1dc593b0f04064e8b1289a2a6ba093ca33f94862@ec2-3-212-45-192.compute-1.amazonaws.com:5432/d98a8s62vq29bn'
app.config['USERNAME']="ajay"
app.config['PASSWORD']='ajay45177'
app.config['SECRET_KEY']='development key'
db=SQLAlchemy(app)

class Cards(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    type=db.Column(db.Integer,nullable=False)
    front=db.Column(db.String(300),nullable=False)
    back=db.Column(db.String(10000),nullable=False)
    known=db.Column(db.Boolean,default=False)
class Tags(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    tagName=db.Column(db.Text,nullable=False)

'''def load_config():
    app.config.update(dict(
        DATABASE='postgres://skfeyedwskfcxn:e334e83faa7f3c1caa038abf1dc593b0f04064e8b1289a2a6ba093ca33f94862@ec2-3-212-45-192.compute-1.amazonaws.com:5432/d98a8s62vq29bn',
        SECRET_KEY='development key',
        USERNAME='ajay',
        PASSWORD='police'
    ))
    app.config.from_envvar('CARDS_SETTINGS', silent=True)

if __name__ == "__main__" or __name__ == "flash_cards":
    load_config()

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'],)
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('data/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
'''
@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('memorize',card_type="all"))
    else:
        return redirect(url_for('login'))


@app.route('/cards')
def cards():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    '''db = get_db()
    query =
        SELECT id, type, front, back, known
        FROM cards
        ORDER BY id DESC
    cur = db.execute(query)
    cards = cur.fetchall()'''
    cards=Cards.query.all()
    tags = getAllTag()
    return render_template('cards.html', cards=cards, tags=tags, filter_name="all")


@app.route('/filter_cards/<filter_name>')
def filter_cards(filter_name):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    filters = {
        "all":      "where 1 = 1",
        "general":  "where type = 1",
        "code":     "where type = 2",
        "known":    "where known = 1",
        "unknown":  "where known = 0",
    }
    '''
    query = filters.get(filter_name)
    if(query is None):
        query = "where type = {0}".format(filter_name)
        filter_name = int(filter_name)

    if not query:
        return redirect(url_for('show'))

    db = get_db()
    fullquery = "SELECT id, type, front, back, known FROM cards " + \
        query + " ORDER BY id DESC"
    cur = db.execute(fullquery)
    cards = cur.fetchall()'''
    if(filter_name=="all"):
        cards=Cards.query.all()
    elif(filter_name=="known" ):
        cards=Cards.query.filter(Cards.known==True)
    elif(filter_name=="unknown"):
        cards=Cards.query.filter(Cards.known==False)
    else:
        cards=Cards.query.filter(Cards.type==filter_name)
    print(list(cards))
    tags = getAllTag()
    return render_template('show.html', cards=list(cards), tags=list(tags), filter_name=filter_name)


@app.route('/add', methods=['POST'])
def add_card():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    '''db = get_db()
    db.execute('INSERT INTO cards (type, front, back) VALUES (?, ?, ?)',
               [request.form['type'],
                request.form['front'],
                request.form['back']
                ])
    db.commit()'''
    new_task=Cards(type=request.form['type'],front=request.form['front'],back=request.form['back'])
    db.session.add(new_task)
    db.session.commit()
    flash('New card was successfully added.')
    return redirect(url_for('cards'))


@app.route('/edit/<card_id>')
def edit(card_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    '''db = get_db()
    query = 
        SELECT id, type, front, back, known
        FROM cards
        WHERE id = ?
    cur = db.execute(query, [card_id])
    card = cur.fetchone()'''
    card=Cards.query.get(card_id)
    tags = getAllTag()
    return render_template('edit.html', card=card, tags=tags)


@app.route('/edit_card', methods=['POST'])
def edit_card():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    selected = request.form.getlist('known')
    known = bool(selected)
    '''db = get_db()
    command = 
        UPDATE cards
        SET
          type = ?,
          front = ?,
          back = ?,
          known = ?
        WHERE id = ?
    db.execute(command,
               [request.form['type'],
                request.form['front'],
                request.form['back'],
                known,
                request.form['card_id']
                ])
    db.commit()'''
    card=Cards.query.get(request.form['card_id'])
    card.type=request.form['type']
    card.front=request.form['front']
    card.back=request.form['back']
    print(request.form)
    try:
        print(request.form['known'])
    except:
        card.known=False
    else:
        card.known=True
    db.session.commit()

    flash('Card saved.')
    return redirect(url_for('show'))


@app.route('/delete/<card_id>')
def delete(card_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    ''''db = get_db()
    db.execute('DELETE FROM cards WHERE id = ?', [card_id])
    db.commit()'''
    card=Cards.query.get(card_id)
    db.session.delete(card)
    db.session.commit()
    flash('Card deleted.')
    return redirect(url_for('cards'))

@app.route('/memorize')
@app.route('/memorize/<card_type>')
@app.route('/memorize/<card_type>/<card_id>')
def memorize(card_type, card_id=None):
    if(card_type=='all'):
        card=get_card(card_type)
        if not card:
            flash("You've learned all the  cards.")
            return redirect(url_for('show'))
        short_answer = (len(card.__dict__['back']) < 75)
        tags = getAllTag()
        card_type = 'all'
        return render_template('memorize.html',
                card=card,
                card_type=card_type,
                short_answer=short_answer, tags=tags)
    tag = getTag(card_type)
    print(tag)
    if tag is None:
        print("tag is none block")
        return redirect(url_for('cards'))

    if card_id:
        card = get_card_by_id(card_id)
    else:
        card = get_card(card_type)
    if not card:
        flash("You've learned all the '" + tag.tagName + "' cards.")
        return redirect(url_for('show'))
    short_answer = (len(card.__dict__['back']) < 75)
    tags = getAllTag()
    card_type = int(card_type)
    return render_template('memorize.html',
                           card=card,
                           card_type=card_type,
                           short_answer=short_answer, tags=tags)

@app.route('/memorize_known')
@app.route('/memorize_known/<card_type>')
@app.route('/memorize_known/<card_type>/<card_id>')
def memorize_known(card_type, card_id=None):
    if(card_type=='all'):
        card=get_card_already_known(card_type)
        if not card:
            flash("You've learned all the  cards.")
            return redirect(url_for('show'))
        short_answer = (len(card.__dict__['back']) < 75)
        tags = getAllTag()
        card_type = 'all'
        return render_template('memorize_known.html',
                card=card,
                card_type=card_type,
                short_answer=short_answer, tags=tags)
    tag = getTag(card_type)
    if tag is None:
        return redirect(url_for('cards'))

    if card_id:
        card = get_card_by_id(card_id)
    else:
        card = get_card_already_known(card_type)
    if not card:
        flash("You haven't learned any '" + tag.tagName + "' cards yet.")
        return redirect(url_for('show'))
    short_answer = (len(card.back) < 75)
    tags = getAllTag()
    card_type = int(card_type)
    return render_template('memorize_known.html',
                           card=card,
                           card_type=card_type,
                           short_answer=short_answer, tags=tags)


def get_card(types):
    '''db = get_db()

    query = 
      SELECT
        id, type, front, back, known
      FROM cards
      WHERE
        type = ?
        and known = 0
      ORDER BY RANDOM()
      LIMIT 1

    cur = db.execute(query, [type])'''
    if(types=='all'):
        cur=Cards.query.filter(Cards.known==0).order_by(func.random()).first()
        return cur
    cur=Cards.query.filter(Cards.type==types,Cards.known==0).order_by(func.random()).first()
    return cur


def get_card_by_id(card_id):
    '''query = 
      SELECT
        id, type, front, back, known
      FROM cards
      WHERE
        id = ?
      LIMIT 1

    cur = db.execute(query, [card_id])'''
    cur=Cards.query.get(card_id)
    return cur


@app.route('/mark_known/<card_id>/<card_type>')
def mark_known(card_id, card_type):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    '''db = get_db()
    db.execute('UPDATE cards SET known = 1 WHERE id = ?', [card_id])
    db.commit()'''
    card=Cards.query.get(card_id)
    card.known=True
    db.session.commit()
    flash('Card marked as known.')
    return redirect(url_for('memorize', card_type=card_type))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username or password!'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password!'
        else:
            session['logged_in'] = True
            session.permanent = True  # stay logged in
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You've logged out")
    return redirect(url_for('index'))


def getAllTag():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    '''db = get_db()
    query = 
        SELECT id, tagName
        FROM tags
        ORDER BY id ASC
    cur = db.execute(query)
    tags = cur.fetchall()'''
    cur=Tags.query.all()
    return cur


@app.route('/tags')
def tags():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    tags = getAllTag()
    return render_template('tags.html', tags=tags, filter_name="all")


@app.route('/addTag', methods=['POST'])
def add_tag():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    '''db = get_db()
    db.execute('INSERT INTO tags (tagName) VALUES (?)',
               [request.form['tagName']])
    db.commit()'''
    new_tag=Tags(tagName=request.form['tagName'])
    db.session.add(new_tag)
    db.session.commit()
    flash('New tag was successfully added.')
    return redirect(url_for('tags'))


@app.route('/editTag/<tag_id>')
def edit_tag(tag_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    tag = getTag(tag_id)
    return render_template('editTag.html', tag=tag)


@app.route('/updateTag', methods=['POST'])
def update_tag():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    '''db = get_db()
    command = 
        UPDATE tags
        SET
          tagName = ?
        WHERE id = ?
    db.execute(command,
               [request.form['tagName'],
                request.form['tag_id']
                ])
    db.commit()'''
    tag=Tags.query.get(request.form['tag_id'])
    tag.tagName=request.form['tagName']
    db.session.commit()
    flash('Tag saved.')
    return redirect(url_for('tags'))
'''
def init_tag():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    db.execute('INSERT INTO tags (tagName) VALUES (?)',
               ["general"])
    db.commit()
    db.execute('INSERT INTO tags (tagName) VALUES (?)',
               ["code"])
    db.commit()
    db.execute('INSERT INTO tags (tagName) VALUES (?)',
               ["bookmark"])
    db.commit()
'''
@app.route('/show')
def show():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('filter_cards', filter_name="all"))

def getTag(tag_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    '''db = get_db()
    query = 
        SELECT id, tagName
        FROM tags
        WHERE id = ?
    cur = db.execute(query, [tag_id])
    tag = cur.fetchone()'''
    tag=Tags.query.get(tag_id)
    return tag

@app.route('/bookmark/<card_type>/<card_id>')
def bookmark(card_type, card_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    '''db = get_db()
    db.execute('UPDATE cards SET type = ? WHERE id = ?',[card_type,card_id])
    db.commit()'''
    card=Cards.query.get(card_id)
    card.type=card_type
    db.session.commit()
    flash('Card saved.')
    return redirect(url_for('memorize', card_type=card_type))
'''
@app.route('/list_db')
def list_db():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    dbs = [f for f in os.listdir(pathDB) if os.path.isfile(os.path.join(pathDB, f))]
    dbs = list(filter(lambda k: '.db' in k, dbs))
    return render_template('listDb.html', dbs=dbs)

@app.route('/load_db/<name>')
def load_db(name):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    global nameDB
    nameDB=name
    load_config()
    handle_old_schema()
    return redirect(url_for('memorize', card_type="1"))

@app.route('/create_db')
def create_db():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('createDb.html')
@app.route('/init', methods=['POST'])
def init():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    global nameDB
    nameDB = request.form['dbName'] + '.db'
    load_config()
    init_db()
    init_tag()
    return redirect(url_for('index'))

def check_table_tag_exists():
    db = get_db()
    cur = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tags'")
    result = cur.fetchone()
    return result

def create_tag_table():
    db = get_db()
    with app.open_resource('data/handle_old_schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def handle_old_schema():
    result = check_table_tag_exists()
    if(result is None):
        create_tag_table()
        init_tag()
'''
def get_card_already_known(types):
    ''''db = get_db()

    query = 
      SELECT
        id, type, front, back, known
      FROM cards
      WHERE
        type = ?
        and known = 1
      ORDER BY RANDOM()
      LIMIT 1

    cur = db.execute(query, [type])'''
    if(types=='all'):
        cur=Cards.query.filter(Cards.known==True).order_by(func.random()).first()
        return cur
    cur=Cards.query.filter(Cards.type==types,Cards.known==True).order_by(func.random()).first()
    return cur

@app.route('/search',methods=["post"])
def search():
    print("entered")
    search_word="%"+request.form["searching"]+"%"
    '''db = get_db()
    query = "SELECT id, type, front, back, known FROM cards WHERE front LIKE '"+search_word+"'"
    cur = db.execute(query)
    cards = cur.fetchall()'''
    cards=Cards.query.filter(Cards.front.like(search_word))
    print(cards,"hey hi",search_word)
    tags = getAllTag()
    return render_template('show.html', cards=list(cards), tags=list(tags), filter_name="all")    


@app.route('/mark_unknown/<card_id>/<card_type>')
def mark_unknown(card_id, card_type):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    '''db = get_db()
    db.execute('UPDATE cards SET known = 0 WHERE id = ?', [card_id])
    db.commit()'''
    card=Cards.query.get(card_id)
    card.known=False
    db.session.commit()
    flash('Card marked as unknown.')
    return redirect(url_for('memorize_known', card_type=card_type))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


