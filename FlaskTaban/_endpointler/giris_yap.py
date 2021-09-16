# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from FlaskTaban import app, FlaskTabanDB, MONGO_DB, jwt_encode
from flask import render_template, request, session, redirect, url_for

@app.route('/giris_yap', methods=['GET', 'POST'])
def giris_yap():
    if session:
        return redirect(url_for('ayar'))

    hata = ""
    if request.method == 'POST':
        if not request.form['mail']:
            hata = 'eposta giriniz..'
        elif not request.form['password']:
            hata = 'password giriniz..'
        else:
            database  = FlaskTabanDB()
            mail = request.form['mail']
            if not MONGO_DB:
                kullanici = database.ara(
                    (database.sorgu.mail  ==  request.form['mail'])
                    and
                    (database.sorgu.sifre ==  request.form['password'])
                )
            else:
                kullanici = database.ara({'mail': request.form['mail'], 'sifre': request.form['password']})

            if kullanici:
                token = jwt_encode(mail)
                session['token'] = token
                return redirect(url_for('monitor'))
            else:
                hata = 'e-Posta veya Şifre Yanlış..'

    return render_template(
        'giris_yap.html',
        baslik = "Giriş Sayfası",
        hata   = hata
    )

@app.route('/cikis_yap')
def cikis_yap():
    if session:
        session.clear()

    return redirect(url_for('ana_sayfa'))
