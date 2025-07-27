
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm

def koordinat_bul(dosya_yolu, cikti_yolu):
    df = pd.read_excel(dosya_yolu)
    proje_ad = "İlçesi"

    geolocator = Nominatim(user_agent="adres_koordinat_bulucu")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    enlemler = []
    boylamlar = []

    for adres in tqdm(df[proje_ad]):
        try:
            location = geocode(adres)
            if location:
                enlemler.append(location.latitude)
                boylamlar.append(location.longitude)
            else:
                enlemler.append(None)
                boylamlar.append(None)
        except:
            enlemler.append(None)
            boylamlar.append(None)

    df["Enlem"] = enlemler
    df["Boylam"] = boylamlar
    df["Koordinatlar"] = df["Enlem"].astype(str) + ", " + df["Boylam"].astype(str)

    df.to_excel(cikti_yolu, index=False)
