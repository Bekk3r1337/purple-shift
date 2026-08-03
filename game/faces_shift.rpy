# -*- coding: utf-8 -*-

################################################################################
## Purple Shift 1.7 — «Лица смены»
## Реактивный визуал, развивающиеся мотивы, новые CG и живой телефон
################################################################################

image cg team_conflict = "images/cg/team_conflict.jpg"
image cg evidence_timeline = "images/cg/evidence_timeline.jpg"
image cg mimic_message = "images/cg/mimic_message.jpg"
image cg route_crossroads = "images/cg/route_crossroads.jpg"
image cg zero_shift = "images/cg/zero_shift.jpg"
image cg team_reflection = "images/cg/team_reflection.jpg"


transform ps_close_left:
    xalign 0.20
    yalign 1.0
    yoffset 8
    xoffset -55
    zoom 0.76
    alpha 0.0
    subpixel True
    ease 0.42 xoffset 0 alpha 1.0
    function ps_character_breathe

transform ps_close_right:
    xalign 0.78
    yalign 1.0
    yoffset 8
    xoffset 55
    zoom 0.78
    alpha 0.0
    subpixel True
    ease 0.42 xoffset 0 alpha 1.0
    function ps_character_breathe

transform ps_growth_grade:
    xalign 0.5
    yalign 0.5
    zoom 1.065
    alpha 0.0
    matrixcolor TintMatrix("#fff4df") * SaturationMatrix(1.08)
    ease 0.8 zoom 1.025 alpha 1.0

transform ps_shadow_grade:
    xalign 0.5
    yalign 0.5
    zoom 1.075
    alpha 0.0
    matrixcolor TintMatrix("#8b79a8") * BrightnessMatrix(-0.12)
    ease 0.8 zoom 1.04 alpha 1.0

transform ps_main_menu_drift:
    xalign 0.5
    yalign 0.5
    zoom 1.08
    alpha 0.34
    linear 14.0 zoom 1.02 alpha 0.42
    block:
        linear 6.0 alpha 0.34
        linear 6.0 alpha 0.42
        repeat

transform ps_signal_breathe:
    alpha 0.12
    linear 1.8 alpha 0.30
    linear 1.8 alpha 0.12
    repeat


