# -*- coding: utf-8 -*-

################################################################################
## Purple Shift 2.0 - «По ту сторону смены»
## Сквозное состояние героя и команды, три фазы дня, расширенный финал,
## эпилоги и «Новая смена+».
################################################################################

default ps2_fatigue = 0
default ps2_pressure = 0
default ps2_resolve = 0

default ps2_team_trust = 0
default ps2_team_fear = 0
default ps2_team_fracture = 0
default ps2_team_aid = 0

default ps2_day_intentions = {}
default ps2_after_choices = {}
default ps2_decision_map = []
default ps2_scenes_seen = []
default ps2_silences = []
default ps2_phase = "до смены"
default ps2_new_shift_plus_active = False
default ps2_final_preparation = None
default ps2_route_crisis_result = None


image cg ps2_platform = "images/cg/ps2_platform.png"
image cg ps2_badge = "images/cg/ps2_badge.png"
image cg ps2_morning = "images/cg/ps2_morning.png"
image cg ps2_afterimage = "images/cg/ps2_afterimage.png"


transform ps2_memory_camera:
    xalign 0.5
    yalign 0.5
    zoom 1.045
    alpha 0.0
    ease 0.8 alpha 1.0 zoom 1.01


init 40 python:
    if getattr(persistent, "ps2_new_shift_plus_unlocked", None) is None:
        persistent.ps2_new_shift_plus_unlocked = False

    if getattr(persistent, "ps2_completed_runs", None) is None:
        persistent.ps2_completed_runs = 0

    if getattr(persistent, "ps2_last_decision_map", None) is None:
        persistent.ps2_last_decision_map = []

    if getattr(persistent, "ps2_seen_echoes", None) is None:
        persistent.ps2_seen_echoes = []

    ps2_cgs = [
        ("ps2_platform", "Остановка после шума", "images/cg/ps2_platform.png"),
        ("ps2_badge", "Жилет, который стал тяжелее", "images/cg/ps2_badge.png"),
        ("ps2_morning", "Утро без будильника", "images/cg/ps2_morning.png"),
        ("ps2_afterimage", "Склад помнит", "images/cg/ps2_afterimage.png"),
    ]

    known_cg_ids = {item[0] for item in ps_cg_catalog}
    for cg_item in ps2_cgs:
        if cg_item[0] not in known_cg_ids:
            ps_cg_catalog.append(cg_item)

    ps2_documents = [
        (
            "decision_map",
            "Карта семи дней",
            "Не список хороших и плохих ответов, а след решений: кого они защитили, чего стоили и кто их запомнил.",
        ),
        (
            "collective_state",
            "Неформальный отчёт смены",
            "Доверие, страх, раскол и взаимовыручка. Четыре показателя, которых нет в официальной панели.",
        ),
        (
            "after_shift_notes",
            "Записи после проходной",
            "Короткие мысли, набранные тогда, когда рабочий день закончился, а смена внутри ещё нет.",
        ),
    ]

    known_document_ids = {item[0] for item in ps_document_catalog}
    for document_item in ps2_documents:
        if document_item[0] not in known_document_ids:
            ps_document_catalog.append(document_item)

    ps2_achievements = [
        (
            "three_phases",
            "До, внутри и после",
            "Прожить все три стороны одного рабочего дня.",
        ),
        (
            "collective_memory",
            "Нас здесь было больше одного",
            "Собрать смену, в которой взаимовыручка сильнее страха и раскола.",
        ),
        (
            "hard_truth",
            "Правда без удобного ответа",
            "Принять решение, которое помогло людям не сразу.",
        ),
        (
            "new_shift_plus",
            "Я это уже слышал",
            "Начать «Новую смену+» и заметить первый повтор.",
        ),
        (
            "beyond_shift",
            "По ту сторону смены",
            "Завершить историю с полной картой решений.",
        ),
    ]

    known_achievement_ids = {item[0] for item in ps_achievement_catalog}
    for achievement_item in ps2_achievements:
        if achievement_item[0] not in known_achievement_ids:
            ps_achievement_catalog.append(achievement_item)

    ps2_messages = [
        {
            "id": "ps2_self_day1",
            "day": 1,
            "sender": "Черновики",
            "time": "07:03",
            "preview": "Зачем я сюда пришёл?",
            "incoming": [
                "Зачем я сюда пришёл? Деньги - честный ответ, но не полный.",
                "Допишу после смены, если останутся силы.",
            ],
            "replies": [
                {
                    "id": "keep",
                    "title": "«Не удалять.»",
                    "answer": "Не удалять. Даже если вечером ответ будет неприятным.",
                    "reaction": "Черновик сохранён.",
                    "effects": {"ps2_resolve": 1, "ps_integrity": 1},
                },
                {
                    "id": "erase",
                    "title": "«Не сейчас.»",
                    "answer": "Не сейчас. Сегодня нужно просто дойти.",
                    "reaction": "Текст удалён. Вопрос остался.",
                    "effects": {"ps_endurance": 1, "ps2_pressure": -1},
                },
            ],
        },
        {
            "id": "ps2_group_count",
            "day": 3,
            "sender": "Смена",
            "time": "04:58",
            "preview": "Кто вышел с линии последним?",
            "incoming": [
                "Кто вчера вышел с линии последним? В табеле все закрыты одновременно.",
                "Лера говорит, что видела человека у дальнего схода уже после сигнала.",
            ],
            "replies": [
                {
                    "id": "count",
                    "title": "«Сегодня считаем людей сами.»",
                    "answer": "Сегодня после стопа пересчитаемся сами. Не по табелю.",
                    "reaction": "Виктор: давно пора.",
                    "effects": {"ps2_team_aid": 2, "ps_team_unity": 1},
                },
                {
                    "id": "facts",
                    "title": "«Нужно точное время.»",
                    "answer": "Пришлите время и сектор. Без этого сообщение исчезнет как слух.",
                    "reaction": "Лера присылает фотографию экрана ТСД.",
                    "effects": {"ps_evidence": 1, "ps2_team_trust": 1},
                },
            ],
        },
        {
            "id": "ps2_unsent_max",
            "day": 4,
            "sender": "Макс",
            "time": "06:19",
            "preview": "Сообщение удалено",
            "incoming": [
                "Сообщение удалено.",
                "Следом: «Неважно. Завтра расскажу смешно».",
            ],
            "replies": [
                {
                    "id": "no_joke",
                    "title": "«Можно рассказать несмешно.»",
                    "answer": "Можно рассказать несмешно. Я всё равно прочитаю.",
                    "reaction": "Макс: тогда завтра без зрительного зала.",
                    "effects": {"ps_humanity": 1, "ps2_team_trust": 2},
                },
                {
                    "id": "wait",
                    "title": "Промолчать",
                    "answer": "",
                    "reaction": "Переписка остаётся открытой до утра.",
                    "effects": {"ps2_pressure": 1},
                },
            ],
        },
        {
            "id": "ps2_future_self",
            "day": 6,
            "sender": "Я",
            "time": "--:--",
            "preview": "Не подписывай тишину.",
            "incoming": [
                "Не подписывай тишину.",
                "Ты уже видел, чем заканчивается смена, в которой каждый решил, что скажет кто-нибудь другой.",
            ],
            "replies": [
                {
                    "id": "who",
                    "title": "«Кто это?»",
                    "answer": "Кто это отправил?",
                    "reaction": "Сообщение отмечается прочитанным вчера.",
                    "effects": {"ps2_pressure": 1, "ps2_resolve": 1},
                },
                {
                    "id": "remember",
                    "title": "Сохранить снимок экрана",
                    "answer": "",
                    "reaction": "Снимок появляется в папке, которой нет в телефоне.",
                    "effects": {"ps_evidence": 1, "ps_integrity": 1},
                },
            ],
        },
        {
            "id": "ps2_gate_after",
            "day": 7,
            "sender": "Смена",
            "time": "07:24",
            "preview": "Не расходиться сразу.",
            "incoming": [
                "После проходной не расходиться сразу.",
                "Не собрание. Просто убедимся, что вышли все.",
            ],
            "replies": [
                {
                    "id": "all",
                    "title": "«Сначала пересчитаемся.»",
                    "answer": "Сначала пересчитаемся. Потом каждый решит, куда идти.",
                    "reaction": "В чате появляются четыре коротких плюса.",
                    "effects": {"ps2_team_aid": 2, "ps2_team_trust": 1},
                },
            ],
        },
    ]

    known_message_ids = {message["id"] for message in ps_message_catalog}
    for message_item in ps2_messages:
        if message_item["id"] not in known_message_ids:
            ps_message_catalog.append(message_item)

    def ps2_clamp(value, high=12):
        return max(0, min(high, value))

    def ps2_apply(**changes):
        for variable_name, delta in changes.items():
            current_value = getattr(renpy.store, variable_name)
            setattr(renpy.store, variable_name, current_value + delta)

    def ps2_record_decision(day, phase, decision_id, title, consequence):
        global ps2_decision_map

        key = "{}:{}:{}".format(day, phase, decision_id)
        if any(item["key"] == key for item in ps2_decision_map):
            return

        ps2_decision_map = ps2_decision_map + [{
            "key": key,
            "day": day,
            "phase": phase,
            "id": decision_id,
            "title": title,
            "consequence": consequence,
        }]
        ps_record_consequence(consequence)

    def ps2_mark_scene(scene_id):
        global ps2_scenes_seen
        if scene_id not in ps2_scenes_seen:
            ps2_scenes_seen = ps2_scenes_seen + [scene_id]
        if len(ps2_scenes_seen) >= 3:
            ps_unlock_achievement("three_phases")

    def ps2_set_intention(day, intention):
        global ps2_day_intentions
        ps2_day_intentions = dict(ps2_day_intentions)
        ps2_day_intentions[day] = intention

    def ps2_set_after_choice(day, choice):
        global ps2_after_choices
        ps2_after_choices = dict(ps2_after_choices)
        ps2_after_choices[day] = choice

    def ps2_collective_score():
        positive = ps2_team_trust + ps2_team_aid + ps_team_unity
        negative = ps2_team_fear + ps2_team_fracture + max(0, ps_burnout - 4)
        return ps2_clamp(6 + positive - negative, 24)

    def ps2_collective_title():
        score = ps2_collective_score()
        if score >= 18:
            return "Смена действует как команда"
        if score >= 12:
            return "Люди учатся замечать друг друга"
        if score >= 7:
            return "Смена держится, но трещины видны"
        return "Каждый пытается выбраться один"

    def ps2_hero_title():
        if ps2_pressure >= 9 and ps2_fatigue >= 8:
            return "На грани срыва"
        if ps2_resolve >= 8 and ps2_pressure >= 6:
            return "Боится, но всё равно говорит"
        if ps2_fatigue >= 8:
            return "Тело дошло, внимание отстаёт"
        if ps2_resolve >= 6:
            return "Начинает выбирать сам"
        return "Пока учится слышать себя"

    def ps2_storm_stage():
        value = ps2_pressure + ps2_team_fear + len(ps_storm_fragments)
        if value >= 18:
            return 3
        if value >= 11:
            return 2
        if value >= 5:
            return 1
        return 0

    def ps2_epilogue_line():
        route = ps_route_target()
        route_names = {
            "newbie": "Лера больше не просит разрешения сообщить об ошибке.",
            "veteran": "Виктор впервые записывает боль раньше, чем она становится травмой.",
            "joker": "Макс всё ещё шутит, но теперь умеет закончить фразу без улыбки.",
            "supervisor": "Артём учится произносить решение от своего имени, а не от имени регламента.",
        }
        return route_names.get(route, "Смена помнит людей по именам.")

    def ps2_finish_run():
        persistent.ps2_new_shift_plus_unlocked = True
        persistent.ps2_completed_runs = int(persistent.ps2_completed_runs or 0) + 1
        persistent.ps2_last_decision_map = [dict(item) for item in ps2_decision_map]
        persistent.ps2_seen_echoes = list(set(
            list(persistent.ps2_seen_echoes or []) + list(ps2_scenes_seen)
        ))
        renpy.save_persistent()

        ps_unlock_achievement("beyond_shift")
        if ps2_collective_score() >= 18:
            ps_unlock_achievement("collective_memory")

    def ps2_last_map():
        if ps2_decision_map:
            return ps2_decision_map
        return list(getattr(persistent, "ps2_last_decision_map", []) or [])


