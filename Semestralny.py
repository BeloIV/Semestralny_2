import hashlib
import os
import shutil
import tkinter
import sqlite3
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class Grafik:
    def __init__(self):
        """
        This function initializes a tkinter window and canvas for a program called "BeloCar".
        """

        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(height=905, width=705)
        self.root.title("BeloCar")
        self.canvas.pack()

        self.vytvor_prostredie()
        self.id_od = 0
        self.zobrazene = False

    def klik(self, event):
        """
        The function handles mouse clicks and performs different actions based on the location of the click.
        """

        if 0 < event.x < 60 and 0 < event.y < 50 and self.nic_sa_nedeje is True:

            if self.zobrazene is False:
                self.vytvor_moznosti_zoradenia()
            else:
                self.vymaz_moznosti_zoradenia(1)

        elif 650 < event.x < 710 and 0 < event.y < 50 and self.nic_sa_nedeje is True:
            self.ukaz_profil()
        else:
            self.zisti_kde_klikol(event)

    def ukaz_profil(self):
        """
        This function displays the user profile page with options for logging in, registering, logging
        out, adding a car to the database, and deleting products.
        """
        try:
            self.vymaz_dakujeme()
        except:
            pass
        if self.nic_sa_nedeje is True:
            self.vymaz_podrobnu_ponuku()

            self.vymaz_ponuku()
            self.vymaz_filtre()
            self.nic_sa_nedeje = False
            self.zoz_profil = []
            self.zoz_profil_but = []
            x = Image.open(r"Images/back.png")
            xx = ImageTk.PhotoImage(x)
            self.zoz_profil.append(xx)
            if CarRent.daj_prihlasenost(self)[0] is False:
                self.zoz_profil.append(
                    self.canvas.create_text(
                        350, 70, text="Prihlásenie", font="Arial 15"
                    )
                )
                self.zoz_profil.append(self.canvas.create_text(260, 100, text="Meno :"))
                meno = tkinter.Entry(width=15)
                meno.place_configure(x=280, y=85)
                self.zoz_profil_but.append(meno)
                self.zoz_profil.append(
                    self.canvas.create_text(260, 125, text="Heslo :")
                )
                heslo = tkinter.Entry(width=15, show="*")
                heslo.place_configure(x=280, y=110)
                self.zoz_profil_but.append(heslo)
                potvrd = tkinter.Button(
                    text="Potvrdiť", command=self.ziskaj_prihlasenie
                )
                potvrd.place_configure(x=310, y=140)
                self.zoz_profil_but.append(potvrd)
                registuj = tkinter.Button(
                    text="Registrácia", command=self.registracia_formular
                )
                registuj.place_configure(x=200, y=55)
                self.zoz_profil_but.append(registuj)

            else:
                registuj = tkinter.Button(
                    text="Odlásiť", command=lambda: CarRent.odhlas(self)
                )
                registuj.place_configure(x=600, y=60)
                self.zoz_profil_but.append(registuj)
                self.moje_objednavky()

            spat = tkinter.Button(
                image=xx,
                borderwidth=0,
                border=0,
                command=self.vymaz_profil,
                background="black",
            )
            spat.place_configure(x=5, y=5)
            self.zoz_profil_but.append(spat)
            if CarRent.daj_prihlasenost(self)[1] == 1:
                formular_button = tkinter.Button(
                    text="Pridaj auto do datábazi", command=self.formular_na_vlozenie
                )
                formular_button.place_configure(x=410, y=60)
                self.zoz_profil_but.append(formular_button)
                vymaz_produkty = tkinter.Button(
                    text="Vymaž produkty", command=self.mazanie_aut
                )
                vymaz_produkty.place_configure(x=280, y=60)
                self.zoz_profil_but.append(vymaz_produkty)

    def mazanie_aut(self):
        """
        This function creates a GUI interface for deleting cars from a car rental system.
        """
        x = Image.open(r"Images/back.png")
        xx = ImageTk.PhotoImage(x)
        self.zoz_profil.append(xx)
        self.zoz_vymat_auto = []
        self.vymaz_profil(1)
        self.zoz_profil.append(self.canvas.create_rectangle(100, 100, 200, 130))
        produkty = CarRent.daj_vsetky_auta(self)
        self.zoz_profil.append(
            self.canvas.create_text(150, 115, text="Id", font="Arial 15")
        )
        self.zoz_profil.append(self.canvas.create_rectangle(200, 100, 400, 130))
        self.zoz_profil.append(
            self.canvas.create_text(300, 115, text="Názov", font="Arial 15")
        )
        self.zoz_profil.append(self.canvas.create_rectangle(400, 100, 500, 130))
        self.zoz_profil.append(
            self.canvas.create_text(450, 115, text="Km", font="Arial 15")
        )
        self.zoz_profil.append(self.canvas.create_rectangle(500, 100, 600, 130))
        self.zoz_profil.append(
            self.canvas.create_text(550, 115, text="Rok", font="Arial 15")
        )
        x = 100
        y = 130

        for cis, i in enumerate(produkty):
            var = tkinter.IntVar()
            check = tkinter.Checkbutton(variable=var)
            check.place_configure(x=x - 35, y=y + 5)
            self.zoz_vymat_auto.append(var)
            self.zoz_profil_but.append(check)
            id = i[0]
            nazov = i[1]
            km = i[3]
            rok = i[4]
            self.zoz_profil.append(
                self.canvas.create_text(x + 50, y + 15, text=id, font="Arial 15")
            )
            self.zoz_profil.append(self.canvas.create_rectangle(x, y, x + 100, y + 30))
            x += 100
            if len(nazov) > 24:
                nazov = nazov[:24] + "..."
            self.zoz_profil.append(
                self.canvas.create_text(x + 100, y + 15, text=nazov, font="Arial 15")
            )
            self.zoz_profil.append(self.canvas.create_rectangle(x, y, x + 200, y + 30))
            x += 200
            self.zoz_profil.append(
                self.canvas.create_text(x + 50, y + 15, text=km, font="Arial 15")
            )
            self.zoz_profil.append(self.canvas.create_rectangle(x, y, x + 100, y + 30))
            x += 100
            self.zoz_profil.append(
                self.canvas.create_text(x + 50, y + 15, text=rok, font="Arial 15")
            )
            self.zoz_profil.append(self.canvas.create_rectangle(x, y, x + 100, y + 30))
            y += 30

            x = 100
        but = tkinter.Button(
            text="Vymazať označené", command=lambda: self.zisti_čo_vymazat(produkty)
        )
        but.place_configure(x=300, y=y + 20)
        self.zoz_profil_but.append(but)
        spat = tkinter.Button(
            image=xx,
            borderwidth=0,
            border=0,
            command=self.vymaz_profil,
            background="black",
        )
        spat.place_configure(x=5, y=5)
        self.zoz_profil_but.append(spat)

    def zisti_čo_vymazat(self, udaje):
        """
        This function checks which items to delete from a list based on user input and then calls another
        function to delete them from a database.

        """
        for cis, i in enumerate(self.zoz_vymat_auto):

            x = i.get()
            if x == 1:
                CarRent.vymaz_z_databazy(self, udaje[cis][0], udaje[cis][-3])

    def moje_objednavky(self):
        """
        This function creates a list of the user's orders with checkboxes to allow for cancellation.
        """
        self.nic_sa_nedeje = False
        self.zoz_moje_obj_chceck = []
        udaje = CarRent.daj_objedavky(self)
        self.zoz_profil.append(self.canvas.create_rectangle(100, 100, 250, 130))
        self.zoz_profil.append(
            self.canvas.create_text(175, 115, text="Názov auta", font="Arial 15")
        )
        self.zoz_profil.append(self.canvas.create_rectangle(250, 100, 350, 130))
        self.zoz_profil.append(
            self.canvas.create_text(300, 115, text="Datum od", font="Arial 15")
        )
        self.zoz_profil.append(self.canvas.create_rectangle(350, 100, 450, 130))
        self.zoz_profil.append(
            self.canvas.create_text(400, 115, text="Datum do", font="Arial 15")
        )
        self.zoz_profil.append(self.canvas.create_rectangle(450, 100, 550, 130))
        self.zoz_profil.append(
            self.canvas.create_text(500, 115, text="Cena", font="Arial 15")
        )

        x = 100
        y = 130
        for cis, i in enumerate(udaje):
            nazov_auta = CarRent.daj_nazov_auta(self, i[1])
            if len(nazov_auta) > 15:
                nazov_auta = nazov_auta[:18] + "..."
            self.zoz_profil.append(self.canvas.create_rectangle(x, y, x + 150, y + 30))
            self.zoz_profil.append(
                self.canvas.create_text(
                    x + 75,
                    y + 15,
                    text=nazov_auta,
                )
            )
            var = tkinter.IntVar()
            check = tkinter.Checkbutton(variable=var)
            check.place_configure(x=x - 35, y=y)
            self.zoz_moje_obj_chceck.append(var)
            self.zoz_profil_but.append(check)
            x += 150
            datum_od = i[3]
            datum_do = i[4]
            cena = i[5]
            for i in datum_od, datum_do, cena:
                self.zoz_profil.append(
                    self.canvas.create_rectangle(x, y, x + 100, y + 30)
                )
                self.zoz_profil.append(
                    self.canvas.create_text(
                        x + 50,
                        y + 15,
                        text=i,
                    )
                )
                x += 100
            y += 30
            x = 100
        zrusit = tkinter.Button(
            text="Zrušiť zaškrtnuté objednavky",
            command=lambda: self.nacitaj_zrusenie(udaje),
        )
        zrusit.place_configure(x=240, y=y + 20)
        self.zoz_profil_but.append(zrusit)

    def nacitaj_zrusenie(self, udaje):
        """
        This function deletes a car rental order based on the selected checkboxes.


        """

        for cis, i in enumerate(self.zoz_moje_obj_chceck):
            x = i.get()
            if x == 1:
                CarRent.vymaz_objednavku(self, udaje[cis][0], udaje[cis][1])

    def registracia_formular(self):
        """
        This function creates a registration form with text fields and a button for submission.
        """

        self.vymaz_profil(1)
        self.zoz_registracia = []
        self.zoz_registracia_but = []
        self.nic_sa_nedeje = False

        zoz = ["Meno", "Mail", "Heslo", "Adresa"]
        x = 260
        y = 100
        self.zoz_registracia.append(
            self.canvas.create_text(350, 70, text="Registracia", font="Arial 15")
        )
        for i in zoz:
            self.zoz_registracia.append(
                self.canvas.create_text(x, y + 15, text=i + " :")
            )
            heslo = tkinter.Entry(
                width=15,
            )
            heslo.place_configure(x=x + 20, y=y)
            self.zoz_registracia_but.append(heslo)
            y += 25

        potvrd = tkinter.Button(text="Potvrdiť", command=self.skontroluj_registraciu)
        potvrd.place_configure(x=310, y=210)
        self.zoz_registracia_but.append(potvrd)
        x = Image.open(r"Images/back.png")
        xx = ImageTk.PhotoImage(x)
        self.zoz_registracia.append(xx)
        spat = tkinter.Button(
            image=xx,
            borderwidth=0,
            border=0,
            command=self.vymaz_registraciu,
            background="black",
        )
        spat.place_configure(x=5, y=5)

        self.zoz_registracia_but.append(spat)

    def vymaz_registraciu(self):
        """
        The function deletes registration information and displays the user's profile.
        """

        try:
            for i in self.zoz_registracia:
                self.canvas.delete(i)
        except:
            pass
        try:
            for i in self.zoz_registracia_but:
                i.place_forget()
        except:
            pass
        self.nic_sa_nedeje = True
        self.ukaz_profil()

    def skontroluj_registraciu(self):
        x = self.zoz_registracia_but[:4]
        xx = []

        for i in x:
            xx.append(i.get())
        if len(xx[0]) < 3:
            pop_up = self.canvas.create_text(
                490, 115, text="Meno príliš krátke", fill="red"
            )
            self.canvas.update()
            self.canvas.after(1000)
            self.canvas.delete(pop_up)

        try:
            mail = xx[1]
            ind = mail.index("@")
            bodka = mail[ind:].index(".")
            if (
                "@" not in mail
                or "." not in mail[ind:]
                or len(mail[:ind]) < 5
                or len(mail[ind:]) < 5
                or len(mail[bodka + ind :]) < 2
            ):
                pop_up = self.canvas.create_text(
                    470, 140, text="Zlý format", fill="red"
                )
                self.canvas.update()
                self.canvas.after(1000)
                self.canvas.delete(pop_up)
        except:
            pop_up = self.canvas.create_text(470, 140, text="Zlý format", fill="red")
            self.canvas.update()
            self.canvas.after(1000)
            self.canvas.delete(pop_up)

        if len(xx[2]) < 5:
            pop_up = self.canvas.create_text(
                490, 165, text="Heslo príliš krátke", fill="red"
            )
            self.canvas.update()
            self.canvas.after(1000)
            self.canvas.delete(pop_up)
        elif len(xx[3]) < 5:
            pop_up = self.canvas.create_text(
                490, 190, text="Adresa príliš krátka", fill="red"
            )
            self.canvas.update()
            self.canvas.after(1000)
            self.canvas.delete(pop_up)
        else:
            CarRent.registruj(self, xx)

    def ziskaj_prihlasenie(self):
        """
        This function retrieves login information from a list of profile buttons and uses it to log in
        to a car rental system.
        """
        x = self.zoz_profil_but[:2]
        xx = []
        for i in x:
            xx.append(i.get())
        CarRent.prihlasienie(self, xx[0], xx[1])

    def zle_meno_heslo(self):
        """
        This function creates and displays a red text message on a canvas for one second, indicating that
        the username or password is incorrect.
        """
        x = self.canvas.create_text(
            350, 180, text="Zle meno alebo heslo :(", fill="red"
        )
        self.canvas.update()
        self.canvas.after(1000)
        self.canvas.delete(x)

    def vymaz_profil(self, ako=0):
        """
        The function "vymaz_profil" deletes profile information and returns to the main menu in a CarRent
        program.

        """
        self.nic_sa_nedeje = True
        try:
            for i in self.zoz_profil_but:
                i.place_forget()
        except:
            pass
        try:
            for i in self.zoz_profil:
                self.canvas.delete(i)
        except:
            pass

        if ako == 0:
            CarRent.spat_na_ponuku(self)

    def vymaz_filtre(self):
        """
        This function deletes filters and their corresponding buttons from a canvas.
        """
        try:
            for i in self.zoz_filtruj:
                self.canvas.delete(i)
            for i in self.zoz_filt_but:
                i.place_forget()
        except:
            pass

    def vytvor_filre(self):
        """
        The function creates a set of filters with corresponding labels and input fields, and a button to
        confirm the filters.
        """
        self.vymaz_filtre()
        self.zoz_filtruj = []
        self.zoz_filt_but = []
        self.zoz_filtruj.append(
            self.canvas.create_rectangle(5, 51, 700, 110, fill="black")
        )

        zoz = [
            "Značka",
            "Km od",
            "Km do",
            "Kw od",
            "Kw do",
            "Rok od",
            "Rok do",
        ]
        x1 = 42
        x2 = 20
        for i in zoz:
            self.zoz_filtruj.append(
                self.canvas.create_text(x1, 100, text=i, fill="white")
            )
            filt = tkinter.Entry()
            filt.place_configure(x=x2, y=60, width=60)
            self.zoz_filt_but.append(filt)
            x1 += 67
            x2 += 65
        filt = tkinter.Button(text="Potvrdiť", command=self.nacitaj_filter)
        filt.place_configure(x=x2, y=60, width=60)
        self.zoz_filt_but.append(filt)

    def nacitaj_filter(self):
        """
        The function "nacitaj_filter" appends the values of a list of tkinter buttons to a new list and
        passes it as an argument to the "filtruj" method of the "CarRent" class.
        """
        zoz = []
        for i in self.zoz_filt_but:
            try:
                zoz.append(i.get())
            except:
                pass
        CarRent.filtruj(self, zoz)

    def vytvor_moznosti_zoradenia(self):
        """
        This function creates a list of sorting options as buttons in a tkinter GUI.
        """

        try:
            self.vymaz_moznosti_zoradenia()
        except:
            pass
        self.zobrazene = True
        self.zoz_sortuj = []
        self.zoz_sor_but = []
        self.zoz_sortuj.append(
            self.canvas.create_rectangle(20, 40, 220, 290, fill="darkgray")
        )

        self.sortuj_button = tkinter.Button(
            text="Najnovšie (pridanie)",
            command=lambda: CarRent.uprav_zoradenie(self, "najnovšie"),
            borderwidth=0,
            border=0,
        )
        self.sortuj_button.place_configure(x=42, y=50)
        self.zoz_sor_but.append(self.sortuj_button)
        self.sortuj_button = tkinter.Button(
            text="Najstaršie (pridanie)",
            command=lambda: CarRent.uprav_zoradenie(self, "od_staršieho"),
            borderwidth=0,
            border=0,
        )
        self.sortuj_button.place_configure(x=42, y=80)
        self.zoz_sor_but.append(self.sortuj_button)
        self.sortuj_button = tkinter.Button(
            text="Od Najlacnejšieho",
            command=lambda: CarRent.uprav_zoradenie(self, "Naj_lacnejsie"),
            borderwidth=0,
            border=0,
        )

        self.sortuj_button.place_configure(x=45, y=110)
        self.zoz_sor_but.append(self.sortuj_button)
        self.sortuj_button = tkinter.Button(
            text="Od Drahšieho",
            command=lambda: CarRent.uprav_zoradenie(self, "Naj_drahsie"),
            borderwidth=0,
            border=0,
        )

        self.sortuj_button.place_configure(x=60, y=140)
        self.zoz_sor_but.append(self.sortuj_button)
        self.sortuj_button = tkinter.Button(
            text="Najazdené km (Najviac)",
            command=lambda: CarRent.uprav_zoradenie(self, "km_Najviac"),
            borderwidth=0,
            border=0,
        )

        self.sortuj_button.place_configure(x=35, y=170)
        self.zoz_sor_but.append(self.sortuj_button)
        self.sortuj_button = tkinter.Button(
            text="Najazdené km (Najmenej)",
            command=lambda: CarRent.uprav_zoradenie(self, "km_menej"),
            borderwidth=0,
            border=0,
        )

        self.sortuj_button.place_configure(x=25, y=200)
        self.zoz_sor_but.append(self.sortuj_button)
        self.sortuj_button = tkinter.Button(
            text="Rok Výroby(Najnovšie) ",
            command=lambda: CarRent.uprav_zoradenie(self, "rok_viac"),
            borderwidth=0,
            border=0,
        )

        self.sortuj_button.place_configure(x=40, y=230)
        self.zoz_sor_but.append(self.sortuj_button)
        self.sortuj_button = tkinter.Button(
            text="Rok Výroby (Najstaršie)",
            command=lambda: CarRent.uprav_zoradenie(self, "rok_menej"),
            borderwidth=0,
            border=0,
        )

        self.sortuj_button.place_configure(x=35, y=260)
        self.zoz_sor_but.append(self.sortuj_button)

    def vymaz_moznosti_zoradenia(self, ako=0):
        """
        This function deletes sorting options and related buttons from a canvas.

        :param ako: The parameter "ako" is a flag that determines whether or not to perform a specific
        action. If its value is 1, then the "self.nic_sa_nedeje" attribute is set to True. Otherwise, it
        remains unchanged, defaults to 0 (optional)
        """
        try:
            for i in self.zoz_sor_but:
                i.place_forget()
            for i in self.zoz_sortuj:
                self.canvas.delete(i)
        except:
            pass

        if ako == 1:
            self.nic_sa_nedeje = True
        self.zobrazene = False

    def vytvor_prostredie(self):
        """
        The function creates a graphical environment with a rectangle, a black rectangle with text, and a
        logo.
        """
        self.canvas.create_rectangle(5, 5, 700, 900)
        self.canvas.create_rectangle(5, 5, 700, 50, fill="black")
        self.canvas.create_text(
            350,
            25,
            text="BeloCar",
            font="Arial 20",
        )
        self.vytvor_logo()

    def vytvor_logo(self):
        """
        The function creates a logo and a profile image on a canvas using tkinter and PIL libraries in
        Python.
        """

        self.nic_sa_nedeje = True
        self.logosubor = Image.open(r"Images/Belo_logo.jpg")
        self.logo = ImageTk.PhotoImage(self.logosubor)
        self.logoo = self.canvas.create_image(350, 30, image=self.logo)
        x = tkinter.Button(text="", command=self.update_logo)
        x.place_configure(x=55555, y=100)
        x = Image.open(r"Images/profil.png")
        self.profil_img = ImageTk.PhotoImage(x)

        self.profil = self.canvas.create_image(670, 28, image=self.profil_img)

    def update_logo(self):
        self.canvas.itemconfig(self.logoo, image=self.logo)

    def klik_na_cokolvek(self):
        """
        The function binds mouse click and mouse wheel events to corresponding methods.
        """

        self.canvas.bind("<ButtonPress>", self.klik)
        self.canvas.bind("<MouseWheel>", self.posun_ponuku)

    def posun_ponuku(self, event):
        """
        This function shifts a menu display up or down based on a mouse scroll event and updates the
        displayed data accordingly.

        :param event: The "event" parameter is an object that represents an event that has occurred, such as
        a mouse click or a mouse wheel scroll. In this specific code snippet, the "event" parameter is used
        to determine the direction and amount of scrolling on a mouse wheel, which is then used to adjust
        the
        """
        if self.nic_sa_nedeje is True:
            if len(self.udaje) > 12:
                self.vymaz_ponuku()
                self.nic_sa_nedeje = True
                self.vytvor_filre()
                if event.delta > 0:
                    self.id_od -= 3
                elif event.delta < 0:
                    self.id_od += 3

                if self.id_od < 0:
                    self.id_od = 0
                if self.id_od > len(self.udaje) - 3:
                    self.id_od = len(self.udaje) - 3
                udaje = self.udaje[self.id_od : self.id_od + 12]
                self.graf_ponuka(udaje)

    def ponuka(self, udaje):
        """
        The function "ponuka" performs various actions related to creating and displaying a graph based on
        input data.

        :param udaje: It is a parameter that represents the data used to generate a graph or chart in the
        `ponuka` method. The method first checks if the length of the data is greater than 12, and if so, it
        truncates the data to the first 12 elements. Then it calls several other
        """
        self.id_od = 0
        self.udaje = udaje
        if len(udaje) > 12:
            udaje = udaje[:12]
            self.aktualne_udaje = udaje
        self.klik_na_cokolvek()
        self.nic_sa_nedeje = True
        self.vymaz_ponuku()
        self.vytvor_filre()
        self.graf_ponuka(udaje)

    def graf_ponuka(self, udaje):
        """
        This function creates a graphical display of car rental offers using data provided as input.

        :param udaje: The parameter "udaje" is likely a list of data containing information about car
        rentals, such as the name of the car, its price, and its image. The function "graf_ponuka" uses
        this data to create a graphical representation of the car rentals on a canvas
        """

        self.zoz_ponuka_hore = []
        x = Image.open(r"Images/icon.png")
        xx = ImageTk.PhotoImage(x)
        self.zoz_ponuka_hore.append(xx)
        self.zoz_ponuka_hore.append(self.canvas.create_image(40, 28, image=xx))
        x = 100
        y = 175
        for cis, i in enumerate(udaje):
            udaje = i
            self.zoz_ponuka_hore.append(
                self.canvas.create_rectangle(x - 75, y - 30, x + 100, y + 120)
            )
            obrazky = udaje[11].split("//")
            img = Image.open(r"Obrazky_aut/" + obrazky[0])
            c = img.getbbox()

            c = (c[3] + c[2]) / c[3]

            a = int(c * 75)

            img = img.resize((a, 100))
            self.obrazok = ImageTk.PhotoImage(img)
            self.zoz_ponuka_hore.append(self.obrazok)
            self.zoz_ponuka_hore.append(
                self.canvas.create_image(x + 13, y + 20, image=self.obrazok)
            )
            nazov = udaje[1]
            if len(nazov) > 20:
                nazov = nazov[:22] + "..."
            self.zoz_ponuka_hore.append(
                self.canvas.create_text(x + 17, y + 77, text=nazov, font="Arial 15")
            )
            male = str(udaje[4]) + " | " + str(udaje[3]) + " | " + str(udaje[5]) + "Kw"
            self.zoz_ponuka_hore.append(
                self.canvas.create_text(
                    x,
                    y + 93,
                    text=male,
                )
            )
            f_day = str(udaje[8]) + " €/Deň"
            self.zoz_ponuka_hore.append(
                self.canvas.create_text(
                    x + 60, y + 110, text=f_day, font="Ariel 15", fill="Red"
                )
            )
            if cis < 2:
                x += 220
            elif cis == 2:
                x = 100
                y += 190
            elif 2 < cis < 5:
                x += 220
            elif cis == 5:
                y += 190
                x = 100
            elif 5 < cis < 8:
                x += 220
            elif cis == 8:
                y += 190
                x = 100
            else:
                x += 220

    def zisti_kde_klikol(self, event):
        """
        The function checks where the user clicked on a grid of cards and retrieves information about the
        selected card.

        :param event: The event parameter is an object that represents the event that triggered the
        function. It contains information about the event, such as the type of event and the location of the
        mouse click. In this case, the function is looking for a mouse click event and using the x and y
        coordinates of the click to
        """
        x = 100
        y = 175

        if self.nic_sa_nedeje is True:

            for i in range(12):
                # rint(x,event.x,x+100,y,event.y,y+120)
                if x < event.x < x + 100 and y < event.y < y + 120:
                    CarRent.daj_udaje_o_kartičke(self, i + self.id_od)
                    break
                if i < 2:
                    x += 220
                elif i == 2:
                    x = 100
                    y += 190
                elif 2 < i < 5:
                    x += 220
                elif i == 5:
                    x = 100
                    y += 190
                elif 5 < i < 8:
                    x += 220
                elif i == 8:
                    x = 100
                    y += 190
                else:
                    x += 220

    def vymaz_ponuku(self):
        """
        This function deletes items from a canvas in a try-except block.
        """
        try:
            for i in self.zoz_ponuka_hore:
                self.canvas.delete(i)
        except:
            pass

    def formular_na_vlozenie(self):
        """
        This function creates a form for inserting new cars into a database.
        """
        self.vymaz_profil(1)

        self.nic_sa_nedeje = False
        zoz = []
        zoz.append(
            self.canvas.create_text(
                375,
                70,
                text="Stránka pre vloženie nových aut do požičovni",
                font="Arial 20",
            )
        )
        zoz.append(self.canvas.create_text(250, 115, text="Názov", font="Arial 15"))
        nazov = tkinter.Entry(width=20)
        nazov.place_configure(x=300, y=100)
        zoz.append(self.canvas.create_text(250, 165, text="Popis", font="Arial 15"))
        popis = tkinter.Entry(
            width=20,
        )
        popis.place_configure(x=300, y=150)
        zoz.append(
            self.canvas.create_text(245, 215, text="Najazdené km", font="Arial 15")
        )
        naj_km = tkinter.Entry(
            width=20,
        )
        naj_km.place_configure(x=300, y=200)
        zoz.append(
            self.canvas.create_text(250, 265, text="Rok výroby", font="Arial 15")
        )
        rok = tkinter.Entry(
            width=20,
        )
        rok.place_configure(x=300, y=250)
        zoz.append(
            self.canvas.create_text(250, 315, text="Výkon v KW", font="Arial 15")
        )
        vykon = tkinter.Entry(
            width=20,
        )
        vykon.place_configure(x=300, y=300)
        zoz.append(
            self.canvas.create_text(250, 365, text="Objem motora", font="Arial 15")
        )
        objem = tkinter.Entry(
            width=20,
        )
        objem.place_configure(x=300, y=350)
        zoz.append(
            self.canvas.create_text(
                220, 415, text="Kombinovaná spotreba", font="Arial 15"
            )
        )
        spotreba = tkinter.Entry(
            width=20,
        )
        spotreba.place_configure(x=300, y=400)
        zoz.append(
            self.canvas.create_text(250, 465, text="Prenajom/deň", font="Arial 15")
        )
        pden = tkinter.Entry(
            width=20,
        )
        pden.place_configure(x=300, y=450)
        zoz.append(
            self.canvas.create_text(240, 515, text="Prenajom/týždeň", font="Arial 15")
        )
        ptyzden = tkinter.Entry(
            width=20,
        )
        ptyzden.place_configure(x=300, y=500)
        zoz.append(self.canvas.create_text(360, 550, text="Typ", font="Arial 20"))

        zoz.append(self.canvas.create_text(280, 572, text="Suv", font="Arial 15"))
        suvv = tkinter.IntVar()
        suv = tkinter.Checkbutton(variable=suvv)
        suv.place_configure(x=300, y=560)
        zoz.append(self.canvas.create_text(275, 592, text="Kombi", font="Arial 15"))
        kombii = tkinter.IntVar()
        kombi = tkinter.Checkbutton(variable=kombii)
        kombi.place_configure(x=300, y=580)
        zoz.append(self.canvas.create_text(275, 612, text="Sedan", font="Arial 15"))
        limuzinaa = tkinter.IntVar()
        limuzina = tkinter.Checkbutton(variable=limuzinaa)
        limuzina.place_configure(x=300, y=600)
        zoz.append(self.canvas.create_text(460, 572, text="Cabriolet", font="Arial 15"))
        cabioo = tkinter.IntVar()
        cabrio = tkinter.Checkbutton(variable=cabioo)
        cabrio.place_configure(x=400, y=560)
        zoz.append(self.canvas.create_text(445, 592, text="Van", font="Arial 15"))
        vann = tkinter.IntVar()
        van = tkinter.Checkbutton(variable=vann)
        van.place_configure(x=400, y=580)
        zoz.append(self.canvas.create_text(465, 612, text="Hatchback", font="Arial 15"))
        hbackk = tkinter.IntVar()
        hback = tkinter.Checkbutton(variable=hbackk)
        hback.place_configure(x=400, y=600)
        self.f_text = zoz
        self.formular = [
            nazov,
            popis,
            naj_km,
            rok,
            vykon,
            objem,
            spotreba,
            pden,
            ptyzden,
            suv,
            kombi,
            limuzina,
            cabrio,
            van,
            hback,
        ]

        self.checkboc = [suvv, kombii, limuzinaa, cabioo, vann, hbackk]
        self.checkbocudaje = ["suv", "kombi", "sedan", "cabrio", "van", "hatchback"]
        self.obrazok = tkinter.Button(
            text="Vybrať obrázok", command=self.otvor_obrazok, font="Arial 20"
        )
        self.obrazok.place_configure(x=275, y=650)
        self.f_sub = tkinter.Button(
            text="Potvrdiť", command=self.skontroluj_formular, font="Arial 20"
        )
        self.f_sub.place_configure(x=300, y=710)

        x = Image.open(r"Images/back.png")
        xx = ImageTk.PhotoImage(x)
        self.f_text.append(xx)
        self.spatt = tkinter.Button(
            image=xx,
            borderwidth=0,
            border=0,
            command=self.vymaz_formular,
            background="black",
        )
        self.spatt.place_configure(x=5, y=5)
        self.f_buttons = [self.obrazok, self.f_sub, self.spatt]
        self.nic_sa_nedeje = False

    def skontroluj_formular(self):
        """
        This function checks the validity of input data in a form and returns a dictionary of the input
        data if it is valid.
        :return: a boolean value, either True or False.
        """

        udaje = {}
        for cis, i in enumerate(self.formular):
            if cis <= 8:
                x = i.get()
                if cis == 0:
                    if len(x) < 3:
                        popup = self.canvas.create_text(
                            580, 115, text="Musí mať aspoň 3 znaky"
                        )
                        self.canvas.update()
                        self.canvas.after(2000)
                        self.canvas.delete(popup)
                        return False
                    else:
                        udaje["nazov"] = x
                elif cis == 1:
                    if len(x) < 10:
                        popup = self.canvas.create_text(
                            580, 165, text="Musí mať aspoň 10 znakov"
                        )
                        self.canvas.update()
                        self.canvas.after(2000)
                        self.canvas.delete(popup)
                        return False
                    else:
                        udaje["popis"] = x
                elif cis == 2:
                    try:
                        x = int(x)
                        if x < 0:
                            popup = self.canvas.create_text(
                                580, 215, text="Musí byť číslo vačšie ako 0"
                            )
                            self.canvas.update()
                            self.canvas.after(2000)
                            self.canvas.delete(popup)
                            return False
                        else:
                            udaje["km"] = x
                    except:
                        popup = self.canvas.create_text(
                            580, 215, text="Musí byť číslo vačšie ako 0"
                        )
                        self.canvas.update()
                        self.canvas.after(2000)
                        self.canvas.delete(popup)
                        return False

                elif cis == 3:
                    try:
                        x = int(x)
                        if 1900 < x < 2023:
                            udaje["rok"] = x
                        else:
                            popup = self.canvas.create_text(
                                580, 265, text="Nesprávny formát roku"
                            )
                            self.canvas.update()
                            self.canvas.after(2000)
                            self.canvas.delete(popup)
                            return False

                    except:
                        popup = self.canvas.create_text(
                            580, 265, text="Nesprávny formát roku"
                        )
                        self.canvas.update()
                        self.canvas.after(2000)
                        self.canvas.delete(popup)
                        return False
                elif cis == 4:
                    try:
                        x = int(x)
                        if x < 0:
                            popup = self.canvas.create_text(
                                580, 315, text="Nesprávny formát Kw"
                            )
                            self.canvas.update()
                            self.canvas.after(2000)
                            self.canvas.delete(popup)
                            return False
                        else:
                            udaje["kw"] = x
                    except:
                        popup = self.canvas.create_text(
                            580, 315, text="Nesprávny formát Kw"
                        )
                        self.canvas.update()
                        self.canvas.after(2000)
                        self.canvas.delete(popup)
                        return False

                elif cis == 5:
                    try:
                        x = int(x)
                        if x < 0:
                            popup = self.canvas.create_text(
                                580, 365, text="Nesprávny formát objemu"
                            )
                            self.canvas.update()
                            self.canvas.after(2000)
                            self.canvas.delete(popup)
                            return False
                        else:
                            udaje["objem"] = x
                    except:
                        popup = self.canvas.create_text(
                            580, 365, text="Nesprávny formát objemu"
                        )
                        self.canvas.update()
                        self.canvas.after(2000)
                        self.canvas.delete(popup)
                        return False
                elif cis == 6:
                    try:
                        x = float(x)
                        if x < 0:
                            popup = self.canvas.create_text(
                                580, 415, text="Nesprávny formát spotreby"
                            )
                            self.canvas.update()
                            self.canvas.after(2000)
                            self.canvas.delete(popup)
                            return False
                        else:
                            udaje["spotreba"] = x
                    except:
                        popup = self.canvas.create_text(
                            580, 415, text="Nesprávny formát spotreby"
                        )
                        self.canvas.update()
                        self.canvas.after(2000)
                        self.canvas.delete(popup)
                        return False

                elif cis == 7:
                    try:
                        x = float(x)
                        if x < 0:
                            popup = self.canvas.create_text(
                                580, 465, text="Nesprávny formát prenajmu"
                            )
                            self.canvas.update()
                            self.canvas.after(2000)
                            self.canvas.delete(popup)
                            return False
                        else:
                            udaje["prenajomDay"] = x
                    except:
                        popup = self.canvas.create_text(
                            580, 465, text="Nesprávny formát prenajmu"
                        )
                        self.canvas.update()
                        self.canvas.after(2000)
                        self.canvas.delete(popup)
                        return False
                elif cis == 8:
                    try:
                        x = float(x)
                        if x < 0:
                            popup = self.canvas.create_text(
                                580, 515, text="Nesprávny formát prenajmu"
                            )
                            self.canvas.update()
                            self.canvas.after(2000)
                            self.canvas.delete(popup)
                            return False
                        else:
                            udaje["prenajomWeek"] = x
                    except:
                        popup = self.canvas.create_text(
                            580, 515, text="Nesprávny formát prenajmu"
                        )
                        self.canvas.update()
                        self.canvas.after(2000)
                        self.canvas.delete(popup)
                        return False
            else:
                kolko = 0
                for cis, i in enumerate(self.checkboc):
                    x = i.get()
                    kolko += x
                    if x == 1:
                        udaje["typ"] = self.checkbocudaje[cis]
                if kolko != 1:
                    popup = self.canvas.create_text(
                        580, 590, text="Musíte označiť práve 1"
                    )
                    self.canvas.update()
                    self.canvas.after(2000)
                    self.canvas.delete(popup)
                    return False
        self.udaje = udaje

        x = None
        try:
            x = self.nazvy_obrazkov
        except:
            pass
        if x is not None:
            if self.nazvy_obrazkov != []:
                self.udaje["obrazky"] = self.nazvy_obrazkov
                xx = self.udaje

                CarRent.uloz_do_databazi(self, xx)

        return True

    def otvor_obrazok(self):
        """
        The function opens an image file from a folder and moves it to a specified destination folder
        while renaming it with a prefix and a sequential number.
        """
        if self.skontroluj_formular() is True:
            self.nazvy_obrazkov = []
            try:
                if os.name == "nt":  # pre Windows
                    desktop = os.path.join(
                        os.path.join(os.environ["USERPROFILE"]), "Desktop"
                    )
                else:  # pre macOS
                    desktop = os.path.join(os.path.expanduser("~"), "Desktop")

                # požiadajte používateľa o výber súborov
                file_paths = filedialog.askopenfilenames(
                    title="Vyberte obrázky",
                    filetypes=[("JPG súbory", "*.jpg"), ("PNG súbory", "*.png")],
                )
                destination_folder = "Obrazky_aut"
                # ak cieľový priečinok neexistuje, vytvorte ho
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                total_files = 0
                moved_files = 0
                for filename in file_paths:
                    if (
                        filename.endswith(".png")
                        or filename.endswith(".jpg")
                        or filename.endswith(".JPG")
                    ):
                        # získaj názov súboru bez prípony
                        file_name = os.path.splitext(os.path.basename(filename))[0]
                        # vytvor nový názov súboru s prefixom a poradovým číslom
                        nazov = self.udaje["nazov"]
                        new_file_name = f"{nazov}_{total_files + 1}.png"
                        # skontrolovať, či súbor s rovnakým názvom už existuje v cieľovom priečinku
                        file_path = os.path.join(destination_folder, new_file_name)
                        if os.path.exists(file_path):
                            raise Exception
                        else:
                            # premenovať súbor
                            os.rename(
                                filename,
                                os.path.join(os.path.dirname(filename), new_file_name),
                            )
                            # presunúť súbor
                            shutil.move(
                                os.path.join(os.path.dirname(filename), new_file_name),
                                destination_folder,
                            )
                            self.nazvy_obrazkov.append(new_file_name)

                            moved_files += 1
                        total_files += 1
                    else:
                        popup = self.canvas.create_text(
                            580, 670, text="Obrazok musí byť JPG alebo png "
                        )
                        self.canvas.update()
                        self.canvas.after(2000)
                        self.canvas.delete(popup)

            except:
                popup = self.canvas.create_text(
                    580, 670, text="Nepodarilo sa presunúť obrázok "
                )
                self.canvas.update()
                self.canvas.after(2000)
                self.canvas.delete(popup)

    def vymaz_formular(self):
        """
        This function deletes a form and its elements from a canvas.
        """

        for i in self.f_text:
            self.canvas.delete(i)
        # for i in self.checkboc:
        #     i.place_forget()
        for i in self.formular:
            i.place_forget()
        for i in self.f_buttons:
            i.place_forget()

        # self.obrazok.place_forget()
        # self.f_sub.place_forget()
        CarRent.spat_na_ponuku(self)

        self.nic_sa_nedeje = True

        # Vloženie hodnôt do databázy

    def vytvor_podrobne_info(self, udaje):
        """
        This function creates a detailed information screen for a car rental service, including text and
        image elements, as well as buttons for navigation and ordering.

        :param udaje: "udaje" is a list of information about a specific item, likely a vehicle, that
        will be used to create a detailed display of the item. The list contains various details such as
        the mileage, year of production, engine power, engine volume, fuel consumption, rental prices,
        and type of
        """
        if self.nic_sa_nedeje is True:

            self.vymaz_filtre()
            self.vymaz_moznosti_zoradenia()
            self.vymaz_ponuku()

            self.zoz_podrobna_ponuka = []
            zoz = [
                "Najazdených (km) : ",
                "       Rok výroby : ",
                "      Výkon Motora : ",
                "            Objem motora : ",
                "                 Spotreba : ",
                "       Cena/deň : ",
                "     Cena/týždeň : ",
                "               Typ : ",
            ]
            zoz2 = [
                "",
                "",
                " kw",
                " cm\u00b3",
                " l/100km",
                " €",
                " €",
                "",
            ]
            self.zoz_podrobna_ponuka.append(
                self.canvas.create_text(350, 70, text=udaje[1], font="Arial 25")
            )
            self.zoz_podrobna_ponuka.append(
                self.canvas.create_rectangle(10, 85, 695, 180)
            )
            x = 150
            y = 100
            dd = 3
            for cc, i in enumerate(zoz):
                xcs = i + str(udaje[dd]) + zoz2[cc]
                self.zoz_podrobna_ponuka.append(
                    self.canvas.create_text(x, y, text=xcs, font="Arial 15")
                )
                dd += 1
                y += 20
                if dd == 7:
                    x += 400
                    y = 100
            text = udaje[2]
            vypis = ""
            asd = 0
            for inde, i in enumerate(text):
                if asd > 85 and i == " ":
                    vypis += "\n"
                    asd = 0
                vypis += i
                asd += 1

            self.zoz_podrobna_ponuka.append(
                self.canvas.create_text(350, 730, text=vypis, font="Arial 15")
            )
            self.obrazky_podrobnej_ponuky = []
            obr = udaje[dd].split("//")
            x = Image.open(r"Images/back.png")
            xx = ImageTk.PhotoImage(x)
            self.obrazky_podrobnej_ponuky.append(xx)
            self.spat = tkinter.Button(
                image=xx,
                borderwidth=0,
                border=0,
                command=self.vymaz_podrobnu_ponuku,
                background="black",
            )
            self.spat.place_configure(x=5, y=5)

            x = Image.open(r"Images/left:rigt.png")
            x1 = x.rotate(180)
            xx1 = ImageTk.PhotoImage(x1)
            self.obrazky_podrobnej_ponuky.append(xx1)
            self.right = tkinter.Button(
                image=xx1,
                borderwidth=0,
                border=0,
                command=lambda: self.zamen(udaje, 1),
                background="black",
            )
            self.right.place_configure(x=535, y=270)

            xx = ImageTk.PhotoImage(x)
            self.obrazky_podrobnej_ponuky.append(xx)
            self.left = tkinter.Button(
                image=xx,
                borderwidth=0,
                border=0,
                command=lambda: self.zamen(udaje, 0),
                background="black",
            )
            self.left.place_configure(x=110, y=270)
            self.objednaj = tkinter.Button(
                text="Objednať",
                font="Arial 25",
                command=lambda: self.obrazovka_objednavka_pocet_dni(udaje),
            )
            self.objednaj.place_configure(x=280, y=635)

            self.vytvor_obrazky_pod(obr)
            self.nic_sa_nedeje = False

            self.zoz_podrobna_ponuka_but = [
                self.right,
                self.left,
                self.spat,
                self.objednaj,
            ]

    def obrazovka_objednavka_pocet_dni(self, udaje):
        """
        This function creates a screen for the user to input the number of days they want to rent a car
        and confirm their order.

        :param udaje: The parameter "udaje" is a list containing information about a specific car rental
        offer, such as the name of the car, its price, and other details. This information is used to
        display the rental offer on the screen and to process the user's rental request
        """
        self.zoz_objedavka = []
        self.zoz_objedavka_but = []
        prihlaseny = 0
        try:
            udaje_uzivatel = CarRent.daj_udaje_uzivatel(self)

            self.vymaz_podrobnu_ponuku(1)
            prihlaseny = 1
        except:
            x = self.canvas.create_text(
                350,
                800,
                text="Najprv sa musíte prihlasiť!",
                font="Arial 40",
                fill="red",
            )
            self.canvas.update()
            self.canvas.after(1000)
            self.canvas.delete(x)
        if prihlaseny == 1:
            self.nic_sa_nedeje = False
            self.zoz_objedavka.append(
                self.canvas.create_text(350, 85, text="Objednávka", font="Arial 25")
            )
            nazov = "Názov : " + udaje[1]
            self.zoz_objedavka.append(
                self.canvas.create_text(200, 120, text=nazov, font="Arial 15")
            )
            self.zoz_objedavka.append(
                self.canvas.create_text(
                    200,
                    150,
                    text="Vyberte počet dni na kolľko si chcete požičiať auto : ",
                    font="Arial 15",
                )
            )
            dni = tkinter.Entry(width=5)
            dni.place_configure(x=390, y=137)
            self.zoz_objedavka_but.append(dni)
            potvrd = tkinter.Button(
                text="Potvrdiť",
                font="Arial 20",
                command=lambda: self.objednavka_potvrd(udaje, udaje_uzivatel),
            )
            potvrd.place_configure(x=300, y=200)
            self.zoz_objedavka_but.append(potvrd)
            x = Image.open(r"Images/back.png")
            xx = ImageTk.PhotoImage(x)
            self.zoz_objedavka.append(xx)
            spatt = tkinter.Button(
                image=xx,
                borderwidth=0,
                border=0,
                command=self.vymaz_objednavka,
                background="black",
            )
            spatt.place_configure(x=5, y=5)
            self.zoz_objedavka_but.append(spatt)

    def vymaz_objednavka(self, ako=0):
        """
        The function deletes order objects and buttons from a canvas in a car rental program.

        """
        try:
            for i in self.zoz_objedavka:
                self.canvas.delete(i)
        except:
            pass
        try:
            for i in self.zoz_objedavka_but:
                i.place_forget()
        except:
            pass

        self.nic_sa_nedeje = True
        if ako == 0:
            CarRent.spat_na_ponuku(self)

    def objednavka_potvrd(self, udaje, udaje_uzivatel):
        """
        This function confirms an order and displays the details on a canvas, including the name,
        address, email, and total price of the order, as well as the start and end dates of the rental
        period.


        """
        pocetdni = self.zoz_objedavka_but[0].get()
        pocetdni2 = 0
        try:
            pocetdni = int(pocetdni)
            pocetdni2 = int(pocetdni)

        except:
            x = self.canvas.create_text(
                350, 180, text="Zle zadané", font="Arial 40", fill="red"
            )
            self.canvas.update()
            self.canvas.after(1000)
            self.canvas.delete(x)
        if pocetdni2 > 0:
            self.vymaz_objednavka(1)
            self.nic_sa_nedeje = False
            self.zoz_objedavka.append(
                self.canvas.create_text(350, 85, text="Objednávka", font="Arial 25")
            )
            nazov = "Názov : " + udaje[1]
            self.zoz_objedavka.append(
                self.canvas.create_text(350, 120, text=nazov, font="Arial 15")
            )
            now = datetime.now()
            date = now.strftime("%d/%m/%Y")
            new_date = now + timedelta(days=pocetdni)
            new_date = new_date.strftime("%d/%m/%Y")
            datet = "Od: " + date + "   Do: " + new_date
            self.zoz_objedavka.append(
                self.canvas.create_text(350, 150, text=datet, font="Arial 15")
            )
            zoz = ["Meno:", "Adresa:", "Mail:", "Cena celkom:"]
            x = 250
            y = 180
            cena = CarRent.daj_cenovku(self, pocetdni, udaje[0])
            cena = round(cena, 2)

            udajezoz = [
                udaje_uzivatel[0][1],
                udaje_uzivatel[0][4],
                udaje_uzivatel[0][2],
                cena,
            ]

            for cis, meno in enumerate(zoz):
                self.zoz_objedavka.append(
                    self.canvas.create_text(x, y, text=meno, font="Arial 15")
                )
                self.zoz_objedavka.append(
                    self.canvas.create_text(
                        x + 200, y, text=udajezoz[cis], font="Arial 15"
                    )
                )
                y += 20

            objednaj = tkinter.Button(
                text="Objednať s povinnosťou platby",
                font="Arial 20",
                command=lambda: CarRent.objenaj(self, udaje[0], cena, date, new_date),
            )
            objednaj.place_configure(x=220, y=y + 30)
            self.zoz_objedavka_but.append(objednaj)

            x = Image.open(r"Images/back.png")
            xx = ImageTk.PhotoImage(x)
            self.zoz_objedavka.append(xx)
            spatt = tkinter.Button(
                image=xx,
                borderwidth=0,
                border=0,
                command=self.vymaz_objednavka,
                background="black",
            )
            spatt.place_configure(x=5, y=5)
            self.zoz_objedavka_but.append(spatt)

            self.zoz_udajov_mail = [
                udaje[1],
                udaje_uzivatel[0][1],
                udaje_uzivatel[0][4],
                cena,
                date,
                new_date,
                udaje[2],
                udaje[-3],
                udaje_uzivatel[0][2],
            ]

        else:
            pocetdni = self.canvas.create_text(
                350, 180, text="Zle zadané", font="Arial 40", fill="red"
            )
            self.canvas.update()
            self.canvas.after(1000)
            self.canvas.delete(pocetdni)

    def dakujeme_za_objednavku(self):
        """
        This function creates a thank you message for an order and displays it on a canvas, along with a
        button to go back and an optional message about sending details via email.
        """
        self.zoz_dakujeme = []
        self.zoz_dakujeme_but = []
        self.zoz_dakujeme.append(
            self.canvas.create_text(
                350, 150, text="Ďakujeme za objednávku", font="Arial 25"
            )
        )
        try:
            self.generuj_mail()
            self.zoz_dakujeme.append(
                self.canvas.create_text(
                    350,
                    180,
                    text="Podrobnosti sme vam zaslali e-mailom",
                    font="Arial 15",
                )
            )
        except:
            pass

        x = Image.open(r"Images/back.png")
        xx = ImageTk.PhotoImage(x)
        self.zoz_dakujeme.append(xx)
        spatt = tkinter.Button(
            image=xx,
            borderwidth=0,
            border=0,
            command=self.vymaz_dakujeme,
            background="black",
        )
        spatt.place_configure(x=5, y=5)
        self.zoz_dakujeme_but.append(spatt)

    def posli_mail(self, message, email_to, img_name):
        """
        This function sends an email with a message and an attached image using the SMTP protocol.

        :param message: The message to be sent in the email, in HTML format
        :param email_to: The email address of the recipient to whom the email will be sent
        :param img_name: The name of the image file that will be attached to the email
        """
        email_from = "belocarrent@gmail.com"
        # Writing Email details
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Ďakujeme za objednávku"
        msg["From"] = "belocarrent@gmail.com"
        msg["To"] = "beluskostefan@gmail.com"
        msg.attach(MIMEText(message, "html"))
        obr = "Obrazky_aut/" + img_name

        img_o = open(obr, "rb").read()
        img = MIMEImage(img_o, "jpg", name="logi.jpg")
        pswd = "lhhoqqwekekeoxhz"
        msg.attach(img)
        # Writing Server Details
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(email_from, pswd)

        server.sendmail(email_from, email_to, msg.as_string())

    def generuj_mail(self):
        """
        This function generates an email message with information about a car rental order and sends it
        to the specified email address.
        """
        img = str(self.zoz_udajov_mail[7])
        img = img.split("//")
        img = img[0]
        emial_to = str(self.zoz_udajov_mail[-1])
        message = f"""
        <body>
        <h1> Ďakujeme za objednávku</h1>
        <table>
            <tr>
            <th>Auto</th>
            <td>{str(self.zoz_udajov_mail[0])}</td>
          </tr>
          <tr>
            <th>Meno</th>
            <td>{str(self.zoz_udajov_mail[1])}</td>
          </tr>
          <tr>
            <th>Adresa</th>
            <td>{str(self.zoz_udajov_mail[2])}</td>
          </tr>
          
          <tr>
            <th>Datum od</th>
            <td>{str(self.zoz_udajov_mail[4])}</td>
          </tr>
          <tr>
            <th>Datum do</th>
            <td>{str(self.zoz_udajov_mail[5])}</td>
          </tr>
          <tr>
            <th>Cena</th>
            <td>{str(self.zoz_udajov_mail[3])}</td>
          </tr>
        </table>

        </body>
        
        """
        self.posli_mail(message, emial_to, img)

    def vymaz_dakujeme(
        self,
    ):
        """
        The function deletes a "thank you" message and button from a canvas in a CarRent object.
        """
        try:
            for i in self.zoz_dakujeme:
                self.canvas.delete(i)
        except:
            pass
        try:
            self.zoz_dakujeme_but[0].place_forget()
        except:
            pass
        CarRent.spat_na_ponuku(self)

    def zamen(self, udaje, ako):
        """
        The function takes in data and a parameter, modifies the data based on the parameter, and
        creates detailed information.

        :param udaje: The variable "udaje" is a list of data that is being passed as an argument to the
        "zamen" method
        :param ako: The parameter "ako" is a flag that determines how the function will modify the
        "udaje" list. If "ako" is equal to 1, the function will move the last element of the third item
        in the "udaje" list to the beginning of the same item. If "
        """
        udaje = list(udaje)
        self.vymaz_podrobnu_ponuku()
        if ako == 1:
            obr = udaje[-3]

            obr = obr.split("//")
            x = obr.pop(0)
            obr.append(x)
            obr = "//".join(obr)
            udaje[-3] = obr
        else:
            obr = udaje[-3]
            obr = obr.split("//")
            x = obr.pop(-1)
            obr.insert(0, x)
            obr = "//".join(obr)
            udaje[-3] = obr

        self.vytvor_podrobne_info(udaje)

    def vymaz_podrobnu_ponuku(self, ako=0):
        """
        This function deletes a detailed offer and associated buttons from a canvas in a car rental
        program.

        :param ako: The parameter "ako" is an optional integer parameter that defaults to 0. It is used
        to determine whether to execute additional code after deleting the detailed offer. If ako is
        equal to 0, the code will call the "spat_na_ponuku" method of the "CarRent", defaults to 0
        (optional)
        """
        x = False
        xx = False
        try:
            for i in self.zoz_podrobna_ponuka:
                self.canvas.delete(i)
            # self.zoz_podrobna_ponuka = []
            x = True
        except:
            pass
        try:
            for i in self.zoz_podrobna_ponuka_but:
                i.place_forget()
            xx = True
        except:
            pass
        if x is True and xx is True and ako == 0:
            CarRent.spat_na_ponuku(self)

            self.nic_sa_nedeje = True

    def vytvor_obrazky_pod(self, obr):
        """
        This function creates and resizes images to be displayed in a canvas, based on a list of image
        file names.

        :param obr: The parameter "obr" is a list of image file names that will be used to create images
        in the program
        """
        x = 130
        y = 450
        for cis, i in enumerate(obr):
            img = Image.open(r"Obrazky_aut/" + i)
            c = img.getbbox()

            c = (c[3] + c[2]) / c[3]

            if cis == 0:
                a = int(c * 280)
                a = a - 280

                img = img.resize((a, 280))
                self.obrazokk = ImageTk.PhotoImage(img)
                self.obrazky_podrobnej_ponuky.append(self.obrazokk)
                self.zoz_podrobna_ponuka.append(
                    self.canvas.create_image(350, 325, image=self.obrazokk)
                )
                y += 100
            else:
                a = int(c * 170)
                a = a - 170

                img = img.resize((a, 170))
                self.obrazokk = ImageTk.PhotoImage(img)
                self.obrazky_podrobnej_ponuky.append(self.obrazokk)
                self.zoz_podrobna_ponuka.append(
                    self.canvas.create_image(x, y, image=self.obrazokk)
                )
                if cis == 3 or cis == 6:
                    y += 170
                    x = 130
                else:
                    x += 220

            if cis == 3:
                break


