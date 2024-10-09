import bcchapi;
import requests;

# def usarSerie():

#     user="marjuan9876@gmail.com"
#     password="Marjuan_12"

#     fecha1="2021-10-10"
#     fecha2="2021-10-15"

#     apiUrl = f"https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user={user}&pass={password}&firstdate={fecha1}&lastdate={fecha2}&timeseries=F022.TPM.TIN.D001.NO.Z.D&function=GetSeries"
#     respuesta = requests.get(apiUrl)

#     if respuesta.status_code == 200:
#         data = respuesta.json()
#         return data
#     else:
#        return f"Error {respuesta.status_code}: {respuesta.text}"

# resultado = usarSerie()
# print(resultado)


def buscarSeries():     
    user="marjuan9876@gmail.com"     
    password="Marjuan_12"

    apiUrl = f"https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user={user}&pass={password}&function=SearchSeries&frequency=ANNUAL"
    respuesta = requests.get(apiUrl)

    if respuesta.status_code == 200:
        data = respuesta.json()
        return data
    else:
        return f"Error {respuesta.status_code}: {respuesta.text}"

        
resultado = buscarSeries()
print(resultado)
    