################################################################################
## Состояние героя, команды и карта решений
################################################################################

screen ps2_meter(title, value, accent, maximum=12):
    vbox:
        spacing 6
        xsize 510

        hbox:
            xfill True
            text title color "#e9e1f1" size 22
            text "[value]" color accent size 22 xalign 1.0

        bar:
            value StaticValue(ps2_clamp(value, maximum), maximum)
            xmaximum 510
            ymaximum 15
            left_bar Solid(accent)
            right_bar Solid("#493951")


screen ps2_journal():
    modal True
    zorder 280

    key "game_menu" action Hide("ps2_journal")
    key "K_p" action Hide("ps2_journal")

    add Solid("#050208ec")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1480
        ysize 930
        padding (50, 36)
        background Solid("#13091ef8")

        vbox:
            spacing 20
            xfill True

            hbox:
                xfill True

                vbox:
                    spacing 2
                    text "ЛИЧНЫЙ ДНЕВНИК // ДЕНЬ [ps_chapter]" color "#d5abff" size 36
                    text "[ps2_hero_title()]" color "#a994bb" size 21

                textbutton "×":
                    id "ps2_journal_close"
                    action Hide("ps2_journal")
                    xalign 1.0
                    xsize 60
                    ysize 52
                    background Solid("#3b244d")
                    hover_background Solid("#70458d")
                    text_color "#ffffff"
                    text_size 34
                    text_xalign 0.5
                    text_yalign 0.5

            hbox:
                spacing 30
                xalign 0.5

                vbox:
                    spacing 15
                    use ps2_meter("Усталость", ps2_fatigue, "#ffb26b")
                    use ps2_meter("Давление", ps2_pressure, "#ff7888")
                    use ps2_meter("Решимость", ps2_resolve, "#a88cff")

                vbox:
                    spacing 15
                    use ps2_meter("Доверие", ps2_team_trust, "#80e2c2")
                    use ps2_meter("Взаимовыручка", ps2_team_aid, "#8fd5ff")
                    use ps2_meter("Страх", ps2_team_fear, "#e58bff")

            frame:
                xfill True
                padding (24, 18)
                background Solid("#241434dd")

                vbox:
                    spacing 7
                    text "[ps2_collective_title()]" color "#ffffff" size 29 xalign 0.5
                    text "Доверие [ps2_team_trust]  ·  Помощь [ps2_team_aid]  ·  Страх [ps2_team_fear]  ·  Раскол [ps2_team_fracture]" color "#c8b9d4" size 21 xalign 0.5

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                ymaximum 320

                vbox:
                    spacing 11
                    xfill True

                    if ps2_last_map():
                        for entry in ps2_last_map()[-8:]:
                            frame:
                                xfill True
                                padding (19, 13)
                                background Solid("#21152ddd")

                                vbox:
                                    spacing 4
                                    text "День [entry['day']] · [entry['phase']] · [entry['title']]" color "#e7d7f7" size 22
                                    text entry["consequence"] color "#ab9bb8" size 19
                    else:
                        text "Здесь появятся решения, которые вернутся позже." color "#93869e" size 23 xalign 0.5

            hbox:
                spacing 18
                xalign 0.5

                textbutton "КАРТА СЕМИ ДНЕЙ":
                    id "ps2_journal_map"
                    action Show("ps2_decision_map")
                    xsize 330
                    ysize 58
                    background Solid("#60378a")
                    hover_background Solid("#8851bd")
                    text_color "#ffffff"
                    text_size 21
                    text_xalign 0.5
                    text_yalign 0.5

                textbutton "ВЕРНУТЬСЯ":
                    id "ps2_journal_return"
                    action Hide("ps2_journal")
                    xsize 280
                    ysize 58
                    background Solid("#33213f")
                    hover_background Solid("#57366d")
                    text_color "#ffffff"
                    text_size 21
                    text_xalign 0.5
                    text_yalign 0.5


