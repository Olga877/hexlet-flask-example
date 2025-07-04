import json
import uuid
from os import abort
from validator import validate
from user_repository import UserRepository
import psycopg2

from flask import Flask, redirect, render_template, request, url_for, flash, get_flashed_messages


conn = psycopg2.connect("dbname=hexlet user=olga877")
repo = UserRepository(conn)

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/users")
def users_index():
    term = request.args.get("term", "")
    if term:
        users = repo.get_by_term(term)
    else:
        users = repo.get_content()
    messages = get_flashed_messages(with_categories=True)
    print(messages)
    return render_template("users/index.html", search=term, users=users)


@app.route("/users/<int:id>")
def users_show(id):
    user = repo.find(id)
    if user is None:
        abort(404)
    return render_template("users/show.html", user=user)


@app.route("/users/new")
def users_new():
    return render_template("users/new.html", user={}, errors={})


@app.route("/users", methods=["POST"])
def users_post():
    data = request.form.to_dict()

    errors = validate(data)

    if not errors:
        user = {"name": data["name"], "email": data["email"]}
        repo.save(user)
        flash("User was added successfully", "success")
        return redirect(url_for("users_index"))

    return render_template("users/new.html", user=data, errors=errors), 422


# users = json.load(open("./users.json", 'r'))


# @app.route('/')
# def hello_world():
#     app.logger.info("Получен запрос к главной странице")
#     return 'Welcome to Flask!'
#
#
# @app.route('/users')
# def users_index():
#     try:
#         app.logger.debug("Начинаем запрос к '/users/'")
#         with open("./users.json", "r") as f:
#             users = json.load(f)
#         term = request.args.get('term', '')
#         filtered_users = [user for user in users if term in user['name']]
#         messages = get_flashed_messages(with_categories=True)
#         print(messages)
#         return render_template(
#                 'users/index.html',
#                 users=filtered_users,
#                 search=term,
#                 messages=messages,
#                 )
#     except Exception as e:
#         app.logger.warning(f"'/users' недоступен")
#
# @app.route("/users/<int:id>/edit")
# def users_edit(id):
#     with open("./users.json", "r") as f:
#         users = json.load(f)
#     filtered_users = [user for user in users if user['id'] == id]
#     # filtered_users_list = list(filtered_users)
#     if not filtered_users:
#         return "user not found", 404
#     user = filtered_users[0]
#     errors = {}
#     return render_template(
#         'users/edit.html',
#         user=user,
#         errors=errors,
#     )
#
# @app.route("/users/<id>/patch", methods=["POST"])
# def users_patch(id):
#     user_data = request.form.to_dict()
#     errors = validate(user_data)
#     if errors:
#         return render_template(
#             'users/edit.html',
#             user=user_data,
#             errors=errors,
#         )
#     id = str(uuid.uuid4())
#     user = {'id': id, 'name': user_data['name'], 'email': user_data['email']}
#
#     # Ручное копирование данных из формы в нашу сущность
#     users.append(user)
#     with open("./users.json", "w") as f:
#         json.dump(users, f)
#     flash("Пользователь успешно обновлен", "success")
#     return redirect(url_for('users_index'), code=302)
#
# @app.route("/users/<int:id>/delete", methods=["POST"])
# def users_delete(id):
#     with open("./users.json", "r") as f:
#         users = json.load(f)
#     filtered_users = [user for user in users if user['id'] == id]
#     if not filtered_users:
#         return "user not found", 404
#     users.remove(filtered_users[0])
#     with open("./users.json", "w") as f:
#         json.dump(users, f)
#     flash("User has been deleted", "success")
#     return redirect(url_for("users_index"))
#
# @app.post('/users')
# def users_post():
#     user_data = request.form.to_dict()
#     errors = validate(user_data)
#     if errors:
#         return render_template(
#             'users/new.html',
#             user=user_data,
#             errors=errors,
#         )
#     id = str(uuid.uuid4())
#     user = {
#         'id': id,
#         'name': user_data['name'],
#         'email': user_data['email']
#     }
#     users.append(user)
#     with open("./users.json", "w") as f:
#         json.dump(users, f)
#     flash("Пользователь успешно добавлен", "success")
#     return redirect(url_for('users_index'), code=302)
#
#
# @app.route('/users/new')
# def users_new():
#     user = {'name': '', 'email': ''}
#     errors = {}
#     return render_template(
#         'users/new.html',
#         user=user,
#         errors=errors,
#     )
#
#
# @app.route('/users/<id>')
# def users_show(id):
#     with open("./users.json", "r") as f:
#         users = json.load(f)
#     user = next(user for user in users if id == str(user['id']))
#     if not user:
#         abort()
#     return render_template(
#         'users/show.html',
#         user=user,
#     )
#
# @app.errorhandler(404)
# def not_found(error):
#     return "Oops!", 404
#
#
# @app.route('/courses/<id>')
# def courses(id):
#     return f'Course id: {id}'


