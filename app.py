from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import  Marshmallow

app = Flask (__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://miusuario:miclave@localhost/prueba_tecnica'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Paciente(db.Model):
    #id = db.Column(db.Integer)
    cedula=db.Column(db.Integer,primary_key =True, unique=True)
    nombre = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    telefono = db.Column(db.Integer, unique=True)
    contrasena= db.Column(db.String(50))
    direccion = db.Column(db.String(120))
    fecha_nacimiento = db.Column(db.String(50))
    estado_salud= db.Column(db.String(500))
    observaciones= db.Column(db.String(500))

    def __init__(self, cedula, nombre, email, telefono, contrasena, direccion, fecha_nacimiento,estado_salud,observaciones):
        self.cedula=cedula
        self.nombre = nombre
        self.email = email
        self.telefono=telefono
        self.contrasena=contrasena
        self.direccion=direccion
        self.fecha_nacimiento=fecha_nacimiento
        self.estado_salud=estado_salud
        self.observaciones=observaciones


        
    #def __repr__ (self):
     #   return '<User %r>' % self.username

db.create_all()


class UsuarioPaciente(ma.Schema):
    class Meta:
        fields = ('cedula','nombre', 'email', 'telefono','direccion','fecha_nacimiento')

usuario_paciente = UsuarioPaciente()
usuarios_paciente = UsuarioPaciente(many=True)


@app.route('/crear', methods=['POST'])
def crearUsuario():
    
    cedula=request.json['cedula']
    nombre=request.json['nombre']
    email=request.json['email']
    telefono=request.json['telefono']
    contrasena=request.json['contrasena']
    direccion=request.json['direccion']
    fecha_nacimiento=request.json['fecha_nacimiento']
    estado_salud=request.json['estado_salud']
    observaciones=request.json['observaciones']

    nuevo_paciente = Paciente( cedula, nombre, email, telefono, contrasena, direccion, fecha_nacimiento, estado_salud, observaciones)
    db.session.add(nuevo_paciente)
    db.session.commit()

    return usuario_paciente.jsonify(nuevo_paciente)

@app.route('/usuarios', methods=['GET'])
def obtenerUsuarios():
    usuarios = Paciente.query.all()
    resultados= usuarios_paciente.dump(usuarios)
    return jsonify(resultados)

@app.route('/usuarios/<cedula>', methods=['GET'])
def ingresar(cedula):
    usuario = Paciente.query.get(cedula)
    return usuario_paciente.jsonify(usuario) 

@app.route('/usuario/<cedula>', methods=['PUT'])
def actualizarContrasena(cedula):
    usuario= Paciente.query.get(cedula)

    contrasena=request.json['contrasena']

    usuario.contrasena=contrasena
    db.session.commit()

    return usuario_paciente.jsonify(usuario)


if __name__ == "__main__":
    app.run(debug=True)