screen ps2_decision_map():
    modal True
    zorder 290

    key "game_menu" action Hide("ps2_decision_map")
    add Solid("#050208f2")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1500
        ysize 900
        padding (48, 34)
        background Solid("#13091efa")

        vbox:
            spacing 22
            xfill True

            hbox:
                xfill True
                vbox:
                    spacing 3
                    text "КАРТА РЕШЕНИЙ" color "#d2a7ff" size 39
                    text "Она показывает след, а не правильный ответ." color "#a695b5" size 21

                textbutton "×":
                    id "ps2_map_close"
                    action Hide("ps2_decision_map")
                    xalign 1.0
                    xsize 60
                    ysize 52
                    background Solid("#3b244d")
                    hover_background Solid("#70458d")
                    text_color "#ffffff"
                    text_size 34
                    text_xalign 0.5
                    text_yalign 0.5

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"

                vbox:
                    spacing 18
                    xfill True

                    for day in range(1, 8):
                        $ day_entries = [entry for entry in ps2_last_map() if entry["day"] == day]

                        frame:
                            xfill True
                            padding (24, 18)
                            background Solid("#27173add" if day_entries else "#17121dcc")

                            vbox:
                                spacing 8
                                text "ДЕНЬ [day]" color ("#caa2f6" if day_entries else "#625a69") size 25

                                if day_entries:
                                    for entry in day_entries:
                                        text "[entry['phase']]: [entry['title']]" color "#f0e7f6" size 22
                                        text entry["consequence"] color "#aa9ab7" size 18
                                else:
                                    text "Эта часть недели ещё не оставила следа." color "#6e6575" size 19


