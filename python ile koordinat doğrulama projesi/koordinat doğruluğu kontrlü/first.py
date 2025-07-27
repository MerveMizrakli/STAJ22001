import pandas as pd
import numpy as np
import matplotlib.pyplot as plt       #kütüphane tanımlamaları
import seaborn as sns
from shapely.geometry import Point,Polygon
from geopy.distance import geodesic



try:
    df=pd.read_excel('ttttt.xlsx')  #Dosya var mı yok mu kontrolü. Varsa dosya okunur yoksa dosya yolu bulunamaz ve koddan exit ile çıkış yapar.
    print("Dosya başariyla yüklendi!")
except FileNotFoundError:
    print("Hata: Dosya yolu bulunamadi. Lütfen yolu ve dosya adini kontrol edin.")
    exit()

district_centers = {
    "Adalar":        (40.8700, 29.1000),
    "Arnavutköy":    (41.1800, 28.7400),
    "Ataşehir":      (40.9950, 29.1000),
    "Avcılar":       (40.9900, 28.7200),     #anahtar değer tanımlamaları. Koordinatlar anahtar olan ilçelere atandı.Bu tanımlama sözlüğümüzdür.
    "Bağcılar":      (41.0290, 28.8660),     #anahtar değerler ilçe adları tamamlayıcı değerler ise koordinatlardır.
    "Bahçelievler":  (41.0000, 28.8500),
    "Bakırköy":      (40.9750, 28.8650),
    "Başakşehir":    (41.1000, 28.7700),
    "Bayrampaşa":    (41.0400, 28.9000),
    "Beşiktaş":      (41.0530, 29.0200),
    "Beykoz":        (41.1260, 29.1050),
    "Beylikdüzü":    (41.0010, 28.6400),
    "Beyoğlu":       (41.0300, 28.9700),
    "Büyükçekmece":  (41.0200, 28.5800),
    "Çatalca":       (41.1500, 28.4500),
    "Çekmeköy":      (41.0300, 29.1800),
    "Esenler":       (41.0450, 28.8900),
    "Esenyurt":      (41.0350, 28.6750),
    "Eyüpsultan":    (41.0900, 28.9300),
    "Fatih":         (41.0180, 28.9500),
    "Gaziosmanpaşa": (41.0800, 28.9100),
    "Güngören":      (41.0200, 28.8750),
    "Kadıköy":       (40.9870, 29.0570),
    "Kağıthane":     (41.0800, 28.9700),
    "Kartal":        (40.8910, 29.1950),
    "Küçükçekmece":  (41.0040, 28.7900),
    "Maltepe":       (40.9360, 29.1460),
    "Pendik":        (40.8700, 29.2500),
    "Sancaktepe":    (41.0100, 29.2400),
    "Sarıyer":       (41.1350, 29.0500),
    "Silivri":       (41.0800, 28.2300),
    "Sultanbeyli":   (40.9630, 29.2660),
    "Sultangazi":    (41.1000, 28.8900),
    "Şile":          (41.1800, 29.6100),
    "Şişli":         (41.0600, 28.9900),
    "Tuzla":         (40.8420, 29.3550),
    "Ümraniye":      (41.0300, 29.1200),
    "Üsküdar":       (41.0300, 29.0300),
    "Zeytinburnu":   (40.9900, 28.9100)
}

  

koor_kolon = df["Koordinatlar (Enlem_Boylam)"].dropna().str.split(',', expand=True) 
#excel dosyasından koordinat verileri çekilir(enlem boylam sütunundan.)Nan yani boş değerleri siler.
#Ardından kalan stringler virgül bazında bölünür ve bu bölünen parçalar yeni sütunlara ayrılır.


ilce = df['İlçesi'] #ilçe verileri excel sütunundan çekilir.


df.loc[koor_kolon.index, "enlem"] = koor_kolon[0].str.strip().astype(float)
#indexi 0 olan kısım bölünmüş virgülle bölünmüş verinin ilk satırını ifade eder.Yani enlemi ifade ediyor.
df.loc[koor_kolon.index, "boylam"] = koor_kolon[1].str.strip().astype(float)
#indexi 1 olan kısım bölünmüş verinin 2. kısmını ifade eder.Yani koordinatı ifade ediyor.


def en_yakin_ilce(enlem, boylam):  #koordinatlardaki eşleşen değerleri bulmak için yakınlık bazlı fonksiyon kullandım. Çünkü hassas değerler(virgül sonrası uzun)
    en_kisa_mesafe = float('inf') 
    yakin_ilce = None #sonuç olan yakın ilçeyi bulabilmek için tanımladım. Başta boş bırakılabilir.
    for ilce, merkez in district_centers.items():
        #Bu sözlükte her anahtar (ilce) bir ilçe adı, karşılığı (merkez) ise o ilçenin enlem-boylam koordinatları (tuple) olarak tutuluyor.
        mesafe = geodesic((enlem, boylam), merkez).kilometers
        #goedesic fonksiyonu girilen iki nokta arasındaki mesafeyi km cinsinden hesaplar.
        if mesafe < en_kisa_mesafe: #if kontrolü.Eğer bulunan mesafe en kısa mesafeden küçükse artık bu ilçenin koordinatları doğru kabul edilir.
            en_kisa_mesafe = mesafe
            yakin_ilce = ilce
    return yakin_ilce #tüm değerler kontrol edilince yakın ilçe değeri döndürülür.Ve sonuç budur.

def kontrol_et(row):
    if pd.isna(row['enlem']) or pd.isna(row['boylam']): #eğer enlem veya boylam hücrelerinden birisi boşsa koordinat eksik değeri yazdırır.
        return "Koordinat Eksik"
    ilce_excel = str(row['İlçesi']).strip().upper() #burada ilçe değeri string değilse string yapılır.Boşlukları temizler ve tüm charları büyük harf yapar.
    tahmin = en_yakin_ilce(row['enlem'], row['boylam']).upper()
    if ilce_excel == tahmin: #Koordinat değerleri kıyaslamaları yapıldığında doğru ilçe yazılmışsa kontrol sütununa doğru yazılır.
        return "Doğru"
    else:
        return f"Yanlış ({tahmin})" #Değilse yanlış yazılır ve olması gereken ilçe yazılır.


df["Doğruluk"] = df.apply(kontrol_et, axis=1) #Dönen tüm değerler doğruluk sütununa yazdırılır.

df.to_excel("koordinat_dogruluk_kontrol.xlsx", index=False) #çıktılar excele kaydedilir.
print("Kontrol tamamlandı ve dosya kaydedildi.")













