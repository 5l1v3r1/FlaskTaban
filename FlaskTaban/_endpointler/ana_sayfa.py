# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from FlaskTaban import app
from flask import render_template, jsonify

@app.route('/')
def ana_sayfa():

    return render_template(
        'ana_sayfa.html',
        baslik = "Merhaba Flask!",
        icerik = "Ben Python Dosyasından Değişken Olarak Geldim.."
    )