screen ps2_final_matrix():
    modal True
    zorder 285

    add Solid("#050208e8")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1320
        ysize 820
        padding (60, 44)
        background Solid("#160b24f8")

        vbox:
            spacing 24
            xfill True

            text "ПЕРЕД ПОСЛЕДНИМ РЕШЕНИЕМ" color "#d4aaff" size 42 xalign 0.5
            text "[ps2_collective_title()]" color "#ffffff" size 31 xalign 0.5

            grid 2 3:
                spacing 20
                xalign 0.5

                use ps2_meter("Решимость", ps2_resolve, "#a88cff")
                use ps2_meter("Давление", ps2_pressure, "#ff7888")
                use ps2_meter("Доверие", ps2_team_trust, "#80e2c2")
                use ps2_meter("Взаимовыручка", ps2_team_aid, "#8fd5ff")
                use ps2_meter("Страх", ps2_team_fear, "#e58bff")
                use ps2_meter("Раскол", ps2_team_fracture, "#f1996e")

            frame:
                xfill True
                padding (28, 20)
                background Solid("#251437dd")

                text "Финал не выбирается одной кнопкой. Сейчас вместе с тобой решают все шесть предыдущих дней." color "#d6c8df" size 24 text_align 0.5 xalign 0.5

            textbutton "ВОЙТИ В ФИНАЛЬНУЮ СМЕНУ":
                id "ps2_final_continue"
                action Return()
                xalign 0.5
                xsize 560
                ysize 70
                background Solid("#6c3aa8")
                hover_background Solid("#9b5ee0")
                text_color "#ffffff"
                text_size 25
                text_xalign 0.5
                text_yalign 0.5


################################################################################
## Три фазы дня
################################################################################

label ps2_pre_shift(day):
    $ ps2_phase = "до смены"
    $ ps2_mark_scene("pre_{}".format(day))

    if day == 1:
        n "До выхода остаётся несколько минут. Впервые за утро ты спрашиваешь себя не о графике, а о том, каким хочешь вернуться."
    elif day == 2:
        n "Перед второй сменой уже нельзя притвориться, что ты не знаешь, куда идёшь. Теперь это возвращение."
    elif day == 3:
        n "Третий день начинается ещё дома: рейтинг уже поселился в голове и считает то, чего не видит."
    elif day == 4:
        n "В телефоне чужая ошибка выглядит одной строкой. За строкой есть лицо, и сегодня это особенно трудно забыть."
    elif day == 5:
        n "Тело просит экономить движения. Система просит сделать больше, чем вчера. Между ними остаёшься ты."
    elif day == 6:
        n "Сегодня на склад приедет человек, которому легче подписать итог, чем прожить его. Нужно решить, что ты понесёшь к нему."
    else:
        n "Перед последней сменой невозможно выбрать спокойствие. Можно только выбрать, ради чего выдержать тревогу."

    if ps2_new_shift_plus_active:
        n "Фраза кажется знакомой. Не похожей - дословно знакомой. Даже пауза перед следующим выбором уже была."
        if day == 1:
            $ ps_unlock_achievement("new_shift_plus")

    menu:
        "Сегодня я буду замечать людей":
            $ ps2_set_intention(day, "люди")
            $ ps2_apply(ps_humanity=1, ps2_team_trust=1, ps2_fatigue=1)
            $ ps2_record_decision(day, "до смены", "people", "Замечать людей", "Ты заранее оставил внимание для тех, кого таблица не показывает.")
            p "Если рядом кто-то начнёт тонуть, я хотя бы не сделаю вид, что не заметил."

        "Сегодня я соберу факты":
            $ ps2_set_intention(day, "правда")
            $ ps2_apply(ps_integrity=1, ps2_resolve=1, ps2_pressure=1)
            $ ps2_record_decision(day, "до смены", "truth", "Собрать факты", "Ты решил не спорить с системой без памяти и доказательств.")
            p "Сначала время, код и имена. И только потом - выводы."

        "Сегодня я сохраню результат":
            $ ps2_set_intention(day, "результат")
            $ ps2_apply(ps_efficiency=1, ps2_resolve=1, ps2_team_fear=1)
            $ ps2_record_decision(day, "до смены", "result", "Удержать результат", "Ты поставил темп впереди сомнений. Смена это почувствовала.")
            p "Сначала вывезти смену. Разбираться буду, когда поток отпустит."

        "Сегодня я не отдам себя целиком":
            $ ps2_set_intention(day, "себя")
            $ ps2_apply(ps_endurance=1, ps_burnout=-1, ps2_fatigue=-1, ps2_resolve=1)
            $ ps2_record_decision(day, "до смены", "self", "Сохранить себя", "Ты признал, что у тебя тоже есть предел, даже если его нет в регламенте.")
            p "Я могу помочь другим только пока сам ещё здесь."

    return


