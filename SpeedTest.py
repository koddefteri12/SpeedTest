import sys
import os

# PyInstaller --noconsole modunda sys.stdout 'None' döner. 
# Bu da kütüphanelerin çökmesine neden olur. Aşağıdaki blok bunu engeller.
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

import tkinter as tk
from tkinter.font import Font
from datetime import datetime
import socket
import speedtest
import time
import sqlite3 as sql


bugün = datetime.now()
version = "v0.0.1"


class veritabanı():
    def kaydet(isim,ping,download,upload,ülke,şehir,sponsor,tarih,version):

        conn = sql.connect("hız_ölçer.db")
        cursor = conn.cursor()
        #isim,ping,download,upload,ülke,şehir,sponsor,tarih,version

        cursor.execute("""INSERT INTO kayıtlar(isim,ping,download,upload,ülke,şehir,sponsor,tarih,version) VALUES (?,?,?,?,?,?,?,?,?)""",(isim,ping,download,upload,ülke,şehir,sponsor,tarih,version))

        conn.commit()
        conn.close()
        


def detaylari_goster():
    root6 = tk.Toplevel()
    root6.title("Kayıtlar")
    root6.geometry("800x600+600+150")
    root6.configure(bg="#000000")
    root6.grab_set() # Diğer pencereleri kilitler

    # 1. Ana Frame (Kaydırma çubuğu ve metin alanını tutar)
    kaydirma_cercevesi = tk.Frame(root6, bg="#000000")
    kaydirma_cercevesi.pack(expand=True, fill="both", padx=10, pady=10)

    # 2. Scrollbar Oluştur
    scrollbar = tk.Scrollbar(kaydirma_cercevesi)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 3. Text Widget (Verilerin yazılacağı alan)
    # yscrollcommand ile Scrollbar'a bağlanıyor
    kayıtlar_text = tk.Text(
        kaydirma_cercevesi, 
        font=("Arial", 11), 
        bg="#000000", 
        fg="white", 
        yscrollcommand=scrollbar.set,
        borderwidth=0,
        padx=10,
        pady=10
    )
    kayıtlar_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 4. Scrollbar'ın kontrolünü Text widget'ına bağla
    scrollbar.config(command=kayıtlar_text.yview)

    # Veritabanı İşlemleri
    try:
        conn = sql.connect("hız_ölçer.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM kayıtlar")
        kayıtlar_verisi = cursor.fetchall()

        for kayıt in kayıtlar_verisi:
            # Verileri Text içine ekliyoruz
            satir = (f"👤 İsim: {kayıt[0]}\n"
                     f"⚡ Ping: {kayıt[1]} ms | ⬇️ Download: {kayıt[2]:.2f} Mbps | ⬆️ Upload: {kayıt[3]:.2f} Mbps\n"
                     f"🌍 Konum: {kayıt[4]} / {kayıt[5]} | 🏢 Sponsor: {kayıt[6]}\n"
                     f"📅 Tarih: {kayıt[7]} | 🛠️ Versiyon: {kayıt[8]}\n"
                     f"{'-'*60}\n\n")
            kayıtlar_text.insert(tk.END, satir)

        conn.close()
    except Exception as e:
        kayıtlar_text.insert(tk.END, f"Hata oluştu: {e}")

    # Yazmayı engellemek için (Sadece okuma modu)
    kayıtlar_text.config(state=tk.DISABLED)

# root6'yı çağırmak için bu fonksiyonu kullanabilirsin.
        

def geri_bildirim_fonksiyonu():
    root5 = tk.Toplevel()
    root5.title("Geri Bildirim GÖNDERİN")
    root5.geometry("700x600+700+250")
    root5.configure(bg="#000000")

    conn = sql.connect("hız_ölçer.db")
    cursor = conn.cursor()

    cursor.execute("SELECT geri_bildirim FROM geri_bildirim")
    geri_bildirim_verisi = cursor.fetchone()[0]

    geri_bildirim_label = tk.Label(root5, text=geri_bildirim_verisi, font=("Arial", 11), bg="#000000", fg="white", justify="left", wraplength=380)
    geri_bildirim_label.pack(pady=10, padx=10)

    conn.commit()
    conn.close()

