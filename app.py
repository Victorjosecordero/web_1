
import os
import sqlite3
from bottle import route,run,TEMPLATE_PATH, jinja2_view, static_file, request,redirect

from modelo_datos import BASE_DATOS

TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')

@route('/')
@jinja2_view('home.html')
def hola():
    cnx= sqlite3.connect(BASE_DATOS)
    consulta = 'SELECT p.id ,p.nombre ,p.apellidos ,p.dni ,to2.descripcion from personas p join t_ocupacion to2 on p.id_ocupacion = to2.id  '
    cursor=cnx.execute(consulta)
    filas = cursor.fetchall()
    cnx.close()

    return{'datos': filas}

@route('/editar')
@route('/editar/<id:int>')
@jinja2_view('formulario.html')
def mi_form(id=None):
    cnx=sqlite3.connect(BASE_DATOS)
    consulta = "select * from t_ocupacion"
    cursor= cnx.execute(consulta)
    ocupaciones = cursor.fetchall()
    
    if id is None:
        return {}
    else:
        cnx=sqlite3.connect(BASE_DATOS)
        consulta=f'SELECT id ,nombre ,apellidos ,dni,id_ocupacion from personas where id="{id}"'
        cursor= cnx.execute(consulta)
        filas = cursor.fetchone()
        
        
    cnx.close()
    return {'datos': filas, 'ocupaciones':ocupaciones}

@route('/eliminar/<id:int>')
def eliminar(id):
        cnx= sqlite3.connect(BASE_DATOS)
        consulta = f'delete from personas where id ="{id}"'
        cnx.execute(consulta)
        cnx.commit()
        cnx.close()
        redirect('/')


@route('/guardar', method='POST')
def guardar():
    nombre = request.POST.nombre
    apellidos = request.POST.apellidos
    dni= request.POST.dni
    id = request.POST.id
    ocupacion = request.POST.ocupacion


    cnx=sqlite3.connect(BASE_DATOS)
    if id =='':#alta
        consulta='insert into personas(nombre,apellidos,dni,id_ocupacion) values (?,?,?,?)'
        cnx.execute(consulta,(nombre,apellidos,dni,ocupacion))
    else:#Actualizacion
        consulta = 'update personas set nombre = ?, apellidos =?, dni=?, id_ocupacion=? where id =?' 
        cnx.execute(consulta,(nombre,apellidos,dni,ocupacion,id))
        
    cnx.commit()
    cnx.close()
    redirect('/')









run(host='localhost',port=8080, debug=True)