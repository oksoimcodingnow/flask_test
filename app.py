from ast import Pass
from flask import Flask, render_template, request, redirect
from sql_con import get_db_connection





app = Flask(__name__)


@app.route('/form_get',methods=['GET'])
def formGET_index():
    if request.method == 'GET':
        conn = get_db_connection()
        data = conn.execute('SELECT "id","username","firstname","lastname" FROM user').fetchall()
        conn.close()
        print('data',len(data))
        print(data)
        if len(data) != 0:
            for k in data:
                print(k[0], k[1], k[2], k[3])
            print('req.args:',len(request.args))
            if(len(request.args)!= 0):
                Firstname = request.args.get('firstname')
                Lastname = request.args.get('lastname')
                conn = get_db_connection()
                data = conn.execute('SELECT "id", "username", "firstname", "lastname" FROM user where firstname=? and lastname=?'\
                    ,(Firstname,Lastname)).fetchall()
                conn.close()
                print(data)
                if data is None:
                    return render_template('form_get.html')
                else:
                    for k in data:
                        print(k[0], k[1], k[2], k[3])
                        #return from search query
                    return render_template('form_get.html', data=data)
                #return if we query all data successfully
            return render_template('form_get.html' ,data=data)
        #return if len data from query all is 0
        return render_template('form_get.html')
    
@app.route('/form_post', methods=['GET','POST'])
def formPOST_index():
    
    if request.method == 'GET':
        return render_template('form_post.html')
    elif request.method == 'POST':
        print(len(request.form))
        if len(request.form) != 0:
            for key, value in request.form.items():
                print(key,value)
            Firstname = request.form.get('firstname')
            Lastname = request.form.get('lastname')
            Username = request.form.get('username')
            Password = request.form.get('password')
            print(Firstname)
            print(Lastname)
            print(Username)
            print(Password)
            conn = get_db_connection()
            conn.execute('INSERT INTO user ("username","firstname","lastname","password") VALUES (?,?,?,?)',(Username,Firstname,Lastname,Password))
            conn.commit()
            conn.close()
            return redirect("./form_get", code=302)




if __name__ =='main':
    app.run(debug=True)