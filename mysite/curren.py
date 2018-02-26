def currency(request, source, result, amount):
    import sqlite3
    import requests
    import time
    import json

    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    from django.http import HttpResponse

    def check_db():

        # Создание и наполнение таблицы
        c.executescript("""
            CREATE TABLE IF NOT EXISTS currency (name varchar primary key, value real, time integer);
            INSERT  OR IGNORE INTO currency (name, time) VALUES ('czk',1),('eur',1),('pln',1),('usd',1);
            """)

        return ()


    def update_db():
        r = {}
        try:
            r = requests.get('https://openexchangerates.org/api/latest.json?app_id='+data['app_id']).json()
        except:
            return HttpResponse(status=500)

        try:
            czk = r['rates']['CZK']
            eur = r['rates']['EUR']
            pln = r['rates']['PLN']
            usd = 1

            c.execute("UPDATE currency SET  time = strftime('%s','now')")
            c.execute("UPDATE currency SET  value =%s WHERE name = 'czk' " % (czk))
            c.execute("UPDATE currency SET  value =%s WHERE name = 'eur' " % (eur))
            c.execute("UPDATE currency SET  value =%s WHERE name = 'pln' " % (pln))
            c.execute("UPDATE currency SET  value =%s WHERE name = 'usd' " % (usd))
            # Подтверждение отправки данных в базу
            conn.commit()
        except:
            return HttpResponse(status=500)

    # Подключение к базе
    conn = sqlite3.connect(data['db_name'])
    # Создание курсора
    c = conn.cursor()
    try:
        amount = float(amount)
    except:
        return HttpResponse(status=415)
    # amount содержит что-то, что может быть спарсено, но во время парсинга произошла любая ошибка
    check_db()
    c.execute("SELECT time FROM currency WHERE name='czk'")
    timeold = c.fetchall()[0]
    dat = time.time()
    # Если прошли сутки, то обновить показатели
    if (timeold[0] + 60 * 60 * 24) < dat:
        update_db()


    c.execute("SELECT value FROM currency")
    cur = c.fetchall()
    print(cur)
    src = cur[source][0]
    res = cur[result][0]

    if int(source) == 3:
        summ = amount * res
    if int(result) == 3:
        summ = 1/src * amount
    else: summ = res/src * amount

    # Завершение соединения
    c.close()
    conn.close()
    return HttpResponse(round(summ, 2))

