import index


#def get_count_of_roles():  # получить количество ролей из БД
 #   return index.get_sql_value("SELECT COUNT(*) FROM [Common].[dbo].[t_USER_BUSINESS_ROLE_SUDIR]")


#def get_list_of_roles():  # получить роли из БД
 #   return index.get_sql_data("SELECT * FROM [Common].[dbo].[t_USER_BUSINESS_ROLE_SUDIR]")


# проверка параметра запроса: есть значение параметра, целое число, больше 0
# def check_param(param, start_value):
#     return start_value if not param or param.isdigit() == False or int(param) <= 0 else int(param)


# def get_item_list(args):  # формирование списка ролей в нужном формате
#     roles = get_list_of_roles()
#     data = [response_config.get_role_item(item) for item in roles]
#     # обработка параметра startIndex
#     left_limit = check_param(args.get("startIndex"), 1)
#     # обработка параметра count
#     right_limit = check_param(args.get("count"), len(data))
#     return data[left_limit - 1: right_limit + left_limit - 1]


# def get_list(args):  # основной метод
#     content = response_config.get_response()
#     if args.get("count") != "0":  # проверка на запрос healthcheck из СУДИР
#         content["Resources"] = get_item_list(args)
#         content["totalResults"] = len(content["Resources"])
#     else:
#         content["totalResults"] = get_count_of_roles()
#     return index.resp(200, content)

# return index.resp(204, '')
# return index.internal_server_error(error_detail="При выполнении SQL DELETE со стороны БД возникла ошибка!")