def bilgi():
    root4 = tk.Toplevel()
    root4.title("Program Hakkında")
    root4.geometry("600x600+650+150")
    root4.configure(bg="#000000")

    try:
        conn = sql.connect("hız_ölçer.db")
        cursor = conn.cursor()
        cursor.execute("SELECT bilgi FROM bilgi")
        bilgi_verisi = cursor.fetchone()[0]
        
        bilgi_label = tk.Label(root4, text=bilgi_verisi, font=("Arial", 12), bg="#000000", fg="white", justify="left", wraplength=580)
        bilgi_label.pack(pady=10, padx=10)
    except Exception:
        hata = tk.Label(root4,text="Veritabanında ilgili metin bulunamadı\nLütfen veritabanını indirin...",font=("Arial",10),fg="#FA7900",bg="#000000").pack()
    else:
        conn.commit()
        conn.close()


class hız_ölç:
    def internet_baglantisi_var_mi():
        try:
            # Google DNS sunucusuna bağlanmayı dene
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except (socket.timeout, socket.error):
            return False

        # Bağlantı kontrolü
        if not internet_baglantisi_var_mi():
            root2 = tk.Toplevel()
            root2.title("Hata")
            root2.geometry("400x200+700+300")
            root2.configure(bg="#ff0000")
            hata_mesajı = tk.Label(root2, text="❌ İnternet bağlantısı yok!", font=("Arial", 16), bg="#ff0000", fg="white")
            hata_mesajı.pack(pady=50)
            root2.grab_set()
            root2.lift()
            root2.focus()

    def hız_testi():
        root3 = tk.Toplevel()
        root3.title("Hız Testi raporu")
        root3.geometry("500x500+700+200")
        root3.configure(bg="#000000")

        try:
            st = speedtest.Speedtest()
            #Otomatik en yakın server seçimi
            st.get_best_server()



            #ping testi
            ping = st.results.ping
            ping_label = tk.Label(root3, text=f"Ping: {ping} ms", font=("Arial", 14), bg="#000000", fg="#FA7900")
            ping_label.place(x=10,y=10)


            #Download testi
            download = st.download()
            download_mbps = download / 1_000_000  # bit / 1.000.000 = Mbps
            download_label = tk.Label(root3, text=f"Download Hızı: {download_mbps:.2f} Mbps", font=("Arial", 14), bg="black", fg="#FA7900")
            download_label.place(x=10,y=40)


            #upload ölçümü
            upload = st.upload()
            upload_mbps = upload / 1_000_000
            upload_label = tk.Label(root3, text=f"Upload Hızı: {upload_mbps:.2f} Mbps", font=("Arial", 14), bg="black", fg="#FA7900")
            upload_label.place(x=10,y=70)

            root.grab_set()

            ülke = st.results.server["country"]
            ülke_label = tk.Label(root3, text=f"Ülke: {ülke}", font=("Arial", 14), bg="black", fg="#FA7900")
            ülke_label.place(x=10,y=100)

            şehir = st.results.server["name"]
            şehir_label = tk.Label(root3, text=f"Şehir: {şehir}", font=("Arial", 14), bg="black", fg="#FA7900")
            şehir_label.place(x=10,y=130)

            sponsor = st.results.server["sponsor"]
            sponsor_label = tk.Label(root3, text=f"Sponsor: {sponsor}", font=("Arial", 14), bg="black", fg="#FA7900")
            sponsor_label.place(x=10,y=160)

            isim = tk.Entry(root3, width=20, font=("Arial", 14))
            isim.place(x=10,y=230)
            isim_label = tk.Label(root3, text="İsminiz (Opsiyonel):", font=("Arial", 14), bg="black", fg="#FA7900")
            isim_label.place(x=10,y=200)

            def kaydet2():
                isim_degeri = isim.get()
                if isim_degeri.strip() == "":
                    isim_degeri = "İsimsiz"
                veritabanı.kaydet(isim_degeri,ping,download_mbps,upload_mbps,ülke,şehir,sponsor,bugün,version)
                başarı_mesajı = tk.Label(root3, text="✅ Sonuç başarıyla kaydedildi!", font=("Arial", 14), bg="black", fg="#00FF00")
                başarı_mesajı.place(x=10,y=310)
            
            kaydet_buton = tk.Button(root3, text="Sonucu Kaydet", font=("Arial", 14), bg="#4f4f4f", fg="white", activebackground="#3a3a3a", command=kaydet2).place(x=10,y=270)

        except Exception:
            hata = tk.Label(root3,text="İnternet bağlantısı bulunamadı",fg="#FA7900",bg="black",font=("Arial",13)).pack()
        else:
            pass

