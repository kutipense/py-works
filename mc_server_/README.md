TCP/IP aracılığıyla ağ üzerinden çalışan kart okuma sistemi.
Özellikler:
    - Kart okuyucuların duruma göre yolladıkları mesajları sqlite3 üzerinden kayıt eder.
    - Oturum ve basma sayısını kontrol eder.
    - Herhangi bir çakışma olmasını engeller
    - Kayıtsız basılan kartların kayıt edilebilmesini sağlar
    - Yanlış girilen bilgi güncellenebilir
    - Kart değiştirilebilir ve basma verisi aktarılabilir.
    
    * 'kayit'
    * 'tel_sorgu'
    * 'uid_sorgu'
    * 'uid_artir'
    * 'oturum'
    gibi fonksiyonların yanına ";" ile ayrılmış veriler eklenebilir.
    Örnek:
        kayit;1;2;3;4;5;6;7 # telefon, isim, mail, okul, bolum, sinif, uid #
        tel_sorgu;111111111 # telefon
        uid_sorgu;FFFFFFFF # uid
        uid_artir;FFFFFFFF # uid
        oturum # ekleme yok
