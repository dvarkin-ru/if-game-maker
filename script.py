import json
import os # TODO: импортозаместить ос
from tkinter import *
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter.filedialog import asksaveasfile, askopenfile

q_id_key, ans_key  = "Вопрос", "Ответы"

def add_dial():
    q_id = entries[q_id_key].get().strip()
    if d.get(q_id):
        showerror(title="Ошибка", message="Такой уже есть")
        return
    box.insert(END, q_id)
    d[q_id] = dict()
    item_d = d[q_id]
    for k, v in entries.items():
        item_d[k] = v.get().strip()
    d[q_id][ans_key] = []
    box.select_clear(0, END)
    box.select_set(END)
    clear_ans()

def upd_dial():
    q_id = entries[q_id_key].get().strip()
    if not d.get(q_id):
        showerror(title="Ошибка", message="Выберите диалог")
        return
    d[q_id]["Текст вопроса"] = entries["Текст вопроса"].get().strip()

def del_dial():
    select = list(box.curselection())
    if len(select)<1:
        return
    for i in select:
        d.pop(box.get(i))
        box.delete(i)
    clear_ans()

def onselectdial(evt):
    sel = box.curselection()
    if len(sel)<1:
        return
    selected = box.get(int(sel[0]))
    for k in entries:
        entries[k].delete(0, END)
        entries[k].insert(0, d[selected][k])
    for k in entries_ans:
        entries_ans[k].delete(0, END)
    q_id = entries[q_id_key].get()
    answer_box.delete(0, END)
    ans = d[q_id][ans_key]
    for a in ans:
        answer_box.insert(END, a["Текст ответа"])

d = dict()

root = Tk()
root.title("Instead of INSTEAD")

f_main = Frame(root)
f_main.pack()

f = Frame(f_main)
f.pack(side=LEFT, fill=Y)
Label(f, text="Диалог").pack()
box = Listbox(f)
box.pack(side=LEFT, fill=Y)
box.bind('<<ListboxSelect>>', onselectdial)
scroll = Scrollbar(f, command=box.yview)
scroll.pack(side=LEFT, fill=Y)
box.config(yscrollcommand=scroll.set)
entries = {q_id_key: None, "Текст вопроса": None}
for k in entries:
    entries[k] = Entry(f, width=40)
    Label(f, text=k).pack()
    entries[k].pack(fill=X)
Button(f, text="Добавить диалог", command=add_dial).pack(fill=X)
Button(f, text="Пересохранить текст вопроса", command=upd_dial).pack(fill=X)
Button(f, text="Удалить диалог", command=del_dial).pack(fill=X)

def clear_ans():
    for k in entries_ans:
        entries_ans[k].delete(0, END)
    answer_box.delete(0, END)

def add_ans():
    q_id = entries[q_id_key].get().strip()
    if q_id == '' or not d.get(q_id):
        showerror(title="Ошибка", message="Выберите диалог")
        return
    ans = entries_ans["Текст ответа"].get().strip()
    oth_ans = [a for a in d[q_id][ans_key] if a["Текст ответа"]==ans]
    if len(oth_ans) > 0:
        showerror(title="Ошибка", message="Такой уже есть")
        return
    answer_box.insert(END, ans)
    item_d = dict()
    d[q_id][ans_key].append(item_d)
    for k, v in entries_ans.items():
        item_d[k] = v.get().strip()
        entries_ans[k].delete(0, END)

def del_ans():
    q_id = entries[q_id_key].get() #.strip()
    if q_id == '' or not d.get(q_id):
        showerror(title="Ошибка", message="Выберите диалог")
        return
    answers = d[q_id][ans_key]
    select = list(answer_box.curselection())
    for i in select:
        answers.pop(i)
        answer_box.delete(i)

def onselectans(evt):
    sel = answer_box.curselection()
    if len(sel)<1:
        return
    selected = int(sel[0])
    q_id = entries[q_id_key].get().strip()
    if q_id == '' or not d.get(q_id):
        showerror(title="Ошибка", message="Выберите диалог")
        return
    for k in entries_ans:
        entries_ans[k].delete(0, END)
        entries_ans[k].insert(0, d[q_id][ans_key][selected][k])

f = Frame(f_main)
f.pack(side=LEFT, fill=Y)
Label(f, text = "Ответ").pack()
answer_box = Listbox(f)
answer_box.pack(side=LEFT, fill=Y)
scroll = Scrollbar(f, command=answer_box.yview)
scroll.pack(side=LEFT, fill=Y)
answer_box.config(yscrollcommand=scroll.set)
answer_box.bind('<<ListboxSelect>>', onselectans)
entries_ans = {"Текст ответа": None, "Следующий вопрос": None,
               "Условие": None, "Действие": None}
for k in entries_ans:
    entries_ans[k] = Entry(f, width=40)
    Label(f, text=k).pack()
    entries_ans[k].pack(fill=X)
Button(f, text="Добавить ответ", command=add_ans).pack(fill=X)
Button(f, text="Удалить ответ", command=del_ans).pack(fill=X)

def save_json():
    f = asksaveasfile(initialfile = 'room.json',
                      defaultextension=".json",
                      filetypes=[("Json комнаты","*.json"),])
    if not f:
        return
    try:
        json.dump(d, f, ensure_ascii=False, indent=' ')
    except:
        showerror(title="Ошибка", message="Не удалось сохранить")
    finally:
        f.close()

def open_json():
    global d
    f = askopenfile(initialfile = 'room.json',
                    defaultextension=".json",
                    filetypes=[("Json комнаты","*.json"),])
    if not f:
        return
    d = json.load(f)
    f.close()
    for k in entries:
        entries[k].delete(0, END)
    box.delete(0, END)
    clear_ans()
    for r in d:
        box.insert(END, r)

def syn_lua_file(f):
    name = os.path.basename(f.name).split(".")[0]
    dlg = 'dlg {\nnam = "'+name+'";\nphr = {\n\n'+lua_phrases()+"}}"
    f.write(dlg)

def lua_phrases():
    enter = [(k, v) for k, v in d.items() if k=='вход']
    if len(enter) != 1:
        showerror(title="Ошибка", message="Нет диалога 'вход'")
        raise ValueError
    res = q_content(*enter[0])
    for k, v in d.items():
        if k != 'вход':
            res += q_content(k, v)
    return res

def q_content(k, v):
    res = "{"
    if k != 'вход':
        res += "false, "
    res += "'#"+k+"', [[" + v["Текст вопроса"] + "]], always=true,\n"
    for a in v[ans_key]:
        res+="{'"+a["Текст ответа"]+"', "
        if a["Условие"] != '':
            res += "cond = function() return "+a["Условие"]+" end, "
        res += "next='#"+a["Следующий вопрос"]+"', always=true"
        if a["Действие"] != '':
            res += ", function() "+a["Действие"]+" end"
        res += "},\n"
    res += '},\n\n'
    return res

def save_lua():
    f = asksaveasfile(initialfile = 'room.lua', defaultextension=".json",
                      filetypes=[("INSTEAD LUA","*.lua"),])
    if not f:
        return
##    try:
    syn_lua_file(f)
##    except:
##        showerror(title="Ошибка", message="Не удалось сохранить")
##    finally:
##        f.close()

Button(root, text="Сохранить в JSON", command=save_json).pack(fill=X)
Button(root, text="Открыть JSON", command=open_json).pack(fill=X)
Button(root, text="Синтезировать INSTEAD LUA", command=save_lua).pack(fill=X)

root.mainloop()
