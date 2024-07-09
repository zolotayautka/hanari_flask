#*******************************************************************************
#
# Copyright (C) 2024 sin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#*******************************************************************************

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import base64
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication, QSize, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from sqlalchemy import text
import sys
import threading
import os
import random
import socket

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
def item_detail(item_id):
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
    return render_template('detail.html', item=item, pi0=p0, p1=pt[0], p2=pt[1], p3=pt[2], p4=pt[3])

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
        return "追加なりました。"
    except:
        return "すでに存在するページです。"

@app.route('/delete')
def delete():
    return render_template('del.html')

@app.route('/delete_action', methods=['POST'])
def delete_exec():
    namae = request.form['del-keyword']
    page = syokubutsu.query.filter(syokubutsu.namae == namae).first()
    if page != None:
        db.session.delete(page)
        db.session.commit()
        with db.engine.connect() as connection:
            connection.execute(text('VACUUM'))
        return "ページを削除しました。"
    else:
        return "該当するページがありません。"

class main_form(object):
    def setupUi(self, mainQT):
        if not mainQT.objectName():
            mainQT.setObjectName(u"mainQT")
        mainQT.resize(905, 704)
        self.setWindowIcon(QIcon('icon.ico'))
        self.centralwidget = QWidget(mainQT)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 905, 704))
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.verticalLayoutWidget = QWidget(self.widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 901, 671))
        self.view_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.view_layout.setObjectName(u"view_layout")
        self.view_layout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.widget, "")
        self.widget1 = QWidget()
        self.widget1.setObjectName(u"widget1")
        self.add_btn = QPushButton(self.widget1)
        self.add_btn.setObjectName(u"add_btn")
        self.add_btn.setGeometry(QRect(20, 10, 91, 31))
        self.del_btn = QPushButton(self.widget1)
        self.del_btn.setObjectName(u"del_btn")
        self.del_btn.setGeometry(QRect(130, 10, 91, 31))
        self.verticalLayoutWidget_2 = QWidget(self.widget1)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 50, 881, 611))
        self.hensyuu_layout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.hensyuu_layout.setObjectName(u"hensyuu_layout")
        self.hensyuu_layout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.widget1, "")
        mainQT.setCentralWidget(self.centralwidget)
        self.retranslateUi(mainQT)
        self.tabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(mainQT)
    def retranslateUi(self, mainQT):
        mainQT.setWindowTitle(QCoreApplication.translate("mainQT", u"\u30cf\u30ca\u30ea", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), QCoreApplication.translate("mainQT", u"\u56f3\u9451", None))
        self.add_btn.setText(QCoreApplication.translate("mainQT", u"\u8ffd\u52a0", None))
        self.del_btn.setText(QCoreApplication.translate("mainQT", u"\u524a\u9664", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget1), QCoreApplication.translate("mainQT", u"\u7de8\u96c6", None))

class mainQT(QMainWindow, main_form):
    def __init__(self):
        global port
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(QSize(905, 704))
        self.web_view = QWebEngineView(self.verticalLayoutWidget)
        self.web_view.setUrl(QUrl(f"http://localhost:{port}"))
        self.view_layout.addWidget(self.web_view)
        self.web_view_ = None
        self.add_btn.clicked.connect(self.add_page)
        self.del_btn.clicked.connect(self.del_page)
    
    def add_page(self):
        if self.web_view_ != None:
            self.hensyuu_layout.removeWidget(self.web_view_)
            self.web_view_.deleteLater()
            del self.web_view_
            self.web_view_ = None
        self.web_view_ = QWebEngineView(self.verticalLayoutWidget)
        self.web_view_.setUrl(QUrl(f"http://localhost:{port}/add"))
        self.hensyuu_layout.addWidget(self.web_view_)

    def del_page(self):
        if self.web_view_ != None:
            self.hensyuu_layout.removeWidget(self.web_view_)
            self.web_view_.deleteLater()
            del self.web_view_
            self.web_view_ = None
        self.web_view_ = QWebEngineView(self.verticalLayoutWidget)
        self.web_view_.setUrl(QUrl(f"http://localhost:{port}/delete"))
        self.hensyuu_layout.addWidget(self.web_view_)

def run_qt():
    a = QApplication(sys.argv)
    main_QT = mainQT()
    main_QT.show()
    a.exec_()
    os._exit(0)

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(os.path.join(BASE_DIR, 'hanari.db')):
            db.create_all()
    global port
    while True:
        port = random.randint(7000, 8999)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) != 0:
                break
    thread = threading.Thread(target = run_qt)
    thread.start()
    app.run('0.0.0.0', port=port, debug=False)
