﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace Progetto_APL_CLIENT.Client_Rest
{
    class ristorante : utente
    {
        [JsonPropertyName("Nome_Ristorante")]
        public string Nome { get; set; }

        [JsonPropertyName("Categoria")]
        public string Cognome { get; set; }

        [JsonPropertyName("Indirizzo")]
        public string Indirizzo { get; set; }

        public ristorante(string username, string password, string nome, string cognome, string indirizzo)
        {
            this.Username = username;
            this.Password = password;
            this.Nome = nome;
            this.Cognome = cognome;
            this.Indirizzo = indirizzo;
        }
    }
}
