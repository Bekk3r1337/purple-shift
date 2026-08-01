# -*- coding: utf-8 -*-

################################################################################
## Purple Shift 1.2 — режиссура, переписки и новые интерактивные сцены
################################################################################

default ps_ambience_zone = None
default ps_phone_replies = {}
default ps_message_reads = []
default ps_phone_selected_message = "system"
default ps_personal_scene_seen = False

default ps_flow_index = 0
default ps_flow_time = 35
default ps_flow_safety = 0
default ps_flow_result = 0
default ps_flow_people = 0
default ps_flow_mistakes = 0

default ps_case_selected = []
default ps_case_completed = False
default ps_case_result = 0


init -10 python:
    renpy.music.register_channel(
        "ambient",
        mixer="sfx",
        loop=True,
        stop_on_mute=True,
        tight=True,
    )


init python:
    if getattr(persistent, "ps_ambient_enabled", None) is None:
        persistent.ps_ambient_enabled = True

    if getattr(persistent, "ps_reduce_motion", None) is None:
        persistent.ps_reduce_motion = False

    if getattr(persistent, "ps_reduce_flashes", None) is None:
        persistent.ps_reduce_flashes = False

    if getattr(persistent, "ps_minigame_assist", None) is None:
        persistent.ps_minigame_assist = False

    ps_ambience_tracks = {
        "warehouse": "audio/conveyor_loop.ogg",
        "quiet": "audio/ventilation_loop.ogg",
        "alert": "audio/conveyor_loop.ogg",
    }

    ps_message_catalog = [
        {
            "id": "system",
            "day": 1,
            "sender": "Система",
            "time": "22:41",
            "preview": "Профиль смены активирован.",
            "incoming": [
                "Профиль сотрудника подключён к ночной смене.",
                "Здесь будут появляться рабочие сообщения и личные переписки.",
            ],
            "replies": [],
        },
        {
            "id": "newbie",
            "day": 2,
            "sender": "Новичок",
            "time": "05:18",
            "preview": "Ты ещё не спишь?",
            "incoming": [
                "Ты ещё не спишь?",
                "Я всё думаю про ту ошибку. Вдруг завтра снова не замечу?",
            ],
            "replies": [
                {
                    "id": "support",
                    "title": "«Напиши мне код ошибки. Разберём вместе.»",
                    "answer": "Напиши мне код ошибки. Завтра разберём вместе.",
                    "reaction": "Спасибо. Тогда хотя бы не одна.",
                    "effects": {"ps_humanity": 1, "ps_newbie_trust": 2},
                },
                {
                    "id": "procedure",
                    "title": "«Сверяй ячейку перед подтверждением.»",
                    "answer": "Сверяй ячейку до подтверждения. Так надёжнее.",
                    "reaction": "Поняла. Сделаю себе короткую памятку.",
                    "effects": {"ps_efficiency": 1, "ps_newbie_trust": 1},
                },
                {
                    "id": "rest",
                    "title": "«Сейчас главное — поспать.»",
                    "answer": "Сейчас главное — поспать. На усталости ошибок больше.",
                    "reaction": "Ладно. Спокойной... почти ночи.",
                    "effects": {"ps_endurance": 1, "ps_burnout": -1},
                },
            ],
        },
        {
            "id": "veteran",
            "day": 3,
            "sender": "Ветеран",
            "time": "06:02",
            "preview": "Про подъёмник никому не говори.",
            "incoming": [
                "Про подъёмник пока никому не говори.",
                "Но если увидишь код LIFT-09 — сфотографируй время. Потом пригодится.",
            ],
            "replies": [
                {
                    "id": "record",
                    "title": "«Сохраню код и время.»",
                    "answer": "Сохраню код, время и номер участка.",
                    "reaction": "Вот теперь говоришь как человек, которому можно доверять.",
                    "effects": {"ps_evidence": 1, "ps_integrity": 1},
                },
                {
                    "id": "protect",
                    "title": "«Сначала убедимся, что ты цел.»",
                    "answer": "Сначала убедимся, что ты цел. Бумаги потом.",
                    "reaction": "Упрямый. Правильный, но упрямый.",
                    "effects": {"ps_humanity": 1, "ps_team_unity": 1},
                },
            ],
        },
        {
            "id": "joker",
            "day": 4,
            "sender": "Шутник",
            "time": "05:47",
            "preview": "Срочный вопрос.",
            "incoming": [
                "Срочный вопрос.",
                "Если склад когда-нибудь остановится, мы тоже автоматически выключимся?",
            ],
            "replies": [
                {
                    "id": "joke",
                    "title": "«Тебя придётся выключать вручную.»",
                    "answer": "Тебя придётся выключать вручную. И по инструкции.",
                    "reaction": "Значит, бессмертие официально подтверждено.",
                    "effects": {"ps_humor": 2},
                },
                {
                    "id": "honest",
                    "title": "«Ты ведь не просто шутишь?»",
                    "answer": "Ты ведь не просто шутишь?",
                    "reaction": "Не просто. Но пока шучу — держусь.",
                    "effects": {"ps_humanity": 1, "ps_team_unity": 1},
                },
            ],
        },
        {
            "id": "supervisor",
            "day": 6,
            "sender": "Супервайзер",
            "time": "19:36",
            "preview": "Перед сменой зайди в диспетчерскую.",
            "incoming": [
                "Перед сменой зайди в диспетчерскую.",
                "Куратор будет давить на цифры. Мне нужен человек, который помнит факты.",
            ],
            "replies": [
                {
                    "id": "conditions",
                    "title": "«Помогу, если ничего не будем скрывать.»",
                    "answer": "Помогу. Но ничего не подписываю задним числом.",
                    "reaction": "Справедливо. На этот раз работаем по фактам.",
                    "effects": {"ps_supervisor_respect": 2, "ps_integrity": 1},
                },
                {
                    "id": "distance",
                    "title": "«Я не хочу участвовать в вашей игре.»",
                    "answer": "Я принесу журнал. В ваши договорённости не полезу.",
                    "reaction": "Понимаю. Журнал всё равно возьми.",
                    "effects": {"ps_evidence": 1, "ps_endurance": 1},
                },
            ],
        },
    ]

    ps_flow_events = [
        {
            "title": "УПАКОВКА // СТЕКЛО",
            "detail": "Хрупкая коробка идёт без защитного вкладыша.",
            "ideal": "safety",
            "choices": [
                ("safety", "Снять коробку с линии", "Безопасность +2", 2, 0, 0),
                ("result", "Пропустить ради темпа", "Результат +2", -1, 2, 0),
                ("people", "Позвать Леру", "Команда +1", 0, 0, 1),
            ],
        },
        {
            "title": "ЛИНИЯ // ЗАТОР",
            "detail": "На левом сходе растёт очередь из мелких заказов.",
            "ideal": "result",
            "choices": [
                ("safety", "Остановить весь поток", "Безопасность +1", 1, -1, 0),
                ("result", "Перебросить мелкое вправо", "Результат +2", 0, 2, 0),
                ("people", "Попросить людей ускориться", "Команда −1", 0, 1, -1),
            ],
        },
        {
            "title": "РАЦИЯ // ЛЕРА",
            "detail": "Лера сообщает о неизвестном коде ошибки.",
            "ideal": "people",
            "choices": [
                ("safety", "Поставить её сектор в стоп", "Безопасность +1", 1, -1, 0),
                ("result", "Сбросить ошибку удалённо", "Результат +1", -1, 1, 0),
                ("people", "Подойти и проверить вместе", "Команда +2", 1, 0, 2),
            ],
        },
        {
            "title": "ПОДЪЁМНИК // LIFT-09",
            "detail": "На панели снова появляется знакомый код.",
            "ideal": "safety",
            "choices": [
                ("safety", "Заблокировать подъёмник", "Безопасность +2", 2, -1, 0),
                ("result", "Закрыть ошибку и продолжить", "Результат +2", -2, 2, 0),
                ("people", "Отправить туда Виктора", "Риск для Виктора", -1, 1, -1),
            ],
        },
        {
            "title": "ФИНИШ // ТРИ МИНУТЫ",
            "detail": "До закрытия рейтинга остаётся три минуты.",
            "ideal": "people",
            "choices": [
                ("safety", "Снизить скорость линии", "Безопасность +1", 1, -1, 1),
                ("result", "Выжать максимум", "Результат +3", -2, 3, -1),
                ("people", "Сверить готовность команды", "Команда +2", 1, 0, 2),
            ],
        },
    ]

    ps_case_items = [
        (
            "terminal",
            "Журнал ТСД",
            "STOP-04 и LIFT-09 с точным временем.",
            True,
        ),
        (
            "camera",
            "Камера сектора",
            "Видно остановку и положение сотрудников.",
            True,
        ),
        (
            "lift",
            "Бирка подъёмника",
            "Дата последнего осмотра просрочена.",
            True,
        ),
        (
            "rating",
            "Скриншот рейтинга",
            "Доказывает только итоговый процент.",
            False,
        ),
        (
            "rumor",
            "Слух из курилки",
            "Источник неизвестен, времени нет.",
            False,
        ),
    ]

    ps_epilogue_catalog = {
        "truth": {
            "tag": "ПОСЛЕ ПРОВЕРКИ",
            "background": "images/bg/control_room.jpg",
            "accent": "#e0b5ff",
            "line": "Правда не остановила весь склад. Она остановила привычку делать вид, что ничего не произошло.",
        },
        "people": {
            "tag": "СЛЕДУЮЩАЯ СМЕНА",
            "background": "images/cg/team_dawn.jpg",
            "accent": "#91f0c0",
            "line": "Цифры обновились утром. Люди запомнили, кто дождался последнего.",
        },
        "voice": {
            "tag": "ПОСЛЕ СМЕНЫ",
            "background": "images/bg/break_room.jpg",
            "accent": "#8fdcff",
            "line": "Шум вернулся. Теперь в нём различали не только команды, но и голоса.",
        },
        "leader": {
            "tag": "ПЕРВЫЙ ДЕНЬ СТАРШЕГО",
            "background": "images/bg/packing_zone.jpg",
            "accent": "#a7ffad",
            "line": "Ответственность оказалась тяжелее нового жилета. Но кнопку остановки больше не прятали.",
        },
        "employee": {
            "tag": "СЕРТИФИКАТ",
            "background": "images/bg/room_morning.jpg",
            "accent": "#ffd37d",
            "line": "Фиолетовая рамка светилась всю ночь. Комната от этого не стала менее пустой.",
        },
        "exit": {
            "tag": "ВОСЬМОЙ ДЕНЬ",
            "background": "images/bg/street_night.jpg",
            "accent": "#ff9fcf",
            "line": "Впервые будильник не назначал тебе новую смену.",
        },
        "silence": {
            "tag": "НЕЗАКРЫТЫЙ ВОПРОС",
            "background": "images/bg/locker_room.jpg",
            "accent": "#b0a4bd",
            "line": "Иногда тишина — не отсутствие ответа. Иногда это место, где ответ только начинает звучать.",
        },
    }

    def ps_set_ambience(zone):
        global ps_ambience_zone

        ps_ambience_zone = zone
        track = ps_ambience_tracks.get(zone)

        if not persistent.ps_ambient_enabled or not track:
            renpy.music.stop(channel="ambient", fadeout=0.5)
            return

        if renpy.loadable(track):
            renpy.music.play(
                track,
                channel="ambient",
                loop=True,
                fadein=1.0,
                if_changed=True,
            )

    def ps_stop_ambience():
        global ps_ambience_zone
        ps_ambience_zone = None
        renpy.music.stop(channel="ambient", fadeout=1.0)

    def ps_toggle_ambience():
        persistent.ps_ambient_enabled = not persistent.ps_ambient_enabled
        renpy.save_persistent()

        if persistent.ps_ambient_enabled and ps_ambience_zone:
            ps_set_ambience(ps_ambience_zone)
        else:
            renpy.music.stop(channel="ambient", fadeout=0.5)

        renpy.restart_interaction()

    def ps_toggle_reduce_motion():
        persistent.ps_reduce_motion = not persistent.ps_reduce_motion
        renpy.save_persistent()
        renpy.restart_interaction()

    def ps_toggle_reduce_flashes():
        persistent.ps_reduce_flashes = not persistent.ps_reduce_flashes
        renpy.save_persistent()
        renpy.restart_interaction()

    def ps_toggle_minigame_assist():
        persistent.ps_minigame_assist = not persistent.ps_minigame_assist
        renpy.save_persistent()
        renpy.restart_interaction()

    def ps_available_messages():
        return [
            message
            for message in ps_message_catalog
            if message["day"] <= ps_chapter
        ]

    def ps_message_data(message_id):
        for message in ps_message_catalog:
            if message["id"] == message_id:
                return message
        return ps_message_catalog[0]

    def ps_read_message(message_id):
        global ps_message_reads

        if message_id not in ps_message_reads:
            ps_message_reads = ps_message_reads + [message_id]
            renpy.restart_interaction()

    def ps_reply_message(message_id, reply_id):
        global ps_phone_replies
        global ps_key_choices

        if message_id in ps_phone_replies:
            return

        message = ps_message_data(message_id)
        reply = next(
            reply_item
            for reply_item in message["replies"]
            if reply_item["id"] == reply_id
        )

        for variable_name, delta in reply["effects"].items():
            current_value = getattr(renpy.store, variable_name)
            setattr(renpy.store, variable_name, current_value + delta)

        ps_phone_replies = dict(ps_phone_replies)
        ps_phone_replies[message_id] = reply_id
        ps_key_choices = ps_key_choices + [
            "Ты ответил на сообщение: {}.".format(message["sender"])
        ]

        route_by_message = {
            "newbie": "newbie",
            "veteran": "veteran",
            "joker": "joker",
            "supervisor": "supervisor",
        }
        message_route = message.get("route") or route_by_message.get(message_id)
        if message_route:
            ps_add_route(message_route, 1)

        ps_play_sfx("phone_unlock")

        if len(ps_phone_replies) >= 3:
            ps_unlock_achievement("connected")

        renpy.restart_interaction()

    def ps_message_reply(message):
        reply_id = ps_phone_replies.get(message["id"])

        if not reply_id:
            return None

        for reply in message["replies"]:
            if reply["id"] == reply_id:
                return reply

        return None

    def ps_personal_scene_target():
        if hasattr(renpy.store, "ps_route_points"):
            return ps_route_target()

        priorities = [
            ("newbie", ps_newbie_trust + (2 if "newbie" in ps_phone_replies else 0)),
            ("veteran", ps_evidence + ps_integrity + (2 if "veteran" in ps_phone_replies else 0)),
            ("joker", ps_humor + (2 if "joker" in ps_phone_replies else 0)),
            ("supervisor", ps_supervisor_respect + (2 if "supervisor" in ps_phone_replies else 0)),
        ]
        priorities.sort(key=lambda item: item[1], reverse=True)
        return priorities[0][0]

    def ps_flow_start():
        global ps_flow_index
        global ps_flow_time
        global ps_flow_safety
        global ps_flow_result
        global ps_flow_people
        global ps_flow_mistakes

        ps_flow_index = 0
        ps_flow_time = 35
        ps_flow_safety = 0
        ps_flow_result = 0
        ps_flow_people = 0
        ps_flow_mistakes = 0

    def ps_flow_choose(choice_id):
        global ps_flow_index
        global ps_flow_time
        global ps_flow_safety
        global ps_flow_result
        global ps_flow_people
        global ps_flow_mistakes

        if ps_flow_index >= len(ps_flow_events):
            return

        event = ps_flow_events[ps_flow_index]
        choice = next(
            item
            for item in event["choices"]
            if item[0] == choice_id
        )

        ps_flow_safety += choice[3]
        ps_flow_result += choice[4]
        ps_flow_people += choice[5]

        if choice_id != event["ideal"]:
            ps_flow_mistakes += 1
            ps_flow_time = max(0, ps_flow_time - 2)

        ps_flow_index += 1

        ps_play_sfx("scan_ok")

        renpy.restart_interaction()

    def ps_flow_tick():
        global ps_flow_time
        ps_flow_time = max(0, ps_flow_time - 1)
        renpy.restart_interaction()

    def ps_flow_assist():
        global ps_flow_index
        global ps_flow_safety
        global ps_flow_result
        global ps_flow_people

        ps_flow_index = len(ps_flow_events)
        ps_flow_safety = 6
        ps_flow_result = 4
        ps_flow_people = 5
        renpy.restart_interaction()

    def ps_case_start():
        global ps_case_selected
        ps_case_selected = []

    def ps_case_toggle(item_id):
        global ps_case_selected

        if item_id in ps_case_selected:
            ps_case_selected = [
                selected
                for selected in ps_case_selected
                if selected != item_id
            ]
        elif len(ps_case_selected) < 3:
            ps_case_selected = ps_case_selected + [item_id]

        ps_play_sfx("radio")

        renpy.restart_interaction()

    def ps_case_score(selected):
        reliable = {
            item_id
            for item_id, item_title, item_desc, item_reliable in ps_case_items
            if item_reliable
        }
        return len(set(selected) & reliable)

    def ps_case_assist():
        global ps_case_selected
        ps_case_selected = ["terminal", "camera", "lift"]
        renpy.restart_interaction()


