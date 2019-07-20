import json
import urllib3
import certifi


class Search:
    # Starts up a manager, uses ssl
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

    @staticmethod
    def ddg_join(msg_list):
        query = ""

        for i in range(len(msg_list) - 1):
            i += 1
            query += msg_list[i] + "+"

        return query[:-1]

    @staticmethod
    def ddg_search(query):
        base_url = "https://duckduckgo.com/?q="
        full_query = query + "&atb=v1-1"
        full_url = base_url + full_query

        return full_url

    def ddg_bang(self, query):
        full_query = query + "&format=json&pretty=1&no_redirect=1&atb=v1-1"
        request = 'https://api.duckduckgo.com/?q=' + full_query
        response = self.http.request('GET', request)
        json_data = json.loads(response.data)

        redirect = json_data['Redirect']

        return redirect

