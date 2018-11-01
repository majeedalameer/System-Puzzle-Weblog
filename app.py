import datetime
import os
import psycopg2

from flask import Flask, render_template


def compute_rate(cur,request_src):
	# Get number of GET requests depending on the source, local, remote or any
	sql_all = """SELECT COUNT(*) FROM weblogs;"""
	if request_src != 'any':
		sql_all = """SELECT COUNT(*) FROM weblogs WHERE src = \'%s\';""" % request_src
	cur.execute(sql_all)
	all = cur.fetchone()[0]

	# Get number of all succesful requests depending on the source, local, remote or any
	sql_success = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\'"""
	if request_src != 'any':
		sql_success = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\' AND src = \'%s\';""" % request_src
	cur.execute(sql_success)
	success = cur.fetchone()[0]

	# Determine rate if there was at least one request
	rate = "No entries yet!"
	if all != 0:
		rate = str(success / all)
	return rate
	

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def index():
    # Connect to database
    conn = psycopg2.connect(host='db', database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()

    rate = compute_rate(cur, request_src = 'any')
    localrate = compute_rate(cur, request_src = 'local')
    remoterate = compute_rate(cur, request_src = 'remote')

    return render_template('index.html', rate = rate ,localrate = localrate, remoterate = remoterate)

if __name__ == '__main__':
    app.run(host='0.0.0.0')



