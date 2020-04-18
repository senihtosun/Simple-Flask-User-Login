import flask_login
from flask_login import LoginManager, UserMixin
from flask import Flask, render_template, url_for, redirect, request
from flask_socketio import SocketIO

login_manager = LoginManager()

app = Flask(__name__,
        static_url_path = '',
        static_folder = 'static',
        template_folder = 'templates')

app.secret_key = 'osmanlineverdies'

socketio = SocketIO(app)

# Login Manager Config
login_manager.init_app(app)

users = {'admin':{'pw':'tosun'}}


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
  if username not in users:
    return

  user = User()
  user.id = username
  return user



@login_manager.request_loader
def request_loader(request):
  username = request.form.get('username')
  if username not in users:
    return

  user = User()
  user.id = username

  user.is_authenticated = request.form['pw'] == users[username]['pw']

  return user



@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    username = request.form.get('username')
    if request.form.get('pw') == users[username]['pw']:
      user = User()
      user.id = username
      flask_login.login_user(user)
      return redirect(url_for('protect'))
  return render_template('index.html')


@app.route('/protect', methods=['GET', 'POST'])
@flask_login.login_required
def protect():
  return render_template('protected.html')


@app.route('/logout')
def logout():
  flask_login.logout_user()
  return 'Logged out'


# Socket IO CONFIG
def messageReceived(methods=['GET', 'POST']):
    print('Message was received')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)



if __name__ == "__main__":
    socketio.run(app, debug=True)
    
