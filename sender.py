import smtplib
import os
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames
import re
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

class Login(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('700x580')
        self.resizable(0, 0)
        self.title('Enviar Correos')
        tk.Label(self, text='De:', font=(
            'Lucida', 10, 'bold')).place(x=20, y=20)
        tk.Label(self, text='Password:', font=('Lucida', 10, 'bold')).place(x=20, y=60)
        tk.Label(self, text='Para:', font=(
            'Lucida', 10, 'bold')).place(x=20, y=100)
        tk.Label(self, text='Asunto:', font=(
            'Lucida', 10, 'bold')).place(x=20, y=140)
        tk.Label(self, text='Adjunto:', font=(
            'Lucida', 10, 'bold')).place(x=20, y=180)
        tk.Label(self, text='Mensaje:', font=(
            'Lucida', 10, 'bold')).place(x=20, y=280)
        self.de_entry = tk.Entry(self, width=40)
        self.de_entry.place(x=100, y=20)
        self.pass_entry = tk.Entry(self, width=40, show='*')
        self.pass_entry.place(x=100, y=60)
        self.para_entry = tk.Entry(self, width=40)
        self.para_entry.place(x=100, y=100)
        self.asunto_entry = tk.Entry(self, width=40)
        self.asunto_entry.place(x=100, y=140)
        self.entryattachmentEmail = tk.Text(self, width=38, height=2)
        self.entryattachmentEmail.place(x=100, y=230)
        self.adjunto_button = tk.Button(self, text='Explorar archivos', command=self.seleccionar_archivo)
        self.adjunto_button.place(x=100, y=180)
        self.mensaje_text = tk.Text(self, width=80, height=10)
        self.mensaje_text.place(x=20, y=310)
        self.enviar_button = tk.Button(
            self, text='Enviar', font=('Lucida', 12, 'bold'), command=self.validar_email)
        self.enviar_button.place(x=280, y=520)
        self.salir_button = tk.Button(
            self, command=self.salir, text='Salir', font=('Lucida', 12, 'bold'))
        self.salir_button.place(x=380, y=520)

    def salir(self):
        self.destroy()

    def seleccionar_archivo(self):
        
        self.archivo = askopenfilenames()
        for files in self.archivo:
            archivo = os.path.basename(files)
            self.entryattachmentEmail.insert('1.0', archivo+'\n')
        self.adjunto_button.config(text=self.archivo)

    def validar_email(self):
        self.de = self.de_entry.get()
        self.para = self.para_entry.get()
        if(re.fullmatch(regex, self.de) and (re.fullmatch(regex, self.para))):
            self.email_sender()
        else:
            messagebox.showerror('Error', 'Falló el envío', parent=self)

    def email_sender(self):
        de = str(self.de_entry.get())
        password = str(self.pass_entry.get())
        para = str(self.para_entry.get())
        asunto = str(self.asunto_entry.get())
        msg = self.mensaje_text.get('1.0', tk.END)

        mensaje = MIMEMultipart()

        mensaje['From'] = "NO NAME"
        mensaje['To'] = para
        mensaje['Subject'] = asunto

        mensaje.attach(MIMEText(msg))
        for file in self.archivo:
            attachment = open(file, 'rb').read()
            emailAttach = MIMEBase('application', 'octet-stream')
            emailAttach.set_payload(attachment)
            encoders.encode_base64(emailAttach)
            emailAttach.add_header('Content-Disposition', 'attachment; filename= %s' % os.path.basename(file))
            mensaje.attach(emailAttach)
        
        try:
            smtp = smtplib.SMTP('smtp.gmail.com:587')
            smtp.ehlo()
            smtp.starttls()
            smtp.login(de, password)
            smtp.sendmail(de, para, mensaje.as_string())
            messagebox.showinfo('Success', 'Email sent to: ' + str(para))
            smtp.quit()
        except Exception as e:
            messagebox.showerror('Error', e)






if __name__ == '__main__':
    root = Root()
    root.mainloop()