################################################################################
## Анимация и постановка
################################################################################

transform ps_enter_left:
    xalign -0.08
    yalign 1.0
    yoffset 5
    zoom 0.60
    alpha 0.0
    ease 0.55 xalign 0.22 alpha 1.0
    function ps_character_breathe

transform ps_enter_right:
    xalign 1.08
    yalign 1.0
    yoffset 5
    zoom 0.65
    alpha 0.0
    ease 0.55 xalign 0.75 alpha 1.0
    function ps_character_breathe

transform ps_attention:
    yalign 1.0
    yoffset 5
    linear 0.08 yoffset -12
    linear 0.12 yoffset 5

transform ps_shock:
    xoffset 0
    linear 0.04 xoffset -10
    linear 0.04 xoffset 10
    linear 0.04 xoffset -6
    linear 0.04 xoffset 0

transform ps_camera_drift:
    zoom 1.025
    xalign 0.5
    yalign 0.5
    linear 9.0 zoom 1.065

transform ps_alarm_pulse:
    alpha 0.0
    linear 0.3 alpha 0.20
    linear 0.45 alpha 0.0
    repeat


################################################################################
## Сообщения в телефоне
################################################################################

screen ps_message_bubble(message_text, outgoing=False):
    frame:
        xalign (1.0 if outgoing else 0.0)
        xmaximum 790
        padding (20, 13)
        background Solid("#633b83" if outgoing else "#2b1b3c")

        text message_text:
            color "#ffffff"
            size 21


