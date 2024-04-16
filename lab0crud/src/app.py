from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

def _SQLtoDict(SQLquery):
    cursor = db.database.cursor()
    cursor.execute(SQLquery)
    myresult = cursor.fetchall()
    columnNames = [column[0] for column in cursor.description]
    cursor.close()
    return [(dict(zip(columnNames,  [x if x!=None else " " for x in record]))) for record in myresult]
    
#Rutas de la aplicación
@app.route('/')
def home(): return render_template('index.html')

@app.route('/persona')
def persona():
    #print('PETICION /persona !!')
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM personas")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames,  [x if x!=None else " " for x in record])))
    cursor.close()
    list_viviendas = _SQLtoDict("SELECT * FROM viviendas")
    list_municipios = _SQLtoDict("SELECT * FROM municipios")
    return render_template('persona.html', data=insertObject, list_viviendas= list_viviendas, list_municipios=list_municipios)


@app.route('/persona_add', methods=['POST'])
def persona_add():
    nombre = request.form['nombre']
    t_doc = request.form['t_doc']
    n_doc = int(request.form['n_doc'])
    nacimiento = datetime.strptime(request.form['nacimiento'], '%Y-%m-%d').date()
    #print( 'datos-->  ',request.form)
    sexo = request.form['sexo']
    tel_cel = request.form.get('tel_cel')
    vivienda_actual =  int(request.form['id_vivienda_actual'])
    id_municipio_origen = int(request.form['id_municipio_origen'])
    if all(x for x in request.form.values()):
        cursor = db.database.cursor()
        sql = "INSERT INTO personas (id, tipo_doc, nombre, fecha_nac,  sexo, telefono, id_vivienda_actual, 'id_municipio_origen') VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data= (n_doc, t_doc, nombre, nacimiento, sexo, tel_cel, vivienda_actual, id_municipio_origen)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('persona'))



@app.route('/persona_edit/<string:id>', methods=["POST"])
def persona_edit(id):
    campos = ['tipo_doc', 'nombre', 'fecha_nac', 'sexo', 'telefono', 'id_vivienda_actual', 'id_municipio_origen']
    resp = [(clave, request.form.get(clave, None)) for clave in campos if request.form.get(clave, None)!=None]
    clear_data = tuple([r[1] for r in resp] + [id])
    sql = "UPDATE personas SET "
    for campo in resp:
        sql += f"{campo[0]} = %s, "
    sql = sql[:-2]  + " WHERE id = %s"
    try: 
        cursor = db.database.cursor()
        cursor.execute(sql, clear_data)
        db.database.commit()
        cursor.close()
    except :
        #print('error---->', e)
        pass
    return redirect(url_for('persona'))


@app.route('/persona_delete/<string:id>')
def persona_delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM personas WHERE id=%s"
    data = (id,)
    try:
        cursor.execute(sql, data)
        db.database.commit()
    except:
        pass
    
    return redirect(url_for('persona'))


@app.route('/vivienda')
def vivienda():
    data = _SQLtoDict("SELECT v.*, m.nombre AS nombre_municipio FROM viviendas v LEFT JOIN municipios m ON v.id_municipio = m.id")
    list_municipios = _SQLtoDict("SELECT * FROM municipios")
    #print(list_municipios,'\n\n', data)
    return render_template('vivienda.html', list_municipios=list_municipios,data=data)


@app.route('/vivienda_add', methods=['POST'])
def vivienda_add():
    ##print('SE LLEGÓ A VIVIENDA-ADD!', request.form)

    direccion = request.form['direccion']
    id_municipio = int(request.form['id_municipio'])
    capacidad = int(request.form['capacidad'])
    niveles = int(request.form['niveles'])

    area = int(request.form['area'])
    estrato = int(request.form['estrato'])
    categoria = request.form['categoria']

    if all(x for x in request.form.values()):
        cursor = db.database.cursor()
        sql = "INSERT INTO viviendas (direccion, id_municipio, capacidad,  niveles, area, estrato, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data= (direccion, id_municipio, capacidad, niveles, area, estrato, categoria)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('vivienda'))

