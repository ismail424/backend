import requests
import json
import datetime
from bs4 import BeautifulSoup as soup


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

class VaktijaEU():
    """
    VaktijaEU is a wrapper around the VaktijaEU API.
    """

    def get_prayertimes(location_slug):
        """
        Returns the prayertimes for a given location.
        """
        url = f"https://api.vaktija.eu/v3/locations/slug/{location_slug}"
        result = {"success": False, "prayertimes": []}
        try:
            response = requests.get(url).json()
            months = response["data"]["months"]
            timestamp = str(datetime.date.today().year)
            for month in months:
                current_month = str(month).zfill(2)
                for day in months[month]["days"]:
                    current_day = str(day).zfill(2)
                    current_date = f"{timestamp}-{current_month}-{current_day}"
                    day_data = months[month]["days"][day]
                    result["prayertimes"].append({
                        "date": current_date,
                        "fajr": day_data["fajr"],
                        "sunrise": day_data["sunrise"],
                        "dhuhr": day_data["dhuhr"],
                        "asr": day_data["asr"],
                        "maghrib": day_data["maghrib"],
                        "isha": day_data["isha"]
                    })
            result["success"] = True

        except Exception as e:
            print(e)
            result["success"] = False

        return result

    def get_locations():
        """
        Returns the available locations.
        """
        try:
            file = open("app/static/vaktijaeu_locations.json", "r")
            return json.load(file)
        except:
            try:
                # Send a request to the VaktijaEU API to get the locations
                return requests.get("https://api.vaktija.eu/v3/locations").json()
            except:
                return None


class VaktijaBA():
    """
    VaktijaBA is a wrapper around the VaktijaBA API.
    """
    
    def get_prayertimes( id: int ):
        
        this_year = datetime.datetime.now().year
        result = {"success": False, "prayertimes": []}
        try:
            for year in range(this_year, (this_year + 2)):
                url = f"https://api.vaktija.ba/vaktija/v1/{id}/{year}"
                prayertimes_this_year = requests.get(url).json()["mjesec"]

                for index, month in enumerate(prayertimes_this_year):
                    for index2, day in enumerate(month["dan"]):

                        date = f"{year}-{str(index+1).zfill(2)}-{str(index2+1).zfill(2)}"
                        result["prayertimes"].append({
                            "date": date,
                            "fajr": str(day["vakat"][0]).zfill(2),
                            "sunrise": day["vakat"][1],
                            "dhuhr": day["vakat"][2],
                            "asr": day["vakat"][3],
                            "maghrib": day["vakat"][4],
                            "isha": day["vakat"][5]
                        })
            result["success"] = True
            
        except Exception as e:
            print(e)
            result["success"] = False
        return result

    def get_locations():
        """
        Returns the available locations.
        """
        try:
            file = open("app/static/vaktijaba_locations.json", "r")
            return json.load(file)
        except:
            try:
                # Send a request to the VaktijaEU API to get the locations
                return requests.get("https://api.vaktija.ba/vaktija/v1/lokacije").json()
            except:
                return None


class IslamiskaForbundet():
    
    def get_prayertimes(city :str):
        """
        Returns the prayertimes for a given location.
        """

        result = {"success": False, "prayertimes": []}
        try:
            url = "https://www.islamiskaforbundet.se/wp-content/plugins/bonetider/Bonetider_Widget.php"
            headers = {
                'accept': '*/*',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                }
            data = {
                'ifis_bonetider_page_city': f"{city}, SE",
                'ifis_bonetider_page_month': "1"
            }
        
            for month in range(1,13):
                
                data['ifis_bonetider_page_month'] = str(month)
                res = requests.post(url, headers=headers, data=data)
                
                html = soup(res.text, 'html.parser')
                all_td = html.find_all('td')
                all_td = [td.text for td in all_td]
                prayertimes_month = []
                for i in range(0, len(all_td), 7):
                    prayertimes_month.append(all_td[i:i+7])
                
                for element in prayertimes_month:
                    current_year =  datetime.datetime.now().year
                    element[0] = f"0{element[0]}" if len(element[0]) == 1 else element[0]
                    month = f"0{month}" if len(str(month)) == 1 else month
                    date = f"{current_year}-{month}-{element[0]}"
                    result["prayertimes"].append({
                        "date": date,
                        "fajr": element[1],
                        "sunrise": element[2],
                        "dhuhr": element[3],
                        "asr": element[4],
                        "maghrib": element[5],
                        "isha": element[6]
                    })
                                    
            result["success"] = True
        except Exception as e:
            print(e)
            result["success"] = False
            
        return result
    
    def get_locations():
        """
        Returns the available locations.
        """
        try:
            file = open("app/static/islamiska-forbundet_locations.json", "r")
            return json.load(file)
        except:
            cities = ['Stockholm', 'Alingsås', 'Avesta', 'Bengtsfors', 'Boden', 'Bollnäs', 'Borlänge', 'Borås', 'Enköping', 'Eskilstuna', 'Eslöv', 'Falkenberg', 'Falköping', 'Flen', 'Filipstad', 'Gislaved', 'Gnosjö', 'Gävle', 'Göteborg', 'Halmstad', 'Haparanda', 'Helsingborg', 'Hudiksvall', 'Hultsfred', 'Härnösand', 'Hässleholm', 'Jokkmokk', 'Jönköping', 'Kalmar', 'Karlskoga', 'Karlskrona', 'Karlstad', 'Katrineholm', 'Kiruna', 'Kristianstad', 'Kristinehamn', 'Köping', 'Landskrona', 'Lessebo', 'Lidköping', 'Linköping', 'Ludvika', 'Luleå', 'Lund', 'Malmö', 'Mariestad', 'Mellerud', 'Mjölby', 'Norrköping', 'Norrtälje', 'Nyköping', 'Nässjö', 'Oskarshamn', 'Oxelösund', 'Pajala', 'Piteå', 'Ronneby', 'Sala', 'Simrishamn', 'Skara', 'Skellefteå', 'Skövde', 'Sollefteå', 'Strängnäs', 'Sundsvall', 'Sävsjö', 'Söderhamn', 'Södertälje', 'Tierp', 'Tranemo', 'Trelleborg', 'Trollhättan', 'Uddevalla', 'Ulricehamn', 'Umeå', 'Uppsala', 'Varberg', 'Vetlanda', 'Visby', 'Vänersborg', 'Värnamo', 'Västervik', 'Västerås', 'Växjö', 'Ystad', 'Åmål', 'Örebro', 'Örnsköldsvik', 'Östersund']
            return cities