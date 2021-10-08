from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from datetime import datetime
import hashlib

app= Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Productos, Pedidos, ItemsPedidos, Usuarios

@app.route('/')
def inicio():
    return render_template('inicio.html')
@app.route('/pedido', methods= ['POST', 'GET'])
def Mpedido():
    DNI=request.form['DNI']
    
    return render_template('pedido.html', DNI=DNI)

@app.route('/mozo', methods= ['POST', 'GET'])
def mozo():
    DNI=request.form['DNI']
    
    return render_template('mozo.html', DNI=DNI)
@app.route('/listadonocobrados', methods= ['POST', 'GET'])
def nocobrados():
    items=ItemsPedidos.query.all()
    pedidos=Pedidos.query.all()
    productos=Productos.query.all()
    DNI=request.form['DNI']
    
  
    return render_template('nocobrados.html',DNI=DNI, pedidos=pedidos, items=items, productos=productos )

@app.route('/cartamozo', methods= ['POST', 'GET'])
def cartamozo():
    DNI=request.form['DNI']
    mesa=request.form['Numero de mesa']
    productos= Productos.query.all()
    name0=productos[0].Nombre
    preciogaseosa='$'+productos[1].PrecioUnitario
    preciopizza='$'+productos[0].PrecioUnitario
    preciocerveza='$'+productos[2].PrecioUnitario
    preciolomo='$'+productos[2].PrecioUnitario
    name1=productos[1].Nombre
    name2=productos[2].Nombre
    name3=productos[3].Nombre
    return render_template('cartamozo.html',DNI=DNI,mesa=mesa, preciolomo = preciolomo, preciocerveza=preciocerveza, preciopizza=preciopizza, preciogaseosa = preciogaseosa,name0 = name0 ,name1 = name1,name2 = name2,name3 = name3)
@app.route('/pedidofinalizado',methods= ['POST', 'GET'] )
def pedidorealizado():
    Itemspedidos= ItemsPedidos.query.all()
    productos= Productos.query.all()
    DNI=request.form['DNI']
    Datospedidos= Pedidos.query.all()
    mesa=request.form['Numero de mesa']
    nump=int(Itemspedidos[len(Itemspedidos)-1].NumPedido)+1
    T=0
    num=int(Itemspedidos[len(Itemspedidos)-1].NumItem)+1

    if request.form['Gaseosa'] != '':
        for i in range(int(request.form['Gaseosa'])):
            
            numpro=productos[1].NumProducto
            pre=productos[1].PrecioUnitario
            estad='Pendiente'
            #print(f"nump {nump}  num {num} numpro {numpro} precio {pre} {estad}")
            producto= ItemsPedidos(NumItem=str(num), NumPedido=nump, NumProducto=numpro, Precio=pre, Estado=estad)
            db.session.add(producto)
            db.session.commit()
            num=int(num)+1
        T=T+(int(pre)*int(request.form['Gaseosa']))
    if request.form['Cerveza'] != '':
        for i in range(int(request.form['Cerveza'])):
            
            numpro=productos[2].NumProducto
            pre=productos[2].PrecioUnitario
            estad='Pendiente'
            #print(f"nump {nump}  num {num} numpro {numpro} precio {pre} {estad}")
            producto= ItemsPedidos(NumItem=str(num), NumPedido=nump, NumProducto=numpro, Precio=pre, Estado=estad)
            db.session.add(producto)
            db.session.commit()
            num=int(num)+1
        T=T+(int(pre)*int(request.form['Cerveza']))
    if request.form['Pizza Muzarrella'] != '':
        for i in range(int(request.form['Pizza Muzarrella'])):
            
            numpro=productos[0].NumProducto
            pre=productos[0].PrecioUnitario
            estad='Pendiente'
            #print(f"nump {nump}  num {num} numpro {numpro} precio {pre} {estad}")
            producto= ItemsPedidos(NumItem=str(num), NumPedido=nump, NumProducto=numpro, Precio=pre, Estado=estad)
            db.session.add(producto)
            db.session.commit()
            num=int(num)+1
        T=T+(int(pre)*int(request.form['Pizza Muzarrella']))
    if request.form['Lomo'] != '':
        for i in range(int(request.form['Lomo'])):
            
            numpro=productos[3].NumProducto
            pre=productos[3].PrecioUnitario
            estad='Pendiente'
            #print(f"nump {nump}  num {num} numpro {numpro} precio {pre} {estad}")
            producto= ItemsPedidos(NumItem=str(num), NumPedido=nump, NumProducto=numpro, Precio=pre, Estado=estad)
            db.session.add(producto)
            db.session.commit()
            num=int(num)+1
        T=T+(int(pre)*int(request.form['Lomo']))
    numped=int(Datospedidos[len(Datospedidos)-1].NumPedido)+1
    
    pedido=Pedidos(NumPedido=numped, Fecha=datetime.now(), Total=T, Cobrado='False', Observacion= request.form['Observaciones'],DNIMozo=DNI, Mesa=mesa)
    db.session.add(pedido)
    db.session.commit()
    return render_template('pedidorealizado.html', DNI=DNI)

@app.route('/listapedidos', methods= ['POST', 'GET'])
def listapedidos():
    items= ItemsPedidos.query.all()
    
    Lista=[]
    bandera=True
    for i in range(len(items)):
        if bandera==True:
            if items[i].Estado == 'Pendiente':
                Lista.append(items[i].NumPedido)
                bandera=False
        else:
            if items[i].Estado == 'Pendiente':
                if items[i].NumPedido not in Lista:
                    Lista.append(items[i].NumPedido)

    
                
            
    return render_template('listapedidos.html',productos=Productos.query.all(),Lista=Lista,items=items ,pedidos= Pedidos.query.all())
 
@app.route('/cambio', methods= ['POST', 'GET'])
def cambio():
    Num=request.form.getlist('Listo')
    for N in Num:
        stmt = (update(ItemsPedidos).where(ItemsPedidos.NumItem == N).values(Estado='Listo'))
        db.session.execute(stmt)
        db.session.commit()
    return render_template('cambio.html')
@app.route('/venta',methods= ['POST', 'GET'])
def venta():
    DNI=request.form['DNI']
    Num=request.form.getlist('Listo')
    Valores=[]
    for N in Num:
        A=int(N)
        if A == 2:
            stmt = (update(Pedidos).where(Pedidos.NumPedido == N).values(Cobrado='True'))    
            Valores.append(A)
        else:
            stmt = (update(Pedidos).where(Pedidos.NumPedido == A).values(Cobrado='True'))
            Valores.append(A)
        db.session.execute(stmt)
        db.session.commit()
    return render_template('venta.html', DNI=DNI, Valores=Valores, pedidos= Pedidos.query.all())
@app.route('/bienvenida', methods= ['POST', 'GET'])
def bienvenida():
    usuarios= Usuarios.query.all()
    DNI=request.form['DNI']
    if request.method == 'POST':
        if request.form['DNI'] and request.form['Clave']:
            band= False
            i=0
            try:
                while i <= len(usuarios) and band == False:
                    if request.form['DNI'] == usuarios[i].DNI:
                        
                        contrasena= hashlib.md5(bytes(request.form['Clave'], encoding='utf-8'))
    
                        if contrasena.hexdigest() == usuarios[i].Clave:
                            if usuarios[i].Tipo == 'Mozo':
                                return render_template('mozo.html', DNI=DNI)
                            else:
                                return render_template('cocinero.html')
                            band= True
                        else:
                            return render_template('pass_mal.html')
                    else:
                        i+=1
            except:
                return render_template('usuario_mal.html')
        else:
            return render_template('login_incorrecto.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug= False)