@app.route('/vivienda_edit/<string:id>', methods=['POST'])
def vivienda_edit(id):
    direccion = request.form['direccion']
    id_municipio = int(request.form['id_municipio'])
    capacidad = int(request.form['capacidad'])
    niveles = int(request.form['niveles'])

    area = int(request.form['area'])
    estrato = int(request.form['estrato'])
    categoria = request.form['categoria']

    if all(x for x in request.form.values()):
        cursor = db.database.cursor()
        sql = "UPDATE viviendas SET direccion = %s, id_municipio = %s, capacidad = %s, niveles = %s, area = %s, estrato = %s, categoria = %s WHERE id = %s"
        data = (direccion, id_municipio, capacidad, niveles, area, estrato, categoria, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('vivienda'))



@app.route('/vivienda_delete/<string:id>')
def vivienda_delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM viviendas WHERE id=%s"
    data = (id,)
    try:
        cursor.execute(sql, data)
        db.database.commit()
    except:
        pass
    return redirect(url_for('vivienda'))



@app.route('/municipio')
def municipio():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM municipios")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()

    return render_template('municipio.html', data=insertObject)

@app.route('/municipio_add', methods=['POST'])
def municipio_add():
    id = int(request.form['id'])
    nombre = request.form['nombre']
    poblacion = int(request.form['poblacion'])
    if all(x for x in request.form.values()):
        cursor = db.database.cursor()
        sql = "INSERT INTO municipios (id, nombre, poblacion) VALUES (%s, %s, %s)"
        data= (id,nombre, poblacion)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('municipio'))


@app.route('/municipio_edit/<string:id>', methods=['POST'])
def municipio_edit(id):
    new_id = int(request.form['id'])
    nombre = request.form['nombre']
    poblacion = int(request.form['poblacion'])

    if all(x for x in request.form.values()):
        cursor = db.database.cursor()
        sql = "UPDATE municipios SET id = %s, nombre = %s, poblacion = %s WHERE id = %s"
        data = (new_id, nombre, poblacion, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('municipio'))


@app.route('/municipio_delete/<string:id>')
def municipio_delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM municipios WHERE id=%s"
    data = (id,)
    try:
        cursor.execute(sql, data)
        db.database.commit()
    except:
        pass

    return redirect(url_for('municipio'))



@app.route('/posesiones/<string:id>', methods=["GET"])
def posesiones(id):
    try:
        cursor = db.database.cursor()
        q="SELECT * FROM posesiones WHERE id_persona=%s"
        data=(id,)
        cursor.execute(q, data)
        myresult = cursor.fetchall()
    except:
        return render_template('index.html')
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()

    return render_template('posesion.html', data=insertObject, id=id)

@app.route('/posesiones_add', methods=['POST'])
def posesiones_add():
    id_persona = int(request.form['id_persona'])
    id_vivienda = int(request.form['id_vivienda'])
    fecha_posesion =  datetime.now().strftime('%Y-%m-%d')
    existen_count= _SQLtoDict(f"SELECT COUNT(*) AS cantidad_registros FROM posesiones WHERE id_persona = {id_persona} AND id_vivienda = {id_vivienda};")[0]
    if existen_count['cantidad_registros']>0:
        return redirect(url_for('posesiones', id=id_persona))
    try:
        if all(x for x in request.form.values()):
            cursor = db.database.cursor()
            sql = "INSERT INTO posesiones (id_persona, id_vivienda, fecha_posesion) VALUES (%s, %s, %s)"
            data= (id_persona,id_vivienda, fecha_posesion)
            cursor.execute(sql, data)
            db.database.commit()
    except:
        redirect(url_for('posesiones', id=id_persona))
    return redirect(url_for('posesiones', id=id_persona))



