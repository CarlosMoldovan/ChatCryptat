Acesta este un chat scris în Python care permite comunicare în timp real între utilizatori, cu criptare AES aplicată pe mesajele trimise. Proiectul vine cu o interfață grafică (Tkinter), unde utilizatorii pot selecta între chat de grup sau privat și pot trimite mesaje în siguranță.

Scopul proiectului
Scopul acestui proiect este să:

Permită comunicarea criptată între mai mulți utilizatori.

Simuleze atât chat de grup, cât și comunicare directă între doi clienți.

Protejeze datele transmise prin criptare AES.

Oferă o interfață grafică intuitivă, ușor de utilizat.

Servească drept unealtă educațională pentru înțelegerea criptării simetrice, a conexiunilor rețea și a interfețelor grafice în Python.

Este o aplicație demonstrativă, cu scop educațional, NU o soluție de comunicație sigură pentru uz real.

Ce face aplicația
Pornește un server care acceptă conexiuni multiple de la clienți pe portul 1540.

Cere autentificare printr-o parolă unică definită pe server.

Oferă clientului două opțiuni după autentificare:

Chat de grup – unde toți utilizatorii pot comunica.

Chat privat – selectezi un alt utilizator și discuți doar cu el.

Criptează toate mesajele cu AES și le decriptează pe server.

Afișează mesajele primite în timp real în interfața clientului.

Folosește threading pentru a primi și afișa mesajele fără a bloca interfața.

Interfață și Funcționalitate
Login simplu
<img width="400" alt="login" src="https://github.com/user-attachments/assets/your-image-id-1" />
Autentificare cu username și parolă.

Selectare mod de comunicare
<img width="400" alt="selectare chat" src="https://github.com/user-attachments/assets/your-image-id-2" />
Alegere între chat de grup sau privat.

Chat de grup
<img width="400" alt="chat grup" src="https://github.com/user-attachments/assets/your-image-id-3" />
Toți utilizatorii conectati pot comunica într-un singur spațiu.

Chat privat
<img width="400" alt="chat privat" src="https://github.com/user-attachments/assets/your-image-id-4" />
Comunicare individuală între doi utilizatori, cu selecție din listă.

Cum se folosește
Setup
Asigură-te că ai Python 3 instalat. Instalează biblioteca necesară:

bash
Copiază
Editează
pip install pycryptodome
Rulează serverul
Deschide un terminal și pornește serverul:

bash
Copiază
Editează
python server.py
Rulează clientul
Pe fiecare client, rulează:

bash
Copiază
Editează
python user.py
Autentificare și folosire
Introdu un nume de utilizator și parola corectă (parola este definită în server.py). După autentificare, alege tipul de chat dorit și începe să comunici.

Librării folosite
socket – pentru conexiuni rețea
threading – pentru execuție paralelă
tkinter – pentru interfața grafică
Crypto.Cipher (AES) – pentru criptare și decriptare
hashlib – pentru hashingul parolei
pickle – pentru serializarea datelor

Surse și inspirație
https://docs.python.org/3/library/socket.html
https://docs.python.org/3/library/tkinter.html
https://pycryptodome.readthedocs.io/en/latest/
https://www.youtube.com/watch?v=Lbfe3-v7yE0
https://www.geeksforgeeks.org/socket-programming-python/
https://www.youtube.com/watch?v=JeznW_7DlB0