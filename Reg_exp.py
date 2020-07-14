# -*- coding: utf-8 -*-
from pprint import pprint
import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv

def find_pattern(s, re):
    res = re.findall(s)
    if len(res) > 0:
        s = s.replace(res[0], '')
        return s, res[0]
    return s, None

def find_phone(s, ph_re, ad_re):
    ad = ad_re.findall(s)
    if len(ad) > 0:
        s = s.replace(ad[0], '')
    phone = ph_re.findall(s)
    if len(phone) > 0:
        phone = phone[0][1:]
        for i in phone:
            s = s.replace(i, '')
        
        if len(ad) > 0:
            s = s.replace(ad[0], '')
            return s, f'{phone[0]}({phone[1]})-{phone[2]}-{phone[3]}-{phone[4]} {ad[0]}'
        return s, f'{phone[0]}({phone[1]})-{phone[2]}-{phone[3]}-{phone[4]}'
    return s, None


def get_name(s):
    name_re = re.compile('([а-яА-Я]+)[\,\s]+([а-яА-Я]+)')
    name_raw = name_re.match(s)
    name = f'{name_raw.group(1)},{name_raw.group(2)}'
    s = s[name_raw.end():]
    return s, name



with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код

name_re = re.compile('([а-яА-Я]+)[\,\s]+([а-яА-Я]+)')
re_s = {
        'surname': re.compile('([А-Я][а-я]+(?:ович|евич|ич|овна|евна|ична|инична))'),
        'email' : re.compile('([\d\w\.\-\_]+@[\d\w\.\-\_]+)'),
        'organization': re.compile('\,([а-яА-Я]+)\,'),
        
    }

phone_re = re.compile('(((?:\+7|8)).*(\d{3}).*(\d{3}).*(\d{2}).*(\d{2}))')
add_re = re.compile('(доб\. \d{4})')
pos_re = re.compile('\,([\w\–\-\ ]{5,})\,')

templist = [','.join(i) for i in contacts_list]
header = templist.pop(0)


phonebook = {}
for i in range(len(templist)):
    templist[i], name = get_name(templist[i])
    
    if name not in phonebook:
        phonebook[name] = {}
        
    for j in re_s:
        templist[i], info = find_pattern(templist[i], re_s[j])
        if info:
            phonebook[name][j] = info
        else:
            if j not in phonebook[name]:
                phonebook[name][j] = ''

    templist[i], phone = find_phone(templist[i], phone_re, add_re)
    if phone:
        phonebook[name]['phone'] = phone
    else:
        if 'phone' not in phonebook[name]:
            phonebook[name]['phone'] = ''
            
    
            
    
for i in templist:
    print(pos_re.findall(i))
    

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)