@app.route('/posesiones_edit/<string:id>', methods=['POST'])
def posesiones_edit(id):
    id_persona = int(request.form['id_persona'])
    id_vivienda = int(request.form['id_vivienda'])
    fecha_posesion = datetime.strptime(request.form['fecha_posesion'], '%Y-%m-%d').date()
    existen_count= _SQLtoDict(f"SELECT COUNT(*) AS cantidad_registros FROM posesiones WHERE id_persona = {id_persona} AND id_vivienda = {id_vivienda};")[0]
    if existen_count['cantidad_registros']>0:
        return redirect(url_for('posesiones', id=id_persona))
    if all(x for x in request.form.values()):
        cursor = db.database.cursor()
        sql = "UPDATE posesiones SET id_persona = %s, id_vivienda = %s, fecha_posesion = %s WHERE id = %s"
        data = (id_persona, id_vivienda, fecha_posesion, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('posesiones', id= id_persona))



@app.route('/posesiones_delete/<string:id>/<string:id_p>')
def posesiones_delete(id, id_p):
    cursor = db.database.cursor()
    sql = "DELETE FROM posesiones WHERE id=%s"
    data = (id,)
    try:
        cursor.execute(sql, data)
        db.database.commit()
    except:
        pass
    return redirect(url_for('posesiones', id= id_p))


@app.route('/cdf/<string:id>', methods=["GET"])
def cdf(id):
    #print('ESTA ES LA ID CDF: ---> ',  id)
    try:
        cursor = db.database.cursor()
        q="SELECT cdf.*, persona1.nombre AS nombre_persona1, persona2.nombre AS nombre_persona2 FROM cdf LEFT JOIN personas AS persona1 ON cdf.id_persona = persona1.id LEFT JOIN personas AS persona2 ON cdf.id_cdf = persona2.id WHERE cdf.id_persona =%s OR cdf.id_cdf =%s;"
        data=(id,id)
        cursor.execute(q, data)
        myresult = cursor.fetchall()

    except :
        #print('ERROR SQL: ---> ', e)
        return render_template('index.html')

    #Convertir los datos a diccionario
    insertObject = []

    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    data_pred= {'id': id}
    return render_template('cdf.html', data=insertObject, data_pred=data_pred)

@app.route('/cdf_add', methods=['POST'])
def cdf_add():
    id_persona = int(request.form['id_persona'])
    id_vivienda = int(request.form['id_cdf'])
    fecha_registro =  datetime.now().strftime('%Y-%m-%d')
    try:

        if all(x for x in request.form.values()):
            cursor = db.database.cursor()
            sql = "INSERT INTO cdf (id_persona, id_cdf, fecha_registro) VALUES (%s, %s, %s)"
            data= (id_persona,id_vivienda, fecha_registro)
            cursor.execute(sql, data)
            db.database.commit()
            cursor.close()
    except:
        pass
    return redirect(url_for('cdf', id=id_persona))

fecha_actual = datetime.now().strftime('%Y-%m-%d')



@app.route('/cdf_edit/<string:id>', methods=['POST'])
def cdf_edit(id):
    id_persona = request.form['id_persona']
    id_vivienda = request.form['id_cdf']
    fecha_registro = datetime.strptime(request.form['fecha_registro'], '%Y-%m-%d').date()
    try:
        if all(x for x in request.form.values()):
            cursor = db.database.cursor()
            sql = "UPDATE cdf SET id_persona = %s, id_cdf = %s, fecha_registro = %s WHERE id = %s"
            data = (id_persona, id_vivienda, fecha_registro, id)
            cursor.execute(sql, data)
            db.database.commit()
            cursor.close()
    except:
        return redirect(url_for('cdf', id=id))
    return redirect(url_for('cdf', id=id_persona))


@app.route('/cdf_delete/<string:id_r>/<string:id_p>')
def cdf_delete(id_r, id_p):
    cursor = db.database.cursor()
    sql = "DELETE FROM cdf WHERE id=%s"
    data = (id_r,)
    try:
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()
    except :
        pass
    return redirect(url_for('cdf', id=id_p))

