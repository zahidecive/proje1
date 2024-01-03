from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os

resim_klasoru = "dizi"
resimler = ["theoriginals.jpg","hımym.jpg","lupin.jpg","winniethepooh.jpg","ayla.jpg","yesilyol.jpg"]


def goster_resmi(index):
    global current_index, resimler, resim_klasoru
    current_index = index

    img_path = os.path.join(resim_klasoru, resimler[current_index])
    img = Image.open(img_path)
    img = img.resize((300, 400))
    img_tk = ImageTk.PhotoImage(img)

    resim_buton.configure(image=img_tk)
    resim_buton.image = img_tk

    goster_kisa_ozet()


def goster_sonraki_resim(index):
    global current_index, resimler
    current_index += index
    if current_index < 0:
        current_index = len(resimler) - 1
    elif current_index >= len(resimler):
        current_index = 0

    goster_resmi(current_index)


def goster_kisa_ozet():
    kisa_ozet_path = os.path.join("kısaozet.txt")
    with open(kisa_ozet_path, "r", encoding="utf-8") as file:
        kisa_ozetler = file.readlines()
        if current_index < len(kisa_ozetler):
            kisa_ozet = kisa_ozetler[current_index].strip()
            ad_ve_ozet_kutucuk.config(state=NORMAL)
            ad_ve_ozet_kutucuk.delete("1.0", END)
            ad_ve_ozet_kutucuk.insert(END, f"Resim Adı: {resimler[current_index]}\nKısa Özet: {kisa_ozet}")
            ad_ve_ozet_kutucuk.config(state=DISABLED)


def listele_resimler():
    listele_pencere = Toplevel(pencere)
    listele_pencere.title("Resim Listesi")

    listbox = Listbox(listele_pencere, selectmode=SINGLE, font=("Helvetica", 12), bg="#9fb6cd")
    listbox.pack(padx=10, pady=10)

    for i, resim in enumerate(resimler):
        listbox.insert(END, f"{i + 1}. {resim}")

    def secilen_resmi_goster():
        selected_index = listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            goster_resmi(selected_index)

    secili_goster_buton = Button(listele_pencere, text="Seçileni Göster", font=("Helvetica", 12, "bold"),
                                 command=secilen_resmi_goster, bg="#708090", fg="white")
    secili_goster_buton.pack(pady=10)


def dosya_sec():
    global resim_klasoru, resimler
    resim_klasoru = filedialog.askdirectory()
    resimler = [dosya for dosya in os.listdir(resim_klasoru) if os.path.isfile(os.path.join(resim_klasoru, dosya))]
    goster_resmi(0)


pencere = Tk()
pencere.geometry("800x500")
pencere.title("Resim Seçici")
pencere.configure(background="#cdb7b5")

ortalama_frame = Frame(pencere, bg="#8b6969")
ortalama_frame.pack(side=LEFT, padx=10, pady=10)

sag_frame = Frame(pencere, bg="#b3e0ff")
sag_frame.pack(side=RIGHT, padx=10, pady=10)

current_index = 0

img_path = os.path.join(resim_klasoru, resimler[current_index])
img = Image.open(img_path)
img = img.resize((300, 400))
img_tk = ImageTk.PhotoImage(img)

resim_buton = Button(ortalama_frame, image=img_tk, command=goster_kisa_ozet, borderwidth=0)
resim_buton.image = img_tk
resim_buton.pack(pady=10)

saga_tus = Button(ortalama_frame, text="Sonraki", font=("Helvetica", 12, "bold"),
                  command=lambda: goster_sonraki_resim(1), bg="#99c2ff", fg="white")
saga_tus.pack(side=RIGHT, padx=5)

sola_tus = Button(ortalama_frame, text="Önceki", font=("Helvetica", 12, "bold"),
                  command=lambda: goster_sonraki_resim(-1), bg="#99c2ff", fg="white")
sola_tus.pack(side=LEFT, padx=5)

ad_ve_ozet_kutucuk = Text(sag_frame, font=("Helvetica", 12), height=8, width=30, wrap=WORD, bg="#e6e6e6",
                          state=DISABLED)
ad_ve_ozet_kutucuk.pack(pady=10, padx=10)

listele_tus = Button(ortalama_frame, text="Listele", font=("Helvetica", 12, "bold"), command=listele_resimler,
                     bg="#99c2ff", fg="white")
listele_tus.pack(pady=10)

dosya_sec_tus = Button(ortalama_frame, text="Resim Klasörünü Seç", font=("Helvetica", 12, "bold"), command=dosya_sec,
                       bg="#99c2ff", fg="white")
dosya_sec_tus.pack(pady=10)

pencere.mainloop()
