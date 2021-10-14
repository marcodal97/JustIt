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
using Client_Rest;

namespace ClientRest
{
    class Program
    {
        static HttpClient client = new HttpClient();

        static async Task<List<T>> getAsync<T>(string path)
        {
            var response = client.GetStreamAsync(path);
            var repositories = await System.Text.Json.JsonSerializer.DeserializeAsync<List<T>>(await response);//crea una lista con la risposta
            return repositories;

        }

        static async Task<Uri> CreateAsync<T>(T t, string path)//POST
        {
            HttpResponseMessage response = await client.PostAsJsonAsync(
                path, t);
            response.EnsureSuccessStatusCode();

            // return URI of the created resource.
            return response.Headers.Location;
        }

        static async Task<T> UpdateAsync<T>(T t, string path)
        {
            HttpResponseMessage response = await client.PutAsJsonAsync(
                path, t);
            response.EnsureSuccessStatusCode();

            // Deserialize the updated product from the response body.
            t = await response.Content.ReadAsAsync<T>();
            return t;
        }//PUT

        static async Task<HttpStatusCode> DeleteAsync(string id, string path)//DELETE
        {
            var url = path + "?" + "delete_id=" + id;
            HttpResponseMessage response = await client.DeleteAsync(
               url);
            Console.WriteLine(response.StatusCode);
            return response.StatusCode;
        }

        static void printUtente(List<Utente> utente)
        {
            int cout = 0;
            foreach (var repo in utente)
            {
                cout++;
                Console.WriteLine("Username: " + repo.Username);
                Console.WriteLine("Password: " + repo.Password);
                Console.WriteLine("\n");
            }
            // if (cout == 0) { Console.WriteLine("Nessun Utente Trovato"); }
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

        static async Task<List<T>> searchForParameters<T>(string typeSearch, List<string> parameters, string path)
        {
            var url = path + createUrl(parameters, typeSearch);
            Console.WriteLine(url);
            var result = await getAsync<T>(url);
            if (result.Count != 0)
                return result;
            else
            {
                Console.WriteLine("NESSUN UTENTE TROVATO!");
                return null;
            }
        }

    }
}