@app.route('/gobernar/<string:id>', methods=["GET"])
def gobernar(id):
    sql = """
SELECT 
    g.id AS id, 
    g.id_persona AS id_gobernante, 
    p.nombre AS nombre_gobernante, 
    d.id AS id_departamento,
    d.nombre AS nombre_departamento,
    g.fecha_registro 
FROM 
    gobernadores g 
INNER JOIN 
    personas p ON g.id_persona = p.id 
INNER JOIN
    departamentos d ON g.id_departamento = d.id
"""    
    if(int(id)>=0):
        sql += f" WHERE g.id_persona = {id};"
    try:
        data = _SQLtoDict(sql)
        personas = _SQLtoDict("SELECT id, nombre FROM personas")
        departamentos = _SQLtoDict("SELECT id, nombre FROM departamentos")

    except :
        #print('ERROR EN GOBERNAR:-->', e)
        return render_template('index.html')
    return render_template('gobernar.html', data=data, id=id, personas=personas, departamentos=departamentos)

@app.route('/gobernar_add', methods=['POST'])
def gobernar_add():
    id_persona = request.form.get('id_persona')
    id_departamento = request.form.get('id_departamento')
    fecha_registro =  datetime.now().strftime('%Y-%m-%d')
    try:
        if (id_persona and id_municipio):

            existen_count= _SQLtoDict(f"SELECT COUNT(*) AS cantidad_registros FROM gobernadores WHERE id_persona = {id_persona} AND id_municipio = {id_municipio};")[0]['cantidad_registros']
            if existen_count>0:
                #print('existen repetidos al agregar, se aviso desde backend!!')
                return redirect(url_for('posesiones', id=-1))
            cursor = db.database.cursor()
            sql = "INSERT INTO gobernadores (id_persona,id_departamento, fecha_registro) VALUES (%s, %s, %s)"
            data= (id_persona,id_municipio, fecha_registro)
            cursor.execute(sql, data)
            db.database.commit()
            cursor.close()
    except :
        pass
    return redirect(url_for('gobernar', id=-1))


@app.route('/gobernar_edit/<string:id>', methods=['POST'])
def gobernar_edit(id):
    fecha_registro = datetime.strptime(request.form['_fecha_registro'], '%Y-%m-%d').date()
    id_persona = request.form.get('_id_persona', None)
    id_departamento = request.form.get('_id_departamento')

    if (id_persona and id_vivienda):
         existen_count= _SQLtoDict(f"SELECT COUNT(*) AS cantidad_registros FROM gobernadores WHERE id_persona = {id_persona} OR id_departamento = {id_departamento};")[0]
         if existen_count['cantidad_registros']>0:
            #print('existen repetidos al editar, se aviso desde backend!!')
            return redirect(url_for('gobernar', id=-1))

    try: 
        cursor = db.database.cursor()
        sql = "UPDATE gobernadores SET id_persona = %s, id_departamento = %s, fecha_registro = %s WHERE id = %s"
        data = (id_persona, id_departamento, fecha_registro, id)
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()
    except :
        pass
    return redirect(url_for('gobernar', id=-1))

@app.route('/gobernar_delete/<string:id_r>/<string:id_p>')
def gobernar_delete(id_r, id_p):
    #print('datos..--->', id_r, type(id_r), id_p, type(id_p), '\n\n')
    cursor = db.database.cursor()
    sql = "DELETE FROM gobernadores WHERE id=%s"
    data = (id_r,)
    try:
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()
    except :
        #print('error en gobernado delete', e)
        pass
    return redirect(url_for('gobernar', id=-1))




@app.route('/gobernar_repetidos/<string:id_persona>/<string:id_municipio>', methods=["GET"])
def gobernar_repetidos(id_persona, id_municipio):
    existen_count= _SQLtoDict(f"SELECT COUNT(*) AS cantidad_registros FROM gobernadores WHERE id_persona = {id_persona} AND id_municipio = {id_municipio};")[0]['cantidad_registros']
    return existen_count

