label ps2_shift_event(day):
    $ ps2_phase = "внутри смены"
    $ ps2_mark_scene("shift_{}".format(day))

    if day == 1:
        n "На соседнем сходе загорается красная лампа. Лера тянется к коробке, не замечая, что лента ещё движется."
        menu:
            "Остановить её рукой и самому потерять темп":
                $ ps2_apply(ps_humanity=1, ps2_team_trust=1, ps2_team_aid=1, ps2_fatigue=1)
                $ ps2_record_decision(day, "в смене", "hand_stop", "Перехватить движение", "Ты потерял несколько операций, но Лера запомнила, что её безопасность заметили раньше ошибки.")
                p "Стой. Сначала лента. Потом коробка."
                newb "Я даже не увидела..."
                p "Поэтому здесь смотрим друг за другом."

            "Громко предупредить и не выходить из своего сектора":
                $ ps2_apply(ps_efficiency=1, ps2_team_fear=1, ps2_resolve=1)
                $ ps2_record_decision(day, "в смене", "voice_stop", "Предупредить голосом", "Ты сохранил участок, но в твоём голосе Лера услышала тот же приказ, что слышит от системы.")
                p "Руки убрала! Лента движется!"
                newb "Поняла. Извини."

    elif day == 2:
        n "В буфере остаётся одна тяжёлая коробка без читаемой маркировки. Если вернуть её в поток, план не пострадает. Если остановить - участок уйдёт в минус."
        menu:
            "Снять коробку и оформить ручную проверку":
                $ ps2_apply(ps_integrity=1, ps_evidence=1, ps2_resolve=1, ps2_pressure=1)
                $ ps2_record_decision(day, "в смене", "manual_check", "Проверить вручную", "План просел, зато у коробки появилась история, которую нельзя стереть одной кнопкой.")
                p "Без маркировки она дальше не идёт. Открываем проверку."

            "Вернуть коробку в поток и запомнить номер":
                $ ps2_apply(ps_efficiency=2, ps2_pressure=1, ps2_team_fracture=1)
                $ ps2_record_decision(day, "в смене", "remember_box", "Пропустить и запомнить", "Ты сохранил цифру, но оставил проблему следующему участку.")
                p "Номер запомнил. Если вернётся - остановим."
                vet "Если вернётся, она уже будет чьей-то чужой ошибкой."

    elif day == 3:
        n "Рейтинг обновляется прямо во время перерыва. У Макса падает показатель: он помогал дальнему сектору, а система записала это как простой."
        menu:
            "Отдать ему часть своих закрытых операций":
                $ ps2_apply(ps_efficiency=-1, ps_humor=1, ps2_team_aid=2, ps2_team_trust=1)
                $ ps2_record_decision(day, "в смене", "share_rate", "Разделить результат", "Твоё место в рейтинге опустилось, зато помощь перестала быть невидимой хотя бы для команды.")
                p "Запиши две мои операции на его сектор. Он там работал больше меня."
                mem "Я запомню этот коррупционный акт доброты."

            "Потребовать исправить учёт официально":
                $ ps2_apply(ps_integrity=1, ps2_resolve=2, ps2_pressure=1, ps_supervisor_respect=1)
                $ ps2_record_decision(day, "в смене", "fix_rate", "Оспорить рейтинг", "Ты сделал помощь предметом официального спора. Теперь система знает, кто задал вопрос.")
                p "Если помощь считается простоем, исправляйте правило, а не человека."
                sv "Повтори это без свидетелей."
                p "Нет."

    elif day == 4:
        n "Леру вызывают подписать объяснительную за сбой, который начался до её входа в систему. Она держит ручку и ждёт, что кто-нибудь скажет, что делать."
        menu:
            "Не дать ей подписать документ без журнала":
                $ ps2_apply(ps_humanity=1, ps_integrity=1, ps2_team_trust=2, ps2_pressure=1)
                $ ps2_record_decision(day, "в смене", "hold_signature", "Остановить подпись", "Лера не стала удобным именем для системной ошибки. Теперь проверка касается всех.")
                p "Ручку положи. Сначала журнал входов."
                newb "Они сказали, это формальность."
                p "Формальность, которая останется на твоём имени."

            "Попросить подписать, но добавить собственное примечание":
                $ ps2_apply(ps_evidence=1, ps_efficiency=1, ps2_team_fear=1, ps2_team_fracture=1)
                $ ps2_record_decision(day, "в смене", "note_signature", "Оставить примечание", "Документ закрыли вовремя. Лера запомнила, что закрыли его всё равно на ней.")
                p "Подпиши только с примечанием о времени сбоя. Я подтвержу."
                newb "То есть виноватой всё равно останусь я?"

    elif day == 5:
        n "На подъёмнике снова мигает LIFT-09. Виктор уже идёт к панели: если остановить механизм, приёмка встанет на сорок минут."
        menu:
            "Заблокировать подъёмник до осмотра":
                $ ps2_apply(ps_integrity=1, ps_endurance=1, ps2_team_aid=2, ps2_resolve=2, ps2_pressure=1)
                $ ps_veteran_safe = True
                $ ps2_record_decision(day, "в смене", "lock_lift", "Заблокировать подъёмник", "Сорок минут стали видимой потерей. Возможная травма так и не стала фактом.")
                p "Виктор, не трогай. Ставим блокировку и вызываем осмотр."
                vet "Наконец-то кто-то испортил красивый отчёт вовремя."

            "Провести одну последнюю разгрузку вручную":
                $ ps2_apply(ps_efficiency=2, ps2_fatigue=2, ps2_team_fear=2, ps_burnout=1)
                $ ps2_record_decision(day, "в смене", "last_lift", "Рискнуть последней разгрузкой", "Поставка закрылась вовремя. После неё никто не назвал тишину облегчением.")
                p "Одна разгрузка. Без рывков. Потом блокируем."
                vet "Так всегда и начинается слово «последняя»."

    elif day == 6:
        n "Морозов предлагает закрыть происшествие одной формулировкой: «отклонение устранено, пострадавших нет». Это правда только в настоящем времени."
        menu:
            "Отказаться и приложить историю предупреждений":
                $ ps2_apply(ps_integrity=2, ps_evidence=1, ps2_resolve=2, ps2_pressure=2, ps2_team_trust=1)
                $ ps2_record_decision(day, "в смене", "history_report", "Приложить историю", "Инцидент перестал быть единичным. Вместе с ним видимой стала цена прежнего молчания.")
                $ ps_unlock_achievement("hard_truth")
                p "Пострадавших нет сегодня. Предупреждения игнорировали два года. Это тоже часть отчёта."

            "Подписать формулировку и потребовать ремонт после смены":
                $ ps2_apply(ps_efficiency=1, ps_supervisor_respect=1, ps2_team_fracture=2, ps2_team_fear=1)
                $ ps_signed_false_report = True
                $ ps2_record_decision(day, "в смене", "quiet_repair", "Обменять подпись на ремонт", "Подъёмник починят. Документы навсегда скажут, что проблемы не было.")
                p "Я подпишу, если заявка на ремонт уйдёт сегодня."
                cur "Разумный компромисс."
                n "Слово звучит так, будто цена поделилась поровну."

    return


