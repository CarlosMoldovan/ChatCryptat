import socket
import threading
import pickle
from Crypto.Cipher import AES
import tkinter as tk
from tkinter import messagebox, scrolledtext 

Server_IP = '127.0.0.1'
Port = 1540
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((Server_IP, Port))

key = b'SecuritateChat12'

def encrypt(message):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    if isinstance(message, str):
        message = message.encode('utf-8') 
    ciphertext, tag = cipher.encrypt_and_digest(message)
    return pickle.dumps((nonce, ciphertext, tag))

def decrypt(data):
    try:
        nonce, ciphertext, tag = pickle.loads(data)
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        cipher.verify(tag)
        return plaintext.decode('utf-8')
    except:
        return "Eroare la decriptare"

def login():
    username = entry_user.get()
    parola = entry_pass.get()
    
    if not username or not parola:
        messagebox.showerror("Eroare", "Completează toate câmpurile!")
        return

    try:
        client.send(encrypt(username)) 
        client.send(encrypt(parola)) 

        raspuns = client.recv(4096)
        raspuns_decriptat = decrypt(raspuns)

        if "Parola incorectă" in raspuns_decriptat:
            messagebox.showerror("Eroare", raspuns_decriptat)
            client.close()
            root.destroy()
        elif "Autentificare reușită" in raspuns_decriptat:
            root.destroy()
            home(username)
    except Exception as e:
        messagebox.showerror("Eroare", f"Conexiune eșuată: {e}")
        client.close()
        root.destroy()

def chat(username):
    chat_win = tk.Tk()
    chat_win.title(f"Chat - {username}")
    chat_win.geometry("800x800")  
    chat_win.configure(bg='white')

    title_label = tk.Label(chat_win, text="Chat Grup", font=("Helvetica", 18, "bold"), bg='white', fg='black')
    title_label.place(relx=0.5, rely=0.1, anchor='center')
 
    center_frame = tk.Frame(chat_win, bg='black', width=1400, height=3000)
    center_frame.place(relx=0.5, rely=0.45, anchor='center') 
 
    text_area = scrolledtext.ScrolledText(center_frame, state='disabled', wrap=tk.WORD,
                                          bg='#1e1e1e', fg='lightgreen', font=('Consolas', 10))
    text_area.pack(padx=10, pady=10, fill='both', expand=True)
 
    entry_msg = tk.Entry(center_frame, bg='#2e2e2e', fg='white', insertbackground='white')
    entry_msg.pack(padx=10, pady=(0, 5), fill='x')
    entry_msg.focus()
 
    btn_back = tk.Button(center_frame, text="Back", bg='gray', fg='white',
                         command=lambda: [chat_win.destroy(), home(username)])
    btn_back.pack(pady=(0, 10))


    def t_mesaj(event=None):
        mesaj = entry_msg.get().strip()
        if mesaj:
            try:
                mesaj_criptat = encrypt(mesaj)
                client.send(mesaj_criptat)
                entry_msg.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Eroare", f"Eroare la trimiterea mesajului: {e}")
                chat_win.destroy()

    entry_msg.bind("<Return>", t_mesaj)

    def p_mesaje():
        while True:
            try:
                mesaj_criptat = client.recv(4096)
                if not mesaj_criptat:
                    break
                mesaj_decriptat = decrypt(mesaj_criptat)
                text_area.after(0, afis_mesaj, mesaj_decriptat)
            except:
                break

        client.close()
        chat_win.after(0, chat_win.destroy)

    def afis_mesaj(mesaj):
        text_area.config(state='normal')

        if mesaj.startswith(f"{username}:"):
            lines = mesaj.split('\n')
            for line in lines:
                text_area.insert(tk.END, f"{line.rjust(70)}\n")
        else: 
            text_area.insert(tk.END, mesaj + '\n')

        text_area.config(state='disabled')
        text_area.see(tk.END)
    
    try:
      client.send(encrypt("/history"))
    except:
      pass

    threading.Thread(target=p_mesaje, daemon=True).start()

    def on_close():
        try:
            client.send(encrypt("/exit"))
        except:
            pass
        chat_win.destroy()

    chat_win.protocol("WM_DELETE_WINDOW", on_close)
    chat_win.mainloop()


def home(username):
    global client
    try:
      client.close()
    except:
      pass

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((Server_IP, Port))
    client.send(encrypt(username))
    selectie_win = tk.Tk()
    selectie_win.title("Alege modul")
    selectie_win.geometry("300x200")

    label = tk.Label(selectie_win, text=f"Bine ai venit, {username}!", font=("Arial", 12))
    label.pack(pady=20)

    btn_chat = tk.Button(selectie_win, text="Chatul Group", width=25, command=lambda: [selectie_win.destroy(), chat(username)])
    btn_chat.pack(pady=10)

    btn_users = tk.Button(selectie_win, text="Private Chat", width=25, command=lambda: pri_chat(username))
    btn_users.pack(pady=10)

    selectie_win.mainloop()