screen ps_phone_messages_panel():
    $ available_messages = ps_available_messages()
    $ selected_data = ps_message_data(ps_phone_selected_message)

    hbox:
        spacing 18

        frame:
            xsize 370
            yfill True
            padding (12, 12)
            background Solid("#120b1ddd")

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"

                vbox:
                    spacing 10
                    xfill True

                    text "ЧАТЫ":
                        color "#917ca8"
                        size 20

                    for message in available_messages:
                        $ message_unread = message["id"] not in ps_message_reads
                        $ message_avatar = ps_message_avatar(message)

                        button:
                            id ("ps_message_chat_" + message["id"])
                            action [
                                SetVariable("ps_phone_selected_message", message["id"]),
                                Function(ps_read_message, message["id"]),
                            ]
                            xfill True
                            yminimum 86
                            padding (10, 8)
                            background Solid(
                                "#533174"
                                if message["id"] == ps_phone_selected_message
                                else "#25172f"
                            )
                            hover_background Solid("#6c438d")

                            hbox:
                                spacing 12

                                frame:
                                    xsize 66
                                    ysize 66
                                    padding (2, 2)
                                    background Solid("#160d20")

                                    if message_avatar:
                                        add message_avatar:
                                            xalign 0.5
                                            yalign 0.5
                                            xysize (62, 62)
                                            fit "contain"
                                    else:
                                        text "•":
                                            color "#c99cff"
                                            size 38
                                            xalign 0.5
                                            yalign 0.5

                                vbox:
                                    spacing 5
                                    yalign 0.5
                                    xmaximum 260

                                    text message["sender"]:
                                        color ("#ffffff" if message_unread else "#cbbdd8")
                                        size 19

                                    text message["preview"]:
                                        color "#a998b7"
                                        size 16

                                    if message["id"] in ps_phone_deferred:
                                        text "ОТВЕТ ОТЛОЖЕН":
                                            color "#ffd078"
                                            size 13

        frame:
            xsize 1010
            yfill True
            padding (24, 18)
            background Solid("#120b1ddd")

            vbox:
                spacing 13
                xfill True

                hbox:
                    xfill True

                    vbox:
                        spacing 2

                        text "[selected_data['sender']]":
                            color "#ffffff"
                            size 29

                        text "[ps_message_status(selected_data)]":
                            color "#8f7ca0"
                            size 16

                    text "[selected_data['time']]":
                        color "#806f91"
                        size 19
                        xalign 1.0

                viewport:
                    mousewheel True
                    draggable True
                    ymaximum 520

                    vbox:
                        spacing 10
                        xfill True

                        for incoming_line in selected_data["incoming"]:
                            use ps_message_bubble(incoming_line)

                        if selected_data.get("attachment"):
                            frame:
                                xalign 0.0
                                xsize 640
                                padding (9, 9)
                                background Solid("#2b1b3c")

                                vbox:
                                    spacing 7

                                    add selected_data["attachment"]:
                                        xsize 620
                                        ysize 220
                                        fit "cover"

                                    text selected_data.get("attachment_caption", "Вложение"):
                                        color "#bba9c7"
                                        size 16

                        if selected_data.get("voice_note"):
                            frame:
                                xalign 0.0
                                xsize 640
                                padding (15, 12)
                                background Solid("#2b1b3c")

                                vbox:
                                    spacing 8

                                    textbutton "▶  ГОЛОСОВОЕ СООБЩЕНИЕ":
                                        id "ps_message_voice_note"
                                        action Function(
                                            ps_play_story_voice,
                                            selected_data["id"],
                                        )
                                        xfill True
                                        ysize 48
                                        background Solid("#5a3474")
                                        hover_background Solid("#8050a1")
                                        text_color "#ffffff"
                                        text_size 18
                                        text_xalign 0.5
                                        text_yalign 0.5

                                    text selected_data.get("voice_caption", ""):
                                        color "#bba9c7"
                                        size 17

                        $ chosen_reply = ps_message_reply(selected_data)

                        if chosen_reply:
                            use ps_message_bubble(chosen_reply["answer"], outgoing=True)
                            use ps_message_bubble(chosen_reply["reaction"])
                        elif selected_data["replies"]:
                            null height 8

                            text "Твой ответ":
                                color "#9887aa"
                                size 19

                            for reply in selected_data["replies"]:
                                textbutton reply["title"]:
                                    action Function(
                                        ps_reply_message,
                                        selected_data["id"],
                                        reply["id"],
                                    )
                                    xfill True
                                    yminimum 58
                                    background Solid("#3b2450")
                                    hover_background Solid("#6d4291")
                                    text_color "#ffffff"
                                    text_size 20
                                    text_xalign 0.0

                            if selected_data["id"] not in ps_phone_deferred:
                                textbutton "ОТВЕТИТЬ ПОЗЖЕ":
                                    id "ps_message_defer"
                                    action Function(
                                        ps_defer_message,
                                        selected_data["id"],
                                    )
                                    xfill True
                                    yminimum 50
                                    background Solid("#241a2c")
                                    hover_background Solid("#46334f")
                                    text_color "#b9a8c7"
                                    text_size 17
                                    text_xalign 0.5


