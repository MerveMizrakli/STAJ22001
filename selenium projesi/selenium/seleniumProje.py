from selenium import webdriver
from selenium.webdriver.common.by import By   #➡️ Web sayfasındaki HTML elementlerini nasıl bulacağını tanımlar.
from selenium.webdriver.common.keys import Keys #➡️ Klavye tuşlarını kullanmanı sağlar. 

from selenium.webdriver.chrome.service import Service #bu ve alttaki satır ile Doğru chromedriver otomatik olarak indirilir.
from webdriver_manager.chrome import ChromeDriverManager

import time

# Tarayıcıyı başlat
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) #tarayıcıyı başlatır ve bana uygun driverı indirir.

# Google'a git
driver.get("https://www.google.com")    #google anasayfasını açar 
print("🔍 Google açıldı.")

# Çerez politikası kabul varsa (bazı bölgelerde çıkar)
try:
    kabul = driver.find_element(By.XPATH, '//button[contains(text(),"Kabul et")]')
    kabul.click()    #kabul et butonuna tıklar.
    print("✔️ Çerez bildirimi kapatıldı.")
except:
    pass  # Çıkmadıysa sorun değil

# Arama kutusunu bul
search_box = driver.find_element(By.NAME, "q")   #googleda name kısmı q olan yer arama kutusudur.(get metoduyla da böyle q ile çekiyoduk.)
search_box.send_keys("Selenium nedir?")  #klavye ile bunu yazar.
search_box.send_keys(Keys.RETURN)      #ve sonra entere tıklar bu keys.return ile
print("📤 'Selenium nedir?' araması yapıldı.")

# Sayfanın yüklenmesini bekle
time.sleep(3) #3 sn sayfanın yüklenmesini bekliyoruz.Web driver wait ile yapılırsa daha profesyonel olur.

# URL kontrolü
current_url = driver.current_url    #şuan içinde bulunan url bulunur.
print("🌐 Şu anki URL:", current_url)

if "search?q=Selenium+nedir" in current_url:   #eğer urlde selenium nedir yazıyorsa yani aranan şey varsa arama yapılabilmiştir demektir..
    print("✅ Arama başarılı.")
else:
    print("❌ Arama başarısız.")

# Arama sonuçları kontrolü
results = driver.find_elements(By.TAG_NAME, "h3") #googleda sonuçlar genelde h3 taginde yer alır (h3 boyutu htmlde olan.)yer alır.Sonuç var mı yok mu kontrolü  yapıyoruz.

if results:
    print("📄 İlk sonuç başlığı: ", results[0].text ) #eğer bir tane bile sonuç varsa onu terminale yazar.
else:
    print("❌ Hiçbir sonuç bulunamadı.")

# Tarayıcıyı açık tut
input("👁️ İncelemek için Enter'a bas, sonra pencere kapanacak...") #ben klavyeden enter tuşuna basana kadar tarayıcıdan çıkmaz.

# Tarayıcıyı kapat
driver.quit()
print("🚪 Tarayıcı kapatıldı.")


#dosya adını selenium.py yapma çünkü bunu kendi modülünü içe aktarmaya çalışırken benim dosyamın adı aynı olduğu için kendi modülü sanıyor.
#ve işlem başarısız olup hat veriyor.

#ekstra web driveri de indirmek gerekli.WebDriver, Selenium’un tarayıcıları kontrol etmesini sağlayan motorudur.
#Yani WebDriver sayesinde Python kodunla Chrome, Firefox gibi bir tarayıcıyı açıp, tıklayıp, yazı yazdırıp, gezdirebilirsin.
#web driver manager web driverı otomatik olarak indirir.