label ps2_after_shift(day):
    $ ps2_phase = "после смены"
    $ ps2_mark_scene("after_{}".format(day))

    stop music fadeout 1.0

    if day in (1, 2, 3):
        scene bg street_night
        with fade
        play music "audio/night_walk.mp3" fadein 1.5 loop
    elif day in (4, 5):
        scene bg break_room
        with fade
        play music "audio/after_shift_ambient.mp3" fadein 1.5 loop
    else:
        scene bg warehouse_outside
        with fade
        play music "audio/city_night.mp3" fadein 1.5 loop

    if day == 1:
        n "После проходной телефон предлагает оценить смену пятью звёздами. Палец зависает над экраном: ни одна звезда не спрашивает, кем ты был внутри этих часов."
        menu:
            "Записать честно: «Я испугался, но вернулся к людям»":
                $ ps2_set_after_choice(day, "честность")
                $ ps2_apply(ps_integrity=1, ps2_resolve=1, ps2_pressure=-1)
                $ ps2_record_decision(day, "после смены", "honest_note", "Оставить честную запись", "Ты сохранил не результат смены, а собственную версию произошедшего.")
                p "Испугался и сначала растерялся. Потом вернулся и помог. На сегодня запишу так."

            "Закрыть приложение и ничего не оценивать":
                $ ps2_set_after_choice(day, "тишина")
                $ ps2_apply(ps_endurance=1, ps2_fatigue=-1)
                $ ps2_silences = ps2_silences + ["day1"]
                $ ps2_record_decision(day, "после смены", "close_rating", "Не ставить оценку", "Ты отказался превращать прожитую смену в ещё одну цифру.")
                n "Ты закрываешь приложение. После двенадцати часов на складе ещё одна оценка от тебя ничего не изменит."

    elif day == 2:
        n "На остановке Лера садится на другой край скамейки. Между вами помещается целая смена и одна коробка без маркировки."
        menu:
            "Сесть рядом и разобрать момент без оправданий":
                $ ps2_set_after_choice(day, "разговор")
                $ ps2_apply(ps_humanity=1, ps_newbie_trust=1, ps2_team_trust=1, ps2_fatigue=1)
                $ ps2_record_decision(day, "после смены", "talk_lera", "Разобрать момент", "Лера услышала не инструкцию, а человека, который тоже не был уверен.")
                p "Я не всё сделал правильно. Давай разберём, пока помним."
                newb "Хорошо. Только без фразы «надо было просто»."

            "Дать ей тишину и написать позже":
                $ ps2_set_after_choice(day, "отложить")
                $ ps2_apply(ps_endurance=1, ps2_pressure=-1)
                $ ps_phone_deferred = ps_phone_deferred + (["newbie"] if "newbie" not in ps_phone_deferred else [])
                $ ps2_record_decision(day, "после смены", "defer_lera", "Отложить разговор", "Вы оба получили передышку. Разговор остался долгом следующего дня.")
                n "Ты не садишься рядом. Но перед автобусом пишешь: «Я отвечу утром. Не пропал»."

    elif day == 3:
        n "Автобус задерживается. Макс листает рейтинг, делает снимок экрана и неожиданно удаляет его."
        menu:
            "Спросить, что он хотел доказать снимком":
                $ ps2_set_after_choice(day, "спросить")
                $ ps2_apply(ps_humanity=1, ps_humor=1, ps2_team_trust=1)
                $ ps2_record_decision(day, "после смены", "ask_max", "Спросить без шутки", "Макс впервые объяснил, что смеётся не над страхом, а чтобы страх не говорил первым.")
                p "Кому хотел отправить?"
                mem "Себе. На случай, если начну думать, что всё придумал."

            "Сделать общее фото вместо рейтинга":
                $ ps2_set_after_choice(day, "фото")
                $ ps2_apply(ps_humor=1, ps2_team_aid=1, ps2_team_trust=1)
                $ ps2_record_decision(day, "после смены", "team_photo", "Сохранить людей", "В памяти телефона осталась смена без процентов и мест.")
                p "Удали таблицу. Лучше сфотографируй, кто сегодня реально вывез."
                mem "Наконец-то контент с человеческими лицами."

    elif day == 4:
        n "В комнате отдыха остаётся объяснительная Леры. Копия лежит в лотке на уничтожение, но на ней видно время системного сбоя."
        menu:
            "Забрать копию в архив дела":
                $ ps2_set_after_choice(day, "архив")
                $ ps2_apply(ps_evidence=1, ps_integrity=1, ps2_pressure=1)
                $ ps2_record_decision(day, "после смены", "save_copy", "Сохранить копию", "Документ, который должен был исчезнуть, стал частью хронологии.")
                n "Ты фотографируешь лист, отдельно снимаешь время и номер терминала, проверяешь, читаются ли цифры, и только потом возвращаешь копию в лоток."

            "Порвать копию, чтобы её не использовали против Леры":
                $ ps2_set_after_choice(day, "защита")
                $ ps2_apply(ps_humanity=1, ps2_team_aid=1, ps_evidence=-1)
                $ ps2_record_decision(day, "после смены", "destroy_copy", "Уничтожить копию", "Ты защитил Леру от документа и лишил команду одного доказательства.")
                n "Ты рвёшь лист на мелкие полосы и выбрасываешь в разные урны. Только уже у выхода понимаешь, что вместе с чужим обвинением уничтожил точное время сбоя."

    elif day == 5:
        n "Виктор долго не снимает рабочую перчатку. Когда снимает, на ладони остаётся красная полоса."
        menu:
            "Настоять, чтобы он оформил травму сейчас":
                $ ps2_set_after_choice(day, "оформить")
                $ ps2_apply(ps_endurance=1, ps_integrity=1, ps2_team_aid=2, ps2_pressure=1)
                $ ps_veteran_safe = True
                $ ps2_record_decision(day, "после смены", "record_pain", "Записать боль вовремя", "Виктор впервые не оставил травму на потом. Смена потеряла красивую статистику без происшествий.")
                p "Идём в медпункт. Не утром. Сейчас."
                vet "Ненавижу, когда новички быстро учатся."

            "Пообещать заменить его завтра на тяжёлом секторе":
                $ ps2_set_after_choice(day, "заменить")
                $ ps2_apply(ps_humanity=1, ps2_team_aid=1, ps2_fatigue=2)
                $ ps2_record_decision(day, "после смены", "cover_victor", "Взять чужую нагрузку", "Виктор получил передышку. Твой собственный предел стал ближе.")
                p "Завтра тяжёлое беру я. Ты работаешь на сканировании."
                vet "Помощь - это не когда один ломается вместо другого. Запомни."

    else:
        call ps21_route_night_scene

    $ ps2_fatigue = ps2_clamp(ps2_fatigue + 1)
    $ ps2_pressure = ps2_clamp(ps2_pressure)
    $ ps2_resolve = ps2_clamp(ps2_resolve)

    return