def pri_chat(username):
    try:
        client.send(encrypt("/get_users"))
        while True:
         raspuns = client.recv(4096)
         text = decrypt(raspuns)
         if text.startswith("/user_list "):
           lista_useri = text.replace("/user_list ", "").split(", ")
           break

        user_win = tk.Toplevel()
        user_win.title("Private Chat")
        user_win.geometry("300x300")

        lbl = tk.Label(user_win, text="Alege un user:", font=("Arial", 10))
        lbl.pack(pady=10)

        listbox = tk.Listbox(user_win)
        for user in lista_useri:
            if user.strip():
                listbox.insert(tk.END, user.strip())
        listbox.pack(padx=10, pady=10, fill="both", expand=True)

        def open():
            selectie = listbox.curselection()
            if selectie:
                destinatar = listbox.get(selectie[0])
                user_win.destroy()
                private_chat(destinatar,username)

        btn_chat_privat = tk.Button(user_win, text="Trimite mesaj privat", command=open)
        btn_chat_privat.pack(pady=5)

    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la obținerea listei: {e}")

def private_chat(destinatar,username):
    priv_win = tk.Toplevel()
    priv_win.title(f"Chat privat cu {destinatar}")
    priv_win.geometry("800x800")
    priv_win.configure(bg='white')
 
    title_label = tk.Label(priv_win, text=f"Chat privat cu {destinatar}",
                           font=("Helvetica", 18, "bold"), bg='white', fg='black')
    title_label.place(relx=0.5, rely=0.1, anchor='center')
 
    center_frame = tk.Frame(priv_win, bg='black', width=700, height=700)
    center_frame.place(relx=0.5, rely=0.55, anchor='center')
 
    text_area = scrolledtext.ScrolledText(center_frame, state='disabled', wrap=tk.WORD,
                                          bg='#1e1e1e', fg='lightgreen', font=('Consolas', 10))
    text_area.pack(padx=10, pady=10, fill='both', expand=True)
    text_area.tag_configure('left', justify='left')
    text_area.tag_configure('right', justify='right')

 
    entry_msg = tk.Entry(center_frame, bg='#2e2e2e', fg='white', insertbackground='white')
    entry_msg.pack(padx=10, pady=(0, 5), fill='x')
    entry_msg.focus()
 
    btn_back = tk.Button(center_frame, text="Închide", bg='gray', fg='white',
                         command=priv_win.destroy)
    btn_back.pack(pady=(0, 10))


    def t_privat(event=None):
        mesaj = entry_msg.get().strip()
        if mesaj:
            comanda = f"/private {destinatar} {mesaj}"
            try:
                client.send(encrypt(comanda))
                entry_msg.delete(0, tk.END)
  
            except Exception as e:
                messagebox.showerror("Eroare", f"Nu s-a putut trimite mesajul privat: {e}")
                priv_win.destroy()

    entry_msg.bind("<Return>", t_privat)

    def p_mesaje():
        while True:
            try:
                mesaj_criptat = client.recv(4096)
                if not mesaj_criptat:
                    break
                mesaj_decriptat = decrypt(mesaj_criptat)

                if username in mesaj_decriptat or destinatar in mesaj_decriptat:
                  text_area.after(0, a_mesaj, mesaj_decriptat)
            except:
                break

    def a_mesaj(mesaj):
      text_area.config(state='normal')

      try:
        sender, rest = mesaj.split(":", 1)
      except ValueError:
        sender = ""
        rest = mesaj

      if sender.strip() == username:
        text_area.insert(tk.END, mesaj.strip() + '\n', 'right')
      else:
        text_area.insert(tk.END, mesaj.strip() + '\n', 'left')

      text_area.config(state='disabled')
      text_area.see(tk.END)

    try:
      client.send(encrypt(f"/private_history {destinatar}"))
    except:
      pass
    threading.Thread(target=p_mesaje, daemon=True).start()

    priv_win.protocol("WM_DELETE_WINDOW", priv_win.destroy)
    priv_win.mainloop()


root = tk.Tk()
root.title("Autentificare Chat")
root.geometry("300x200")

tk.Label(root, text="Username:").pack(pady=(20, 5))
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Parola:").pack(pady=5)
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

btn_login = tk.Button(root, text="Conectare", command=login)
btn_login.pack(pady=20)

root.mainloop()