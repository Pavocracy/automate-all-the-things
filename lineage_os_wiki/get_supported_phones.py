from urllib3 import PoolManager
from bs4 import BeautifulSoup
from tqdm import tqdm
from dateutil.parser import parse
from re import findall
from json import dump
from importlib.metadata import version

base_url = "https://wiki.lineageos.org/devices/"
custom_headers = {"User-Agent": f"urllib3/{version('urllib3')}"}
wanted_info = ["released", "soc", "ram", "network"]
sort_by = "released"
supported_phones = []

if __name__ == "__main__":
    with open("supported_phones.json", "w", encoding="utf-8") as file, PoolManager(num_pools=2, headers=custom_headers) as http:
        vendor_html = http.request("GET", base_url)
        vendor_soup = BeautifulSoup(vendor_html.data, "html.parser")
        for vendor in tqdm(vendor_soup.find_all("div", {"class": "devices"}), desc="Vendors"):
            vendor_name = vendor.get("data-vendor")
            for phone in tqdm(vendor.find_all("div", {"class": "item"}), desc="Phones", leave=False):
                phone_info = {}
                phone_info["vendor"] = vendor_name
                phone_info["model"] = phone.find("span", {"class": "devicename"}).get_text().strip().replace("\n", "/")
                phone_info["discontinued"] = True if "discontinued" in phone["class"] else False
                phone_info["code"] = phone.find("span", {"class": "codename"}).get_text().strip()
                phone_html = http.request("GET", base_url + phone_info["code"])
                phone_soup = BeautifulSoup(phone_html.data, "html.parser")
                table = phone_soup.find("table", {"class": "deviceinfo"})
                for info in table.find_all("tr"):
                    th = info.find("th").get_text().strip().lower() if info.find("th") else None
                    if th in wanted_info:
                        td = info.find("td").get_text().strip().replace("\n", "/")
                        if th == "released":
                            try:
                                released_date = parse(td)
                                phone_info[th] = str(released_date).split(" ")[0]
                            except Exception:
                                fix_release_date = findall("\d{4}", td)
                                released_date = parse(fix_release_date[-1])
                                phone_info[th] = str(released_date).split(" ")[0]
                        else:
                            phone_info[th] = td
                supported_phones.append(phone_info)
        supported_phones.sort(key=lambda sort: sort[sort_by], reverse=True)
        dump(supported_phones, file, indent=2)