using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace Progetto_APL_CLIENT.Client_Rest
{
    class utente
    {

        [JsonPropertyName("Username")]
        public string Username { get; set; }

        [JsonPropertyName("Password")]
        public string Password { get; set; }


    }
}