root = tk.Tk()
root.title("Hız ölçer")
root.geometry("900x700+490+100")
root.configure(bg="#0000cd")
root.minsize(900,700)
root.maxsize(900,700)





#Kontrol
def internet_baglantisi_var_mi():
    try:
        # Google DNS sunucusuna bağlanmayı dene
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except (socket.timeout, socket.error):
        return False

      # Bağlantı kontrolü
if not internet_baglantisi_var_mi():
    root2 = tk.Toplevel()
    root2.title("Hata")
    root2.geometry("400x200+700+300")
    root2.configure(bg="#ff0000")
    hata_mesajı = tk.Label(root2, text="❌ İnternet bağlantısı yok!", font=("Arial", 16), bg="#ff0000", fg="white")
    hata_mesajı.pack(pady=50)
    root2.grab_set()
    root2.lift()
    root2.focus()


label = tk.Label(root, text="", font=("Arial", 12), bg="#0000cd", fg="white")
label.place(x=750, y=60)

def guncelle_saat():
    label.config(text=datetime.now().strftime("%H:%M:%S"))
    root.after(1000, guncelle_saat)  # Her 1 saniyede çağır


saat = tk.Label(root, text=guncelle_saat , font=("Arial", 12), bg="#0000cd", fg="white").place(x=750, y=60)

çizgi1 =  tk.Label(root, text="", font=("Arial", 24), bg="#1c0f45", fg="white").place(x=0,y=0 ,width=6000,height=100)

başlık_font = Font(family="Verdana", size=24, weight="bold", slant="italic", underline=True)

başlık1 = tk.Label(root, text="Hız Ölçer", font=başlık_font, bg="#1c0f45", fg="white").place(x=380,y=20)

küçük_başlık = tk.Label(root, text="Ping testi, Download testi, Upload testi...", font=("Arial", 14), bg="#1c0f45", fg="white").place(x=300,y=70)

tarih = tk.Label(root, text=bugün.strftime("%d.%m.%Y"), font=("bold", 12), bg="#1c0f45", fg="white").place(x=750,y=20)

versiyon = tk.Label(root, text="v0.0.1", font=("bold", 12), bg="#1c0f45", fg="white").place(x=750,y=40)

önemli = tk.Label(root,text="*Bu program tamamen ücretsiz ve açık kaynaktır...",bg="#0000cd",fg="red",font=("arial",10)).place(x=305,y=110)

Hızını_ölç = tk.Button(root,command=hız_ölç.hız_testi, text="Hızını Ölç", font=("Arial", 16), bg="#4f4f4f", fg="white",activebackground="#3a3a3a").place(x=355,y=150,width=200,height=50)

çizgi2 = tk.Label(root, text="" , font=("Arial", 24), bg="#ffc125", fg="white").place(x=0,y=215 ,width=6000,height=50)

kayıtlar = tk.Button(root,command=detaylari_goster, text="Kayıtlar", font=("Arial", 20), bg="#ffc125", fg="white").place(x=20,y=220)

geri_bildirim = tk.Button(root,command=geri_bildirim_fonksiyonu, text="Geri Bildirim", font=("Arial", 20), bg="#ffc125", fg="white").place(x=370,y=220)

bilgi = tk.Button(root,command=bilgi, text="Bilgi", font=("Arial", 20), bg="#ffc125", fg="white").place(x=720,y=220)



çizgi3 = tk.Label(root,text="",fg="Black").place(x=0,y=375,width=6000,height=5)





root.mainloop()