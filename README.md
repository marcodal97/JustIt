# JustIt

# Classi da utilizzare

CLASSE UTENTE: (Username, Password)

CLASSE CLIENTE EREDITA DA UTENTE: (Nome, Cognome, Indirizzo)

CLASSE RISTORANTE EREDITA DA UTENTE: (Nome_Ristorante, Categoria, Indirizzo_Ristorante, Aperto)

CLASSE MENU: (ID (incr), Username_Ristorante, Categoria (Primi, secondi, contorni ...), Lista_Pietanze)

CLASSE PIETANZE: (ID, Nome, Descrizione, Categoria, Prezzo)

CLASSE ORDINI: (ID, Lista_Pietanza, Costo_Totale)


# Tabelle DB

UTENTE: (Username, Password, Tipologia_Utente) //Flag: 0 (Cliente), 1 (Ristorante)

CLIENTE: (Username, Nome, Cognome, Indirizzo)

RISTORANTE: (Username, Nome_Ristorante, Categoria, Indirizzo_Ristorante, Aperto)

MENU: (ID, Username_Ristorante, Categoria)

MENU-PIETANZE: (ID_MENU, ID_PIETANZA) - AL MOMENTO NON SERVE

PIETANZA (ID, ID_MENU, Nome, Descrizione, Categoria, Prezzo)

ORDINI: (ID, Username_Ristorante, Username_Utente, stato) --  STATO: Conferma, Spedito, In Attesa

ORDINI-PIETANZA: (ID, ID_PIETANZA)


# Ipotetiche funzionalità da implementare

  Login (FATTO), registrazione (FATTO)
  logout (FATTO)
  
  1. Home clienti
  
    a.  Visualizzare ristoranti aperti/chiusi (FATTO)
    
    b.  Visualizzazione mediante ricerca dei ristoranti aperti/chiusi (?) -- NO
    
    c.  Visualizzazione menu del ristorante scelto 
    
    d.  Scelta pietanze relative ai vari menu o scelta di soli menu fissi (?) forse conviene di più
    
    e.  Attendere notifica di avvenuta conferma -- THREAD
   
    f.  Attendere notifica di avvenuta consegna -- THREAD
    
    g. Compilazione questionario per il client (R)
    
 
 2. Home Ristorante
 
      a. Bottone per apertura/chiusura ristorante (FATTO)

      b. Inserire menu (con relative pietanze) -- FORM  

      c. Attendere arrivo ordini -- THREAD

      d. Conferma dell'ordine -- BOTTONE
 
      f. Conferma della consegna -- BOTTONE
      
      g. Visualizzione valutazioni (Visualizza statistiche)
    
    
**********************************************


  3. Server

    a.  Menu
       a.1  Visualizzazione menu del ristorante scelto (FATTO)
       a.2  Inserimento nuovo menu (FATTO)
       a.3  Restituzione informazioni base menu (FATTO)
       a.4  Rimozione menu (FATTO)
    
    b.  Pietanze           
       b.1  Inserimento di pietanze in un menu (FATTO)
       b.2  Restituzione pietanze di un menu (FATTO)
       b.3  Rimozione di pietanze in un menu (FATTO)
       
    c.  Ordini
       c.1  Inserimento ordine (FATTO)
       c.2  Inserimento pietanze in un ordine (FATTO)
       c.3  Restituzione informazioni base di un ordine (FATTO)
       c.4  Restituzione pietanze di un ordine con dettagli (FATTO)
       c.5  Aggiornamento e restituzione stato ordine (FATTO)
