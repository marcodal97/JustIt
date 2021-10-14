using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Net.Http.Formatting;
using System.Net.Http.Headers;
using System.Threading.Tasks;

using System.Text.Json;
using System.Text.Json.Serialization;
using System.Collections.Specialized;
using System.Text.RegularExpressions;
using System.Linq;

namespace Progetto_APL_CLIENT.Client_Rest
{
    public class FunctionRest
    {
        static HttpClient client = new HttpClient();

        public static void clientHttp(string url)
        {

            client.BaseAddress = new Uri(url);
            client.DefaultRequestHeaders.Accept.Clear();
            client.DefaultRequestHeaders.Accept.Add(
            new MediaTypeWithQualityHeaderValue("application/json"));
        }

        public static async Task<List<T>> getAsync<T>(string path)
        {

            var response = client.GetStreamAsync(path);
            var repositories = await System.Text.Json.JsonSerializer.DeserializeAsync<List<T>>(await response);//crea una lista con la risposta
            return repositories;

        }


        public static void getImage(string url, string saveimg)
        {
            WebClient client1 = new WebClient();
            client1.DownloadFile(new Uri(url), saveimg);//Posizione in cui viene scaricata il file\nome del file.jpg

        }

        public static void GetStatistic(string path)
        {
            var response = client.GetStreamAsync(path);
            return;
        }
        public static async Task<Uri> CreateAsync<T>(T t, string path)//POST
        {

            HttpResponseMessage response = await client.PostAsJsonAsync(path, t);
            response.EnsureSuccessStatusCode();

            // return URI of the created resource.
            return response.Headers.Location;
        }

        public static async Task<T> UpdateAsync<T>(T t, string path)
        {
            HttpResponseMessage response = await client.PutAsJsonAsync(
                path, t);
            response.EnsureSuccessStatusCode();

            // Deserialize the updated product from the response body.
            t = await response.Content.ReadAsAsync<T>();
            return t;
        }//PUT

        public static async Task<HttpStatusCode> DeleteAsync(string id, string path)//DELETE
        {
            var url = path + "?" + "delete_id=" + id;
            HttpResponseMessage response = await client.DeleteAsync(url);

            return response.StatusCode;
        }

        static string createUrl(List<string> parameters, string typeSearch)
        {
            int i = 1;
            string url = "?type=" + typeSearch; ;
            foreach (string parameter in parameters)
            {
                url += "&parameter" + i + "=" + parameter;
                i++;
            }

            return url;
        }

        static string createUrlDictionary(Dictionary<string, string> parameters)
        {
            string url = "?";
            foreach (KeyValuePair<string, string> parameter in parameters)
            {
                    url += "&" + parameter.Key + "=" + parameter.Value;
            }
            return url;
        }

        //Metodo utilizzato per la creazione di una richiesta
        public static async Task<List<T>> createRequest<T>(Dictionary<string, string> parameters, string path)
        {
           var url = path + createUrlDictionary(parameters);

            List<T> result;
            
            result = await getAsync<T>(url);

            return result;
            
        }

        public static async Task<List<T>> searchForParametersDictionary<T>(string typeSearch, Dictionary<string, string> parameters, string path)
        {
            var url = path + createUrlDictionary(parameters);

            List<T> result;
            try
            {
                result = await getAsync<T>(url);
            }
            catch (System.Net.Http.HttpRequestException e)
            {
                Console.WriteLine("Errore nella connessione al database, prego aprire una connessione al database!");
                Console.WriteLine(e.Message);
                throw new System.Net.Http.HttpRequestException("Errore nella connessione al database, prego avviare il server!");
            }

            if (result.Count != 0)
                return result;
            else
            {
                Console.WriteLine("NESSUN UTENTE TROVATO!");
                return null;
            }
        }

        public static void ControlloCaratteriSpecialiStringa(string input, string ControlType)
        {
            switch (ControlType)
            {
                case "username":
                    var regexItem = new Regex("^[a-zA-Z0-9àèìòù' ]*$");
                    if (regexItem.IsMatch(input))
                        return;
                    else
                        throw new System.ArgumentException("La stringa \"" + input + "\" contiene dei caratteri speciali, Eliminare i caratteri speciali e riprovare.");


                case "password":
                    var regexItemMail = new Regex(@"\A(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)\Z");
                    if (regexItemMail.IsMatch(input))
                        return;
                    else
                        throw new System.ArgumentException("L'email " + input + " inserita non rispetta il formato desiderato, prego inserire una mail valida e riprovare!");

            }


        }
        public static string FirstCharToUpper(string input)
        {
            input = input.ToLower();
            return input.First().ToString().ToUpper() + input.Substring(1);
        }

    }
}