label ps2_route_crisis:
    call ps21_route_night_scene
    return


################################################################################
## Шторм и финальная сборка недели
################################################################################

label ps2_storm_echo(day):
    $ ps2_stage = ps2_storm_stage()

    if ps2_stage == 0:
        return

    if ps2_stage == 1:
        n "ТСД на секунду показывает не номер ячейки, а твою сегодняшнюю установку. Потом экран возвращается в норму."
    elif ps2_stage == 2:
        n "По громкой связи произносят твоё имя. Никто рядом не реагирует. Через секунду голос повторяет решение, принятое тобой утром."
    else:
        n "Лента движется без коробок. На каждом пустом участке лежит карточка с одним из решений недели. Некоторые написаны твоим почерком, хотя ты их не писал. Последняя карточка пустая. Система словно оставила место для финала."
        $ ps_collect_storm_fragment("empty_decision")

    $ ps2_pressure = ps2_clamp(ps2_pressure + 1)
    return


label ps2_final_convergence:
    $ ps2_phase = "последняя развилка"

    call ps2_storm_echo(7)

    scene bg locker_room
    with fade

    n "До запуска остаётся несколько минут. В раздевалке впервые за неделю находятся все четверо. Никто не садится. У тебя есть вся история: коды, сообщения, чужие паузы и собственные решения. Но правда, сказанная не вовремя, тоже может стать ударом."

    menu:
        "Показать команде всё до начала смены":
            $ ps2_final_preparation = "вся правда"
            $ ps2_apply(ps_integrity=2, ps_evidence=1, ps2_resolve=2, ps2_team_trust=1, ps2_team_fear=2)
            $ ps2_record_decision(7, "перед финалом", "full_truth", "Показать всё", "Команда вошла в аварию напуганной, но никто больше не принимал решения вслепую.")
            p "Сначала посмотрите. Потом можете сказать, что не готовы. Но вслепую сегодня не идёт никто."

        "Собрать простой план: стоп, пересчёт, выход":
            $ ps2_final_preparation = "общий план"
            $ ps2_apply(ps_team_unity=1, ps2_team_aid=2, ps2_team_trust=1, ps2_resolve=1)
            $ ps2_record_decision(7, "перед финалом", "shared_plan", "Договориться о действиях", "У команды не было полной картины, зато у каждого появилось понятное действие на случай аварии.")
            p "Если связь падает: Макс считает людей, Лера передаёт стоп, Виктор блокирует подъёмник, Артём выводит дальний сектор."
            mem "А ты?"
            p "Я проверяю, что никто не остался один."

        "Ничего не говорить и взять ответственность на себя":
            $ ps2_final_preparation = "в одиночку"
            $ ps2_apply(ps_efficiency=1, ps_endurance=1, ps2_resolve=2, ps2_fatigue=2, ps2_team_fracture=2)
            $ ps2_record_decision(7, "перед финалом", "solo", "Удержать всё самому", "Команда сохранила спокойствие до аварии. Ты вошёл в неё единственным человеком с полной картиной.")
            p "Ничего. Просто держитесь сегодня ближе."
            vet "Когда человек говорит «ничего», обычно там уже слишком много."

    call screen ps2_final_matrix
    return