@app.route('/alcaldia/', methods=["GET"])
def alcaldia():
    sql = """
SELECT 
    a.id AS id, 
    a.id_persona AS id_alcalde, 
    p.nombre AS nombre_alcalde, 
    a.id_municipio, 
    m.nombre AS nombre_municipio
FROM 
    alcaldes a 
INNER JOIN 
    personas p ON a.id_persona = p.id 
INNER JOIN 
    municipios m ON a.id_municipio = m.id
"""  
  
    try:
        alcaldes = _SQLtoDict(sql)
        personas = _SQLtoDict("SELECT id, nombre FROM personas")
        municipios = _SQLtoDict("SELECT id, nombre FROM municipios")
        alcaldes_p = _SQLtoDict("""
SELECT 
    *
FROM 
    personas p 
INNER JOIN 
    alcaldes a ON a.id_persona = p.id""")

    except Exception as e:
        print('ERROR EN GOBERNAR:-->', e)
        return render_template('index.html')
    return render_template('alcaldes.html', data=alcaldes, id=id, personas=personas, alcaldes_p=alcaldes_p, municipios=municipios)

@app.route('/alcaldia_add', methods=['POST'])
def alcaldia_add():
    id_persona = request.form.get('id_persona')
    id_municipio = request.form.get('id_municipio')
    fecha_registro =  datetime.now().strftime('%Y-%m-%d')
    try:
        if (id_persona and id_municipio):

            existen_count= _SQLtoDict(f"SELECT COUNT(*) AS cantidad_registros FROM alcaldes WHERE id_persona = {id_persona} AND id_municipio = {id_municipio};")[0]['cantidad_registros']
            if existen_count>0:
                #print('existen repetidos al agregar, se aviso desde backend!!')
                return redirect(url_for('alcaldia', id=-1))
            cursor = db.database.cursor()
            sql = "INSERT INTO alcaldes (id_persona, id_municipio, fecha_registro) VALUES (%s, %s, %s)"
            data= (id_persona,id_municipio, fecha_registro)
            cursor.execute(sql, data)
            db.database.commit()
            cursor.close()
    except :
        pass
    return redirect(url_for('alcaldia', id=-1))


@app.route('/alcaldia_edit/<string:id>', methods=['POST'])
def alcaldia_edit(id):
    fecha_registro = datetime.strptime(request.form['_fecha_registro'], '%Y-%m-%d').date()
    id_persona = request.form.get('_id_persona')
    id_municipio = request.form.get('_id_municipio')
    if (id_persona and id_vivienda):
         existen_count= _SQLtoDict(f"SELECT COUNT(*) AS cantidad_registros FROM alcaldes WHERE id_persona = {id_persona} AND id_municipio = {id_municipio};")[0]
         if existen_count['cantidad_registros']>0:
            #print('existen repetidos al editar, se aviso desde backend!!')
            return redirect(url_for('alcaldia', id=-1))

    try: 
        cursor = db.database.cursor()
        sql = "UPDATE alcaldes SET id_persona = %s, id_municipio = %s, fecha_registro = %s WHERE id = %s"
        data = (id_persona,id_municipio, fecha_registro, id)
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()
    except :
        pass
    return redirect(url_for('alcaldia', id=-1))

@app.route('/alcaldia_delete/<string:id_r>/<string:id_p>')
def alcaldia_delete(id_r, id_p):
    #print('datos..--->', id_r, type(id_r), id_p, type(id_p), '\n\n')
    cursor = db.database.cursor()
    sql = "DELETE FROM alcaldes WHERE id=%s"
    data = (id_r,)
    try:
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()
    except :
        #print('error en gobernado delete', e)
        pass
    return redirect(url_for('alcaldia', id=-1))

























if __name__ == '__main__':
    app.run()

