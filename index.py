from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
import platform
import urllib
import json
import model


# конфигурация подключения к СУБД
# db = {
#     'driver': '{ODBC Driver 17 for SQL Server}' if platform.system() == 'Linux' else '{SQL Server}',
#     'server': 'TKSDD-SAP000001.delta.sbrf.ru,1102',
#     # 'server': 'v-sap-12r2-002.ca.sbrf.ru,1102',
#     'database': 'Pimop_www',

#     'dbCreditionalsStr': '' if platform.system() == 'Linux' else 'trusted_connection=yes',
#     'dbCreditionalsFile': '/etc/odbc_mssql_creditionals.secret' if platform.system() == 'Linux' else None,

#     'dbConnectionStringFormat': 'driver={driver};server={server};database={database};{dbCreditionalsStr};',
#     'dbConnectionStringExtra': 'mssql+pyodbc:///?odbc_connect=',
#     'dbConnectionString': None,

#     'dbConnection': None,
#     'dbRawConnection': None,

#     'dateFormat': '%Y-%m-%d %H:%M:%S',
# }

# настройка для работы под ТУЗ на сервере Linux
# if db['dbCreditionalsFile'] is not None:
#     try:
#         dbCreditionalsStr = open(db['dbCreditionalsFile']).read()
#     except:
#         dbCreditionalsStr = ''

#     if dbCreditionalsStr != '':
#         db['dbCreditionalsStr'] = dbCreditionalsStr

# формирование строки подключения
# db['dbConnectionString'] = db['dbConnectionStringFormat'].format(**db)
# if db['dbConnectionStringExtra'] is not None:
#     db['dbConnectionString'] = db['dbConnectionStringExtra'] + \
#         urllib.parse.quote_plus(db['dbConnectionString'])

# инициация приложения и конфигурации подключения к БД
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'dfkl;gj sldfjg lsdfjgl;sjdfl;gjkl;*(#$)W&*@()#TLDFKZJFO) UWE()*F'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = db['dbConnectionString']
# db['dbConnection'] = SQLAlchemy(app)
# db['dbEngine'] = db['dbConnection'].engine
# db['dbRawConnection'] = db['dbEngine'].raw_connection()


# def get_sql_data(param_request):  # получение списка словарей из SQL запроса к БД
#     cursor = db['dbEngine'].execute(param_request)
#     return [dict(zip([c[0] for c in cursor.cursor.description], r)) for r in cursor.cursor.fetchall()]


# def get_sql_value(param_request):  # получение значения из SQL запроса к БД
#     result = db['dbEngine'].execute(param_request)
#     result = result.cursor.fetchone()
#     return result[0] if result is not None else '-'


def resp(code, data):  # типовой ответ response
    return Response(
        status=code,
        content_type="application/json;",
        response=json.dumps(data)
    )


@app.route('/', methods=['GET'])
def root():
    return resp(200, 'Welcome to MEDIC-ML!')


# @app.route('/ServiceProviderConfig', methods=['GET'])
# def get_service_config():  # информация о настройках и возможностях сервиса
#     return service.get_config()


@app.route('/Users', methods=['GET', 'POST'])
def get_post_users():  # работа с УЗ пользователя
    return {
        'GET': users.find_users,
        'POST': users.create_new_user
    }.get(request.method)(request.args, request.data)


@app.route('/Users/<user_id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def users_by_id(user_id):  # работа с УЗ пользователя по id
    return {
        'GET': users.find_user_by_id,
        'PATCH': users.change_user_attributes,
        'PUT': users.update_user_data,
        'DELETE': users.delete_user
    }.get(request.method)(user_id, request.args, request.data)


def error_template(err_code, err_type, err_detail):
    return resp(err_code, {
        "schemas": [
            "urn:ietf:params:scim:api:messages:2.0:Error"
        ],
        "status": f"{err_code}",
        "scimType": f"{err_type}",
        "detail": f"{err_detail}"
    })


@app.errorhandler(400)
def bad_request(e = "400: Bad Request", error_type = "Bad Request", error_detail = "Ошибка синтаксического анализа запроса, либо нарушение схемы"):
    return error_template(400, error_type, error_detail)


@app.errorhandler(401)
def unauthorized(e = "401: Unauthorized", error_type = "Unauthorized", error_detail = "Ошибка авторизации"):
    return error_template(401, error_type, error_detail)


@app.errorhandler(403)
def forbidden(e = "403: Forbidden", error_type = "Forbidden", error_detail = "Операция запрещена"):
    return error_template(403, error_type, error_detail)


@app.errorhandler(404)
def not_found(e = "404: Not Found", error_type = "Not Found", error_detail = "Указанный ресурс (пользователь, endpoint) не найден"):
    return error_template(404, error_type, error_detail)

@app.errorhandler(409)
def conflict(e = "404: Conflict", error_type = "Conflict", error_detail = "Cервис-провайдер отклонил запрос на создание дубля ресурса"):
    return error_template(409, error_type, error_detail)


@app.errorhandler(500)
def internal_server_error(e = "500: Internal Server Error", error_type = "Internal Server Error", error_detail = "Внутренняя ошибка сервера"):
    return error_template(500, error_type, error_detail)


@app.errorhandler(501)
def not_implemented(e = "501: Not Implemented", error_type = "Not Implemented", error_detail = "Сервис-провайдер не поддерживает запрошенную операцию"):
    return error_template(501, error_type, error_detail)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