# def validate(user):
#     errors = {}
#     if not user['name']:
#         errors['name'] = "Can't be blank"
#     if not user['email']:
#         errors['email'] = "Can't be blank"
#     return errors


# users = [
#     {"id": 1, "name": "mike"},
#     {"id": 2, "name": "mishel"},
#     {"id": 3, "name": "adel"},
#     {"id": 4, "name": "keks"},
#     {"id": 5, "name": "kamila"},
# ]
#
#
# @app.route("/users")
# def users_show():
#     query = request.args.get('query', default=None)
#     if query is None:
#         return render_template(
#         "users/index.html",
#         users = users,
#     )
#     filtered_users = filter(lambda user: query in user["name"], users)
#     final_users = list(filtered_users)
#
#     return render_template(
#         "users/index.html",
#         users = final_users,
#         search=query,
#     )


# @app.before_request
# def check_id():
#     if request.endpoint == "resource":
#         id = request.args.get("id")
#         if not id:
#             # в случае запроса на /resouce сработает условие мидлвары
#             return 'Bad Request: Missing "id" parameter', 400
#     return None  # иначе возвращаем None, чтобы продолжить цепочку
#
#
# @app.before_request
# def log_path():
#     print(f"Request path: {request.path}")
#
#
# @app.route("/")
# def home():
#     return "Hello from Hexlet"
#
#
# @app.route("/resource")
# def resource():
#     id = request.args.get("id")
#     return f"Resource with id: {id}"

# @app.route("/courses/<lala>")
# def courses_show(lala):
#     return f"Course id: {lala}\n"
#
#
# @app.post('/users')
# def users():
#     return 'Users', 302
#
# @app.route("/hello")
# def hello():
#     # создаем объект response
#     response = make_response("Hello, World!")
#     # Устанавливаем заголовок
#     response.headers["X-MyHeader"] = "Thats my header!"
#     # Меняем тип ответа
#     response.mimetype = "text/plain"
#     # Задаем статус
#     response.status_code = 201
#     # Устанавливаем cookie
#     response.set_cookie("super-cookie", "42")
#     return response
#
# @app.route("/json/")
# def json():
#     return {"json": 42}  # Возвращает тип application/json
#
#
# @app.route("/html/")
# def html():
#     return "<h1>Hello, world!</h1>"  # Возвращает тип text/html
#
# @app.errorhandler(404)
# def not_found(error):
#     return "Oops!", 404


# @app.route('/')
# def hello_world():
#     print(request.headers)  # Выводит все заголовки
#     return "Hello, World!"
#
#
# @app.get('/users')
# def users_get():
#     return 'GET /users'
#
#
# @app.post('/users')
# def users_post():
#     return 'POST /users\n'

if __name__ == "__main__":
    # debug=True — чтобы при правках перезапускался сервер
    app.run(host="0.0.0.0", port=8000, debug=True)