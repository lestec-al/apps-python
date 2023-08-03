import json, xml.etree.ElementTree as et

tree = et.parse('sportsman_data.xml')
root = tree.getroot()
new = []
for i in range(50):
    try:
        attr = root[i].attrib
    except Exception as e:
        break

    attr = root[i].attrib
    if attr["name"] == "pref_statistics_pull_ups" or attr["name"] == "pref_statistics_push_ups":
        print(attr)

        data = root[i].text
        data = data.replace('{"date":1611812186143,"rem":true},', "")
        data = eval(data)

        idx = 1
        for o in data:
            # print(o)

            min = str(o["dur"] // 60)
            sec = str(o["dur"] % 60)
            if len(min) < 2:
                min = "0"+min
            if len(sec) < 2:
                sec = "0"+sec

            dict_o = {
                "type":"ex_e",
                "st_e_id":idx,
                "st_e_res_s":sum(o["reps"]),
                "st_e_res_l":" + ".join(map(str, o["reps"])),
                "st_e_time":min+":"+sec,
                "st_e_date":str(o["date"]),
                "st_e_weights":"",
                "parent_id":1 if attr["name"] == "pref_statistics_pull_ups" else 2
            }
            new.append(dict_o)

            idx += 1


with open("data_r.json", 'r+') as f:
    exist_data = json.load(f)
    for i2 in new:
        exist_data.append(i2)
    f.seek(0)
    json.dump(exist_data, f, separators=(',', ':'), indent=None)



"""
{"type":"ex_e","st_e_id":156,"st_e_res_s":38,"st_e_res_l":"15 + 14 + 9","st_e_time":"07:45","st_e_date":"1677434400000","st_e_weights":"","parent_id":2}
{"type":"ex_e","st_e_id":262,"st_e_res_s":52,"st_e_res_l":"16 + 11 + 9 + 9 + 7","st_e_time":"14:21","st_e_date":"1677434400000","st_e_weights":"","parent_id":1}
"""