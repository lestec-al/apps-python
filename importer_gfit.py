import json, time, datetime, requests


data = []
idx = 0
with open("google_fit_data.json") as f:

    for i in json.load(f)['Data Points']:
        idx += 1

        value = i["fitValue"][0]["value"]["fpVal"]
        if type(value) == type(21.15):
            value = round(value, 1)
        else:
            value = float(value)

        # date = datetime.datetime.fromtimestamp(i["endTimeNanos"] // 1000000000).strftime("%Y.%m.%d")
        d = i["endTimeNanos"] // 1000000
        # date2 = datetime.datetime.fromtimestamp(d / 1000).strftime("%Y.%m.%d")
        # print(value, " - ", date, date2)

        data.append({
            "type": "st_e",
            "st_v_id": idx,
            "st_v_value": value,
            "st_v_date": str(d),
            "parent_id": 1
        })

# response = requests.post("https://lestec.pythonanywhere.com/client_server/", json=data)