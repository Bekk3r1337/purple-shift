# -*- coding: utf-8 -*-

################################################################################
## Постоянный прогресс, достижения и коллекция финалов
################################################################################

default ps_sort_index = 0
default ps_sort_score = 0
default ps_sort_mistakes = 0
default ps_sort_time = 30

default ps_signal_index = 0
default ps_signal_score = 0
default ps_signal_mistakes = 0
default ps_signal_time = 20


init python:
    if getattr(persistent, "ps_unlocked_endings", None) is None:
        persistent.ps_unlocked_endings = []

    if getattr(persistent, "ps_achievements", None) is None:
        persistent.ps_achievements = []

    ps_achievement_catalog = [
        (
            "first_shift",
            "Первая есть",
            "Завершить первый рабочий день.",
        ),
        (
            "red_button",
            "Красная кнопка",
            "Остановить линию до того, как опасность станет происшествием.",
        ),
        (
            "archive",
            "Склад помнит",
            "Собрать не меньше трёх доказательств.",
        ),
        (
            "team",
            "Одна смена",
            "Поднять единство команды до пяти.",
        ),
        (
            "specialist",
            "Свой маршрут",
            "Развить одну из характеристик до двенадцати.",
        ),
        (
            "clean_sort",
            "Без пересорта",
            "Пройти проверку ТСД без единой ошибки.",
        ),
        (
            "dispatcher",
            "Ручное управление",
            "Без ошибок передать команды при отказе системы.",
        ),
        (
            "seven_days",
            "Семь дней спустя",
            "Дойти до финала рабочей недели.",
        ),
        (
            "connected",
            "На связи",
            "Ответить как минимум в трёх переписках.",
        ),
        (
            "flow_keeper",
            "Живая линия",
            "Удержать безопасность, результат и команду во время перегруза.",
        ),
        (
            "investigator",
            "Только факты",
            "Собрать безошибочное дело по происшествию.",
        ),
        (
            "wanderer",
            "Знаю каждый проход",
            "Посетить все пять зон свободной смены.",
        ),
        (
            "confidant",
            "Личный маршрут",
            "Открыть кульминацию отношений с одним из персонажей.",
        ),
        (
            "archive_master",
            "Полная цепочка",
            "Собрать все документы архива за несколько прохождений.",
        ),
        (
            "purple_signal",
            "Сектор V",
            "Найти три базовых следа Фиолетового Шторма за одно прохождение.",
        ),
        (
            "observer",
            "Не проходи мимо",
            "Осмотреть восемь интерактивных точек склада.",
        ),
        (
            "storm_decoder",
            "Шторм на линии",
            "Восстановить скрытую последовательность канала V-13.",
        ),
        (
            "names",
            "По именам",
            "Узнать людей смены не только по их должностям.",
        ),
        (
            "planner",
            "Люди — не ресурс",
            "Самостоятельно составить расстановку ночной смены.",
        ),
        (
            "known_by_storm",
            "Смена узнала тебя",
            "Увидеть своё имя на отключённом табло V-13.",
        ),
    ]

    ps_ending_catalog = [
        (
            "truth",
            "Свет над складом",
            "Сделать скрытые нарушения видимыми.",
            "ending_truth",
        ),
        (
            "people",
            "Смена, в которой остались люди",
            "Поставить команду выше последней зелёной цифры.",
            "ending_people",
        ),
        (
            "voice",
            "Голос в шуме",
            "Собрать людей в единый ритм.",
            "ending_voice",
        ),
        (
            "leader",
            "Старший линии",
            "Принять ответственность, не продав безопасность.",
            "ending_leader",
        ),
        (
            "employee",
            "Сотрудник месяца",
            "Получить первое место и увидеть его настоящую цену.",
            "ending_employee",
        ),
        (
            "exit",
            "Выход существует",
            "Уйти до того, как смена заберёт право решать.",
            "ending_exit",
        ),
        (
            "silence",
            "Тишина после сигнала",
            "Закончить неделю без окончательного ответа.",
            "ending_silence",
        ),
    ]

    ps_sort_items = [
        ("Футболка", "light", "Мягкая упаковка"),
        ("Набор кружек", "fragile", "Хрупкий товар"),
        ("Пауэрбанк", "tech", "Электроника"),
        ("Плед", "light", "Мягкая упаковка"),
        ("Стеклянная ваза", "fragile", "Хрупкий товар"),
        ("Наушники", "tech", "Электроника"),
    ]

    ps_sort_zones = [
        ("light", "A-12\nМЯГКОЕ"),
        ("fragile", "F-07\nХРУПКОЕ"),
        ("tech", "T-03\nТЕХНИКА"),
    ]

    ps_signal_sequence = [
        ("left", "ЛЕВАЯ ЛИНИЯ"),
        ("buffer", "БУФЕР B-04"),
        ("right", "ПРАВАЯ ЛИНИЯ"),
        ("stop", "ОБЩИЙ СТОП"),
    ]

    ps_signal_buttons = [
        ("right", "ПРАВАЯ"),
        ("stop", "СТОП"),
        ("left", "ЛЕВАЯ"),
        ("buffer", "БУФЕР"),
    ]

    def ps_unlock_achievement(achievement_id, notify=True):
        if achievement_id in persistent.ps_achievements:
            return False

        persistent.ps_achievements.append(achievement_id)
        renpy.save_persistent()

        if notify:
            title = next(
                item[1]
                for item in ps_achievement_catalog
                if item[0] == achievement_id
            )
            renpy.notify("Достижение: {}".format(title))

        return True

    def ps_unlock_ending(ending_id):
        if ending_id in persistent.ps_unlocked_endings:
            return False

        persistent.ps_unlocked_endings.append(ending_id)
        renpy.save_persistent()
        renpy.notify("Открыт финал: {}".format(ps_ending_title(ending_id)))
        return True

    def ps_evaluate_achievements():
        if ps_chapter >= 2:
            ps_unlock_achievement("first_shift")

        if ps_second_shift_path == "остановил линию":
            ps_unlock_achievement("red_button")

        if ps_evidence >= 3:
            ps_unlock_achievement("archive")

        if ps_team_unity >= 5:
            ps_unlock_achievement("team")

        if max(ps_humanity, ps_endurance, ps_efficiency, ps_humor) >= 12:
            ps_unlock_achievement("specialist")

    def ps_sort_start():
        global ps_sort_index
        global ps_sort_score
        global ps_sort_mistakes
        global ps_sort_time

        ps_sort_index = 0
        ps_sort_score = 0
        ps_sort_mistakes = 0
        ps_sort_time = 30

    def ps_sort_choose(zone_id):
        global ps_sort_index
        global ps_sort_score
        global ps_sort_mistakes
        global ps_sort_time

        if ps_sort_index >= len(ps_sort_items):
            return

        correct_zone = ps_sort_items[ps_sort_index][1]

        if zone_id == correct_zone:
            ps_sort_score += 1
            ps_sort_index += 1

            ps_play_sfx("scan_ok")
        else:
            ps_sort_mistakes += 1
            ps_sort_time = max(0, ps_sort_time - 3)

            ps_play_sfx("scan_error")

        renpy.restart_interaction()

    def ps_sort_tick():
        global ps_sort_time

        ps_sort_time = max(0, ps_sort_time - 1)
        renpy.restart_interaction()

    def ps_signal_start():
        global ps_signal_index
        global ps_signal_score
        global ps_signal_mistakes
        global ps_signal_time

        ps_signal_index = 0
        ps_signal_score = 0
        ps_signal_mistakes = 0
        ps_signal_time = 20

    def ps_signal_choose(signal_id):
        global ps_signal_index
        global ps_signal_score
        global ps_signal_mistakes
        global ps_signal_time

        if ps_signal_index >= len(ps_signal_sequence):
            return

        expected_id = ps_signal_sequence[ps_signal_index][0]

        if signal_id == expected_id:
            ps_signal_score += 1
            ps_signal_index += 1

            ps_play_sfx("scan_ok")
        else:
            ps_signal_mistakes += 1
            ps_signal_time = max(0, ps_signal_time - 3)

            ps_play_sfx("scan_error")

        renpy.restart_interaction()

    def ps_signal_tick():
        global ps_signal_time

        ps_signal_time = max(0, ps_signal_time - 1)
        renpy.restart_interaction()


