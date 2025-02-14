from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import base64
from sqlalchemy import text
import sys
import os

app = Flask(__name__)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'hanari.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class syokubutsu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namae = db.Column(db.String(50), nullable=False, unique=True)
    pic = db.Column(db.LargeBinary, nullable=False)
    naiyou = db.Column(db.Text, nullable=False)
    bunrui = db.Column(db.Text, nullable=True)
    p1 = db.Column(db.LargeBinary, nullable=True)
    p2 = db.Column(db.LargeBinary, nullable=True)
    p3 = db.Column(db.LargeBinary, nullable=True)
    p4 = db.Column(db.LargeBinary, nullable=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    results1 = syokubutsu.query.filter(syokubutsu.namae.like(f'%{keyword}%')).all()
    results2 = syokubutsu.query.filter(syokubutsu.bunrui.like(f'%{keyword}%')).all()
    results3 = syokubutsu.query.filter(syokubutsu.naiyou.like(f'%{keyword}%')).all()
    t = results1 + results2 + results3
    results = list(set(t))
    i = 0
    while i < len(results):
        results[i].pic = base64.b64encode(results[i].pic).decode('utf-8')
        i += 1
    return render_template('list.html', items=results)

@app.route('/list/<int:item_id>')
def view(item_id):
    item = syokubutsu.query.get_or_404(item_id)
    p0 = None
    p0 = base64.b64encode(item.pic).decode('utf-8')
    pt = [None, None, None, None]
    if item.p1 != None:
        pt[0] = base64.b64encode(item.p1).decode('utf-8')
    if item.p2 != None:
        pt[1] = base64.b64encode(item.p2).decode('utf-8')
    if item.p3 != None:
        pt[2] = base64.b64encode(item.p3).decode('utf-8')
    if item.p4 != None:
        pt[3] = base64.b64encode(item.p4).decode('utf-8')
    return render_template('view.html', item=item, pi0=p0, p1=pt[0], p2=pt[1], p3=pt[2], p4=pt[3])

@app.route('/bar1')
def bar1():
    return render_template('bar.html', mode=1)

@app.route('/bar2')
def bar2():
    return render_template('bar.html', mode=2)

@app.route('/amd', methods=['POST'])
def amd():
    yarukoto = request.form.get('action')
    namae = request.form.get('namae')
    if yarukoto == 'modify':
        bunrui = request.form.get('bunrui')
        naiyou = request.form.get('naiyou')
        p1 = bool(int(request.form.get('p1')))
        p2 = bool(int(request.form.get('p2')))
        p3 = bool(int(request.form.get('p3')))
        p4 = bool(int(request.form.get('p4')))
        return redirect(url_for('modify', namae=namae, bunrui=bunrui, naiyou=naiyou, p1=p1, p2=p2, p3=p3, p4=p4))
    elif yarukoto == 'delete':
        delete_page(namae)
        return render_template('init.html', mode=3)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/add_action', methods=['POST'])
def add_exec():
    try:
        namae = request.form['namae']
        naiyou = request.form['naiyou']
        bunrui = request.form['bunrui']
        photos = request.files.getlist('photos')
        t = [None, None, None, None, None]
        t[0] = photos[0].read()
        new_page = syokubutsu(namae=namae, naiyou=naiyou, bunrui=bunrui, pic=t[0])
        if len(photos) > 1 and len(photos) < 3:
            i = 1
            while i < 2:
                t[i] = photos[i].read()
                i += 1
            new_page = syokubutsu(namae=namae, naiyou=naiyou, bunrui=bunrui, pic=t[0], p1=t[1])
        elif len(photos) > 2 and len(photos) < 4:
            i = 1
            while i < 3:
                t[i] = photos[i].read()
                i += 1
            new_page = syokubutsu(namae=namae, naiyou=naiyou, bunrui=bunrui, pic=t[0], p1=t[1], p2=t[2])
        elif len(photos) > 3 and len(photos) < 5:
            i = 1
            while i < 4:
                t[i] = photos[i].read()
                i += 1
            new_page = syokubutsu(namae=namae, naiyou=naiyou, bunrui=bunrui, pic=t[0], p1=t[1], p2=t[2], p3=t[3])
        elif len(photos) > 4 and len(photos) < 6:
            i = 1
            while i < 5:
                t[i] = photos[i].read()
                i += 1
            new_page = syokubutsu(namae=namae, naiyou=naiyou, bunrui=bunrui, pic=t[0], p1=t[1], p2=t[2], p3=t[3], p4=t[4])
        else:
            new_page = syokubutsu(namae=namae, naiyou=naiyou, bunrui=bunrui, pic=t[0])
        db.session.add(new_page) 
        db.session.commit()
        return render_template('init.html', mode=1)
    except:
        return "<style> body { font-family: Arial, sans-serif; background-color: #abced8; } </style>すでに存在するページです。"

@app.route('/modify')
def modify():
    namae = request.args.get('namae')
    bunrui = request.args.get('bunrui')
    naiyou = request.args.get('naiyou')
    p1 = request.args.get('p1')
    p2 = request.args.get('p2')
    p3 = request.args.get('p3')
    p4 = request.args.get('p4')
    return render_template('modify.html', item=syokubutsu(namae=namae, naiyou=naiyou, bunrui=bunrui), p1=p1, p2=p2, p3=p3, p4=p4)

@app.route('/modify_exec', methods=['POST'])
def modify_exec():
    namae = request.form['namae']
    naiyou = request.form['naiyou']
    bunrui = request.form['bunrui']
    photo1 = request.files.get('photo1')
    photo2 = request.files.get('photo2')
    photo3 = request.files.get('photo3')
    photo4 = request.files.get('photo4')
    photo5 = request.files.get('photo5')
    page:syokubutsu = syokubutsu.query.filter(syokubutsu.namae == namae).first()
    page.naiyou = naiyou
    page.bunrui = bunrui
    if photo1:
        page.pic = photo1.read()
    if request.form['cb1'] == "True":
        page.p1 = None
    else:
        if photo2:
            page.p1 = photo2.read()
    if request.form['cb2'] == "True":
        page.p2 = None
    else:
        if photo3:
            page.p2 = photo3.read()
    if request.form['cb3'] == "True":
        page.p3 = None
    else:
        if photo4:
            page.p3 = photo4.read()
    if request.form['cb4'] == "True":
        page.p4 = None
    else:
        if photo5:
            page.p4 = photo5.read()
    db.session.commit()
    with db.engine.connect() as connection:
            connection.execute(text('VACUUM'))
    return render_template('init.html', mode=2)

def delete_page(namae):
    page = syokubutsu.query.filter(syokubutsu.namae == namae).first()
    if page != None:
        db.session.delete(page)
        db.session.commit()
        with db.engine.connect() as connection:
            connection.execute(text('VACUUM'))

@app.route('/init')
def kb():
    return render_template('init.html')

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(os.path.join(BASE_DIR, 'hanari.db')):
            db.create_all()
    app.run('0.0.0.0', port=5000, debug=False)