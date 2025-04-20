import socket
import threading
import pickle
from Crypto.Cipher import AES
import hashlib

Host = '0.0.0.0'
Port = 1540

key = b'SecuritateChat12'
keyH = b'cdfgnjmjhygtfcvg67'
parola_corecta = "paroLa"
hash = hashlib.pbkdf2_hmac('sha256', parola_corecta.encode(), keyH, 100000)

users = {}
usernames = {}

mesaje_grup = []
mesaje_private = []

def encrypt(message):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
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

def broadcast(data, sender_socket):
    for user in list(users.keys()):
        if user != sender_socket:
            try:
                user.send(data)
            except:
                user.close()
                if user in users:
                    del usernames[users[user]]
                    del users[user]

def handle(user_socket):
    try:
        username_data = user_socket.recv(4096)
        if not username_data:
            return
        username = decrypt(username_data)

        try:
            user_socket.settimeout(1.0)
            password_data = user_socket.recv(4096)
            parola = decrypt(password_data)

            hash_c = hashlib.pbkdf2_hmac('sha256', parola.encode(), keyH, 100000)
            if hash_c != hash:
                user_socket.send(encrypt("Parola incorectă. Conexiune închisă."))
                user_socket.close()
                return
        except socket.timeout:
            pass
        finally:
            user_socket.settimeout(None)

        users[user_socket] = username
        usernames[username] = user_socket
        user_socket.send(encrypt("Autentificare reușită."))
        broadcast(encrypt(f"{username} s-a alăturat conversației."), user_socket)

        for msg in mesaje_grup[-20:]:
            user_socket.send(encrypt("[istoric] " + msg))

        while True:
            data = user_socket.recv(4096)
            if not data:
                break
            mesaj = decrypt(data)

            if mesaj == "/get_users":
                lista_useri = ", ".join(usernames.keys())
                user_socket.send(encrypt(f"/user_list {lista_useri}"))
                continue

            if mesaj == "/history":
                for m in mesaje_grup[-20:]:
                    user_socket.send(encrypt(m))
                continue

            if mesaj.startswith("/private_history "):
                partener = mesaj.split(" ")[1]
                for exp, dest, msg in mesaje_private:
                    if (exp == username and dest == partener) or (exp == partener and dest == username):
                        user_socket.send(encrypt(msg))
                continue

            if mesaj.startswith("/private "):
                parts = mesaj.split(" ", 2)
                if len(parts) < 3:
                    user_socket.send(encrypt("Format invalid. Folosește: /private username mesaj"))
                    continue
                destinatar, continut = parts[1], parts[2]
                if destinatar in usernames:
                    socket_destinatar = usernames[destinatar]
                    mesaj_priv = f"{username} (privat): {continut}"
                    socket_destinatar.send(encrypt(mesaj_priv))
                    user_socket.send(encrypt(mesaj_priv))
                    mesaje_private.append((username, destinatar, mesaj_priv))
                else:
                    user_socket.send(encrypt("Utilizatorul nu este conectat."))
                continue

            mesaj_final = f"{username}: {mesaj}"
            mesaje_grup.append(mesaj_final)
            broadcast(encrypt(mesaj_final), user_socket)
            user_socket.send(encrypt(mesaj_final))

    except Exception as e:
        print(f"Eroare: {e}")
    finally:
        user_socket.close()
        if user_socket in users:
            broadcast(encrypt(f"{users[user_socket]} a părăsit conversația."), user_socket)
            if users[user_socket] in usernames:
                del usernames[users[user_socket]]
            del users[user_socket]

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((Host, Port))
    server.listen(5)

    
    print(f"Server pornit pe {Host}:{Port}")

    while True:
        user_socket, addr = server.accept()
        threading.Thread(target=handle, args=(user_socket,)).start()

start()