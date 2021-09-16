# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from FlaskTaban import app, FlaskTabanDB
from flask import render_template, request, session, redirect, url_for

@app.route('/kayit_ol', methods=['GET', 'POST'])
def kayit_ol():
    if session:
        return redirect(url_for('ayar'))

    hata = ""
    if request.method == 'POST':
        if not request.form['name']:
            hata = 'isim ve soyisim giriniz..'
        elif not request.form['username']:
            hata = 'kullanıcı adınızı giriniz..'
        elif not request.form['mail']:
            hata = 'eposta giriniz..'
        elif not request.form['password']:
            hata = 'sifre giriniz..'
        else:
            database = FlaskTabanDB()
            kayit = database.ekle(request.form['mail'], request.form['name'], request.form['password'], request.form['username'])
            database.log_salla(request.form['mail'], "Kayit", "Ol", request.form['name'], request.form['password'], request.form['username'])
            if kayit:
                return render_template('giris_yap.html', baslik="Giriş Sayfası", basari=f"{request.form['mail']} Kaydı Başarılı..")
            else:
                hata = 'E-Posta Adresi veya Kullanıcı Adı Kullanılıyor..'

    return render_template(
        'kayit_ol.html',
        baslik = "Kayıt Sayfası",
        hata   = hata
    )