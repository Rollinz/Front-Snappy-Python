from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from modelo.comestible import *
from modelo.bebestible import *
from modelo.mesa import *
from modelo.venta import *
import requests
import json
import smtplib
from email.mime.text import MIMEText

class Ventana:
    emisor = "rolandoaburto7@gmail.com" 
    receptor = "raburtolivares@gmail.com"

    bebestible = Bebestible()
    mesa = Mesa()
    #usar arrays para busqueda
    comestibles = []
    bebestibles = []
    ventas = []
    mesas = []
    def __init__(self, window):
        self.url = "http://127.0.0.1:4000/comestibles"
        self.urlBebestible = "http://127.0.0.1:4000/bebestibles"
        self.url_post = "http://127.0.0.1:4000/ventas"
        self.url_mesa = "http://127.0.0.1:4000/mesas"
        self.win = window
        self.win.title("Snappy")

        self.venta = Venta()

        #Container
        frame = LabelFrame(self.win, text="Selecciona tu pedido")
        frame.grid(row = 0, column = 0, columnspan = 3, padx=10, pady = 10)

        #radio button
        self.var = IntVar()
        self.radio_comida = Radiobutton(frame, text="", variable=self.var, value=1, command=self.sel).grid(row = 1, column = 0)
        self.radio_bebida = Radiobutton(frame, text="", variable=self.var, value=2, command=self.sel).grid(row = 2, column = 0)

        #Label de titulo
        Label(frame, text = "Elige la comida que pediras:").grid(row = 1, column = 1, pady = 10)
        self.comboComestible = ttk.Combobox(frame)
        self.comboComestible.grid(row = 1, column = 2)
        #Label de titulo 2
        Label(frame, text = "Elige la bebida que pediras:").grid(row = 2, column = 1, pady = 20)
        self.comboBebestible = ttk.Combobox(frame, state = DISABLED)
        self.comboBebestible.grid(row = 2, column = 2)

        #Label de titulo 3
        Label(frame, text = "Mesa:").grid(row = 5, column = 0, pady = 5)
        self.combo_mesa = ttk.Combobox(frame)
        self.combo_mesa.grid(row = 5, column = 1)

        #checkbox
        #self.check_mesa = ttk.Checkbutton(frame, text = "Bloquear mesa", command = self.seleccion_mesa).grid(row = 5, column = 2)


        #boton
        self.botonEnviar = ttk.Button(frame, text = "Enviar Pedido", command = self.enviar_pedido).grid(row = 3, column = 0)
        self.botonPedir = ttk.Button(frame, text = "Pedir Cuenta", command = self.calcular_ventas).grid(row = 3, column = 1)
        self.botonPedir = ttk.Button(frame, text = "bloquear_mesa", command = self.seleccion_mesa).grid(row = 5, column = 2)

        response = requests.get(self.url)
        if response.status_code == 200:
            respuesta_server = json.loads(response.text)
            comestible = Comestible()
            for respuesta in respuesta_server:
                comestible.id_comestible = respuesta['id_comestible']
                comestible.nombre_comestible = respuesta['nombre_comestible']
                comestible.precio = respuesta['precio']
                self.comestibles.append(comestible)
                self.comboComestible['values'] = (*self.comboComestible['values'],comestible.nombre_comestible)
                comestible = Comestible()



        responseBebestible = requests.get(self.urlBebestible)
        if responseBebestible.status_code == 200:
            respuesta_serverB = json.loads(responseBebestible.text)
            for resp in respuesta_serverB:
                self.bebestible.id_bebestible = resp['id_bebestible']
                self.bebestible.nombre_bebestible = resp['nombre_bebestible']
                self.bebestible.precio = respuesta = resp['precio']
                self.bebestibles.append(self.bebestible)
                self.comboBebestible['values'] = (*self.comboBebestible['values'],self.bebestible.nombre_bebestible)
                self.bebestible = Bebestible()

        response_mesa = requests.get(self.url_mesa)
        if response_mesa.status_code == 200:
            respuesta_mesa = json.loads(response_mesa.text)
            for resp in respuesta_mesa:
                self.mesa.id_mesa = resp['id_mesa']
                self.mesa.numero_mesa = resp['numero_mesa']
                self.mesas.append(self.mesa)
                self.combo_mesa['values'] = (*self.combo_mesa['values'], self.mesa.numero_mesa)
                self.mesa = Mesa()

        
        self.tabla = ttk.Treeview(frame, height = 10, columns = 2)
        self.tabla.grid(row = 4, column = 0, columnspan = 4)
        self.tabla.heading("#0", text = "Pedido", anchor = CENTER)
        self.tabla.heading("#1", text = "Precio", anchor = CENTER)

        self.cargar_tabla(self.tabla)

        self.total = 0
    def sel(self):
        self.selection = self.var.get()
        if self.selection == 1:
            self.comboComestible.configure(state = NORMAL)
            self.comboBebestible.configure(state = DISABLED)
        elif self.selection == 2:
            self.comboBebestible.configure(state = NORMAL)
            self.comboComestible.configure(state = DISABLED)

    def seleccion_mesa(self):
        self.venta.id_mesa = self.combo_mesa.get()
        self.combo_mesa.configure(state = DISABLED)
        print(self.venta.id_mesa)


    def buscar_comestible(self, mi_comestible):
        comida = Comestible()
        for c in self.comestibles:
            if mi_comestible == c.nombre_comestible:
                comida.id_comestible = c.id_comestible
                comida.nombre_comestible = c.nombre_comestible
                comida.precio = c.precio
        return comida
    
    def buscar_bebestible(self, mi_bebestible):
        bebida = Bebestible()
        for b in self.bebestibles:
            if mi_bebestible == b.nombre_bebestible:
                bebida.id_bebestible = b.id_bebestible
                bebida.nombre_bebestible = b.nombre_bebestible
                bebida.precio = b.precio
        return bebida

    def captura_comestible(self):
        self.mi_comestible = self.comboComestible.get()
        return self.mi_comestible

    def captura_bebestible(self):
        self.mi_bebestible = self.comboBebestible.get()
        return self.mi_bebestible
    
    def enviar_pedido(self):
        mi_comestible = self.captura_comestible()
        mi_bebestible = self.captura_bebestible()
        #print(mi_comestible)
        comida = self.buscar_comestible(mi_comestible)
        bebida = self.buscar_bebestible(mi_bebestible)

        if comida.id_comestible != 0 and comida.nombre_comestible != '' and comida.precio != 0 and self.var.get() == 1:
            self.ventas.append(comida)
            mensaje = MIMEText("""****Pedido****\nMesa: {0}\nPedidos: {1}""".format(self.venta.id_mesa, comida.nombre_comestible))
            mensaje['From']=self.emisor
            mensaje['To']=self.receptor
            mensaje['Subject']="Pedido comidas y bebidas"
            serverSMTP = smtplib.SMTP('smtp.gmail.com',587)
            serverSMTP.ehlo()
            serverSMTP.starttls()
            serverSMTP.ehlo()
            serverSMTP.login(self.emisor, "Vibranium434.")
            if len(serverSMTP.sendmail(self.emisor,self.receptor,mensaje.as_string())) == 0:
                messagebox.showinfo("Correcto", "Pedido solicitado a la cocina")
            else:
                messagebox.showerror("Error", "Error al pedir a la cocina")
            serverSMTP.close()
            
        if bebida.id_bebestible != 0 and bebida.nombre_bebestible != '' and bebida.precio != 0 and self.var.get() == 2:
            self.ventas.append(bebida)
            mensaje = MIMEText("""****Pedido****\nMesa: {0}\nPedidos: {1}""".format(self.venta.id_mesa, bebida.nombre_bebestible))
            mensaje['From']=self.emisor
            mensaje['To']=self.receptor
            mensaje['Subject']="Pedido comidas y bebidas"
            serverSMTP = smtplib.SMTP('smtp.gmail.com',587)
            serverSMTP.ehlo()
            serverSMTP.starttls()
            serverSMTP.ehlo()
            serverSMTP.login(self.emisor, "Vibranium434.")
            if len(serverSMTP.sendmail(self.emisor,self.receptor,mensaje.as_string())) == 0:
                messagebox.showinfo("Correcto", "Pedido solicitado a la cocina")
            else:
                messagebox.showerror("Error", "Error al pedir a la cocina")
            serverSMTP.close()
        
        if self.ventas:
            if self.ventas.__contains__(comida) and self.var.get() == 1:
                self.tabla.insert('', 0, text = comida.nombre_comestible, values = comida.precio)
            elif self.ventas.__contains__(bebida) and self.var.get() == 2:
                self.tabla.insert('', 0, text = bebida.nombre_bebestible, values = bebida.precio)
        
        # falta calcular total
    
    def cargar_tabla(self, tabla):
        registros = self.tabla.get_children()
        for registro in registros:
            self.tabla.delete(registro)
        
    def calcular_ventas(self):
        pedidos = ""
        data = {
            'id_mesa': 0,
            'total': 0
        }
        for venta in self.ventas:
            if isinstance(venta, Comestible):
                self.venta.id_comestible = venta.id_comestible
                pedidos+=venta.nombre_comestible+": $"+str(venta.precio)+"\n"
            elif isinstance(venta, Bebestible):
                self.venta.id_bebestible = venta.id_bebestible
                pedidos+=venta.nombre_bebestible+": $"+str(venta.precio)+"\n"
            self.total = self.total + venta.precio
            data['id_mesa'] = self.venta.id_mesa
            data['total'] =  self.total
        
        self.venta.total = self.total   
        response = requests.post(self.url_post, json=data)
            
        mensaje = MIMEText("""****Cuenta****\nMesa:{0}\nPedidos:\n{1}\nTotal:{2}""".format(self.venta.id_mesa, pedidos, self.venta.total))
        mensaje['From']=self.emisor
        mensaje['To']=self.receptor
        mensaje['Subject']="Pago de Cuenta"
        serverSMTP = smtplib.SMTP('smtp.gmail.com',587)
        serverSMTP.ehlo()
        serverSMTP.starttls()
        serverSMTP.ehlo()
        serverSMTP.login(self.emisor, "Vibranium434.")
        if len(serverSMTP.sendmail(self.emisor,self.receptor,mensaje.as_string())) == 0 and response.status_code == 200:
            messagebox.showinfo("Correcto", "Cuenta pedida")
            self.cargar_tabla(self.tabla)
            self.bebestibles.clear()
            self.comestibles.clear()
        else:
            messagebox.showerror("Error", "Error al pedir cuenta")
        serverSMTP.close()

if __name__ == "__main__":
    window = Tk()
    Ventana(window)
    window.mainloop()
    
#Solo falta el combo de la Mesa