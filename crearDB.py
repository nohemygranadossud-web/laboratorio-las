from flask import Flask, render_template, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        
        password_encriptada = generate_password_hash(password)
        
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO usuarios (usuario, password) VALUES (?, ?)",
                (usuario, password_encriptada)
            )
            conexion.commit()
            conexion.close()
            return "Usuario registrado exitosamente"
        except sqlite3.IntegrityError:
            conexion.close()
            return "El usuario ya existe"
            
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado and check_password_hash(resultado[2], password):
            return "Inicio de sesión correcto"
        else:
            return "Credenciales incorrectas"
            
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)