class CarRent(Grafik):
    def __init__(self):
        """
        This is a constructor function that initializes some attributes of an object.
        """
        super().__init__()
        self.vytvor_ponuku()
        self.prihlasieni = False
        self.admin = 0

        # super().formular_na_vlozenie()

    def vymaz_objednavku(self, id, id_auta):
        """
        This function deletes an order from a database and updates the rental status of a car in another
        database.

        :param id: The ID of the order to be deleted from the "objednavky" table in the "objednavky.db"
        database
        :param id_auta: The parameter "id_auta" is likely an identifier for a specific car that was
        rented in the "pozicovna" database. It is used in the SQL query to update the "rented" column of
        the "pozicovna" table to 0 (indicating
        """

        obj = sqlite3.connect("objednavky.db")
        pozic = sqlite3.connect("pozicovna.db")
        obj.execute("DELETE FROM objednavky WHERE id = " + str(id))
        pozic.execute(
            "UPDATE pozicovna SET rented = ? WHERE id = ?",
            (
                0,
                id_auta,
            ),
        )
        pozic.commit()
        pozic.close()
        obj.commit()
        obj.close()
        super().vymaz_profil(1)
        super().ukaz_profil()

    def vymaz_z_databazy(self, id, obrazky):
        """
        This function deletes a record from two different databases and removes associated images from a
        directory.

        :param id: The ID of the car to be deleted from the database and its associated images to be
        removed
        :param obrazky: The parameter "obrazky" is a string containing the names of image files separated
        by "//"
        """

        obj = sqlite3.connect("objednavky.db")
        pozic = sqlite3.connect("pozicovna.db")
        pozic.execute("DELETE FROM pozicovna WHERE id = " + str(id))
        obj.execute("DELETE FROM objednavky WHERE id_auta = " + str(id))
        pozic.commit()
        pozic.close()
        obj.commit()
        obj.close()
        obrazky = obrazky.split("//")
        for i in obrazky:
            os.remove(
                "/Users/stefanbelusko/Desktop/skola/programovanie/Semestralny_2/Obrazky_aut/"
                + i
            )

        super().vymaz_profil(1)
        super().ukaz_profil()

    def daj_vsetky_auta(self):
        """
        This function retrieves all data from a table named "pozicovna" in a SQLite database and returns
        it as a list.
        :return: all the rows from the "pozicovna" table in the "pozicovna.db" database.
        """
        conn = sqlite3.connect("pozicovna.db")
        c = conn.cursor()
        c.execute("SELECT * FROM pozicovna")
        x = c.fetchall()
        conn.commit()
        conn.close()
        return x

    def daj_cenovku(self, pocetdni, id):
        """
        This function retrieves the rental price for a given number of days and rental item ID from a
        SQLite database, with a discount applied for rentals longer than 7 days.

        """
        conn = sqlite3.connect("pozicovna.db")
        c = conn.cursor()
        c.execute("SELECT * FROM pozicovna WHERE id = " + str(id))
        x = c.fetchall()
        conn.commit()
        conn.close()
        if pocetdni >= 7:
            return x[0][9] * (pocetdni / 7)
        else:
            return x[0][8] * pocetdni

    def objenaj(self, id_auta, cena, datum_od, datum_do):
        """
        This function inserts a new car rental order into a database and updates the corresponding tables
        with the rental information.

        :param id_auta: The ID of the car being rented in the order
        :param cena: The price of the rental. It is a float value
        :param datum_od: The starting date of the rental period for the car
        :param datum_do: "datum_do" is a variable that represents the end date of a car rental
        reservation. It is likely a string or date object that specifies the date and time when the
        rental period ends
        """
        super().vymaz_objednavka(1)
        super().dakujeme_za_objednavku()
        uzivatel = self.pouzivatel[0][0]

        pouzivat = sqlite3.connect("pouzivatelia.db")
        obj = sqlite3.connect("objednavky.db")
        pozic = sqlite3.connect("pozicovna.db")
        id_auta = int(id_auta)
        id_uzivatela = int(uzivatel)
        datum_od = str(datum_od)
        datum_do = str(datum_do)
        cena = float(cena)

        obj.execute(
            f"INSERT INTO objednavky (id_auta, id_uzivatela, datum_od, datum_do, cena) VALUES (?, ?, ?,?,?)",
            (id_auta, id_uzivatela, datum_od, datum_do, cena),
        )

        pouzivat.execute(
            "UPDATE pouzivatelia SET pozicane_auto = ? WHERE id = ?",
            (id_auta, id_uzivatela),
        )
        pozic.execute(
            "UPDATE pozicovna SET rented = ? WHERE id = ?",
            (
                1,
                id_auta,
            ),
        )
        pozic.commit()
        pozic.close()
        obj.commit()
        obj.close()
        pouzivat.commit()
        pouzivat.close()

    def daj_udaje_uzivatel(self):
        """
        This function returns the user's information if it exists, otherwise it raises an exception.
        :return: If the `self.pouzivatel` is not `None`, then the method returns the value of
        `self.pouzivatel`. Otherwise, it raises an exception.
        """
        if self.pouzivatel is not None:

            return self.pouzivatel
        else:
            raise Exception

    def daj_udaje_o_kartičke(self, id):
        """
        This function retrieves detailed information about a card based on its ID and calls a superclass
        method to create a detailed information object.

        :param id: The parameter "id" is an identifier that is used to retrieve information about a
        specific card from the "my" dictionary. It is passed as an argument to the method
        "daj_udaje_o_kartičke"
        """
        x = self.my[id]
        super().vytvor_podrobne_info(x)

    def odhlas(self):
        """
        This function logs out a user by resetting their login status, admin status, and user profile.
        """
        self.prihlasieni = False
        self.admin = 0
        self.pouzivatel = None
        super().vymaz_profil()
        super().ukaz_profil()

    def daj_objedavky(self):
        """
        This function retrieves all orders from a SQLite database for a specific user.
        :return: a list of tuples containing all the rows from the "objednavky" table in the
        "objednavky.db" database where the "id_uzivatela" column matches the ID of the user specified by
        the "self.pouzivatel" attribute.
        """
        conn = sqlite3.connect("objednavky.db")
        c = conn.cursor()

        c.execute(
            "SELECT * FROM objednavky WHERE id_uzivatela = "
            + str(self.pouzivatel[0][0])
        )
        x = c.fetchall()
        conn.commit()
        conn.close()
        return x

    def daj_nazov_auta(self, id):
        """
        This function retrieves the name of a car from a SQLite database based on its ID.

        :param id: The parameter "id" is an integer that represents the unique identifier of a car in a
        car rental database
        :return: the name of a car from a database table called "pozicovna" based on the input parameter
        "id". The name of the car is located in the second column of the table. The function connects to
        the database, executes a SELECT query to retrieve the row with the specified id, fetches the
        result, closes the connection, and returns the name of the car
        """
        conn = sqlite3.connect("pozicovna.db")
        c = conn.cursor()

        c.execute("SELECT * FROM pozicovna WHERE id = " + str(id))
        x = c.fetchall()
        conn.commit()
        conn.close()
        return x[0][1]

    def registruj(self, udaje):
        """
        The function registers a user by inserting their information into a SQLite database and then
        deletes the registration form.

        :param udaje: "udaje" is a variable that contains a list of user data, including their name,
        email, password, and address. The data is passed as an argument to the "registruj" method
        """
        conn = sqlite3.connect("pouzivatelia.db")
        heslo = udaje[2]
        meno = udaje[0]
        mail = udaje[1]
        sifra = hashlib.sha256(heslo.encode("utf-8")).hexdigest()
        adresa = udaje[3]
        conn.execute(
            f"INSERT INTO pouzivatelia (meno, mail, heslo,Adresa) VALUES (?, ?, ?,?)",
            (meno, mail, sifra, adresa),
        )
        conn.commit()
        conn.close()
        super().vymaz_registraciu()

    def prihlasienie(self, meno, heslo):
        """
        This function checks if a given username and password match a record in a SQLite database and
        logs the user in if they do.

        :param meno: The parameter "meno" is a string variable that represents the username of a user
        trying to log in
        :param heslo: The parameter "heslo" is a string variable that represents the password entered by
        the user during the login process
        """
        conn = sqlite3.connect("pouzivatelia.db")
        c = conn.cursor()
        sifra = hashlib.sha256(heslo.encode("utf-8")).hexdigest()
        req = f"SELECT * FROM pouzivatelia WHERE meno = '{meno}' AND heslo = '{sifra}'"
        c.execute(req)
        my = c.fetchall()
        if my != []:
            self.prihlasieni = True
            self.pouzivatel = my

            if my[0][-1] == 1:
                self.admin = 1
            super().vymaz_profil()
        else:
            super().zle_meno_heslo()
        conn.commit()
        conn.close()

    def daj_prihlasenost(self):
        """
        This function returns the values of "prihlasieni" and "admin" attributes.
        :return: The method `daj_prihlasenost` is returning a tuple containing two values:
        `self.prihlasieni` and `self.admin`.
        """
        return self.prihlasieni, self.admin

    def vytvor_ponuku(self):
        """
        This function creates a list of available items for rent from a SQLite database and displays it
        using a superclass method.
        """
        tab = sqlite3.connect("pozicovna.db")
        c = tab.cursor()
        self.order = " ORDER BY id DESC"
        self.request = "SELECT * FROM pozicovna WHERE rented = 0 ORDER BY id DESC"
        self.request_dd = "WHERE rented = 0"
        c.execute(self.request)
        self.my = c.fetchall()
        super().ponuka(self.my)

        tab.commit()
        tab.close()

    def uprav_zoradenie(self, ako):
        """
        This function modifies the sorting order of a database query based on the input parameter and
        displays the results.

        :param ako: The parameter "ako" is a string that specifies the type of sorting to be applied to
        a database query. It can take one of the following values: "od_staršieho", "najnovšie",
        "Naj_lacnejsie", "Naj_drahs
        """
        super().vymaz_moznosti_zoradenia(1)
        super().vymaz_ponuku()
        tab = sqlite3.connect("pozicovna.db")
        c = tab.cursor()
        if ako == "od_staršieho":
            request = " ORDER BY id ASC"
        elif ako == "najnovšie":
            request = " ORDER BY id DESC"
        elif ako == "Naj_lacnejsie":
            request = " ORDER BY cenaden ASC"
        elif ako == "Naj_drahsie":
            request = " ORDER BY cenaden DESC"
        elif ako == "km_Najviac":
            request = " ORDER BY km DESC"
        elif ako == "km_menej":
            request = " ORDER BY km ASC"
        elif ako == "rok_menej":
            request = " ORDER BY rok ASC"
        elif ako == "rok_viac":
            request = " ORDER BY rok DESC"
        self.order = request
        try:
            x = self.request_dd
        except:
            self.request_dd = " "
        self.request = "SELECT * FROM pozicovna " + self.request_dd + request
        c.execute(self.request)
        self.my = c.fetchall()

        super().ponuka(self.my)
        tab.commit()
        tab.close()

    def spat_na_ponuku(self):
        """
        The function "spat_na_ponuku" calls the "vytvor_ponuku" method.
        """
        self.vytvor_ponuku()

    def uloz_do_databazi(self, udaje):
        """
        This function saves data to a database by inserting values into a table.

        :param udaje: "udaje" is a dictionary containing information about a rental item, such as its
        name, description, mileage, year, power, volume, fuel consumption, rental price per day and
        week, type, and images. The function takes this dictionary as a parameter and saves the
        information to a database
        """
        """"ulozi do databazi"""

        super().vymaz_formular()
        x = udaje["obrazky"]
        x = "//".join(x)
        udaje["obrazky"] = x
        tab = sqlite3.connect("pozicovna.db")
        c = tab.cursor()
        zudaje = []

        for i in udaje:
            zudaje.append(udaje[i])
        otazniky = ",".join(["?" for _ in udaje])
        c.execute(
            f"INSERT INTO pozicovna (nazov, popis, km, rok, kw, objem, spotreba, cenaden, cenatyzden, typ,obrazky) VALUES ({otazniky})",
            zudaje,
        )
        tab.commit()
        tab.close()

    def filtruj(self, filtre):
        """
        This is a Python function that filters data based on certain criteria and returns the filtered
        results.

        :param filtre: `filtre` is a list of filter parameters used to filter the results of a database
        query. The function `filtruj` takes this list as an argument and uses it to construct a SQL
        query to retrieve the relevant data from the database. The filters can include criteria such as
        the name of the
        """
        reqest = f" WHERE rented = {0}"
        km_od = None
        kw_od = None
        for cis, i in enumerate(filtre):
            if cis == 0 and i != "":

                c = "WHERE nazov "
                if c not in reqest:
                    reqest += " AND nazov LIKE " + "'%" + i + "%'"
            if cis == 1 and i != "":
                try:
                    i = int(i)
                    if reqest != "":
                        if filtre[cis + 1] != "":
                            try:
                                xx = int(filtre[cis + 1])
                                reqest += (
                                    " AND  km  BETWEEN " + str(i) + " AND " + str(xx)
                                )
                            except:
                                pass
                        else:
                            reqest += " AND  km >= " + str(i)
                    else:
                        if filtre[cis + 1] != "":
                            try:
                                xx = int(filtre[cis + 1])
                                reqest += (
                                    " WHERE km BETWEEN " + str(i) + " AND " + str(xx)
                                )
                            except:
                                pass
                        else:
                            reqest += " WHERE km >= " + str(i)
                    km_od = i

                except:
                    pass
            if cis == 2 and i != "" and km_od is None:
                try:
                    i = int(i)
                    if reqest != "":
                        reqest += " AND  km <= " + str(i)
                    else:
                        reqest += " WHERE km <= " + str(i)
                except:
                    pass
            if cis == 3 and i != "" and "WHERE kw" not in reqest:
                try:
                    i = int(i)
                    if reqest != "":
                        if filtre[cis + 1] != "":
                            try:
                                xx = int(filtre[cis + 1])
                                reqest += (
                                    " AND  kw  BETWEEN " + str(i) + " AND " + str(xx)
                                )
                            except:
                                pass
                        else:
                            reqest += " AND  kw >= " + str(i)
                    else:
                        if filtre[cis + 1] != "":
                            try:
                                xx = int(filtre[cis + 1])
                                reqest += (
                                    " WHERE kw BETWEEN " + str(i) + " AND " + str(xx)
                                )
                            except:
                                pass
                        else:
                            reqest += " WHERE kw >= " + str(i)
                    kw_od = i

                except:
                    pass
            if cis == 4 and i != "" and kw_od is None and "WHERE kw" not in reqest:
                try:
                    i = int(i)
                    if reqest != "":

                        reqest += " AND  kw <= " + str(i)
                    else:
                        reqest += " WHERE kw <= " + str(i)
                except:
                    pass
            if cis == 5 and i != "" and "WHERE rok" not in reqest:
                try:
                    i = int(i)
                    if reqest != "":
                        if filtre[cis + 1] != "":
                            try:
                                xx = int(filtre[cis + 1])
                                reqest += (
                                    " AND  rok  BETWEEN " + str(i) + " AND " + str(xx)
                                )
                            except:
                                pass
                        else:
                            reqest += " AND rok >= " + str(i)
                    else:
                        if filtre[cis + 1] != "":
                            try:
                                xx = int(filtre[cis + 1])
                                reqest += (
                                    " WHERE rok BETWEEN " + str(i) + " AND " + str(xx)
                                )
                            except:
                                pass
                        else:
                            reqest += " WHERE rok >= " + str(i)
                    kw_od = i

                except:
                    pass
            if cis == 6 and i != "" and kw_od is None and "WHERE rok" not in reqest:
                try:
                    i = int(i)
                    if reqest != "":

                        reqest += " AND  rok <= " + str(i)
                    else:
                        reqest += " WHERE rok <= " + str(i)
                except:
                    pass

        tab = sqlite3.connect("pozicovna.db")
        c = tab.cursor()

        self.request_dd = reqest

        self.request = "SELECT * FROM pozicovna " + reqest + self.order

        # self.request = "SELECT * FROM pozicovna ORDER BY id DESC"
        c.execute(self.request)
        self.my = c.fetchall()
        super().ponuka(self.my)

        tab.commit()
        tab.close()


CarRent()
tkinter.mainloop()