################################################################################
## Расширенный эпилог и повторное прохождение
################################################################################

label ps2_extended_epilogue:
    $ ps2_finish_run()

    if ps_final_ending in ("truth", "people", "voice"):
        $ ps_unlock_cg("ps2_platform")
        scene cg ps2_platform at ps2_memory_camera
        with fade
        n "Через неделю на остановке снова стоят четверо. Не потому, что график совпал. Они договорились дождаться друг друга."
    elif ps_final_ending in ("leader", "employee"):
        $ ps_unlock_cg("ps2_badge")
        scene cg ps2_badge at ps2_memory_camera
        with fade
        n "Новый жилет висит на спинке стула. На нём больше карманов и ответственности, чем ты представлял."
    elif ps_final_ending == "exit":
        $ ps_unlock_cg("ps2_morning")
        scene cg ps2_morning at ps2_memory_camera
        with fade
        n "Через неделю утро приходит без вибрации телефона. Первые минуты ты всё равно ждёшь сигнал, которого больше нет."
    else:
        $ ps_unlock_cg("ps2_afterimage")
        scene cg ps2_afterimage at ps2_memory_camera
        with fade
        n "Склад работает дальше. Иногда на пустом экране появляется список людей, которые в эту ночь были внутри. Твоё имя там тоже есть."

    n "[ps2_epilogue_line()]"

    if ps2_collective_score() >= 18:
        n "Общий чат не закрылся вместе с неделей. Теперь туда пишут не только о подменах, но и о том, кто добрался домой."
    elif ps2_collective_score() >= 10:
        n "Команда не стала семьёй. Это и не требовалось. Люди просто научились спрашивать, кто ещё не вышел."
    else:
        n "После финала каждый ушёл своей дорогой. Иногда это честнее обещания держаться вместе, которое никто не смог бы выполнить."

    if ps2_resolve >= 8:
        n "Ты не стал бесстрашным. Просто перестал считать страх приказом молчать."
    elif ps2_fatigue >= 9:
        n "Главное последствие недели проявилось позже: впервые ты признал усталость до того, как она превратилась в поломку."
    else:
        n "Неделя не дала готового ответа. Она вернула тебе право задавать вопрос самому."

    centered "Открыто: Новая смена+\nКарта прошлой недели сохранена"
    return


label ps2_new_shift_plus_start:
    $ ps2_new_shift_plus_active = True
    $ ps2_pressure = 1
    $ ps2_resolve = 1
    $ ps_key_choices = ps_key_choices + ["Ты вернулся в смену с памятью о предыдущей неделе."]
    jump start
