using System;
using System.Collections.Generic;
using System.Text;
using System.Text.Json.Serialization;

namespace Client_Rest
{
    class Cliente : Utente
    {
        [JsonPropertyName("Nome")]
        public string Nome { get; set; }

        [JsonPropertyName("Cognome")]
        public string Cognome { get; set; }

        [JsonPropertyName("Indirizzo")]
        public string Indirizzo { get; set; }

    }
}
