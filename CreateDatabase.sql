create database justit;
use justit;

create table Utente(
username char(20) primary key,
pass char(20) not null,
tipo int not null /*0 cliente - 1 ristorante*/
);

create table Cliente(
username char (20) primary key,
nome char(20) not null,
cognome char(20) not null,
indirizzo char(50) not null,

foreign key(username) references Utente(username)
on delete cascade on update cascade
);

create table Ristorante(
username char (20) primary key,
nome char(20) not null,
categoria char(20) not null,
indirizzo char(50) not null,
aperto boolean default false,

foreign key(username) references Utente(username)
on delete cascade on update cascade
);

create table Menu(
id int NOT NULL AUTO_INCREMENT,
username_ristorante char(20) not null,
categoria char(20),

PRIMARY KEY(id),

foreign key(username_ristorante) references Ristorante(username)
on delete cascade on update cascade
);

create table Pietanza(
id int NOT NULL AUTO_INCREMENT,
id_menu int not null,
nome char(20) not null,
descrizione char(50),
categoria char(20) not null,
prezzo float not null,

PRIMARY KEY(id),

foreign key(id_menu) references Menu(id)
on delete cascade on update cascade
);

create table Ordine(
id int NOT NULL AUTO_INCREMENT,
username_ristorante char(20) not null,
username_utente char(20) not null,
stato char(20),
compilato bool default false,

PRIMARY KEY(id),

foreign key(username_ristorante) references Ristorante(username)
on delete cascade on update cascade,
foreign key(username_utente) references Utente(username)
on delete cascade on update cascade
);

create table Ordine_Pietanza(
id_ordine int NOT NULL,
id_pietanza int NOT NULL,

PRIMARY KEY(id_ordine, id_pietanza),

foreign key(id_ordine) references Ordine(id)
on delete cascade on update cascade,
foreign key(id_pietanza) references Pietanza(id)
on delete cascade on update cascade
);

create table questionario(
id_questionario int NOT NULL auto_increment,
id_ordine int NOT NULL,
qualità_cibo int NOT NULL,
servizio_ristorante int NOT NULL,
tempo_consegna int NOT NULL,

PRIMARY KEY (id_questionario),

foreign key(id_ordine) references Ordine(id)
on delete cascade on update cascade
);
