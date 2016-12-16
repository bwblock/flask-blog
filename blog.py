import os, re
from string import letters
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash    #import flask class

app = Flask(__name__)

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Post


import datetime


engine = create_engine('sqlite:///blog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


@app.route("/")
def MainPage():
      return '<h1>Brian is Cool!</h1>'

@app.route("/welcome")
def welcome():
    username = request.args.get('username')
    if valid_username(username):
      return render_template('welcome.html', username = username)
    else:
      return redirect(url_for('signup'))

@app.route("/rot13", methods = ['POST','GET'])
def rot13():
    if request.method == 'GET':
       return render_template('rot13-form.html')
    if request.method == 'POST':
       rot13 = ''
       text = request.form['text']
       if text:
          rot13 = text.encode('rot13')
       return render_template('rot13-form.html', text = rot13)

@app.route("/signup", methods = ['POST','GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup-form.html')
    if request.method == 'POST':
        have_error = False
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']

        print email
        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True
        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True
        if not valid_email(email):
            params['error_email'] = "Please enter a valid email address."
            have_error = True

        if have_error:
            return render_template('signup-form.html', **params)
        else:
          return redirect('/welcome?username=' +username)

@app.route("/blog/", methods = ['GET'])
def BlogFront():
#        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        posts = session.query(Post).order_by(desc(Post.created)).limit(10).all()
        return render_template('front.html', posts = posts)

@app.route("/blog/permalink/<int:post_id>")
def PostPage(post_id):

#        post_id = request.args['post']
#        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = session.query(Post).filter_by(id = post_id).one()
        if not post:
            return "Error: file not found"
        subject = post.subject
        content = post.content
        return render_template("permalink.html", subject=subject, content=content)


@app.route('/blog/newpost', methods = ['GET','POST'])
def NewPost():
    if request.method == 'GET':
        return render_template("newpost.html")

    if request.method == 'POST':
        subject = request.form['subject']
        content = request.form['content']

        if subject and content:
            newpost = Post(subject=subject, content = content)
            session.add(newpost)
            session.commit()

            return redirect(url_for('PostPage', post_id = newpost.id))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)



#   -------------------  regular expressions for signup ---------------------------------#

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{5,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return email and EMAIL_RE.match(email)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)