import pandas as pd
import numpy as np
import matplotlib.pyplot as plt       #kütüphane tanımlamaları
import seaborn as sns
from shapely.geometry import Point,Polygon
from geopy.distance import geodesic



try:
    df=pd.read_excel('KoordinatlariBosProjeler.xlsx')  #Dosya var mı yok mu kontrolü. Varsa dosya okunur yoksa dosya yolu bulunamaz ve koddan exit ile çıkış yapar.
    print("Dosya başariyla yüklendi!")
except FileNotFoundError:
    print("Hata: Dosya yolu bulunamadi. Lütfen yolu ve dosya adini kontrol edin.")
    exit()

project_coordinates = {
   5970: (40.8776, 29.2483),    # Pendik Papatya Deresi
    5971: (41.0036, 29.2214),    # Sancaktepe Paşaköy Deresi
    5972: (40.8619, 29.3268),    # Tuzla Umur Deresi
    5973: (40.9828, 29.1183),    # Ataşehir Küçükbakkalköy Deresi
    6031: (41.0186, 28.9408),    # Fatih Uşşaki Camii
    6049: (40.9634, 28.8079),    # Bakırköy Florya İtfaiye
    6052: (41.0031, 28.6436),    # Beylikdüzü Beykent İtfaiye
    6054: (41.1536, 28.8931),    # Eyüpsultan Kemerburgaz Kent Ormanı
    6058: (41.1125, 29.0564),    # Sarıyer İstinye İtfaiye
    6063: (40.9019, 29.1947),    # Kartal Hayvan Bakımevi
    6064: (40.8578, 29.1269),    # Adalar Büyükada Arabacılar Meydanı
    6065: (41.0936, 28.8025),    # Başakşehir Meydan
    6066: (41.0444, 28.9019),    # Bayrampaşa Meydan
    6067: (41.0875, 29.0822),    # Beykoz Çubuklu Tarihi İtfaiye
    6068: (41.1358, 29.0986),    # Beykoz Tarımsal Yapılar
    6069: (41.0583, 29.2014),    # Çekmeköy Alemdağ Meydanı
    6070: (41.0439, 28.8769),    # Esenler Engelliler Sarayı
    6071: (41.0647, 28.9258),    # Eyüpsultan Rami Kütüphanesi
    6072: (41.0714, 28.9336),    # Eyüpsultan Sivil Savunma
    6073: (41.0719, 28.8964),    # Gaziosmanpaşa İSMEK Binası
    6075: (41.0156, 28.7769),    # Küçükçekmece Atakent Cem Evi
    6076: (40.9358, 29.1553),    # Maltepe Cemevi
    6077: (40.9417, 29.1636),    # Maltepe Aydınevler Kız Yurdu
    6078: (40.9333, 29.1408),    # Maltepe Küçükyalı Sosyal Yaşam Merkezi
    6079: (40.8764, 29.2336),    # Pendik Güzelyalı Meydanı
    6081: (41.1742, 29.6139),    # Şile Çavuş Mahallesi Kreş
    6082: (40.8386, 29.3097),    # Tuzla Kent Meydanı
    6083: (41.0228, 29.1075),    # Ümraniye Akdeniz Caddesi Alt Geçit
    6084: (41.0397, 29.0164),    # Üsküdar 15 Temmuz Köprüsü Metrobüs
    6085: (40.8536, 29.1333),    # Adalar Büyükada Maden Mahallesi
    6086: (41.1928, 28.7219),    # Arnavutköy Deliklikaya İtfaiye
    6087: (40.9867, 29.1242),    # Ataşehir Darülaceze Güçlendirme
    6088: (40.9867, 29.1242),    # Ataşehir Darülaceze Master Plan
    6089: (40.9967, 28.7178),    # Avcılar Satış Ofisi Kreş
    6090: (40.9914, 28.7214),    # Avcılar Tıp Merkezi
    6091: (40.9936, 28.7139),    # Avcılar Gümüşpala Parsel
    6092: (41.0025, 28.8569),    # Bahçelievler Yol Bakım Binaları
    6093: (40.9764, 28.7903),    # Bakırköy Florya Engelliler Havuzu
    6094: (40.9819, 28.8764),    # Bakırköy 110 Ada 13 Parsel
    6095: (41.1533, 28.7639),    # Başakşehir Kayabaşı Rekreasyon
    6096: (41.0450, 28.9025),    # Bayrampaşa 347-23198 Parsel
    6097: (41.0433, 28.9011),    # Bayrampaşa 0 Ada 22445 Parsel
    6098: (41.0428, 28.9036),    # Bayrampaşa Mehmet Akif Kültür Merkezi
    6099: (41.0408, 28.9003),    # Bayrampaşa Belediye Hizmet Binası
    6100: (41.0575, 29.0367),    # Beşiktaş Arnavutköy Sosyal Tesis
    6101: (41.0864, 29.0333),    # Beşiktaş Etiler Spor Kompleksi
    6102: (41.0472, 29.0086),    # Beşiktaş Tünel Maçka Laboratuvarı
    6103: (41.0406, 29.0103),    # Beşiktaş Dikilitaş Spor Merkezi
    6104: (41.0406, 29.0103),    # Beşiktaş Dikilitaş Mahallesi Spor Merkezi
    6105: (41.1389, 29.0917),    # Beykoz Belediye Hizmet Alanı
    6106: (41.0325, 28.9639),    # Beyoğlu Küçükpiyale Kültür Tesis
    6107: (41.0314, 28.9667),    # Beyoğlu Piyalepaşa Otopark
    6108: (41.0236, 28.5786),    # Büyükçekmece İtfaiye
    6109: (41.0208, 28.5769),    # Büyükçekmece Halk Sağlığı Merkezi
    6110: (41.1414, 28.4619),    # Çatalca Minibüs Terminali
    6111: (41.1397, 28.4633),    # Çatalca 19 Mayıs Gençlik Merkezi
    6112: (41.2569, 28.4664),    # Çatalca Subaşı Hayvan Bakımevi
    6113: (41.1436, 28.4658),    # Çatalca Ferhatpaşa Afet Lojistik
    6114: (41.0519, 29.1936),    # Çekmeköy Köpek Eğitim Merkezi
    6115: (41.0439, 28.8769),    # Esenler Dörtyol Meydanı
    6116: (41.0450, 28.8783),    # Esenler Hakkı Başar Spor Salonu
    6117: (41.0339, 28.6764),    # Esenyurt 348 Ada Kültür Merkezi
    6118: (41.0350, 28.6783),    # Esenyurt Sosyal Yaşam Merkezi
    6119: (41.1564, 28.8919),    # Eyüpsultan Vialand Atletizm Pisti
    6120: (41.0647, 28.9258),    # Eyüpsultan Rami Kütüphane Çevresi
    6121: (41.0936, 28.9514),    # Eyüp Alibeyköy AKOM Binası
    6122: (41.1236, 28.9014),    # Eyüpsultan Hasdal Hayvan Bakımevi
    6123: (41.0086, 28.9514),    # Fatih Aksaray İSKİ Sanat Meydanı
    6124: (41.0125, 28.9486),    # Fatih İnebey Hizmet Binası
    6125: (41.0769, 28.9036),    # Gaziosmanpaşa Küçükköy Kreş
    6126: (41.0778, 28.9050),    # Gaziosmanpaşa Küçükköy Kültür Merkezi
    6127: (41.0714, 28.8964),    # Gaziosmanpaşa Fetih Parkı
    6128: (40.9908, 29.0250),    # Kadıköy İSMEK Sanat Binası
    6129: (40.9903, 29.0264),    # Kadıköy Hizmet Binası
    6130: (40.9869, 29.0306),    # Kadıköy Rasimpaşa Parsel
    6131: (40.9036, 29.1917),    # Kartal Zabıta Yerleşkesi
    6132: (40.9019, 29.1947),    # Kartal Hayvan Bakımevi
    6133: (40.8983, 29.1875),    # Kartal Hürriyet Mahallesi Dini Tesis
    6134: (41.0125, 28.7769),    # Küçükçekmece Filenin Sultanları Yurdu
    6135: (40.9336, 29.1517),    # Maltepe Şehir Hatları Lojistik Depo
    6136: (41.0028, 29.2314),    # Sancaktepe Meclis Mah. Kültür Merkezi
    6137: (41.0150, 29.2186),    # Sancaktepe Sarıgazi Kültür Merkezi
    6138: (41.0036, 29.2214),    # Sancaktepe Paşaköy Makine İkmal
    6139: (41.0086, 29.2014),    # Sancaktepe Fatih Mah. Cami
    6140: (41.0258, 29.2417),    # Sancaktepe Samandıra Cemevi
    6141: (41.1686, 29.0514),    # Sarıyer Çayırbaşı Hizmet Binası
    6142: (41.1525, 29.0633),    # Sarıyer Büyükdere Eski Belediye Binası
    6143: (41.1614, 29.0586),    # Sarıyer Atletizm Pisti
    6144: (41.1786, 29.0236),    # Sarıyer Zekeriyaköy Spor Vadisi
    6145: (41.1667, 29.0567),    # Sarıyer İsmail Akgün Hastanesi
    6146: (41.1725, 29.0389),    # Sarıyer Uskumruköy Sağlıklı Yaşam
    6147: (41.0739, 28.2464),    # Silivri Gençlik ve Kültür Merkezi
    6148: (41.0761, 28.2486),    # Silivri Otobüs Terminali
    6149: (41.1064, 28.8639),    # Sultangazi 912 Ada Belediye Hizmet
    6150: (41.1742, 29.6139),    # Şile Engelliler Yüzme Havuzu
    6151: (41.0614, 28.9936),    # Şişli Gmall Rehabilitasyon
    6152: (41.0608, 28.9917),    # Şişli Dikilitaş İtfaiye
    6153: (41.0678, 29.0086),    # Şişli Zincirlikuyu Camii Mezarlık
    6154: (40.8386, 29.3097),    # Tuzla Hayvan Bakımevi
    6155: (41.0228, 29.1075),    # Ümraniye Kazım Karabekir Spor Salonu
    6156: (41.0264, 29.0236),    # Üsküdar Zeynep Kamil İtfaiye
    6157: (41.0464, 29.0636),    # Üsküdar Çengelköy Tescilli Yapı
    6158: (41.0472, 29.0650),    # Üsküdar Çengelköy Yurt
    6159: (41.0283, 29.0389),    # Üsküdar Ahmet Çelebi Sanat Akademisi
    6160: (41.0250, 29.0400),    # Üsküdar 1838 ada 1-25 parseller
    6161: (41.0214, 29.0364),    # Üsküdar Altunizade 8 ada 17 parsel
    6162: (41.0292, 29.0808),    # Üsküdar Kısıklı 795 ada 47-50 parseller
    6163: (40.9964, 28.9136),    # Zeytinburnu Kent Müzesi
    6164: (40.9819, 28.8764),    # Bakırköy Botanik Parkı
    6165: (41.1083, 29.0617),    # Beykoz Paşabahçe Limanı
    6166: (41.0125, 28.9486),    # Fatih Akşemsettin Caddesi
    6167: (41.0256, 28.9742),    # Beyoğlu Galata Kulesi
    6168: (40.9867, 29.1242),    # Ataşehir Celal Yadımcı Okulu Duvar
    6169: (40.9967, 28.7178),    # Avcılar Cihangir E5 Duvarı
    6170: (41.1389, 29.0917),    # Beykoz Rüzgarlıbahçe Lisesi Duvarı
    6171: (41.0253, 28.9775),    # Beyoğlu Karaköy Kemankeş Meydanı
    6172: (41.0286, 28.9667),    # Beyoğlu Unkapanı Köprüsü
    6173: (41.0439, 28.8769),    # Esenler Birlik Mah. Duvarı
    6174: (41.0339, 28.6764),    # Esenyurt Kıraç Mezarlığı Duvarı
    6175: (41.0647, 28.9258),    # Eyüpsultan Bulvarı Duvarı
    6176: (41.0714, 28.9336),    # Eyüpsultan Alacatepe Parkı Duvarı
    6177: (41.0125, 28.9486),    # Fatih 8 No'lu Aile Sağlığı Merkezi
    6178: (39.8606, 29.9714),    # Kütahya Dumlupınar Tören Yolu
    6179: (40.9819, 29.0636),    # Kadıköy Göztepe Köprüsü
    6180: (40.9417, 29.1636),    # Maltepe Altıntepe Üstgeçit
    6181: (41.0150, 29.2186),    # Sancaktepe Sarıgazi İETT Duvarı
    6182: (41.1083, 29.0617),    # Sarıyer Emirgan Korusu Duvarı
    6183: (41.0564, 28.2214),    # Silivri Selimpaşa Duvarı
    6184: (41.0739, 28.2464),    # Silivri İtfaiye Duvarı
    6185: (40.8386, 29.3097),    # Tuzla Şelale Sosyal Tesisleri Duvarı
    6186: (41.0214, 29.0364),    # Üsküdar Altunizade Köprüsü
    6187: (41.1928, 28.7219),    # Arnavutköy Bolluca Heyelan Önleme
    6188: (41.1800, 28.7400),    # Arnavutköy Merkez Cami Üstgeçit
    6189: (41.1825, 28.7361),    # Arnavutköy Gazi Fahrettin Paşa Kavşak
    6190: (40.9867, 29.1242),    # Ataşehir Kozyatağı Kavşağı
    6191: (40.9914, 29.1186),    # Ataşehir TEİAŞ Üstgeçidi
    6192: (40.9933, 29.1214),    # Ataşehir Turgut Özal Bulvarı Kavşak
    6193: (40.9950, 29.1250),    # Ataşehir Dudullu-Dereboyu Kavşak
    6194: (40.9936, 28.7139),    # Avcılar Gümüşpala Yol Duvarları
    6195: (40.9914, 28.7214),    # Avcılar Tahtakale Üstgeçit
    6196: (40.9967, 28.7178),    # Avcılar Üniversite Metrobüs Düzenleme
    6197: (40.9983, 28.7158),    # Avcılar D-100-Firuzköy Bağlantı
    6198: (40.9967, 28.7178),    # Avcılar Üniversite Kavşağı
    6199: (41.0392, 28.8569),    # Bağcılar Fatih Mah. Üstgeçit
    6200: (41.0439, 28.8236),    # Bağcılar Mahmutbey-Bahçeşehir Yol
    6201: (41.0025, 28.8569),    # Bağcılar Güneşli Köprüsü
    6202: (40.9764, 28.7903),    # Bakırköy Aytekin Kotil Parkı
    6203: (40.9819, 28.8764),    # Bakırköy Sakızağacı Üstgeçit
    6204: (40.9833, 28.8736),    # Bakırköy Çobançeşme Kavşak
    6205: (40.9819, 28.8764),    # Bakırköy Merter-Taşhan Yolu
    6206: (40.9819, 28.8764),    # Bakırköy Fikret Yüzatlı Caddesi
    6207: (40.9819, 28.8764),    # Bakırköy Kennedy Köprüsü
    6208: (41.0936, 28.8025),    # Başakşehir Şeyh Şamil Üstgeçidi
    6209: (41.0936, 28.8025),    # Başakşehir Gazi Mustafa Kemal Üstgeçit
    6210: (41.0936, 28.8025),    # Başakşehir Çam ve Sakura Üstgeçit
    6211: (41.0936, 28.8025),    # Başakşehir Otogar Yolları
    6212: (41.0936, 28.8025),    # Başakşehir TEM-İkitelli Kavşak
    6213: (41.1533, 28.7639),    # Başakşehir Deliklikaya-Altınşehir Yolu
    6214: (41.0936, 28.8025),    # Başakşehir Altınşehir Kavşak
    6215: (41.0936, 28.8025),    # Başakşehir İtfaiye Menfez Köprüsü
    6216: (41.0444, 28.9019),    # Bayrampaşa Maltepe Metrobüs Üstgeçit
    6217: (41.0444, 28.9019),    # Bayrampaşa Osmangazi Okulu Duvarı
    6218: (41.0444, 28.9019),    # Bayrampaşa Sağmacılar Duvarı
    6219: (41.1389, 29.0917),    # Beykoz Deresi Köprüleri
    6220: (41.0031, 28.6436),    # Beylikdüzü Liman Yolu Üstgeçit
    6221: (41.0325, 28.9639),    # Beyoğlu Halil Rıfatpaşa Üstgeçit
    6222: (41.0236, 28.5786),    # Büyükçekmece Kumburgaz Üstgeçit
    6223: (41.0236, 28.5786),    # Büyükçekmece Tüyap Heyelan Önleme
    6224: (41.0236, 28.5786),    # Büyükçekmece Mimarsinan Üstgeçit
    6225: (41.0236, 28.5786),    # Büyükçekmece Mimar Sinan-Mimaroba Yol
    6226: (41.1414, 28.4619),    # Çatalca Ovayenice Köprüsü
    6227: (41.0519, 29.1936),    # Çekmeköy Şile Yolu Üstgeçit
    6228: (41.0339, 28.6764),    # Esenyurt Ardıçevler Üstgeçit
    6229: (41.0339, 28.6764),    # Esenyurt Güzelyurt Metrobüs
    6230: (41.0647, 28.9258),    # Eyüpsultan Haliç Köprüsü Merdivenleri
    6231: (41.0647, 28.9258),    # Eyüpsultan AKOM Bağlantı Yolu
    6232: (41.0186, 28.9750),    # Fatih Çatladıkapı Sahil Duvarı
    6233: (41.0397, 28.9458),    # Fatih Feshane Sahil Projesi
    6234: (41.0086, 28.9514),    # Fatih-Zeytinburnu Ulubatlı Hasan Kavşağı Güney
    6235: (41.0086, 28.9514),    # Fatih-Zeytinburnu Ulubatlı Hasan Kavşağı Kuzey
    6236: (41.0719, 28.8964),    # Gaziosmanpaşa Abdi İpekçi Üstgeçit
    6237: (41.0153, 28.8869),    # Güngören Tozkoparan Üstgeçit
    6238: (41.0153, 28.8869),    # Güngören Merter Metrobüs
    6239: (41.0082, 28.9784),    # İstanbul Geneli Metrobüs İstasyonları
    6240: (40.9869, 29.0306),    # Kadıköy Fikirtepe Altgeçit
    6241: (40.9714, 29.0608),    # Kadıköy Caddebostan Sahil Yolu
    6242: (40.9819, 29.0636),    # Kadıköy Bağdat Caddesi Köprülü Kavşak
    6243: (40.9869, 29.0306),    # Kadıköy Söğütlüçeşme Köprüsü
    6244: (40.9869, 29.0306),    # Kadıköy Söğütlüçeşme Kavşağı
    6245: (40.9819, 29.0636),    # Kadıköy Yumurtacı Abdi Bey Köprüsü
    6246: (40.9358, 29.1553),    # Kadıköy-Maltepe D-100 Yan Yolları
    6247: (40.9819, 29.0636),    # Kadıköy Yenisahra-Bostancı Tüneli
    6248: (41.0725, 28.9836),    # Kağıthane Çağlayan Üstgeçit
    6249: (41.0725, 28.9836),    # Kağıthane Deresi Üstgeçit
    6250: (41.0725, 28.9836),    # Kağıthane Cendere Köprüsü
    6251: (41.0725, 28.9836),    # Kağıthane-Eyüpsultan Sadabat Viyadüğü
    6252: (40.9036, 29.1917),    # Kartal Hacılar Caddesi Üstgeçit
    6253: (40.9036, 29.1917),    # Kartal Lütfi Kırdar Hastanesi Üstgeçit
    6254: (40.8764, 29.2336),    # Kartal-Pendik Sahil Pazar Alanı
    6291: (40.8386, 29.3097)     # Tuzla Sahil İtfaiye
    
}

  

KOOR_COL = "Koordinatlar (Enlem_Boylam)"   # Koordinat sütunu adı
ID_COL = "Id"                             # Proje ID sütunu adı
ILCE_COL = "İlçesi"                       # İlçe sütunu adı

def kontrol_et(row):
    koor = row[KOOR_COL]
    if pd.isna(koor) or koor == "":
        proje_id = row[ID_COL]
        if proje_id in project_coordinates:
            lat, lon = project_coordinates[proje_id]
            return f"{lat},{lon}"
    return koor

# Koordinatları doldur
df[KOOR_COL] = df.apply(kontrol_et, axis=1)

df["Doğruluk"] = df[KOOR_COL].apply(
    lambda x: "Tamamlandı" if pd.notna(x) and x != "" else "Koordinat Eksik"
)

# Dosyaya yaz
df.to_excel("koordinat_doldurulmus_hali.xlsx", index=False)
print("Kontrol tamamlandı ve dosya kaydedildi.")