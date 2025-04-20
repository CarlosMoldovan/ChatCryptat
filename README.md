Acesta este un honeypot scris in Python, care simuleaza un server SSH si salveaza date despre incercarile de conectare. Proiectul vine cu o interfata grafica (Tkinter), unde poti vedea loguri live si statistici despre conexiuni.

Scopul proiectului

Scopul acestui proiect este sa:

Simuleze un server SSH vulnerabil pentru a atrage potentiali atacatori.
Inregistreze toate incercarile de autentificare (nume de utilizator + parola).
Ofera o interfata prietenoasa pentru vizualizarea activitatii in timp real.
Analizeze si afiseze statistici relevante pentru studii de securitate si testare.
Este o unealta educationala si de analiza, NU un sistem de securitate pentru productie.

Ce face aplicatia

Porneste un server pe portul 2222 care accepta conexiuni SSH.
Nu permite autentificarea, dar salveaza userul si parola folosita.
Pastreaza logurile si le afiseaza in interfata grafica.
Salveaza toate datele (nume, parola, ip, data si ora) intr-un fisier CSV.
Ofera o pagina separata cu statistici: conexiuni, IP-uri unice si parole frecvente.
Interfata si Functionalitate

Loguri in timp real
<img width="1165" alt="Screenshot 2025-04-09 at 18 50 49" src="https://github.com/user-attachments/assets/4664363f-9cbe-45c5-a5da-f574e2fb484c" />
Vezi toate incercarile de conectare in timp real.
Butoane pentru pornirea si oprirea serverului.
Comutare rapida intre loguri si statistici.
Statistici in timp real
<img width="694" alt="Screenshot 2025-04-09 at 18 50 21" src="https://github.com/user-attachments/assets/fe497bd8-155b-4e8d-a127-95febb1cfd60" />
Numar total de conexiuni primite.
Numar de IP-uri unice care au incercat sa se conecteze.
Top 5 parole cel mai des incercate.
Cum se foloseste

1. Setup
Asigura-te ca ai fisierul key (cheie privata RSA) in acelasi folder cu scriptul.
Poti genera o cheie cu:
ssh-keygen -t rsa -b 2048 -f key
2. Ruleaza scriptul
python honeypot.py
3. Foloseste interfata
Apasa pe "porneste server" pentru a incepe.
Vezi in timp real cine incearca sa se conecteze.
Acceseaza pagina "vezi statistici" pentru raportul in timp real.
4. Datele sunt salvate automat
Toate incercarile de conectare sunt salvate in utilizatori.csv.
Librarii folosite

paramiko – pentru simularea serverului SSH.
socket si threading – pentru conexiuni multiple.
tkinter – pentru interfata grafica.
csv si datetime – pentru salvarea datelor.
Surse si inspiratie

Am folosit urmatoarele linkuri pentru inspiratie si intelegere:

https://docs.paramiko.org/
https://realpython.com/python-sockets/
https://docs.python.org/3/library/socket.html
https://www.youtube.com/watch?v=gDjDxS55890&t=27s&pp=ygUWY3JlYXRlIGhvbmV5cG90IHB5dGhvbg%3D%3D
https://www.youtube.com/watch?v=HO1h57CiF98&pp=ygUWY3JlYXRlIGhvbmV5cG90IHB5dGhvbg%3D%3D
https://docs.python.org/3/library