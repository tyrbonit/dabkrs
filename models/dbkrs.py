# -*- coding: utf-8 -*-
from bkrstools import repres_perevod,sokr_perevod,reshala
from gluon import current#Локальный объект потока исполнения запроса (используется в модулях)

slovar = db.define_table('slovar',
    Field('slovo','string',unique=True,label="Слово"),
    Field('pinyin',label="Пиньин"),
    Field('perevod',"text",label="Перевод"),
    Field('bywords_short',"text",label="Краткий перевод в пословном"),
    Field('use_short','boolean',label="Использ. сокр."),
    Field('dlina','integer',label="Длина"),
    Field('choiselist','list:string', default=[],label="Варианты"),
    Field('linksto','list:reference slovar', default=[],writable=False, readable=False,label="Ссылка на"),
    Field('linksfrom','list:reference slovar', default=[],writable=False, readable=True,label="Ссылка c"),
    Field('processed', 'boolean', default=False,label="Обработан"),
    Field('is_example', 'boolean', default=False,label="Это пример?"),
    Field('is_valid', 'boolean',label="Валидный"),
    Field('with_appendix', 'boolean',label="С дополнением"),
    Field('with_examples', 'boolean',label="С примерами"),
    Field('with_ru', 'boolean',label="С русским переводом"),
    Field('bywords_out', 'boolean',label="Пропускать в пословном"),
    auth.signature,#Поля пользователей
    Field('is_active', 'boolean',writable=False, readable=False, default=True),#для контроля версий
    #migrate=True, fake_migrate=True,#если база заполнена вне web2py, то расскомментировать, запустить просмотр базы и обратно закомментировать
    #rname="dabkrs"#если таблица в базе имеет другое реальное имя, то задать реальное имя  (для полей тоже есть rname, на случай миграции с другой БД)
)
#Вычисляемые поля (автоматически при вставке и обновлении)
slovar.dlina.compute=lambda row:len(row.slovo if isinstance(row.slovo,unicode) else unicode(row.slovo, 'utf-8'))
slovar.is_valid.compute=lambda row:re.search(r"[a-zA-Z 0-9\[\](),.-]",row.slovo if isinstance(row.slovo,unicode) else unicode(row.slovo, 'utf-8'),re.U)==None
slovar.with_appendix.compute=lambda row:re.search(r"\[apndx\]",row.perevod)!=None
slovar.with_examples.compute=lambda row:re.search(r"\[ex{0,1}\]",row.perevod)!=None
slovar.with_ru.compute=lambda row:re.search(u"[а-яёА-ЯЁ]",row.perevod if isinstance(row.perevod,unicode) else unicode(row.perevod, 'utf-8'),re.U)!=None
#Виртуальные поля
slovar.choisecalc=Field.Virtual('choisecalc',lambda row:"",label="Тест варианты")
slovar.short=Field.Virtual('short',lambda row:"",label="Тест примеры")

"""slovar._enable_record_versioning(#включаем версионность
    archive_db=db,#версии храним в этойже базе
    archive_name='slovar_archive',#в архивной таблице с этим названием
    current_record='current_slovo',#с этим полем идентификатора в архивной таблице на измененную запись
    is_active='is_active',#полем для пометки об удалении в основной таблице
    current_record_label="Измененная запись"
)"""
current.db=db#Создает атрибут со ссылкой на базу данных (для ипользования в модулях)
current.slovar=slovar#Создает атрибут со ссылкой на таблицу в базе данных (для ипользования в модулях)
#Html - представления полей, используемые по умолчанию
slovar.slovo.represent=lambda slovo,row:DIV(slovo,_class="ch")#Помещаем в контейнер, чтобы применить стили оформления согласно классу
slovar.pinyin.represent=lambda pinyin,row:DIV(repres_perevod(pinyin),_class="py")#Помещаем в контейнер, чтобы применить стили оформления согласно классу
slovar.perevod.represent=repres_perevod#Заменяем DSL-тэги на HTML-тэги, помещаем в контейнеры, чтобы применить стили оформления согласно классам
slovar.bywords_short.represent=repres_perevod#Заменяем DSL-тэги на HTML-тэги, помещаем в контейнеры, чтобы применить стили оформления согласно классам
slovar.linksfrom.represent=lambda value,row:UL([A(x,_href=URL(c="slovar",f="slovo",vars=dict(id=x))) for x in value])
slovar.choiselist.represent=lambda value,row:UL([x for x in value])
slovar.short.represent=lambda value,row: TABLE([[x.slovo,x.pinyin,x.perevod]for x in extract(row.perevod)],_border="2px")
slovar.choisecalc.represent=lambda value,row: UL(sokr_perevod(row.perevod,row.slovo))