################################################################################
## Настройки 1.2
################################################################################

screen ps_director_settings():
    modal True
    zorder 270

    key "game_menu" action Hide("ps_director_settings")

    add Solid("#050208e8")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1120
        ysize 760
        padding (55, 42)
        background Solid("#160b27fa")

        vbox:
            spacing 22
            xfill True

            hbox:
                xfill True

                vbox:
                    text "ПОСТАНОВКА И ДОСТУПНОСТЬ":
                        color "#d2a7ff"
                        size 35

                    text "Настройки сохраняются между прохождениями.":
                        color "#9684aa"
                        size 20

                textbutton "×":
                    id "ps_director_close"
                    action Hide("ps_director_settings")
                    xalign 1.0
                    xsize 60
                    ysize 52
                    background Solid("#3b244d")
                    hover_background Solid("#70458d")
                    text_color "#ffffff"
                    text_size 34
                    text_xalign 0.5
                    text_yalign 0.5

            textbutton "[u'✓' if persistent.ps_ambient_enabled else u'—'] Атмосфера склада":
                action Function(ps_toggle_ambience)
                xfill True
                ysize 82
                background Solid("#4a2d66" if persistent.ps_ambient_enabled else "#28202e")
                hover_background Solid("#714593")
                text_color "#ffffff"
                text_size 25
                text_xalign 0.0

            text "Конвейер, вентиляция и рабочая среда играют отдельным тихим слоем.":
                color "#a99ab8"
                size 20

            textbutton "[u'✓' if persistent.ps_reduce_motion else u'—'] Уменьшить движение":
                action Function(ps_toggle_reduce_motion)
                xfill True
                ysize 82
                background Solid("#4a2d66" if persistent.ps_reduce_motion else "#28202e")
                hover_background Solid("#714593")
                text_color "#ffffff"
                text_size 25
                text_xalign 0.0

            textbutton "[u'✓' if persistent.ps_reduce_flashes else u'—'] Уменьшить вспышки":
                action Function(ps_toggle_reduce_flashes)
                xfill True
                ysize 82
                background Solid("#4a2d66" if persistent.ps_reduce_flashes else "#28202e")
                hover_background Solid("#714593")
                text_color "#ffffff"
                text_size 25
                text_xalign 0.0

            textbutton "[u'✓' if persistent.ps_minigame_assist else u'—'] Помощь в мини-играх":
                action Function(ps_toggle_minigame_assist)
                xfill True
                ysize 82
                background Solid("#4a2d66" if persistent.ps_minigame_assist else "#28202e")
                hover_background Solid("#714593")
                text_color "#ffffff"
                text_size 25
                text_xalign 0.0

            text "Убирает таймер, показывает безопасные решения и разрешает пропуск.":
                color "#a99ab8"
                size 20


