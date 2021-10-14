using System;
using System.Collections.Generic;
using System.Text;
using System.Text.Json.Serialization;

//https://github.com/marcodal97/JustIt/

namespace Client_Rest
{
    class Utente
    {
        [JsonPropertyName("Username")]
        public string Username { get; set; }

        [JsonPropertyName("Password")]
        public string Password { get; set; }


    }
}
