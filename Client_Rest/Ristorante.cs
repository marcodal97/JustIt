using System;
using System.Collections.Generic;
using System.Text;
using System.Text.Json.Serialization;

namespace Client_Rest
{
    class Ristorante : Utente
    {

        [JsonPropertyName("Nome_Ristorante")]
        public string Nome { get; set; }

        [JsonPropertyName("Categoria")]
        public string Cognome { get; set; }

        [JsonPropertyName("Indirizzo")]
        public string Indirizzo { get; set; }

    }
}