################################################################################
## Живая линия — день 5
################################################################################

screen ps_flow_challenge():
    modal True
    zorder 255

    add Solid("#050309ed")
    add "bg packing_zone":
        alpha 0.24

    if ps_flow_index >= len(ps_flow_events) or ps_flow_time <= 0:
        timer 0.15 action Return(
            (
                ps_flow_safety,
                ps_flow_result,
                ps_flow_people,
                ps_flow_mistakes,
            )
        )
    elif not persistent.ps_minigame_assist:
        timer 1.0 repeat True action Function(ps_flow_tick)

    $ flow_event = ps_flow_events[
        min(ps_flow_index, len(ps_flow_events) - 1)
    ]

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1380
        ysize 850
        padding (58, 42)
        background Solid("#140a20f7")

        vbox:
            spacing 22
            xfill True

            hbox:
                xfill True

                vbox:
                    text "ЖИВАЯ ЛИНИЯ":
                        color "#d9b1ff"
                        size 36

                    text "Нельзя спасти всё. Выбери приоритет.":
                        color "#a694b5"
                        size 22

                text (
                    "БЕЗ ТАЙМЕРА"
                    if persistent.ps_minigame_assist
                    else "00:{:02d}".format(ps_flow_time)
                ):
                    color "#ffd078"
                    size 34
                    xalign 1.0

            hbox:
                spacing 14
                xalign 0.5

                frame:
                    xsize 380
                    padding (18, 13)
                    background Solid("#34223f")
                    text "Безопасность: [ps_flow_safety]":
                        color "#83e6a0"
                        size 23

                frame:
                    xsize 380
                    padding (18, 13)
                    background Solid("#34223f")
                    text "Результат: [ps_flow_result]":
                        color "#7fd9ff"
                        size 23

                frame:
                    xsize 380
                    padding (18, 13)
                    background Solid("#34223f")
                    text "Люди: [ps_flow_people]":
                        color "#ff9bd2"
                        size 23

            frame:
                xfill True
                ysize 230
                padding (38, 28)
                background Solid("#0a0710e8")

                vbox:
                    spacing 16
                    xalign 0.5
                    yalign 0.5

                    text "[ps_flow_index + 1] / [len(ps_flow_events)]":
                        color "#81728e"
                        size 19

                    text "[flow_event['title']]":
                        color "#ffffff"
                        size 42
                        xalign 0.5

                    text "[flow_event['detail']]":
                        color "#c7bacf"
                        size 25
                        xalign 0.5

            vbox:
                spacing 13
                xfill True

                for choice in flow_event["choices"]:
                    $ recommended = (
                        persistent.ps_minigame_assist
                        and choice[0] == flow_event["ideal"]
                    )

                    textbutton (
                        (u"РЕКОМЕНДОВАНО // " if recommended else u"")
                        + choice[1]
                        + u"\n"
                        + choice[2]
                    ):
                        id ("ps_flow_" + choice[0])
                        action Function(ps_flow_choose, choice[0])
                        xfill True
                        ysize 92
                        background Solid("#553775" if recommended else "#2d2038")
                        hover_background Solid("#704c91")
                        text_color "#ffffff"
                        text_size 23
                        text_xalign 0.0

            if persistent.ps_minigame_assist:
                textbutton "ПРОПУСТИТЬ С БЕЗОПАСНЫМ РЕЗУЛЬТАТОМ":
                    action [
                        Function(ps_flow_assist),
                        Return((6, 4, 5, 0)),
                    ]
                    xalign 0.5
                    xsize 620
                    ysize 58
                    background Solid("#324c42")
                    hover_background Solid("#47705f")
                    text_color "#d8ffeb"
                    text_size 19
                    text_xalign 0.5
                    text_yalign 0.5


