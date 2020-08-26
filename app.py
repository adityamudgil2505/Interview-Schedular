from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

# Helper function

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getting_user_id():
    try:
        with sql.connect('database.db') as con:
            con.row_factory = dict_factory
            curr = con.cursor()
            curr.execute("SELECT user_id FROM users")
            rows = curr.fetchall()
            rows = [ x['user_id'] for x in rows]
    except Exception as ex:
            con.rollback()
            print(ex)
    finally:
        return rows
        con.close()

    con.close()

def candidates_from_interview_id(interview_id):
    cmd = "SELECT DISTINCT(T1.email_id) FROM users as T1 INNER JOIN candidates as T2 on T1.user_id = T2.candidate_id WHERE T2.interview_id = {}".format(interview_id)
    candidates = []
    with sql.connect('database.db') as con:
        con.row_factory = dict_factory
        curr = con.cursor()
        curr.execute(cmd)
        rows = curr.fetchall()
        candidates = [ x['email_id'] for x in rows]
        print(candidates)
    return candidates

# Return 0 if free
# Return 1 if we interviewer have other event
# Return 2 if we candidate have other event
def validationHelper(candidates, start_time, end_time, interviewer_id):    
    cmd1 = "SELECT interview_id, interviewer_id FROM interview WHERE NOT(end_time < {}  OR  {} < start_time)".format(start_time, end_time)
    cmd2 = "SELECT count(DISTINCT(candidate_id)) FROM candidates  as T1 WHERE T1.interview_id = ( SELECT T2.interview_id FROM interview as T2 WHERE NOT(T2.end_time < {}  OR  {} < T2.start_time))".format(start_time, end_time)
    print(cmd1)
    print(cmd2)
    ans = 3
    try:
        with sql.connect('database.db') as con:
            con.row_factory = dict_factory
            curr = con.cursor()
            curr.execute(cmd1)
            rows = curr.fetchall()
            print(rows)
            for row in rows:
                if row['interviewer_id'] == interviewer_id:
                    ans = 1
                    raise Exception("1")
            curr.execute(cmd2)
            candidateBusy = curr.fetchall()[0]['count(DISTINCT(candidate_id))']
            print(candidateBusy)
            if candidateBusy > 0:
                ans = 2
                raise Exception("2")
            con.close()
            ans=0
    except Exception as ex:
            con.rollback()
            print(ex)
    finally:
        return ans
        con.close()



# Routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def addInterview():
    user_id = getting_user_id()
    return render_template('interviewForm.html', msg = "", user_id = user_id)

@app.route('/submitForm', methods = ['POST', 'GET'])
def submitForm():
    if request.method == 'POST':
        msg = ""
        try:
            interviewer_id = int(request.form['interviewer_id'])
            start_time = int(request.form['start_time'])
            end_time = int(request.form['end_time'])
            candidates = request.form.getlist('candidate_id')
            valid = validationHelper(candidates, start_time, end_time, interviewer_id)
            print(valid)
            if valid == 1:
                msg = "interviewer have other event"
                print(msg)
            elif valid == 2:
                msg = "candidate have other event"
                print(msg)
            elif valid == 3:
                msg = "database error"
                print(msg)
            else:
                with sql.connect('database.db') as con:
                    cur = con.cursor()
                    print(interviewer_id, start_time, end_time, candidates)
                    cur.execute("INSERT INTO interview (start_time, end_time, interviewer_id) VALUES (?, ?, ?)", (start_time, end_time, interviewer_id))
                    interview_id = int(cur.lastrowid)
                    for candidate_id in candidates:
                        candidate_id = int(candidate_id)
                        cur.execute("INSERT INTO candidates (interview_id, candidate_id) VALUES (?, ?)", (interview_id, candidate_id))
                    con.commit()
                    msg="Interview Details successfully added"
        except Exception as ex:
            con.rollback()
            msg = "Error while updating interview details"
            print(ex)
        finally:
            return render_template("interviewForm.html", msg = msg)
            con.close()

@app.route('/viewList')
def viewList():
    con = sql.connect('database.db')
    con.row_factory = dict_factory
    curr = con.cursor()
    curr.execute("SELECT * FROM interview")
    rows = curr.fetchall()
    con.close()
    for i in range(len(rows)):
        row = rows[i]
        email_id = candidates_from_interview_id(row['interview_id'])
        email_id = '  ||  '.join(email_id)
        rows[i]['email'] = email_id
    return render_template('list.html', rows = rows)

if __name__ == '__main__':
    app.run(debug=True)