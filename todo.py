# -*- coding: utf-8 -*-

import sqlite3
from bottle import route, run, debug, template, request, static_file, error, redirect

# only needed when you run Bottle on mod_wsgi
from bottle import default_app

import argparse

parser = argparse.ArgumentParser(description='Example: $ todo.py -s 127.0.0.1 -p 8080')
parser.add_argument('-s', '--server', metavar='{1024..65535}', type=str, default='127.0.0.1')
parser.add_argument('-p', '--port', metavar='{0..65535}', type=str, default='8080')

args = parser.parse_args()

def connect(func): #func(c=None)
    def _connect(*args,**kw):
        con = sqlite3.connect("todo.db")
        c = con.cursor()
        result = func(c)
        con.close()
        return result
    return _connect

@route('/')
def main():
    redirect("/todo")

@route('/urls')
def urls():
	for i in ['/todo', '/new', '/edit/1', '/item/1', '/json/1', '/help']:
		yield('<a href="http://localhost:8080%s"> %s </a></br>') % (i, i)

@route('/todo')
@connect
def todo_list(c=None):

    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    c.close()

    url = urls()

    output = template('src/templates/make_table', rows=result, url=urls, root='/src/')
    return output

@route('/src/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='src/css')

@route('/new', method='GET')
@connect
def new_item(c=None):

    if request.GET.save:

        new = request.GET.task.strip()

        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new, 1))
        new_id = c.lastrowid

        conn.commit()
        c.close()

        return '<p>The new task was inserted into the database, the ID is %s</p>' % new_id

    else:
        return template('src/templates/new_task.tpl')


@route('/edit/<no:int>', method='GET')
def edit_item(no):

    if request.GET.save:
        edit = request.GET.task.strip()
        status = request.GET.status.strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, no))
        conn.commit()

        return '<p>The item number %s was successfully updated</p>' % no
    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no)))
        cur_data = c.fetchone()

        return template('src/templates/edit_task.tpl', old=cur_data, no=no, root='/src/')


@route('/item/<item:re:[0-9]+>')
def show_item(item):

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
        result = c.fetchall()
        c.close()

        if not result:
            return 'This item number does not exist!'
        else:
            return 'Task: %s' % result[0]


@route('/help')
def help():

    static_file('src/templates/help.html', root='.')


@route('/json/<json:re:[0-9]+>')
def show_json(json):

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (json,))
    result = c.fetchall()
    c.close()

    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {'task': result[0]}


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

debug(True)
run(host=args.server, port=args.port, reloader=True)
# remember to remove reloader=True and debug(True) when you move your
# application from development to a productive environment
