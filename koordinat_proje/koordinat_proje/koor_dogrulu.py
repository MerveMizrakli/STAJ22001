
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm
from geopy.distance import geodesic

def koordinat_dogrulugu_kontrol(input_path, output_path):
    df = pd.read_excel(input_path)
    proje_ad = "İlçesi"

    geolocator = Nominatim(user_agent="adres_koordinat_bulucu")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    def bulunan_koordinatlar():
        koordinat_sozlugu = {}
        for ilce in tqdm(df[proje_ad]):
            try:
                location = geocode(ilce)
                if location:
                    koordinat_sozlugu[ilce.strip().upper()] = (location.latitude, location.longitude)
            except:
                continue
        return koordinat_sozlugu

    district_coordinates = bulunan_koordinatlar()

    koor_kolon = df["Koordinatlar (Enlem_Boylam)"].dropna().str.split(',', expand=True)
    df.loc[koor_kolon.index, "enlem"] = koor_kolon[0].str.strip().astype(float)
    df.loc[koor_kolon.index, "boylam"] = koor_kolon[1].str.strip().astype(float)

    def en_yakin_ilce(enlem, boylam):
        en_kisa_mesafe = float('inf')
        yakin_ilce = None
        for ilce, merkez in district_coordinates.items():
            if merkez is None:
                continue
            mesafe = geodesic((enlem, boylam), merkez).kilometers
            if mesafe < en_kisa_mesafe:
                en_kisa_mesafe = mesafe
                yakin_ilce = ilce
        return yakin_ilce

    def kontrol_et(row):
        if pd.isna(row['enlem']) or pd.isna(row['boylam']):
            return "Koordinat Eksik"
        ilce_excel = str(row['İlçesi']).strip().upper()
        tahmin = en_yakin_ilce(row['enlem'], row['boylam'])
        if tahmin is None:
            return "Tahmin Edilemedi"
        elif ilce_excel == tahmin:
            return "Doğru"
        else:
            return f"Yanlış ({tahmin})"

    df["Doğruluk"] = df.apply(kontrol_et, axis=1)
    df.to_excel(output_path, index=False)