################################################################################
## Доска происшествия — день 6
################################################################################

screen ps_case_board():
    modal True
    zorder 255

    add Solid("#050309ed")
    add "bg control_room":
        alpha 0.22

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1420
        ysize 870
        padding (52, 38)
        background Solid("#130b1df8")

        vbox:
            spacing 22
            xfill True

            hbox:
                xfill True

                vbox:
                    text "РАЗБОР ПРОИСШЕСТВИЯ":
                        color "#d6adff"
                        size 35

                    text "Выбери три материала, которые выдержат проверку.":
                        color "#a895b8"
                        size 22

                text "[len(ps_case_selected)] / 3":
                    color "#ffffff"
                    size 33
                    xalign 1.0

            grid 2 3:
                spacing 16
                xalign 0.5

                for item_id, item_title, item_desc, item_reliable in ps_case_items:
                    $ selected = item_id in ps_case_selected
                    $ reliable_hint = (
                        persistent.ps_minigame_assist
                        and item_reliable
                    )

                    textbutton (
                        (u"НАДЁЖНО // " if reliable_hint else u"")
                        + item_title
                        + u"\n"
                        + item_desc
                    ):
                        action Function(ps_case_toggle, item_id)
                        xsize 630
                        ysize 155
                        background Solid(
                            "#563a73"
                            if selected
                            else "#2a2032"
                        )
                        hover_background Solid("#704b90")
                        text_color "#ffffff"
                        text_size 21
                        text_xalign 0.0

                if persistent.ps_minigame_assist:
                    textbutton "АВТОВЫБОР\nСобрать надёжное дело":
                        action [
                            Function(ps_case_assist),
                            Return(["terminal", "camera", "lift"]),
                        ]
                        xsize 630
                        ysize 155
                        background Solid("#315243")
                        hover_background Solid("#47765f")
                        text_color "#e0ffed"
                        text_size 22
                        text_xalign 0.0
                else:
                    frame:
                        xsize 630
                        ysize 155
                        background Solid("#1c1621")

                        text "Факт важнее громкости.\nСлух важнее факта только в курилке.":
                            color "#786d80"
                            size 21
                            xalign 0.5
                            yalign 0.5
                            text_align 0.5

            textbutton "СОБРАТЬ ДЕЛО":
                id "ps_case_confirm"
                action Return(list(ps_case_selected))
                sensitive len(ps_case_selected) == 3
                xalign 0.5
                xsize 470
                ysize 68
                background Solid("#6c3aa8")
                hover_background Solid("#965bd6")
                insensitive_background Solid("#332a39")
                text_color "#ffffff"
                text_insensitive_color "#726b77"
                text_size 27
                text_xalign 0.5
                text_yalign 0.5


