import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Film:
    def __init__(self, title, description, image_filename):
        self.title = title
        self.description = description
        self.image_filename = image_filename

class FilmListesi:
    def __init__(self, resim_klasoru, resimler, aciklamalar):
        self.resim_klasoru = resim_klasoru
        self.resimler = resimler
        self.aciklamalar = aciklamalar
        self.filmler = [
            Film("The Originals", aciklamalar[0], "theoriginals.jpg"),
            Film("How I Met Your Mother", aciklamalar[1], "hımym.jpg"),
            Film("Lupin", aciklamalar[2], "lupin.jpg"),
            Film("Winnie the Pooh", aciklamalar[3], "winniethepooh.jpg"),
            Film("Ayla", aciklamalar[4], "ayla.jpg"),
            Film("Yeşil Yol", aciklamalar[5], "yesilyol.jpg"),
        ]

class Kullanici:
    def __init__(self):
        self.giris_yapildi = False
        self.kullanici_adi = ""

    def giris_yap(self, kullanici_adi):
        if not kullanici_adi:
            messagebox.showerror("Hata", "Kullanıcı adı boş olamaz. Lütfen bir kullanıcı adı girin.")
            return False

        # Burada giriş yapma işlemleri gerçekleştirilebilir.
        # Ancak bu örnek uygulamada sadece giriş yaptığımızı varsayalım.
        self.giris_yapildi = True
        self.kullanici_adi = kullanici_adi  # Kullanıcı adını sakla
        messagebox.showinfo("Giriş Yapıldı", f"Hoşgeldin, {kullanici_adi}!")
        return True

class GUI:
    def __init__(self, root, resim_klasoru, resimler, aciklamalar):
        self.root = root
        self.root.title("Film Listesi Uygulaması")

        self.kullanici = Kullanici()
        self.filmler = FilmListesi(resim_klasoru, resimler, aciklamalar)

        # Create frames for better organization
        self.login_frame = tk.Frame(root, pady=10)
        self.login_frame.pack()

        self.list_frame = tk.Frame(root)

        self.giris_label = tk.Label(self.login_frame, text="Kullanıcı Adı:", font=("Helvetica", 12))
        self.giris_label.grid(row=0, column=0, padx=10)

        self.giris_entry = tk.Entry(self.login_frame, font=("Helvetica", 12))
        self.giris_entry.grid(row=0, column=1, padx=10)

        self.giris_button = tk.Button(self.login_frame, text="Giriş Yap", command=self.giris_yap, font=("Helvetica", 12))
        self.giris_button.grid(row=0, column=2, padx=10)

        self.liste_button = tk.Button(self.list_frame, text="Listele", command=self.liste_goster, state=tk.DISABLED, font=("Helvetica", 12))
        self.liste_button.pack(pady=10)

    def giris_yap(self):
        kullanici_adi = self.giris_entry.get().strip()
        if self.kullanici.giris_yap(kullanici_adi):
            self.giris_button.config(state=tk.DISABLED)
            self.liste_button.config(state=tk.NORMAL)
            self.list_frame.pack()


    def liste_goster(self):
        liste_penceresi = tk.Toplevel(self.root)
        liste_penceresi.title("Film Listesi")

        self.listebox = tk.Listbox(liste_penceresi, font=("Helvetica", 12))
        for film in self.filmler.filmler:
            self.listebox.insert(tk.END, film.title)
        self.listebox.pack()

        self.listebox.bind("<ButtonRelease-1>", self.film_detay)

    def film_detay(self, event):
        secilen_index = self.listebox.curselection()
        if secilen_index:
            secilen_index = secilen_index[0]
            secilen_film = self.filmler.filmler[secilen_index]

            detay_penceresi = tk.Toplevel(self.root)
            detay_penceresi.title(secilen_film.title + " Detayları")

            resim_yolu = os.path.join(self.filmler.resim_klasoru, secilen_film.image_filename)
            img = Image.open(resim_yolu)
            img = img.resize((700, 500),)  # Resmi boyutlandırabilirsiniz
            resim = ImageTk.PhotoImage(img)

            resim_etiket = tk.Label(detay_penceresi, image=resim)
            resim_etiket.image = resim
            resim_etiket.grid(row=1, column=0, columnspan=2)

            aciklama_text = tk.Text(detay_penceresi, height=10, width=70, font=("Helvetica", 12))
            aciklama_text.insert(tk.END, secilen_film.description)
            aciklama_text.config(state=tk.DISABLED)
            aciklama_text.grid(row=2, column=0, columnspan=2, pady=10)

# Ana uygulama döngüsü
if __name__ == "__main__":
    resim_klasoru = "dizi"
    resimler = ["theoriginals.jpg", "hımym.jpg", "lupin.jpg", "winniethepooh.jpg", "ayla.jpg", "yesilyol.jpg"]

    # Açıklamaları kısaozet.txt dosyasından okuma
    aciklamalar = []
    with open("kısaozet.txt", "r", encoding="utf-8") as file:
        aciklamalar = [line.strip() for line in file.readlines()]

    root = tk.Tk()
    gui = GUI(root, resim_klasoru, resimler, aciklamalar)
    root.mainloop()