################################################################################
## Общие визуальные компоненты
################################################################################

screen ps_progress_dots(current_day):
    hbox:
        spacing 18
        xalign 0.5

        for day_number in range(1, 8):
            frame:
                xsize 92
                ysize 74
                padding (0, 0)
                background Solid(
                    "#9a5ee6"
                    if day_number == current_day
                    else "#51306f"
                    if day_number < current_day
                    else "#241731"
                )

                vbox:
                    spacing 1
                    xalign 0.5
                    yalign 0.5

                    text "ДЕНЬ":
                        color "#d8c9e9"
                        size 16
                        xalign 0.5

                    text "[day_number]":
                        color "#ffffff"
                        size 30
                        xalign 0.5


screen ps_day_card(day, title, subtitle):
    modal True
    zorder 230

    on "show" action Function(ps_evaluate_achievements)

    add Solid("#08030fee")
    add "images/ui/fon.jpg":
        alpha 0.18

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1380
        ysize 820
        padding (86, 64)
        background Solid("#160b27f7")

        vbox:
            spacing 28
            xfill True

            text "ФИОЛЕТОВАЯ СМЕНА":
                color "#8665a8"
                size 25
                kerning 4
                xalign 0.5

            text "ГЛАВА [day]":
                color "#c99cff"
                size 34
                xalign 0.5

            text title:
                color "#ffffff"
                size 64
                text_align 0.5
                xalign 0.5

            text subtitle:
                color "#cdbde0"
                size 27
                text_align 0.5
                xalign 0.5

            null height 10

            use ps_progress_dots(day)

            frame:
                xfill True
                padding (30, 20)
                background Solid("#221235cc")

                hbox:
                    xfill True

                    text "Текущий путь":
                        color "#9d88b8"
                        size 23

                    text "[ps_route_name()]":
                        color "#ffffff"
                        size 27
                        xalign 1.0

            textbutton "НАЧАТЬ ДЕНЬ":
                id "ps_day_start"
                action Return()
                xalign 0.5
                xsize 450
                ysize 72
                background Solid("#6c3aa8")
                hover_background Solid("#9b5ee0")
                text_color "#ffffff"
                text_size 28
                text_xalign 0.5
                text_yalign 0.5


