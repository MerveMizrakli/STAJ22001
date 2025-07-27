import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# 1. Adres listesini hazırla (200 adres)
addresses = [
    "Pendik Papatya Deresi, İstanbul",
    "Sancaktepe Paşaköy Deresi (Ayazma Deresi Anakol), İstanbul",
    "Tuzla Umur Deresi, İstanbul",
    # ... Diğer 197 adresi buraya ekleyin
]

# 2. Geocoder ayarları (1 saniyede 1 sorgu)
geolocator = Nominatim(user_agent="istanbul_projeleri")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# 3. Koordinatları çek
data = []
for idx, address in enumerate(addresses, 1):
    try:
        location = geocode(address)
        lat, lon = location.latitude, location.longitude if location else (None, None)
        data.append({"Sıra": idx, "Proje Adı": address, "Enlem": lat, "Boylam": lon})
        print(f"{idx}/200: {address} → {lat}, {lon}")
    except Exception as e:
        print(f"Hata: {address} - {str(e)}")
        data.append({"Sıra": idx, "Proje Adı": address, "Enlem": None, "Boylam": None})

# 4. CSV'ye kaydet
df = pd.DataFrame(data)
df.to_csv("istanbul_projeleri_koordinatlar.csv", index=False)
print("CSV dosyası oluşturuldu!")