init 20 python:
    ps_route_variant_tracks = {
        "newbie:growth": "audio/live/route_newbie_growth.ogg",
        "newbie:shadow": "audio/live/route_newbie_shadow.ogg",
        "veteran:growth": "audio/live/route_veteran_growth.ogg",
        "veteran:shadow": "audio/live/route_veteran_shadow.ogg",
        "joker:growth": "audio/live/route_joker_growth.ogg",
        "joker:shadow": "audio/live/route_joker_shadow.ogg",
        "supervisor:growth": "audio/live/route_supervisor_growth.ogg",
        "supervisor:shadow": "audio/live/route_supervisor_shadow.ogg",
    }

    ps_new_cgs = [
        ("team_conflict", "Спор у линии", "images/cg/team_conflict.jpg"),
        ("evidence_timeline", "Причина по порядку", "images/cg/evidence_timeline.jpg"),
        ("mimic_message", "Чужой голос", "images/cg/mimic_message.jpg"),
        ("route_crossroads", "Две стороны близости", "images/cg/route_crossroads.jpg"),
        ("zero_shift", "Нулевая смена", "images/cg/zero_shift.jpg"),
        ("team_reflection", "Лица после решения", "images/cg/team_reflection.jpg"),
    ]

    known_cg_ids = {item[0] for item in ps_cg_catalog}
    for cg_item in ps_new_cgs:
        if cg_item[0] not in known_cg_ids:
            ps_cg_catalog.append(cg_item)

    ps_new_achievements = [
        (
            "two_sides",
            "У каждого две стороны",
            "Открыть четыре внутренних варианта маршрутов.",
        ),
        (
            "team_chemistry",
            "Не просто коллеги",
            "Пройти четыре конфликта внутри команды.",
        ),
        (
            "chain_of_cause",
            "Причина, а не крайний",
            "Безошибочно восстановить системную цепочку происшествий.",
        ),
        (
            "human_voice",
            "Я знаю, как ты говоришь",
            "Определить сообщение, подделанное V-13.",
        ),
        (
            "zero_shift",
            "Нулевая смена",
            "Открыть истинный посткредитный эпизод.",
        ),
        (
            "all_faces",
            "Все лица смены",
            "Увидеть обе стороны всех четырёх маршрутов за несколько прохождений.",
        ),
    ]

    known_achievement_ids = {item[0] for item in ps_achievement_catalog}
    for achievement_item in ps_new_achievements:
        if achievement_item[0] not in known_achievement_ids:
            ps_achievement_catalog.append(achievement_item)

    ps_new_documents = [
        (
            "zero_roster",
            "Табель нулевой смены",
            "Список сотрудников существовал между двумя отчётными днями и исчез после запуска рейтинга.",
        ),
    ]

    known_document_ids = {item[0] for item in ps_document_catalog}
    for document_item in ps_new_documents:
        if document_item[0] not in known_document_ids:
            ps_document_catalog.append(document_item)

    ps_variant_messages = [
        {
            "id": "lera_growth",
            "day": 7,
            "sender": "Лера",
            "time": "18:42",
            "preview": "Я уже отправила свою версию.",
            "route": "newbie",
            "requires_route": "newbie",
            "requires_variant": "growth",
            "avatar": "newb relief",
            "status": "в сети",
            "incoming": [
                "Я уже отправила свою версию. Не проверяй — там мои слова и мои ошибки тоже.",
                "Если захочешь помочь, просто сохрани копию.",
            ],
            "replies": [
                {
                    "id": "respect",
                    "title": "«Сохраню. Исправлять не буду.»",
                    "answer": "Сохраню копию. Исправлять ничего не буду.",
                    "reaction": "Спасибо. Именно это сейчас и было помощью.",
                    "effects": {"ps_newbie_trust": 1, "ps_integrity": 1},
                },
            ],
        },
        {
            "id": "lera_shadow",
            "day": 7,
            "sender": "Лера",
            "time": "18:42",
            "preview": "Можешь ответить за меня?",
            "route": "newbie",
            "requires_route": "newbie",
            "requires_variant": "shadow",
            "avatar": "newb worried",
            "status": "печатает…",
            "incoming": [
                "Мне снова прислали форму. Можешь ответить за меня? Ты лучше понимаешь, что они хотят услышать.",
                "Я потом всё подтвержу.",
            ],
            "replies": [
                {
                    "id": "return_voice",
                    "title": "«Напиши сама. Я останусь рядом.»",
                    "answer": "Напиши сама. Я проверю только даты и останусь рядом.",
                    "reaction": "Страшно. Но попробую хотя бы начать.",
                    "effects": {"ps_humanity": 1, "ps_newbie_trust": 1},
                },
            ],
        },
        {
            "id": "viktor_growth",
            "day": 7,
            "sender": "Виктор",
            "time": "18:37",
            "preview": "Ключ отдал Артёму.",
            "route": "veteran",
            "requires_route": "veteran",
            "requires_variant": "growth",
            "avatar": "vet concerned",
            "status": "был недавно",
            "incoming": [
                "Ключ отдал Артёму. Пишу, чтобы через пять минут не сделать вид, будто забыл.",
                "Если попрошу обратно — это не просьба, а старая привычка.",
            ],
            "replies": [
                {
                    "id": "hold",
                    "title": "«Напомню твоими же словами.»",
                    "answer": "Напомню тебе этим сообщением.",
                    "reaction": "Нечестный приём. Одобряю.",
                    "effects": {"ps_endurance": 1, "ps_team_unity": 1},
                },
            ],
        },
        {
            "id": "viktor_shadow",
            "day": 7,
            "sender": "Виктор",
            "time": "18:37",
            "preview": "Последнюю смену дотяну.",
            "route": "veteran",
            "requires_route": "veteran",
            "requires_variant": "shadow",
            "avatar": "vet neutral",
            "status": "на смене",
            "incoming": [
                "Последнюю смену дотяну. Потом хоть к врачу, хоть в отпуск.",
                "Только сегодня не начинай снова про руку.",
            ],
            "replies": [
                {
                    "id": "refuse_exception",
                    "title": "«Последняя смена не отменяет тело.»",
                    "answer": "Последняя смена не делает руку запасной. Говорить всё равно будем.",
                    "reaction": "Знал, что зря написал. И всё-таки написал.",
                    "effects": {"ps_humanity": 1},
                },
            ],
        },
        {
            "id": "max_growth",
            "day": 7,
            "sender": "Макс",
            "time": "18:51",
            "preview": "Мне страшно. Без шутки.",
            "route": "joker",
            "requires_route": "joker",
            "requires_variant": "growth",
            "avatar": "mem serious",
            "status": "в сети",
            "incoming": [
                "Мне страшно. Без шутки и без второй версии сообщения.",
                "Ответ не обязателен. Просто хочу, чтобы это где-то осталось настоящим.",
            ],
            "replies": [
                {
                    "id": "present",
                    "title": "«Осталось. И я тоже.»",
                    "answer": "Осталось. И я тоже рядом.",
                    "reaction": "Принято. Теперь можно дышать.",
                    "effects": {"ps_team_unity": 2},
                },
            ],
        },
        {
            "id": "max_shadow",
            "day": 7,
            "sender": "Макс",
            "time": "18:51",
            "preview": "Финальная шутка уже готова.",
            "route": "joker",
            "requires_route": "joker",
            "requires_variant": "shadow",
            "avatar": "mem grin",
            "status": "печатает…",
            "incoming": [
                "Финальная шутка уже готова. Если не вернусь с линии, публикуй без редакторских правок.",
                "Это была шутка. Наверное.",
            ],
            "replies": [
                {
                    "id": "name_it",
                    "title": "«Скажи, что стоит после “наверное”.»",
                    "answer": "Скажи прямо, что стоит после «наверное».",
                    "reaction": "Не хочу исчезнуть незаметно. Вот. Всё испортил честностью.",
                    "effects": {"ps_humanity": 1, "ps_humor": 1},
                },
            ],
        },
        {
            "id": "artyom_growth",
            "day": 7,
            "sender": "Артём",
            "time": "19:02",
            "preview": "Общий стоп открыт всем.",
            "route": "supervisor",
            "requires_route": "supervisor",
            "requires_variant": "growth",
            "avatar": "sv stern",
            "status": "на смене",
            "incoming": [
                "Общий стоп открыт всем терминалам. Решение моё, право остановить — общее.",
                "Если спросят, эту формулировку повторю сам.",
            ],
            "replies": [
                {
                    "id": "witness",
                    "title": "«Сохраню как свидетель, не как разрешение.»",
                    "answer": "Сохраню сообщение как свидетель. Разрешение нам больше не нужно.",
                    "reaction": "Именно так.",
                    "effects": {"ps_integrity": 1, "ps_supervisor_respect": 1},
                },
            ],
        },
        {
            "id": "artyom_shadow",
            "day": 7,
            "sender": "Артём",
            "time": "19:02",
            "preview": "Без подтверждения ничего не делать.",
            "route": "supervisor",
            "requires_route": "supervisor",
            "requires_variant": "shadow",
            "avatar": "sv neutral",
            "status": "на смене",
            "incoming": [
                "Без моего подтверждения ничего не останавливать и не запускать.",
                "Сегодня одна ошибка должна оставаться одной ошибкой.",
            ],
            "replies": [
                {
                    "id": "challenge",
                    "title": "«А если ошибёшься ты?»",
                    "answer": "А если ошибёшься ты — кто остановит тебя?",
                    "reaction": "Ты. Поэтому сообщение отправлено именно тебе.",
                    "effects": {"ps_endurance": 1, "ps_supervisor_respect": 1},
                },
            ],
        },
    ]

    known_message_ids = {message["id"] for message in ps_message_catalog}
    for variant_message in ps_variant_messages:
        if variant_message["id"] not in known_message_ids:
            ps_message_catalog.append(variant_message)

    def ps_person_route_memory(route_id):
        state = ps_route_variant_data(route_id)
        if ps_route_tendency(route_id, "growth") == 0 and ps_route_tendency(route_id, "shadow") == 0:
            return "Вы пока не дошли до решения, которое изменит этот маршрут."
        return "{}: {}".format(state["title"], state["description"])

    def ps_investigation_hypothesis_title():
        for hypothesis_id, title, detail in ps_investigation_hypotheses:
            if hypothesis_id == ps_investigation_hypothesis:
                return title
        return "Версия не выбрана"

    def ps_investigation_result_caption():
        if not ps_investigation_complete:
            return "Хронология ещё не собрана."
        if ps_investigation_result >= 9:
            return "Цепочка выдерживает проверку: причина системная."
        if ps_investigation_result >= 5:
            return "Часть связей подтверждена, но в деле остались разрывы."
        return "Материалы не образуют проверяемой последовательности."


