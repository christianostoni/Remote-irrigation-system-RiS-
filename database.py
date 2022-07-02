import sqlite3
import hashlib
from datetime import date, datetime, timedelta

# Inizializzazione database credenziali
class Database:
    def __init__(self):
        self.database = sqlite3.connect("credentials.sqlite", check_same_thread=False)
        self.database.execute('''
            CREATE TABLE IF NOT EXISTS utenti (
                user VARCHAR(30) PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                token VARCHAR(255) NULL,
                token_expire DATETIME NULL
            );
        ''')
        self.database.commit()

        usercount = self.database.execute("SELECT COUNT(user) FROM utenti").fetchone()
        self.database.commit()
        # Crea un utente 'admin' con password 'admin' se non è già stato registrato un account
        if usercount[0] == 0: self.register('admin', 'ZDAzM2UyMmFlMzQ4YWViNTY2MGZjMjE0MGFlYzM1ODUwYzRkYTk5Nw==')

    # Registra un nuovo nick
    def register(self, user, password) -> bool:
        sql = "INSERT INTO utenti (user, password) VALUES (?, ?);"
        udata = (user, password) # User Data
        try:
            self.database.execute(sql, udata)
            self.database.commit()
            print(f"[{datetime.now()}] Registrazione @{user} effettuata")
            return True
        except:
            print(f"[{datetime.now()}] Errore registrazione nickname : @{user}")
            return False

    # Controlla credenziali d'accesso
    def login(self, user, password) -> bool:
        sql = "SELECT * FROM utenti WHERE user = ? AND password = ?;"
        udata = (user, password)
        
        matches = self.database.execute(sql, udata).fetchone()
        self.database.commit()
        if matches != None:
            if matches[1] == password:
                print(f"[{datetime.now()}] Login @{user} effettuato")
                return True
            else:
                print(f"[{datetime.now()}] Login @{user} non riuscito")
                return False
        
        print(f"[{datetime.now()}] Login @{user} non riuscito")
        return False

    # Genera un token con SHA256
    def gen_token(self, user, password) -> str:
        sql = "UPDATE utenti SET token = ?, token_expire = ? WHERE user = ?"
        token = hashlib.sha256(f"{user}-{datetime.today().microsecond}-{password}".encode('utf-8'))
        udata = (token.hexdigest(), (datetime.today() + timedelta(days=14)), user)
        try:
            self.database.execute(sql, udata)
            self.database.commit()
            print(f"[{datetime.now()}] Generato token per @{user}")
            return token.hexdigest()
        except:
            print(f"[{datetime.now()}] Errore generazione token per @{user}")
    
    # Leggi e convalida il token
    def retrive_token(self, token) -> str:
        sql = "SELECT user FROM utenti WHERE token = ?"
        udata = (token,)
        try:
            nick = self.database.execute(sql, udata).fetchone()
            self.database.commit()
            if nick != None:
                print(f"[{datetime.now()}] Token recuperato")
                # controlla se il token non è scaduto
                sql = "SELECT token_expire FROM utenti WHERE user = ?"
                expire_date = self.database.execute(sql, (nick[0],)).fetchone()
                self.database.commit()

                if datetime.strptime(expire_date[0], '%Y-%m-%d %H:%M:%S.%f') > datetime.today():
                    print(f"[{datetime.now()}] Il token è valido")
                    return True
                else:
                    print(f"[{datetime.now()}] Il token è scaduto")
                    self.destroy_token(token)
                    return False
        except:
            print(f"[{datetime.now()}] Token inesistente")
            return False    

    # Distruggi il token al logout
    def destroy_token(self, token):
        sql = "UPDATE utenti SET token = NULL WHERE token = ?"
        udata = (token,)
        try:
            self.database.execute(sql, udata)
            self.database.commit()
            print(f"[{datetime.now()}] Token eliminato")
        except: 
            print(f"[{datetime.now()}] Errore eliminazione token")

    # Elimina un account
    def delete_account(self, user):
        sql = "DELETE FROM utenti WHERE user = ?"
        udata = (user,)
        try:
            self.database.execute(sql, udata)
            self.database.commit()
            print(f"[{datetime.now()}] Account @{user} eliminato")
            return True
        except:
            print(f"[{datetime.now()}] Errore eliminazione account @{user}")
            return False