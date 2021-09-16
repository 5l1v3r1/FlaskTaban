# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from FlaskTaban import app, FlaskTabanDB, jwt_decode
from flask import render_template, request, jsonify, redirect, url_for, session

@app.route('/monitor', methods=['GET', 'POST'])
def monitor():
    if not session.get("token"):
        return redirect(url_for('giris_yap'))

    token     = jwt_decode(session.get('token'))
    database  = FlaskTabanDB()
    mail      = token["mail"]

    if request.method == 'GET':
        database.log_salla(mail, "tm", "ok", "kkk", "bks", "abv")

    kullanici = lambda : database.kull_ver(mail)

    if (request.method == 'POST') and (kullanici()['log']):
        return jsonify(kullanici()['log'][-1])

    return render_template(
        'monitor.html',
        baslik      = "Monitör",
        loglar      = kullanici()['log'][:-1]
    )