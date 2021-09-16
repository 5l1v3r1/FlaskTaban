# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.
 
from tinydb import TinyDB, Query
from tinydb.operations import delete, add
from tinydb.queries import QueryLike
import datetime, pytz

class FlaskTabanDB:
    tarih = lambda : datetime.datetime.now(pytz.timezone("Turkey")).strftime("%d-%m-%Y %X")

    def __init__(self):
        TinyDB.default_table_name = self.__class__.__name__
        self.db    = TinyDB(f"@FlaskTaban_DB.json", ensure_ascii=False, indent=2, sort_keys=False)
        self.sorgu = Query()

    def ara(self, sorgu:QueryLike):
        arama = self.db.search(sorgu)
        say   = len(arama)
        if say == 1:
            return arama[0]
        elif say > 1:
            cursor = arama
            return {
                bak['mail'] : {
                    "ad_soyad" : bak['ad_soyad'],
                    "kull_adi" : bak['kull_adi'],
                    "sifre"    : bak['sifre'],
                    "log"      : bak['log'],
                }
                for bak in cursor
            }
        else:
            return None

    def ekle(self, mail, ad_soyad, sifre, kull_adi):
        if (not self.ara(self.sorgu.uye_id == mail)) and (not self.ara(self.sorgu.kull_adi == kull_adi)):
            return self.db.insert({
                "mail"      : mail.strip(),
                "kull_adi"  : kull_adi.strip(),
                "ad_soyad"  : ad_soyad.strip(),
                "sifre"     : sifre.strip(),
                "log"       : []
            })
        else:
            return None

    def sil(self, mail):
        if not self.ara(self.sorgu.mail == mail):
            return None

        # self.db.update(delete('mail'), self.sorgu.mail == mail)
        self.db.remove(self.sorgu.mail == mail)
        return True

    def kull_ver(self, mail:str):
        data = self.ara(self.sorgu.mail == mail)
        if not data:
            return None
        else:
            return data

    def log_salla(self, mail, bir, iki, uc, dort, bes):
        kullanici = self.ara(self.sorgu.mail == mail)
        if not kullanici:
            return None

        self.db.update(add(
            'log', [
                {
                    "tarih" : FlaskTabanDB.tarih(),
                    "bir"   : bir,
                    "iki"   : iki,
                    "uc"    : uc,
                    "dort"  : dort,
                    "bes"   : bes
                }
            ]
        ))

        return self.ara(self.sorgu.mail == mail)