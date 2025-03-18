crear el fichero .env
crear las variables en el fichero .env
dejo un ejemplo del fichero con las 2 variables :FLASK_SECRET_KEY, USERS

#inicio de fichero .env 
# genero clave con : python3 -c "import secrets; print(secrets.token_hex(32))"
FLASK_SECRET_KEY=4d6b3acf49db32a615b408d155857624b611f441ab8e7642daa165e7f4088b5f
#dos usuarios de muestra para pruebas
USERS={"test": "1234","admin": "12345"}
# final del fichero .env 
