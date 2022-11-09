from flask import Flask
from flask import render_template, request
from flaskext.msql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

@app.route('/')
def index():
    """ Esta función corre el index"""

    sql = ""
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    return render_template('empleados/index.html')

@app.route('/create')
def create():
    """ Esta función corre el create"""
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():
    """ Esta función"""

    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    sql = "INSERT INTO `empleados` (`nombre`, `correo`, `foto`) VALUES (NULL,%s, %s, %s);"

    datos = (_nombre, _correo, _foto.filename)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return render_template('empleados/index.html')

if __name__ == '__main__':
    app.run(debug=True)
    