screen ps_phone_stat(title, value, accent):
    frame:
        xsize 510
        ysize 96
        padding (20, 13)
        background Solid("#25163ae8")

        vbox:
            spacing 8

            hbox:
                xfill True

                text title:
                    color "#eee6f7"
                    size 23

                text "[value]":
                    color accent
                    size 23
                    xalign 1.0

            bar:
                value StaticValue(ps_clamp(value), 12)
                xmaximum 470
                ymaximum 14
                left_bar Solid(accent)
                right_bar Solid("#49345f")


screen ps_relation_row(name, value, accent, caption):
    frame:
        xfill True
        ysize 112
        padding (24, 16)
        background Solid("#25163ae8")

        vbox:
            spacing 8

            hbox:
                xfill True

                text name:
                    color "#ffffff"
                    size 26

                text "[value]":
                    color accent
                    size 26
                    xalign 1.0

            bar:
                value StaticValue(max(0, min(12, value + 3)), 15)
                xmaximum 940
                ymaximum 14
                left_bar Solid(accent)
                right_bar Solid("#49345f")

            text caption:
                color "#a997bf"
                size 19


################################################################################
## Телефон героя
################################################################################

screen ps_phone(initial_tab="status"):
    modal True
    zorder 240
    default tab = initial_tab
    default person = "newbie"

    on "show" action Function(ps_play_sfx, "phone_unlock")

    key "game_menu" action Hide("ps_phone")
    key "K_p" action Hide("ps_phone")

    add Solid("#050208dd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1540
        ysize 940
        padding (42, 32)
        background Solid("#11091dfb")
        at ps_phone_arrive

        vbox:
            spacing 22
            xfill True

            hbox:
                xfill True

                vbox:
                    spacing 3

                    text "СМЕНА // ТЕЛЕФОН":
                        color "#c99cff"
                        size 35

                    text "День [ps_chapter] из 7":
                        color "#9382a8"
                        size 21

                textbutton "×":
                    id "ps_phone_close"
                    action Hide("ps_phone")
                    xalign 1.0
                    xsize 62
                    ysize 54
                    background Solid("#3b244d")
                    hover_background Solid("#70458d")
                    text_color "#ffffff"
                    text_size 35
                    text_xalign 0.5
                    text_yalign 0.5

            hbox:
                spacing 10
                xalign 0.5

                textbutton "СОСТОЯНИЕ":
                    action SetScreenVariable("tab", "status")
                    background Solid("#7442a7" if tab == "status" else "#291a38")
                    hover_background Solid("#8d55c4")
                    text_color "#ffffff"
                    xsize 185
                    ysize 58
                    text_size 19
                    text_xalign 0.5
                    text_yalign 0.5

                textbutton "ЛЮДИ":
                    action SetScreenVariable("tab", "people")
                    background Solid("#7442a7" if tab == "people" else "#291a38")
                    hover_background Solid("#8d55c4")
                    text_color "#ffffff"
                    xsize 185
                    ysize 58
                    text_size 19
                    text_xalign 0.5
                    text_yalign 0.5

                textbutton ("ЧАТЫ ({})".format(ps_unread_message_count()) if ps_unread_message_count() else "ЧАТЫ"):
                    id "ps_phone_messages_tab"
                    action SetScreenVariable("tab", "messages")
                    background Solid("#7442a7" if tab == "messages" else "#291a38")
                    hover_background Solid("#8d55c4")
                    text_color "#ffffff"
                    xsize 185
                    ysize 58
                    text_size 19
                    text_xalign 0.5
                    text_yalign 0.5

                textbutton "АРХИВ":
                    id "ps_phone_archive_tab"
                    action SetScreenVariable("tab", "archive")
                    background Solid("#7442a7" if tab == "archive" else "#291a38")
                    hover_background Solid("#8d55c4")
                    text_color "#ffffff"
                    xsize 185
                    ysize 58
                    text_size 19
                    text_xalign 0.5
                    text_yalign 0.5

                textbutton "V-13":
                    id "ps_phone_signal_tab"
                    action SetScreenVariable("tab", "signal")
                    background Solid("#7442a7" if tab == "signal" else "#291a38")
                    hover_background Solid("#8d55c4")
                    text_color "#ffffff"
                    xsize 185
                    ysize 58
                    text_size 18
                    text_xalign 0.5
                    text_yalign 0.5

                textbutton "ДОСТИЖЕНИЯ":
                    action SetScreenVariable("tab", "achievements")
                    background Solid("#7442a7" if tab == "achievements" else "#291a38")
                    hover_background Solid("#8d55c4")
                    text_color "#ffffff"
                    xsize 185
                    ysize 58
                    text_size 17
                    text_xalign 0.5
                    text_yalign 0.5

                textbutton "ФИНАЛЫ":
                    action SetScreenVariable("tab", "endings")
                    background Solid("#7442a7" if tab == "endings" else "#291a38")
                    hover_background Solid("#8d55c4")
                    text_color "#ffffff"
                    xsize 185
                    ysize 58
                    text_size 19
                    text_xalign 0.5
                    text_yalign 0.5

            frame:
                xfill True
                ysize 690
                padding (34, 28)
                background Solid("#190e29e8")

                if tab == "status":
                    vbox:
                        spacing 20

                        use ps_progress_dots(ps_chapter)

                        grid 2 2:
                            spacing 16
                            xalign 0.5

                            use ps_phone_stat("Человечность", ps_humanity, "#ff86c8")
                            use ps_phone_stat("Выносливость", ps_endurance, "#7fd9ff")
                            use ps_phone_stat("Эффективность", ps_efficiency, "#8dff9b")
                            use ps_phone_stat("Юмор", ps_humor, "#ffd36f")

                        frame:
                            xfill True
                            padding (25, 18)
                            background Solid("#27163ddd")

                            vbox:
                                spacing 7

                                text "[ps_route_name()]":
                                    color "#ffffff"
                                    size 31
                                    xalign 0.5

                                text "[ps_route_description()]":
                                    color "#b7a5ce"
                                    size 22
                                    xalign 0.5

                        hbox:
                            spacing 18
                            xalign 0.5

                            text "Улики: [ps_evidence]":
                                color "#c6a4ed"
                                size 23

                            text "Команда: [ps_team_unity]":
                                color "#89e6c1"
                                size 23

                            text "Честность: [ps_integrity]":
                                color "#ffd083"
                                size 23

                            text "Выгорание: [ps_burnout]":
                                color "#ff8d92"
                                size 23

                elif tab == "people":
                    hbox:
                        spacing 22
                        xfill True
                        yfill True

                        vbox:
                            spacing 12
                            xsize 330

                            text "ЛЮДИ СМЕНЫ":
                                color "#ffffff"
                                size 31

                            for route_id, accent in [
                                ("newbie", "#ff7ad7"),
                                ("veteran", "#ffd27a"),
                                ("joker", "#7ad7ff"),
                                ("supervisor", "#7cff7c"),
                            ]:
                                textbutton ps_character_display_name(route_id):
                                    id ("ps_people_" + route_id)
                                    action SetScreenVariable("person", route_id)
                                    xfill True
                                    ysize 66
                                    background Solid("#4e2a68" if person == route_id else "#271733")
                                    hover_background Solid("#694087")
                                    text_color accent
                                    text_size 24
                                    text_xalign 0.08
                                    text_yalign 0.5

                            null height 8

                            frame:
                                xfill True
                                padding (18, 15)
                                background Solid("#211334cc")

                                vbox:
                                    spacing 7

                                    text "КОМАНДА // [ps_team_unity]":
                                        color "#89e6c1"
                                        size 21

                                    text "Виктор: [u'в порядке' if ps_veteran_safe else u'травмирован']":
                                        color "#d9cae9"
                                        size 19

                        $ profile = ps_character_profile(person)

                        frame:
                            xfill True
                            yfill True
                            padding (30, 24)
                            background Solid("#211334dd")

                            if not ps_names_revealed:
                                vbox:
                                    spacing 20
                                    xalign 0.5
                                    yalign 0.45

                                    text ps_character_display_name(person):
                                        color "#d9b8ff"
                                        size 38
                                        xalign 0.5

                                    text "Вы пока знаете друг друга только по должностям. Иногда имя — первое настоящее действие против системы, которая видит в людях строки отчёта.":
                                        color "#bbaaca"
                                        size 24
                                        text_align 0.5
                                        xmaximum 780
                            else:
                                vbox:
                                    spacing 15

                                    text profile["full_name"]:
                                        color "#ffffff"
                                        size 38

                                    text "[profile['role']]  ·  [profile['age']]":
                                        color "#b99bd4"
                                        size 22

                                    frame:
                                        xfill True
                                        padding (20, 15)
                                        background Solid("#2b1940")

                                        vbox:
                                            spacing 7

                                            text "ЧТО НЕ ГОВОРИТ ВСЛУХ":
                                                color "#d49cff"
                                                size 18

                                            text profile["truth"]:
                                                color "#eee7f2"
                                                size 22

                                    frame:
                                        xfill True
                                        padding (20, 15)
                                        background Solid("#251935")

                                        vbox:
                                            spacing 7

                                            text "ЧЕГО ЖДЁТ ОТ ТЕБЯ":
                                                color "#8de6c2"
                                                size 18

                                            text profile["need"]:
                                                color "#eee7f2"
                                                size 22

                                    text "Близость маршрута: [ps_route_points.get(person, 0)]":
                                        color "#d8c8e4"
                                        size 22

                                    if ps_relationship_memories:
                                        text "Последний общий момент":
                                            color "#a98bc2"
                                            size 18

                                        text ps_relationship_memories[-1]:
                                            color "#cfc2d9"
                                            size 20

                elif tab == "messages":
                    use ps_phone_messages_panel()

                elif tab == "archive":
                    use ps_archive_panel()

                elif tab == "signal":
                    use ps_storm_signal_panel()

                elif tab == "achievements":
                    viewport:
                        mousewheel True
                        draggable True
                        scrollbars "vertical"

                        vbox:
                            spacing 13
                            xfill True

                            text "Открыто: [len(persistent.ps_achievements)] / [len(ps_achievement_catalog)]":
                                color "#ffffff"
                                size 31

                            for achievement_id, achievement_title, achievement_desc in ps_achievement_catalog:
                                $ achievement_open = achievement_id in persistent.ps_achievements

                                frame:
                                    xfill True
                                    ysize 96
                                    padding (22, 14)
                                    background Solid("#38214c" if achievement_open else "#1d1623")

                                    vbox:
                                        spacing 5

                                        text (achievement_title if achievement_open else "???"):
                                            color ("#d7b4ff" if achievement_open else "#6f6678")
                                            size 26

                                        text (achievement_desc if achievement_open else "Условие пока скрыто"):
                                            color ("#b9a8ca" if achievement_open else "#5f5865")
                                            size 20

                else:
                    viewport:
                        mousewheel True
                        draggable True
                        scrollbars "vertical"

                        vbox:
                            spacing 13
                            xfill True

                            text "Открыто: [len(persistent.ps_unlocked_endings)] / [len(ps_ending_catalog)]":
                                color "#ffffff"
                                size 31

                            for ending_id, ending_title, ending_desc, ending_label in ps_ending_catalog:
                                $ ending_open = ending_id in persistent.ps_unlocked_endings

                                frame:
                                    xfill True
                                    ysize 108
                                    padding (22, 14)
                                    background Solid("#38214c" if ending_open else "#1d1623")

                                    hbox:
                                        xfill True

                                        vbox:
                                            spacing 5
                                            xmaximum 970

                                            text (ending_title if ending_open else "Неизвестный финал"):
                                                color ("#d7b4ff" if ending_open else "#6f6678")
                                                size 26

                                            text (ending_desc if ending_open else "Продолжай принимать решения"):
                                                color ("#b9a8ca" if ending_open else "#5f5865")
                                                size 20

                                        if ending_open:
                                            textbutton "ПОВТОРИТЬ":
                                                action Replay(ending_label, locked=False)
                                                xalign 1.0
                                                yalign 0.5
                                                xsize 210
                                                ysize 54
                                                background Solid("#61358c")
                                                hover_background Solid("#8c54c2")
                                                text_color "#ffffff"
                                                text_xalign 0.5
                                                text_yalign 0.5


################################################################################
## Выбор разговора на перерыве
################################################################################

screen ps_break_choice():
    modal True
    zorder 220

    add Solid("#08040ddd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1320
        ysize 720
        padding (60, 48)
        background Solid("#160b27f7")

        vbox:
            spacing 26
            xfill True

            text "ПЕРЕРЫВ // 10 МИНУТ":
                color "#c99cff"
                size 42
                xalign 0.5

            text "К кому подойти?":
                color "#d8cbe7"
                size 27
                xalign 0.5

            grid 2 2:
                spacing 18
                xalign 0.5

                textbutton "ЛЕРА\nПоговорить о недостаче":
                    id "ps_break_newbie"
                    action Return("newbie")
                    xsize 520
                    ysize 160
                    background Solid("#4c2448")
                    hover_background Solid("#7c3a73")
                    text_color "#ffffff"
                    text_size 24
                    text_xalign 0.5
                    text_yalign 0.5

                textbutton "ВИКТОР\nСпросить про подъёмник":
                    id "ps_break_veteran"
                    action Return("veteran")
                    xsize 520
                    ysize 160
                    background Solid("#4a3b25")
                    hover_background Solid("#765e36")
                    text_color "#ffffff"
                    text_size 24
                    text_xalign 0.5
                    text_yalign 0.5

                textbutton "МАКС\nДать мозгу выдохнуть":
                    id "ps_break_joker"
                    action Return("joker")
                    xsize 520
                    ysize 160
                    background Solid("#234153")
                    hover_background Solid("#37677e")
                    text_color "#ffffff"
                    text_size 24
                    text_xalign 0.5
                    text_yalign 0.5

                textbutton "ТИШИНА\nПобыть одному":
                    id "ps_break_alone"
                    action Return("alone")
                    xsize 520
                    ysize 160
                    background Solid("#2f2935")
                    hover_background Solid("#51455b")
                    text_color "#ffffff"
                    text_size 24
                    text_xalign 0.5
                    text_yalign 0.5


################################################################################
## Мини-игра ТСД
################################################################################

screen ps_sort_challenge():
    modal True
    zorder 250

    add Solid("#030507ee")

    $ ps_sort_item = ps_sort_items[
        min(ps_sort_index, len(ps_sort_items) - 1)
    ]

    if ps_sort_index >= len(ps_sort_items) or ps_sort_time <= 0:
        timer 0.15 action Return((ps_sort_score, ps_sort_mistakes))
    else:
        timer 1.0 repeat True action Function(ps_sort_tick)

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1260
        ysize 820
        padding (58, 42)
        background Solid("#11151af8")

        vbox:
            spacing 25
            xfill True

            hbox:
                xfill True

                text "ТСД // КОНТРОЛЬНАЯ СЕРИЯ":
                    color "#b8ffca"
                    size 32

                text "00:[ps_sort_time:02d]":
                    color ("#ffdc79" if ps_sort_time > 10 else "#ff7b83")
                    size 32
                    xalign 1.0

            bar:
                value StaticValue(ps_sort_time, 30)
                xmaximum 1140
                ymaximum 15
                left_bar Solid("#55c779")
                right_bar Solid("#3a2631")

            frame:
                xfill True
                ysize 250
                padding (35, 28)
                background Solid("#07090bdd")

                vbox:
                    spacing 12
                    xalign 0.5
                    yalign 0.5

                    text "ТОВАР [ps_sort_index + 1] / [len(ps_sort_items)]":
                        color "#718079"
                        size 22

                    text "[ps_sort_item[0]]":
                        color "#ffffff"
                        size 53
                        xalign 0.5

                    text "[ps_sort_item[2]]":
                        color "#aab8b0"
                        size 25
                        xalign 0.5

            text "Выбери правильный сектор":
                color "#d4ded8"
                size 25
                xalign 0.5

            hbox:
                spacing 18
                xalign 0.5

                for zone_id, zone_title in ps_sort_zones:
                    textbutton zone_title:
                        action Function(ps_sort_choose, zone_id)
                        xsize 350
                        ysize 125
                        background Solid("#1f5131" if zone_id == "light" else "#5c3425" if zone_id == "fragile" else "#263f5c")
                        hover_background Solid("#34794a" if zone_id == "light" else "#8c4e36" if zone_id == "fragile" else "#3b6189")
                        text_color "#ffffff"
                        text_size 25
                        text_xalign 0.5
                        text_yalign 0.5

            hbox:
                xfill True

                text "Верно: [ps_sort_score]":
                    color "#7fe79a"
                    size 24

                text "Ошибки: [ps_sort_mistakes]":
                    color "#ff858c"
                    size 24
                    xalign 1.0


################################################################################
## Мини-игра ручного управления
################################################################################

screen ps_signal_challenge():
    modal True
    zorder 250

    add Solid("#08020bea")
    add "bg warehouse_alert":
        alpha 0.23

    if ps_signal_index >= len(ps_signal_sequence) or ps_signal_time <= 0:
        timer 0.15 action Return((ps_signal_score, ps_signal_mistakes))
    else:
        timer 1.0 repeat True action Function(ps_signal_tick)

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1320
        ysize 830
        padding (58, 44)
        background Solid("#160a20f5")

        vbox:
            spacing 24
            xfill True

            hbox:
                xfill True

                text "РУЧНОЕ УПРАВЛЕНИЕ":
                    color "#f2b4ff"
                    size 35

                text "00:[ps_signal_time:02d]":
                    color ("#ffdc79" if ps_signal_time > 8 else "#ff737d")
                    size 35
                    xalign 1.0

            text "Передай команды в указанном порядке":
                color "#d7c9df"
                size 25
                xalign 0.5

            hbox:
                spacing 13
                xalign 0.5

                for sequence_index, sequence_item in enumerate(ps_signal_sequence):
                    $ sequence_done = sequence_index < ps_signal_index
                    $ sequence_current = sequence_index == ps_signal_index

                    frame:
                        xsize 270
                        ysize 105
                        padding (12, 10)
                        background Solid(
                            "#2d7044"
                            if sequence_done
                            else "#7b3f91"
                            if sequence_current
                            else "#2c2033"
                        )

                        vbox:
                            spacing 4
                            xalign 0.5
                            yalign 0.5

                            text "[sequence_index + 1]":
                                color "#b9a7c4"
                                size 18
                                xalign 0.5

                            text "[sequence_item[1]]":
                                color "#ffffff"
                                size 22
                                xalign 0.5
                                text_align 0.5

            null height 12

            grid 2 2:
                spacing 18
                xalign 0.5

                for signal_id, signal_title in ps_signal_buttons:
                    textbutton signal_title:
                        action Function(ps_signal_choose, signal_id)
                        xsize 520
                        ysize 150
                        background Solid("#443052")
                        hover_background Solid("#784e91")
                        text_color "#ffffff"
                        text_size 29
                        text_xalign 0.5
                        text_yalign 0.5

            hbox:
                xfill True

                text "Передано: [ps_signal_score] / [len(ps_signal_sequence)]":
                    color "#83e6a0"
                    size 24

                text "Ошибки: [ps_signal_mistakes]":
                    color "#ff858c"
                    size 24
                    xalign 1.0
