import sqlite3 as sql

conn = sql.connect("hız_ölçer.db")
cursor = conn.cursor()

#Kayıtlar tablosu
cursor.execute("""CREATE TABLE IF NOT EXISTS kayıtlar(
                    isim TEXT,
                    ping REAL,
                    download REAL,
                    upload REAL,
                    ülke TEXT,
                    şehir TEXT,
                    sponsor TEXT,
                    tarih TEXT,
                    version TEXT
               )""")

#Kontrol tablosu
cursor.execute("""CREATE TABLE IF NOT EXISTS kontrol(durum TEXT)""")

#Kontrol tablosu içine başlangıç değeri ekleme
cursor.execute("""INSERT INTO kontrol(durum) VALUES('yes')""")


#Bilgi tablosu
cursor.execute("""CREATE TABLE IF NOT EXISTS bilgi(
                    bilgi TEXT
               )""")

bilgiler = """
Not: Olabildiğince sade şekilde yazmaya çalıştım.Anlayışınız için teşekkürler!

Program Hakkında:

KULLANDIĞIM TEKLONOLOJİLER:
-Python
     - Tkinter (GUI Kütüphanesi)
     - Sqlite3 (Veritabanı)
     - Speedtest-cli (Hız testi için)
     - Datetime (Tarih ve saat için)
     - Socket (İnternet bağlantısı kontrolü için)
     - PyInstaller (Programı .exe yapma için)








Program tamamen ücretsizdir ve açık kaynak kodludur.
Bu programı kullanarak hız testi yapabilir ve sonuçlarınızı kaydedebilirsiniz.
Düzenleme yapabilir ve kendi ihtiyaçlarınıza göre uyarlayabilirsiniz.
Katkıda bulunmak isterseniz, lütfen GitHub sayfasını ziyaret edin.
Github:https://github.com/koddefteri12

@koddefteri12
"""

cursor.execute("INSERT INTO bilgi(bilgi) VALUES(?)", (bilgiler,))

cursor.execute("""CREATE TABLE IF NOT EXISTS geri_bildirim(
                    geri_bildirim TEXT
               )""")

geri_bildirim_metni = """
GERİ BİLDİRİMLER İÇİN ONLİNE BİR BÖLÜM VEYA FORUM BÖLÜMÜ YAZAMADIM.

FAKAT BİR SONRAKİ VERSİONDA YAPMAK İÇİN GELİŞTİRME YAPMAYA DEVAM EDİYORUM.

LÜTFEN GERİ BİLDİRİMLERİNİZİ AŞAĞIDAKİ E-POSTA ADRESİNE GÖNDERİNİZ:

-------------------------------------------
e posta: akkayaaliimran12@gmail.com
-------------------------------------------
github: @koddefteri12
-------------------------------------------
GERİ BİLDİRİMLERİNİZ BENİM İÇİN ÇOK DEĞERLİDİR.

ANLAYIŞINIZ İÇİN TEŞEKKÜR EDERİM.
"""

cursor.execute("INSERT INTO geri_bildirim(geri_bildirim) VALUES(?)", (geri_bildirim_metni,))

#ID sayaç tablosu
#İPTAL EDİLDİ KOD YAPISI GEREĞİ SİLİNMEDİ
cursor.execute("""CREATE TABLE IF NOT EXISTS ıd_sayar(
                    id INTEGER
               )""")

cursor.execute("""INSERT INTO ıd_sayar(id) VALUES (1)""")

import tkinter as tk
from tkinter import ttk
import time

class LoadingScreen:
    def __init__(self, root, app_name="Uygulama"):
        self.root = root
        self.root.title(f"Yükleniyor — {app_name}")
        self.root.configure(bg="#1f2937")
        self.root.resizable(False, False)

        # Pencere boyutu ve ortalama
        width, height = 520, 260
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")

        # Ana çerçeve
        frame = tk.Frame(root, bg="#111827")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=480, height=200)

        # Başlık
        title = tk.Label(frame, text=app_name, font=("Segoe UI", 18, "bold"), bg="#111827", fg="#F9FAFB")
        title.pack(pady=(14, 6))

        # Alt açıklama
        desc = tk.Label(frame, text="Hazırlanıyor...", font=("Segoe UI", 10), bg="#111827", fg="#9CA3AF")
        desc.pack()

        # İlerleme çubuğu
        self.progress = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=360, mode='determinate')
        self.progress.pack(pady=(18, 6))
        self.progress['maximum'] = 100

        # Yüzde etiketi
        self.percent_label = tk.Label(frame, text="0%", font=("Segoe UI", 10, "bold"), bg="#111827", fg="#F9FAFB")
        self.percent_label.pack()

        # Animasyon için
        self.dot_count = 0
        self.loading_text = desc

        # Stil (opsiyonel) - ttk tema
        try:
            style = ttk.Style()
            style.theme_use('clam')
            style.configure("TProgressbar", troughcolor='#0f1720', background='#3B82F6', thickness=10)
        except Exception:
            pass

    def start(self, duration=3000):
        steps = 100
        delay = duration // steps
        self._update(0, steps, delay)
        self._animate_dots()
        self.root.mainloop()

    def _update(self, i, steps, delay):
        if i > steps:
            self.loading_text.config(text="Tamamlandı", fg="#10B981")
            self.percent_label.config(text="100%")
            self.progress['value'] = 100
            # Kısa bir gecikmeden sonra pencereyi kapat
            self.root.after(800, self.root.destroy)
            return
        value = int(i / steps * 100)
        self.progress['value'] = value
        self.percent_label.config(text=f"{value}%")
        self.root.after(delay, lambda: self._update(i + 1, steps, delay))

    def _animate_dots(self):
        self.dot_count = (self.dot_count + 1) % 4
        dots = '.' * self.dot_count
        self.loading_text.config(text=f"Hazırlanıyor{dots}")
        self.root.after(400, self._animate_dots)


if __name__ == '__main__':
    root = tk.Tk()
    app = LoadingScreen(root, app_name="SpeedTest Veritabanı Oluşumu")
    # duration milisaniye cinsinden; örn 3000 = 3s
    app.start(duration=3000)


conn.commit()
conn.close()