screen ps_investigation_archive_panel():
    vbox:
        spacing 18
        xfill True

        text "ДЕЛО СМЕНЫ // ХРОНОЛОГИЯ":
            color "#d4adff"
            size 31

        text ps_investigation_result_caption():
            color "#c8b9d1"
            size 21

        hbox:
            spacing 12
            xalign 0.5

            for index in range(4):
                frame:
                    xsize 265
                    ysize 145
                    padding (16, 13)
                    background Solid("#332044" if index < len(ps_investigation_chain) else "#1e1724")

                    if index < len(ps_investigation_chain):
                        $ event = ps_investigation_event(ps_investigation_chain[index])
                        vbox:
                            spacing 6
                            text "[index + 1] // [event['stamp']]":
                                color event["accent"]
                                size 17
                            text event["title"]:
                                color "#ffffff"
                                size 21
                            text event["detail"]:
                                color "#bfb1c6"
                                size 16
                    else:
                        text "[index + 1] // —":
                            color "#6c6372"
                            size 21
                            xalign 0.5
                            yalign 0.5

        frame:
            xfill True
            padding (22, 17)
            background Solid("#251633")

            vbox:
                spacing 7
                text "ИТОГОВАЯ ВЕРСИЯ":
                    color "#8ee3bc"
                    size 18
                text ps_investigation_hypothesis_title():
                    color "#ffffff"
                    size 28
                text "Надёжность: [ps_investigation_result] / 9":
                    color "#bca9c8"
                    size 20

        if ps_storm_mimic_seen:
            frame:
                xfill True
                padding (22, 15)
                background Solid("#21142d")

                text ("Поддельный голос V-13 определён." if ps_storm_mimic_correct else "Поддельный голос остался в переписке."):
                    color ("#86e9ba" if ps_storm_mimic_correct else "#e1909b")
                    size 21
