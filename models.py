from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy(app)

class Productos(db.Model):
    NumProducto= db.Column(db.Integer, primary_key= True, nullable= False)
    Nombre= db.Column(db.String(100), nullable= False)
    PrecioUnitario= db.Column(db.Float, nullable= False)
    
    item= db.relationship('ItemsPedidos', backref='productos', cascade='all, delete-orphan', lazy='dynamic')
    

class Pedidos(db.Model):
    NumPedido= db.Column(db.Integer, primary_key= True, nullable= False)
    Fecha= db.Column(db.DateTime)
    Total= db.Column(db.Float(20), nullable= False)
    Cobrado= db.Column(db.String(20), nullable= False)
    Observacion= db.Column(db.Text)
    DNIMozo= db.Column(db.String(9), db.ForeignKey('usuarios.DNI') , nullable= False)
    Mesa= db.Column(db.Integer, nullable= False)
    
    item1= db.relationship('ItemsPedidos', backref='pedidos', cascade= 'all, delete-orphan', lazy='dynamic') 
    
class ItemsPedidos(db.Model):
    __tablename__ = 'ItemsPedidos'
    NumItem= db.Column(db.Integer, primary_key= True, nullable= False)
    NumPedido= db.Column(db.Integer, db.ForeignKey('pedidos.NumPedido'), nullable= False)
    NumProducto= db.Column(db.Integer, db.ForeignKey('productos.NumProducto'), nullable= False)
    Precio= db.Column(db.Integer, nullable= False)
    Estado= db.Column(db.String(9), nullable= False)
    
class Usuarios(db.Model):
    DNI= db.Column(db.String(10), primary_key= True, nullable= False)
    Clave= db.Column(db.String(30), nullable= False)
    Tipo= db.Column(db.String(8), nullable= False)
    
    pedidos= db.relationship('Pedidos', backref='usuarios', cascade= 'all, delete-orphan', lazy='dynamic')
    