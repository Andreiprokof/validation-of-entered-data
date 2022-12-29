db_host = 'degtyarev'
db_name = 'AFOND_DB'
db_user = 'SA'
db_password = '1'

connection = pyodbc.connect('Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';')
print (connection)

cursor = connection.cursor()