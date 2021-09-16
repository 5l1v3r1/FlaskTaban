# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.
 
import pymongo, datetime, pytz
from FlaskTaban import MONGO_DB

class FlaskTabanDB:
    tarih = lambda : datetime.datetime.now(pytz.timezone("Turkey")).strftime("%d-%m-%Y %X")

    def __init__(self):
        client          = pymongo.MongoClient(MONGO_DB)
        db              = client['FLASK']
        self.collection = db['FlaskTaban']

    def ara(self, sorgu:dict):
        say = self.collection.count_documents(sorgu)
        if say == 1:
            return self.collection.find_one(sorgu, {'_id': 0})
        elif say > 1:
            cursor = self.collection.find(sorgu, {'_id': 0})
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
        if (not self.ara({'mail': mail})) and (not self.ara({'kull_adi': kull_adi})):
            return self.collection.insert_one({
                "mail"      : mail.strip(),
                "kull_adi"  : kull_adi.strip(),
                "ad_soyad"  : ad_soyad.strip(),
                "sifre"     : sifre.strip(),
                "log"       : []
            })
        else:
            return None

    def sil(self, mail):
        if not self.ara({'mail': mail}):
            return None

        self.collection.delete_one({'mail': mail})
        return True

    def kull_ver(self, mail:str):
        data = self.ara({'mail': mail})
        if not data:
            return None
        else:
            return data

    def log_salla(self, mail, bir, iki, uc, dort, bes):
        kullanici = self.ara({'mail': mail})
        if not kullanici:
            return None

        self.collection.update_one({'mail': mail},
            {
                "$push" : {
                    "log": {
                        "tarih" : FlaskTabanDB.tarih(),
                        "bir"   : bir,
                        "iki"   : iki,
                        "uc"    : uc,
                        "dort"  : dort,
                        "bes"   : bes
                    }
                }
            }, upsert = True
        )

        return self.ara({'mail': mail})