################################################################################
## Эпилог и личная сцена
################################################################################

screen ps_ending_epilogue(ending_id):
    modal True
    zorder 260

    $ epilogue = ps_epilogue_catalog[ending_id]

    add epilogue["background"]
    add Solid("#07030bc4")

    frame:
        xalign 0.5
        yalign 0.78
        xsize 1420
        padding (54, 38)
        background Solid("#100819e8")

        vbox:
            spacing 16
            xfill True

            text "[epilogue['tag']]":
                color epilogue["accent"]
                size 24
                kerning 3
                xalign 0.5

            text "[epilogue['line']]":
                color "#ffffff"
                size 34
                text_align 0.5
                xalign 0.5

            textbutton "ЗАВЕРШИТЬ ИСТОРИЮ":
                id "ps_epilogue_continue"
                action Return()
                xalign 0.5
                xsize 430
                ysize 62
                background Solid("#5d3680")
                hover_background Solid("#8652b2")
                text_color "#ffffff"
                text_size 23
                text_xalign 0.5
                text_yalign 0.5


label ps_personal_scene:
    if ps_personal_scene_seen:
        return

    $ ps_personal_scene_seen = True
    $ ps_personal_target = ps_personal_scene_target()
    $ ps_play_route_motif(ps_personal_target)

    scene bg break_room
    with fade

    $ ps_set_ambience("quiet")
    show screen ps_cinematic_bars

    n "До конца смены остаётся двенадцать минут. В комнате отдыха горит только дальний ряд ламп."

    if ps_personal_target == "newbie":
        show newb relief at ps_enter_right
        with dissolve

        newb "Я хотела сказать спасибо."
        p "За что?"
        newb "За то, что мои ошибки у тебя не превращаются в моё имя."
        p "Ошибка — это событие. Не человек."
        newb "Я записала. Не в ТСД. Себе."

        menu:
            "Предложить вместе составить её собственную инструкцию":
                $ ps_add_route("newbie", 2)
                $ ps_efficiency += 1
                $ ps_newbie_trust += 1

                p "Давай запишем, что делать, когда экран врёт."
                newb "Не памятку «как не ошибаться»?"
                p "Нет. Инструкцию «как доказать, что ошиблась система»."
                newb "Такую я сохраню."

            "Сказать, что в следующий раз она должна говорить первой":
                $ ps_add_route("newbie", 2)
                $ ps_humanity += 1
                $ ps_team_unity += 1

                p "В следующий раз говоришь первой."
                newb "А если голос снова пропадёт?"
                p "Начни с одного слова. Мы подхватим."
                newb "Тогда слово будет «стоп»."

        $ ps_newbie_trust += 2
        $ ps_humanity += 1
        $ ps_key_choices = ps_key_choices + ["Лера перестала бояться говорить об ошибках."]

        hide newb

    elif ps_personal_target == "veteran":
        show vet concerned at ps_enter_left
        with dissolve

        vet "Я раньше думал: опытный — это тот, кто может работать через боль."
        p "А теперь?"
        vet "Теперь думаю: опытный первым замечает, когда пора остановиться. Не дай им снова перепутать выносливость с расходником."

        menu:
            "Потребовать, чтобы завтра он не скрывал боль":
                $ ps_add_route("veteran", 2)
                $ ps_endurance += 1
                $ ps_team_unity += 1

                p "Завтра рука заболела — говоришь сразу."
                vet "Командовать старшими некрасиво."
                p "Тогда считай это обменом опытом."
                vet "Ладно. Один раз разрешаю."

            "Попросить показать всю историю заявок":
                $ ps_add_route("veteran", 2)
                $ ps_evidence += 1
                $ ps_integrity += 1

                p "Мне нужны все номера заявок. Не только последняя."
                vet "Там два года."
                p "Значит, это уже не случайность."
                vet "Вот теперь ты понял."

        $ ps_endurance += 1
        $ ps_evidence += 1
        $ ps_team_unity += 1
        $ ps_key_choices = ps_key_choices + ["Виктор доверил тебе историю подъёмника."]

        hide vet

    elif ps_personal_target == "joker":
        show mem serious at ps_enter_left
        with dissolve

        p "Странно видеть тебя без улыбки."
        mem "Я её на зарядку поставил. Если сегодня всё пойдёт плохо — не пытайся один стать героем."
        p "Это сейчас была серьёзная мысль?"
        mem "Никому не рассказывай. Репутация."

        menu:
            "Пообещать пересчитывать людей вместе с ним":
                $ ps_add_route("joker", 2)
                $ ps_team_unity += 2

                p "Если станет тихо — считаем вдвоём."
                mem "Романтика складского уровня."
                p "Один, два, три, все на месте."
                mem "Звучит лучше большинства признаний."

            "Разрешить ему не шутить хотя бы рядом с тобой":
                $ ps_add_route("joker", 2)
                $ ps_humanity += 1
                $ ps_humor += 1

                p "Рядом со мной можешь иногда не держать зал."
                mem "А если тишина окажется неловкой?"
                p "Переживём."
                mem "Опасный уровень доверия."

        $ ps_humor += 1
        $ ps_team_unity += 2
        $ ps_key_choices = ps_key_choices + ["Макс впервые попросил тебя не геройствовать в одиночку."]

        hide mem

    else:
        show sv stern at ps_enter_right
        with dissolve

        sv "Куратор спросит, кто виноват."
        p "А ты что ответишь?"
        sv "Что вопрос неправильный. Нужно спрашивать, почему три предупреждения не остановили линию."
        p "И ты готов это подписать?"
        sv "Если ты принесёшь факты — да."

        menu:
            "Напомнить, что его подпись важнее твоих доказательств":
                $ ps_add_route("supervisor", 2)
                $ ps_supervisor_respect += 1
                $ ps_integrity += 1

                p "Факты принесу я. Но приказ и подпись будут твоими."
                sv "Знаю."
                p "Хочу услышать это без должности между нами."
                sv "Решение будет моим."

            "Предложить говорить перед куратором вместе":
                $ ps_add_route("supervisor", 2)
                $ ps_team_unity += 1
                $ ps_evidence += 1

                p "Не второй голос. Два человека с одной хронологией."
                sv "Он попробует разделить показания."
                p "Тогда начнём со времени на камерах."
                sv "Хорошо. Вместе."

        $ ps_supervisor_respect += 2
        $ ps_integrity += 1
        $ ps_key_choices = ps_key_choices + ["Артём согласился говорить о причине, а не о виноватом."]

        hide sv

    with dissolve

    hide screen ps_cinematic_bars
    $ ps_stop_route_motif()
    $ ps_stop_ambience()
    return
