class Altinkaynak:
    username = "AltinkaynakWebServis"
    password = "AltinkaynakWebServis"
    headers = {"Content-Type":"text/xml; charset=utf-8"}
    raw_response = None

    def get_try_currencies(self):
        import http.client
        import urllib.parse
        import xml.etree.ElementTree as ET
        from datetime import datetime,timedelta

        xml_data =   """<?xml version="1.0" encoding="utf-8"?>
                        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Header>
                                <AuthHeader xmlns="http://data.altinkaynak.com/">
                                    <Username>{username}</Username>
                                    <Password>{password}</Password>
                                </AuthHeader>
                            </soap:Header>
                            <soap:Body>
                                <GetCurrency xmlns="http://data.altinkaynak.com/" />
                            </soap:Body>
                        </soap:Envelope>""".format(username=self.username,password=self.password)

        url = 'http://data.altinkaynak.com/DataService.asmx'
        params = urllib.parse.urlencode({})
        conn = http.client.HTTPConnection("data.altinkaynak.com")
        conn.request("POST", "/DataService.asmx?%s" % params, xml_data, self.headers)
        self.raw_response = conn.getresponse().read()
        root = ET.fromstring(self.raw_response)
        envelope = root[0]
        body = envelope[0]
        getcurrencyresponse = body[0]

        curr_root = ET.fromstring(getcurrencyresponse.text.encode("utf-8").strip())

        curr_dict = {}
        for kur in curr_root:
            date_tr = datetime.strptime(kur[4].text,"%d.%m.%Y %H:%M:%S")
            date_aware =  (date_tr - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

            curr_dict[kur[0].text] = {
                                      "sell":float(kur[3].text),
                                      "buy":float(kur[2].text),
                                      "datetime_utc":date_aware
                                     }
            curr_dict.update({"TRY":{"sell":1,"buy":1,"datetime_utc":date_aware}})
        return curr_dict

    def get_rate(self,base_currency,currency):
        base_currency = base_currency.upper()
        currency = currency.upper()
        try_currencies = self.get_try_currencies()

        try:
            return {
                    "sell":try_currencies[base_currency]["sell"] / try_currencies[currency]["sell"],
                    "buy":try_currencies[base_currency]["buy"] / try_currencies[currency]["buy"],
                    "datetime_utc":try_currencies[base_currency]["datetime_utc"]
                   }
        except KeyError:
            raise Exception("Base currency or currency not found")


if __name__ == "__main__":
    import sys

    altin = Altinkaynak()

    try:
        sell_or_buy = sys.argv[3]
    except IndexError:
        sell_or_buy = "sell"

    if "=" in sys.argv[1] and "=" in sys.argv[2]:
        curr_args = {}
        split_argv1 = sys.argv[1].split("=")
        curr_args[split_argv1[0].replace("-","")] = split_argv1[1]
        split_argv2 = sys.argv[2].split("=")
        curr_args[split_argv2[0].replace("-","")] = split_argv2[1]

        print(altin.get_rate(**curr_args)[sell_or_buy])
    else:
        print (altin.get_rate(sys.argv[1],sys.argv[2])[sell_or_buy])
