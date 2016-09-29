# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bkrstools import text_tokenizer,repres_perevod,cut_perevod,sokr_perevod,reshala,splitby

def index():
    """Действие по умолчанию, показывает таблицу словарной базы данных"""
    form=SQLFORM.grid(
        slovar,
        csv=False,
        #fields=[slovar.slovo,slovar.pinyin,slovar.perevod,slovar.spisok],
    )
    return dict(form=form)

def slovintersection(x):
    return CAT(SPAN(x.slovo[:x.lspan],_class="text-warning") if x.lspan!=None else "",
               x.slovo[x.lspan:x.rspan] if x.rspan!=None or x.lspan!=None else x.slovo,
               SPAN(x.slovo[x.rspan:],_class="text-warning") if x.rspan!=None else "")

#@cache.action(cache_model=cache.ram)
def slovo():
    return otvet()


def otvet():
    if request.vars.id!=None:
        sl=slovar(request.vars.id)
        if sl!=None:request.vars.slovo=sl.slovo
    if request.vars.slovo==None:return ""
    if isinstance(request.vars.slovo,list):request.vars.slovo=request.vars.slovo[-1]
    text=unicode(request.vars.slovo, 'utf-8')#Декодируем строку на всякий случай
    rez=reshala(text)#Расчленение текста и выдача списка найденных слов в базе
    first=rez.pop(0)#Первым объектом идет весь текст, и если он есть базе, то появятся соответсвующие атрибуты
    #Словарный блок
    first=DIV(
        DIV("Словарный:",_class="txt-label ru"),
        DIV(first.slovo,_class="hidden",_id="hidekitext"),
        DIV(first.slovo,_class="ch2 col-md-12",_id="kitext",data={'spy':'affix','offset-top':'50'}),
        DIV(first.pinyin,_class="py"),
        DIV(repres_perevod(first.perevod,first.slovo),_class="ru"),
        _class="iskomyi-text row"
        )
    proc_func=cut_perevod#Функция обработки статьи перевода
    #Список пословных блоков
    bywords=DIV(
        DIV("Пословный:",_class="txt-label ru"),
        *[DIV(
            A(slovintersection(x),_class="black ch",_href=URL("slovo",vars=dict(slovo=x.slovo))),#Найденое слово, после обработки на смежность
            DIV(repres_perevod(x.pinyin),_class="py"),#Пиньин
            DIV(proc_func(x.perevod,x.slovo),_class="ru"),#Обработанная статья перевода
            _class="slovo col-md-3 col-sm-4 col-xs-6",#Класс блока
            _i=str(x.start)+"-"+str(x.end),#расположение слова в тексте
            _n=str(i),#номер блока(отсчет с нуля)
            _slovo=x.slovo#само слово
                )
             for i,x in enumerate(rez)],
        _class="row",
        _id="shkatulka-slov"
    )
    #Блок псевдоперевода (экспериментальный), берет только первые слова из списка и сшивает в предложение
    slovlist=DIV(
        DIV("Псевдоперевод:",_class="txt-label ru"),
        " ".join([x.choiselist[0] if x.choiselist!=None and x.choiselist!=[] else x.slovo for x in rez if x!=None]),
        _class="slovlist row"
    )
    return dict(first=first,bywords=bywords,slovlist=slovlist)
