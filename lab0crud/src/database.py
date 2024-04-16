import mysql.connector
local = False
success = False
config = {
    'user': 'uauvrvass9qcwgye',
    'password': 'Zx80kAeYM8J6lEiuh64W',
    'host': 'bmb72wbdmjin8klxpert-mysql.services.clever-cloud.com',
    'database': 'bmb72wbdmjin8klxpert'  # Puerto predeterminado de MySQL
}

localConfig = {
    'user': 'root',
    'password': 'labcrud123456',
    'host': 'localhost',  # Nombre o dirección IP del servidor MySQL
    'port': 3306,
    'database': 'lab_crud'  # Puerto predeterminado de MySQL
}
try:
    if local:
        database = mysql.connector.connect(**localConfig)
    else:
        database = mysql.connector.connect(**config)
    success = True
except Exception as e:
    print("Error al conectar a la base de datos", e)



if success:
    print('BBDD conectada!!', "Modo localhost!" if local else "Modo pythonanywhere!")
    # despues de conectar ejecutar codigo que quiera