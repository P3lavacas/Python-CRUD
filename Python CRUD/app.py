from flask import Flask
from flask import render_template, request, redirect, url_for
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    """Esta función permitira acceder a las fotos"""
    return send_from_directory(app.config['CARPETA'], nombreFoto)

@app.route('/')
def index():
    """ Esta función corre el index"""

    sql = "SELECT * FROM `empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()
    #print(empleados)
    conn.commit()

    return render_template('empleados/index.html', empleados = empleados)

@app.route('/destroy/<int:id>')
def destroy(id):
    """Esta funcion va a eliminar un elemento de la tabla"""
    conn = mysql.connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT Fotografía FROM empleados WHERE id=%s", id)
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
    
    cursor.execute("DELETE FROM empleados WHERE ID=%s", (id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    """Esta funcion va a editar un elemento de la tabla"""
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(" SELECT * FROM empleados WHERE id=%s", (id))
    empleados = cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados = empleados)

@app.route('/update', methods=['POST'])
def update():
    """Esta función va a actualizar los datos editados"""
    id = request.form['txtID']
    _nombre = request.form['txtNombre']
    _aPaterno = request.form['txtAPaterno']
    _aMaterno = request.form['txtAMaterno']
    _fechaN = request.form['txtFechaN']
    _alias = request.form['txtAlias']
    _correo = request.form['txtCorreo']
    _telefono = request.form['txtTelefono']
    _direccion = request.form['txtDireccion']
    _foto = request.files['txtFoto']

    sql = "UPDATE `empleados` SET `Nombre`=%s, `Apellido_Paterno`=%s, `Apellido_Materno`=%s, `Fecha_Nacimiento`=%s, `Alias`=%s, `Correo`=%s, `Teléfono`=%s, `Dirección`=%s  WHERE id =%s;"

    datos = (_nombre,_aPaterno, _aMaterno, _fechaN, _alias, _correo, _telefono, _direccion, id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)
        
        cursor.execute("SELECT Fotografía FROM empleados WHERE id=%s", id)
        fila = cursor.fetchall()
        
        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE empleados SET Fotografía=%s WHERE id=%s", (nuevoNombreFoto, id))
        conn.commit()
    
    conn.commit()
    return redirect('/')

@app.route('/create')
def create():
    """ Esta función corre el create, para ingresar datos de los empleados"""
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():
    """ Esta funciónmanda los datos ingresados a la BD"""

    _nombre = request.form['txtNombre']
    _aPaterno = request.form['txtAPaterno']
    _aMaterno = request.form['txtAMaterno']
    _fechaN = request.form['txtFechaN']
    _alias = request.form['txtAlias']
    _correo = request.form['txtCorreo']
    _telefono = request.form['txtTelefono']
    _direccion = request.form['txtDireccion']
    _foto = request.files['txtFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO `empleados` (`ID`, `Nombre`, `Apellido_Paterno`, `Apellido_Materno`, `Fecha_Nacimiento`, `Alias`, `Correo`, `Teléfono`, `Dirección`, `Fotografía`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    datos = (_nombre,_aPaterno, _aMaterno, _fechaN, _alias, _correo, _telefono, _direccion, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
    