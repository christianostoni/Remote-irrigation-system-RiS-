# Remote-irrigation-system-RiS-

Sistema RIS per l'irrigazione di piante comandato da Raspberry Pi3

## Struttura cartelle
* `templates/` contiene le **pagine web** HTML
* `static/css` contiene i **fogli di stile** CSS delle pagine web
* `static/js ` contiene le **utility** Javascript

`init.py` è il file principale

`database.py` contiene le funzioni per la gestione del database

`test.py` contiene i test del database

## Creare un ambiente per l'esecuzione

**Ambiente reale nel Raspberry Pi3**

(configurazione porta raspberry nel file `init.py`)
```sh
pip install flask serial RPi.GPIO
python init.py 
```

**Ambiente di sviluppo**

Se si necessita modificare solo le pagine HTML/CSS o apportare cambiamenti alle funzionalità interne al database, è possibile seguire il seguente procedimento:

* `pip install flask`
* **commentare gli import** delle dipendenze non trovate nel file `init.py` 
```py
# import serial
# import RPi.GPIO as gpio
```
* commentare/modificare le linee di codice che dipendono dalle dipendenze non trovate
* `python init.py`

**VERSIONE MINIMA RICHIESTA DI PYTHON: 3.7**