# -*- coding: utf-8 -*-

################################################################################
## Purple Shift 1.3 — «Следы смены»
## Карта склада, маршруты персонажей, архив и скрытая линия Шторма
################################################################################

default ps_exploration_visits = {}
default ps_route_points = {
    "newbie": 0,
    "veteran": 0,
    "joker": 0,
    "supervisor": 0,
}
default ps_trace_clues = []
default ps_consequence_log = []
default ps_storm_fragments = []
default ps_route_scene_seen = False
default ps_route_scene_id = None
default ps_chapter_replay_mode = False
default ps_run_recorded = False


init python:
    if getattr(persistent, "ps_unlocked_documents", None) is None:
        persistent.ps_unlocked_documents = []

    if getattr(persistent, "ps_unlocked_cgs", None) is None:
        persistent.ps_unlocked_cgs = []

    if getattr(persistent, "ps_unlocked_tracks", None) is None:
        persistent.ps_unlocked_tracks = []

    if getattr(persistent, "ps_unlocked_chapters", None) is None:
        persistent.ps_unlocked_chapters = [1]

    if getattr(persistent, "ps_completed_routes", None) is None:
        persistent.ps_completed_routes = []

    if getattr(persistent, "ps_storm_unlocked", None) is None:
        persistent.ps_storm_unlocked = False

    if getattr(persistent, "ps_total_runs", None) is None:
        persistent.ps_total_runs = 0

    ps_map_zone_catalog = [
        {
            "id": "break",
            "title": "Комната отдыха",
            "subtitle": "Люди говорят тише, когда рядом нет табло.",
            "image": "images/bg/break_room.jpg",
            "accent": "#ff86c8",
        },
        {
            "id": "mezzanine",
            "title": "Мезонин",
            "subtitle": "Наверху лучше видно поток и его слабые места.",
            "image": "images/bg/mezzanine.jpg",
            "accent": "#ffd083",
        },
        {
            "id": "packing",
            "title": "Упаковка",
            "subtitle": "Здесь цифры получают вес, ленту и чужие руки.",
            "image": "images/bg/packing_zone.jpg",
            "accent": "#8dff9b",
        },
        {
            "id": "control",
            "title": "Диспетчерская",
            "subtitle": "Экраны знают больше, чем написано в отчётах.",
            "image": "images/bg/control_room.jpg",
            "accent": "#c99cff",
        },
        {
            "id": "dock",
            "title": "Погрузочный док",
            "subtitle": "На краю склада остаётся место для воздуха.",
            "image": "images/bg/loading_dock.jpg",
            "accent": "#7fd9ff",
        },
    ]

    ps_route_catalog = [
        (
            "newbie",
            "Маршрут Леры",
            "Не дать чужой ошибке превратиться в имя человека.",
            "#ff7ad7",
        ),
        (
            "veteran",
            "Маршрут Виктора",
            "Научиться останавливать работу раньше, чем тело остановит её само.",
            "#ffd27a",
        ),
        (
            "joker",
            "Маршрут Макса",
            "Услышать серьёзное между двумя шутками.",
            "#7ad7ff",
        ),
        (
            "supervisor",
            "Маршрут Артёма",
            "Понять цену приказа и ответственность за тех, кто его выполняет.",
            "#7cff7c",
        ),
    ]

    ps_document_catalog = [
        (
            "handover_note",
            "Ночная передача участка",
            "В журнале передачи есть остановка, которой нет в цифровой истории.",
        ),
        (
            "lift_marking",
            "Метка LIFT-09",
            "Датчик перегруза отмечали неисправным ещё до начала недели.",
        ),
        (
            "account_trace",
            "Цепочка сорока семи",
            "Недостача прошла через буфер после сбоя привязки аккаунтов.",
        ),
        (
            "maintenance_ticket",
            "Заявка на ремонт",
            "Подъёмник разрешили использовать после отменённой заявки.",
        ),
        (
            "camera_copy",
            "Копия с камеры",
            "Запись подтверждает время остановки и присутствие всей смены.",
        ),
        (
            "sealed_manifest",
            "Накладная V-13",
            "Груз из закрытого сектора отсутствует в обычном реестре.",
        ),
    ]

    ps_cg_catalog = [
        (
            "emergency_stop",
            "Красная кнопка",
            "images/cg/emergency_stop.jpg",
        ),
        (
            "report_pressure",
            "Цена подписи",
            "images/cg/report_pressure.jpg",
        ),
        (
            "team_dawn",
            "После смены",
            "images/cg/team_dawn.jpg",
        ),
        (
            "route_newbie",
            "Не ошибка",
            "images/cg/route_newbie.jpg",
        ),
        (
            "route_veteran",
            "Опыт не обязан болеть",
            "images/cg/route_veteran.jpg",
        ),
        (
            "route_joker",
            "Пока смеёмся",
            "images/cg/route_joker.jpg",
        ),
        (
            "route_supervisor",
            "Правильный вопрос",
            "images/cg/route_supervisor.jpg",
        ),
        (
            "storm_signal",
            "Сектор V",
            "images/cg/storm_signal.jpg",
        ),
        (
            "team_names",
            "Больше не должности",
            "images/cg/team_names.jpg",
        ),
        (
            "shift_plan",
            "Цена расстановки",
            "images/cg/shift_plan.jpg",
        ),
        (
            "monitor_guest",
            "Лишний сотрудник",
            "images/cg/monitor_guest.jpg",
        ),
        (
            "future_message",
            "Сообщение из завтра",
            "images/cg/future_message.jpg",
        ),
        (
            "named_shift",
            "Смена узнала тебя",
            "images/cg/named_shift.jpg",
        ),
    ]

    ps_music_catalog = [
        (
            "menu",
            "Фиолетовая смена",
            "audio/menu_theme.mp3",
            1,
        ),
        (
            "home",
            "До выхода",
            "audio/home_ambient.mp3",
            1,
        ),
        (
            "city",
            "Город идёт домой",
            "audio/city_night.mp3",
            2,
        ),
        (
            "walk",
            "Ночной маршрут",
            "audio/night_walk.mp3",
            2,
        ),
        (
            "shift",
            "Начало потока",
            "audio/night_shift.mp3",
            3,
        ),
        (
            "warehouse",
            "Ритм линии",
            "audio/warehouse_chill.mp3",
            3,
        ),
        (
            "after",
            "После сигнала",
            "audio/after_shift_ambient.mp3",
            4,
        ),
    ]

    ps_chapter_catalog = [
        (1, "Первая смена", "start"),
        (2, "Вторая смена", "ps_replay_day_2"),
        (3, "Чужие цифры", "ps_replay_day_3"),
        (4, "Чужая ошибка", "ps_replay_day_4"),
        (5, "Предел нагрузки", "ps_replay_day_5"),
        (6, "Цена подписи", "ps_replay_day_6"),
        (7, "Последняя смена", "ps_replay_day_7"),
    ]

    def ps_append_unique_persistent(attribute_name, item_id):
        items = list(getattr(persistent, attribute_name, []) or [])
        if item_id in items:
            return False

        items.append(item_id)
        setattr(persistent, attribute_name, items)
        renpy.save_persistent()
        return True

    def ps_begin_day(day):
        ps_append_unique_persistent("ps_unlocked_chapters", day)
        ps_note_story_day(day)

        for track_id, track_title, track_path, unlock_day in ps_music_catalog:
            if unlock_day <= day:
                ps_append_unique_persistent("ps_unlocked_tracks", track_id)

    def ps_day_zone_visits(day):
        return list(ps_exploration_visits.get(day, []))

    def ps_record_visit(day, zone_id):
        global ps_exploration_visits

        visits = dict(ps_exploration_visits)
        day_visits = list(visits.get(day, []))

        if zone_id not in day_visits:
            day_visits.append(zone_id)

        visits[day] = day_visits
        ps_exploration_visits = visits

        unique_zones = set()
        for visited_zones in ps_exploration_visits.values():
            unique_zones.update(visited_zones)

        if len(unique_zones) >= 5:
            ps_unlock_achievement("wanderer")

    def ps_add_route(route_id, amount=1):
        global ps_route_points

        route_points = dict(ps_route_points)
        route_points[route_id] = route_points.get(route_id, 0) + amount
        ps_route_points = route_points

    def ps_route_score(route_id):
        base_scores = {
            "newbie": ps_newbie_trust,
            "veteran": ps_evidence + ps_integrity,
            "joker": ps_humor + ps_team_unity,
            "supervisor": ps_supervisor_respect + ps_efficiency,
        }
        return ps_route_points.get(route_id, 0) * 3 + base_scores[route_id]

    def ps_route_target():
        priorities = [
            (route_id, ps_route_score(route_id))
            for route_id, route_title, route_desc, route_accent in ps_route_catalog
        ]
        priorities.sort(key=lambda item: item[1], reverse=True)
        return priorities[0][0]

    def ps_route_title(route_id):
        for item_id, title, description, accent in ps_route_catalog:
            if item_id == route_id:
                return title
        return "Маршрут смены"

    def ps_record_consequence(text):
        global ps_consequence_log
        if text not in ps_consequence_log:
            ps_consequence_log = ps_consequence_log + [text]

    def ps_collect_document(document_id, trace=True):
        global ps_trace_clues

        unlocked = ps_append_unique_persistent(
            "ps_unlocked_documents",
            document_id,
        )

        if trace and document_id not in ps_trace_clues:
            ps_trace_clues = ps_trace_clues + [document_id]

        if unlocked:
            title = next(
                item[1]
                for item in ps_document_catalog
                if item[0] == document_id
            )
            renpy.notify("Архив пополнен: {}".format(title))

        if len(persistent.ps_unlocked_documents) >= len(ps_document_catalog):
            ps_unlock_achievement("archive_master")

        return unlocked

    def ps_collect_storm_fragment(fragment_id):
        global ps_storm_fragments

        if fragment_id not in ps_storm_fragments:
            ps_storm_fragments = ps_storm_fragments + [fragment_id]
            renpy.notify(
                "Неизвестный сигнал: {}/{}".format(
                    len(ps_storm_fragments),
                    len(ps_storm_fragment_catalog),
                )
            )

        if len(ps_storm_fragments) >= 3:
            ps_unlock_achievement("purple_signal")

    def ps_storm_ready():
        required = {"violet_stamp", "dead_channel", "sealed_manifest"}
        return required.issubset(set(ps_storm_fragments))

    def ps_unlock_cg(cg_id, notify=False):
        unlocked = ps_append_unique_persistent("ps_unlocked_cgs", cg_id)
        if unlocked and notify:
            title = next(
                item[1]
                for item in ps_cg_catalog
                if item[0] == cg_id
            )
            renpy.notify("Открыт CG: {}".format(title))
        return unlocked

    def ps_unlock_route(route_id):
        if ps_append_unique_persistent("ps_completed_routes", route_id):
            renpy.notify("Открыт {}".format(ps_route_title(route_id)))
        ps_unlock_achievement("confidant")

    def ps_finish_run():
        global ps_run_recorded

        if ps_run_recorded:
            return

        persistent.ps_total_runs += 1
        ps_run_recorded = True
        renpy.save_persistent()

    def ps_cg_data(cg_id):
        for item_id, title, image_path in ps_cg_catalog:
            if item_id == cg_id:
                return (title, image_path)
        return ("Неизвестный кадр", "images/bg/bg_black.jpg")

    def ps_completion_percent():
        ending_part = len(persistent.ps_unlocked_endings)
        achievement_part = len(persistent.ps_achievements)
        document_part = len(persistent.ps_unlocked_documents)
        cg_part = len(persistent.ps_unlocked_cgs)
        route_part = len(persistent.ps_completed_routes)
        inspection_part = len(
            getattr(persistent, "ps_inspected_hotspots", []) or []
        )
        inspection_total = sum(
            len(inspection["hotspots"])
            for inspection in ps_inspection_catalog.values()
        )

        total = (
            len(ps_ending_catalog)
            + len(ps_achievement_catalog)
            + len(ps_document_catalog)
            + len(ps_cg_catalog)
            + len(ps_route_catalog)
            + inspection_total
        )
        opened = (
            ending_part
            + achievement_part
            + document_part
            + cg_part
            + route_part
            + min(inspection_part, inspection_total)
        )

        if total <= 0:
            return 0

        return int(round(100.0 * opened / total))

    def ps_zone_event_label(day, zone_id):
        return "ps_trace_d{}_{}".format(day, zone_id)

    def ps_prepare_chapter(day):
        global ps_humanity
        global ps_endurance
        global ps_efficiency
        global ps_humor
        global ps_newbie_trust
        global ps_supervisor_respect
        global ps_team_unity
        global ps_integrity
        global ps_evidence
        global ps_burnout
        global ps_first_shift_path
        global ps_second_shift_path
        global ps_third_day_path
        global ps_fourth_day_path
        global ps_fifth_day_path
        global ps_sixth_day_path
        global ps_veteran_safe
        global ps_signed_false_report
        global ps_key_choices
        global ps_chapter_replay_mode
        global ps_route_tendencies
        global ps_route_turns_seen
        global ps_route_resolutions_seen
        global ps_reactive_echoes_seen
        global ps_team_conflicts_seen
        global ps_team_conflict_results
        global ps_investigation_chain
        global ps_investigation_hypothesis
        global ps_investigation_result
        global ps_investigation_complete
        global ps_storm_mimic_choice
        global ps_storm_mimic_correct
        global ps_storm_mimic_seen
        global ps_zero_shift_seen
        global ps2_fatigue
        global ps2_pressure
        global ps2_resolve
        global ps2_team_trust
        global ps2_team_fear
        global ps2_team_fracture
        global ps2_team_aid
        global ps2_day_intentions
        global ps2_after_choices
        global ps2_decision_map
        global ps2_scenes_seen
        global ps2_silences
        global ps2_final_preparation
        global ps2_route_crisis_result
        global ps21_route_day6_choice
        global ps21_route_final_action
        global ps21_route_outcome
        global ps21_route_memory

        ps_humanity = min(11, day + 4)
        ps_endurance = min(10, day + 3)
        ps_efficiency = min(12, day + 5)
        ps_humor = min(10, day + 3)
        ps_newbie_trust = min(6, max(2, day - 1))
        ps_supervisor_respect = min(6, max(2, day - 2))
        ps_team_unity = min(6, max(2, day - 2))
        ps_integrity = min(5, max(1, day - 3))
        ps_evidence = min(4, max(1, day - 3))
        ps_burnout = max(0, day - 4)
        ps_first_shift_path = "протянул руку"
        ps_second_shift_path = "остановил линию"
        ps_third_day_path = "сохранил журнал"
        ps_fourth_day_path = "защитил новичка"
        ps_fifth_day_path = "остановил подъёмник"
        ps_sixth_day_path = "отказался подписывать"
        ps_veteran_safe = True
        ps_signed_false_report = False
        ps_key_choices = [
            "Выбор главы восстановил сбалансированный путь до этого дня."
        ]
        ps_chapter_replay_mode = True

        route_seed = 2 if day >= 6 else (1 if day >= 4 else 0)
        ps_route_tendencies = {
            route_id: {"growth": route_seed, "shadow": 0}
            for route_id in ("newbie", "veteran", "joker", "supervisor")
        }
        ps_route_turns_seen = (
            ["3:{}".format(route_id) for route_id in ps_route_tendencies]
            if day >= 4 else []
        )
        if day >= 6:
            ps_route_turns_seen += [
                "5:{}".format(route_id) for route_id in ps_route_tendencies
            ]
        ps_route_resolutions_seen = []
        ps_reactive_echoes_seen = [echo_day for echo_day in (4, 5, 6, 7) if echo_day < day]
        ps_team_conflicts_seen = [conflict_day for conflict_day in (3, 4, 5, 6) if conflict_day < day]
        ps_team_conflict_results = {
            3: "listen",
            4: "lera_first",
            5: "record_stop",
            6: "shared_timeline",
        }
        ps_investigation_chain = list(ps_investigation_expected) if day >= 7 else []
        ps_investigation_hypothesis = "systemic" if day >= 7 else None
        ps_investigation_result = 9 if day >= 7 else 0
        ps_investigation_complete = day >= 7
        ps_storm_mimic_choice = "max" if day >= 7 else None
        ps_storm_mimic_correct = day >= 7
        ps_storm_mimic_seen = day >= 7
        ps_zero_shift_seen = False

        ps2_fatigue = min(8, max(1, day - 1))
        ps2_pressure = min(8, max(1, day - 2))
        ps2_resolve = min(8, max(2, day))
        ps2_team_trust = min(7, max(1, day - 1))
        ps2_team_fear = min(5, max(0, day - 3))
        ps2_team_fracture = min(3, max(0, day - 5))
        ps2_team_aid = min(7, max(1, day - 2))
        ps2_day_intentions = {
            previous_day: "люди"
            for previous_day in range(1, day)
        }
        ps2_after_choices = {
            previous_day: "разговор"
            for previous_day in range(1, day)
        }
        ps2_decision_map = [
            {
                "key": "{}:восстановлено:chapter".format(previous_day),
                "day": previous_day,
                "phase": "восстановлено",
                "id": "chapter",
                "title": "Сбалансированный путь",
                "consequence": "Выбор главы восстановил человеческий путь до этого дня.",
            }
            for previous_day in range(1, day)
        ]
        ps2_scenes_seen = [
            "{}_{}".format(phase, previous_day)
            for previous_day in range(1, day)
            for phase in ("pre", "shift", "after")
        ]
        ps2_silences = []
        ps2_final_preparation = None
        ps2_route_crisis_result = None
        ps21_route_day6_choice = None
        ps21_route_final_action = None
        ps21_route_outcome = None
        ps21_route_memory = []

        if day >= 2:
            ps_reveal_character_names()
        if day >= 6:
            ps_set_curator_name()

    def ps_save_metadata(data):
        data["ps_day"] = ps_chapter
        data["ps_route"] = ps_route_name()
        data["ps_version"] = config.version

    if ps_save_metadata not in config.save_json_callbacks:
        config.save_json_callbacks.append(ps_save_metadata)


################################################################################
## Карта склада и память решений
################################################################################

screen ps_warehouse_map(day, remaining):
    modal True
    zorder 245

    $ visited_zones = ps_day_zone_visits(day)

    add Solid("#050208ee")
    add "images/ui/fon.jpg":
        alpha 0.10

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1540
        ysize 960
        padding (48, 34)
        background Solid("#11091df8")

        vbox:
            spacing 18
            xfill True

            text "КАРТА НОЧНОЙ СМЕНЫ":
                color "#c99cff"
                size 39
                xalign 0.5

            text "Свободное время ограничено. Осталось действий: [remaining]":
                color "#b9aacb"
                size 23
                xalign 0.5

            grid 3 2:
                spacing 18
                xalign 0.5

                for zone in ps_map_zone_catalog:
                    $ zone_visited = zone["id"] in visited_zones

                    button:
                        id ("ps_map_" + zone["id"])
                        xsize 445
                        ysize 350
                        padding (12, 12)
                        sensitive not zone_visited
                        action Return(zone["id"])
                        background Solid(
                            "#211334"
                            if not zone_visited
                            else "#16111be8"
                        )
                        hover_background Solid("#43245e")

                        vbox:
                            spacing 10
                            xfill True

                            add Transform(
                                zone["image"],
                                xysize=(420, 205),
                            )

                            text zone["title"]:
                                color (
                                    zone["accent"]
                                    if not zone_visited
                                    else "#71687a"
                                )
                                size 27

                            text (
                                zone["subtitle"]
                                if not zone_visited
                                else "Событие этой зоны уже прожито."
                            ):
                                color (
                                    "#c7bbd3"
                                    if not zone_visited
                                    else "#69616f"
                                )
                                size 18

                null width 445 height 350

            text "Не все сцены можно увидеть за одно прохождение.":
                color "#8f80a1"
                size 20
                xalign 0.5


screen ps_consequence_echo(day):
    modal True
    zorder 244

    add Solid("#07030dee")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1260
        padding (72, 52)
        background Solid("#160b27f7")

        vbox:
            spacing 22
            xfill True

            text "СМЕНА ПОМНИТ":
                color "#c99cff"
                size 30
                kerning 4
                xalign 0.5

            text "Перед началом дня [day]":
                color "#ffffff"
                size 42
                xalign 0.5

            for consequence in ps_consequence_log[-3:]:
                frame:
                    xfill True
                    padding (26, 18)
                    background Solid("#25163ae8")

                    text "• [consequence]":
                        color "#ded4e9"
                        size 24

            textbutton "ПРОДОЛЖИТЬ":
                id "ps_echo_continue"
                action Return()
                xalign 0.5
                xsize 400
                ysize 64
                background Solid("#6c3aa8")
                hover_background Solid("#9b5ee0")
                text_color "#ffffff"
                text_size 24
                text_xalign 0.5
                text_yalign 0.5


label ps_exploration_phase(day, slots=1):
    $ ps_exploration_remaining = slots

    while ps_exploration_remaining > 0:
        call screen ps_warehouse_map(day, ps_exploration_remaining)
        $ ps_selected_zone = _return
        $ ps_record_visit(day, ps_selected_zone)
        $ ps_set_ambience(ps_zone_soundscape(ps_selected_zone))
        call expression ps_zone_event_label(day, ps_selected_zone)
        $ ps_exploration_remaining -= 1

    return


label ps_show_consequence_echo(day):
    if ps_consequence_log:
        call screen ps_consequence_echo(day)
    return


################################################################################
## Архив, галерея и музыка
################################################################################

screen ps_archive_panel():

    vbox:
        spacing 15
        xfill True

        hbox:
            xfill True

            text "Исследовано: [ps_completion_percent()]%":
                color "#ffffff"
                size 29

            text "Прохождений: [persistent.ps_total_runs]":
                color "#9e8bb5"
                size 21
                xalign 1.0
                yalign 0.5

        bar:
            value StaticValue(ps_completion_percent(), 100)
            xmaximum 1320
            ymaximum 14
            left_bar Solid("#9a5ee6")
            right_bar Solid("#39264b")

        hbox:
            spacing 10
            xalign 0.5

            for section_id, section_title in [
                ("documents", "ДОКУМЕНТЫ"),
                ("cgs", "CG"),
                ("music", "МУЗЫКА"),
                ("routes", "МАРШРУТЫ"),
            ]:
                textbutton section_title:
                    id ("ps_archive_" + section_id)
                    action SetVariable("ps_archive_section", section_id)
                    xsize 285
                    ysize 48
                    background Solid(
                        "#7442a7"
                        if ps_archive_section == section_id
                        else "#291a38"
                    )
                    hover_background Solid("#8d55c4")
                    text_color "#ffffff"
                    text_size 18
                    text_xalign 0.5
                    text_yalign 0.5

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"

            vbox:
                spacing 12
                xfill True

                if ps_archive_section == "documents":
                    for document_id, document_title, document_desc in ps_document_catalog:
                        $ document_open = document_id in persistent.ps_unlocked_documents

                        frame:
                            xfill True
                            padding (22, 15)
                            background Solid(
                                "#38214c"
                                if document_open
                                else "#1d1623"
                            )

                            vbox:
                                spacing 5

                                text (
                                    document_title
                                    if document_open
                                    else "ЗАКРЫТЫЙ ДОКУМЕНТ"
                                ):
                                    color (
                                        "#d7b4ff"
                                        if document_open
                                        else "#6f6678"
                                    )
                                    size 24

                                text (
                                    document_desc
                                    if document_open
                                    else "Исследуй склад между сюжетными сценами."
                                ):
                                    color (
                                        "#b9a8ca"
                                        if document_open
                                        else "#5f5865"
                                    )
                                    size 19

                elif ps_archive_section == "cgs":
                    for cg_id, cg_title, cg_path in ps_cg_catalog:
                        $ cg_open = cg_id in persistent.ps_unlocked_cgs

                        frame:
                            xfill True
                            ysize 86
                            padding (22, 13)
                            background Solid(
                                "#38214c"
                                if cg_open
                                else "#1d1623"
                            )

                            hbox:
                                xfill True

                                text (cg_title if cg_open else "Неизвестный кадр"):
                                    color (
                                        "#d7b4ff"
                                        if cg_open
                                        else "#6f6678"
                                    )
                                    size 24
                                    yalign 0.5

                                if cg_open:
                                    textbutton "СМОТРЕТЬ":
                                        action Show(
                                            "ps_gallery_viewer",
                                            asset_id=cg_id,
                                        )
                                        xalign 1.0
                                        xsize 220
                                        ysize 50
                                        background Solid("#61358c")
                                        hover_background Solid("#8c54c2")
                                        text_color "#ffffff"
                                        text_size 19
                                        text_xalign 0.5
                                        text_yalign 0.5

                elif ps_archive_section == "music":
                    for track_id, track_title, track_path, unlock_day in ps_music_catalog:
                        $ track_open = track_id in persistent.ps_unlocked_tracks

                        frame:
                            xfill True
                            ysize 86
                            padding (22, 13)
                            background Solid(
                                "#38214c"
                                if track_open
                                else "#1d1623"
                            )

                            hbox:
                                xfill True

                                text (
                                    track_title
                                    if track_open
                                    else "Неизвестная композиция"
                                ):
                                    color (
                                        "#d7b4ff"
                                        if track_open
                                        else "#6f6678"
                                    )
                                    size 24
                                    yalign 0.5

                                if track_open:
                                    textbutton "СЛУШАТЬ":
                                        action Play(
                                            "music",
                                            track_path,
                                            loop=True,
                                            fadein=0.8,
                                        )
                                        xalign 1.0
                                        xsize 210
                                        ysize 50
                                        background Solid("#31557a")
                                        hover_background Solid("#477da9")
                                        text_color "#ffffff"
                                        text_size 18
                                        text_xalign 0.5
                                        text_yalign 0.5

                    textbutton "ОСТАНОВИТЬ МУЗЫКУ":
                        action Stop("music", fadeout=0.8)
                        xalign 0.5
                        xsize 360
                        ysize 50
                        background Solid("#4b273d")
                        hover_background Solid("#75405e")
                        text_color "#ffffff"
                        text_size 18
                        text_xalign 0.5
                        text_yalign 0.5

                else:
                    for route_id, route_title, route_desc, route_accent in ps_route_catalog:
                        $ route_open = route_id in persistent.ps_completed_routes

                        frame:
                            xfill True
                            padding (22, 15)
                            background Solid(
                                "#38214c"
                                if route_open
                                else "#1d1623"
                            )

                            vbox:
                                spacing 5

                                text (
                                    route_title
                                    if route_open
                                    else "Неизвестный маршрут"
                                ):
                                    color (
                                        route_accent
                                        if route_open
                                        else "#6f6678"
                                    )
                                    size 24

                                text (
                                    route_desc
                                    if route_open
                                    else "Проведи больше свободного времени с одним персонажем."
                                ):
                                    color (
                                        "#b9a8ca"
                                        if route_open
                                        else "#5f5865"
                                    )
                                    size 19

                    if persistent.ps_storm_unlocked:
                        frame:
                            xfill True
                            padding (22, 15)
                            background Solid("#2b1642")

                            text "Скрытая линия: Фиолетовый Шторм":
                                color "#c884ff"
                                size 24


screen ps_gallery_viewer(asset_id):
    modal True
    zorder 280

    $ gallery_title, gallery_path = ps_cg_data(asset_id)

    add gallery_path
    add Solid("#05020888")

    frame:
        xalign 0.5
        yalign 0.94
        xsize 1000
        padding (30, 18)
        background Solid("#100819e8")

        hbox:
            xfill True

            text gallery_title:
                color "#ffffff"
                size 27
                yalign 0.5

            textbutton "ЗАКРЫТЬ":
                id "ps_gallery_close"
                action Hide("ps_gallery_viewer")
                xalign 1.0
                xsize 220
                ysize 50
                background Solid("#61358c")
                hover_background Solid("#8c54c2")
                text_color "#ffffff"
                text_size 19
                text_xalign 0.5
                text_yalign 0.5


screen ps_chapter_select():
    tag menu

    use ps_chapter_select_content


screen ps_chapter_select_content():
    add "images/ui/fon.jpg"
    add Solid("#08030fcf")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1360
        ysize 900
        padding (70, 48)
        background Solid("#150a26f6")

        vbox:
            spacing 20
            xfill True

            text "ВЫБОР ГЛАВЫ":
                color "#c99cff"
                size 44
                xalign 0.5

            text "Открытые главы запускаются со сбалансированным набором прошлых решений.":
                color "#b9a8ca"
                size 22
                text_align 0.5
                xalign 0.5

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"

                vbox:
                    spacing 12
                    xfill True

                    for chapter_day, chapter_title, chapter_label in ps_chapter_catalog:
                        $ chapter_open = chapter_day in persistent.ps_unlocked_chapters

                        textbutton "ДЕНЬ [chapter_day] — [chapter_title]":
                            id (
                                "ps_chapter_{}".format(chapter_day)
                                if chapter_day == 1
                                else None
                            )
                            action (
                                Start(chapter_label)
                                if chapter_open
                                else NullAction()
                            )
                            sensitive chapter_open
                            xfill True
                            ysize 68
                            background Solid(
                                "#4c2b6d"
                                if chapter_open
                                else "#1d1623"
                            )
                            hover_background Solid("#8050ad")
                            text_color (
                                "#ffffff"
                                if chapter_open
                                else "#625a69"
                            )
                            text_size 24
                            text_xalign 0.5
                            text_yalign 0.5

            textbutton "НАЗАД":
                action ShowMenu("main_menu")
                xalign 0.5
                xsize 320
                ysize 58
                background Solid("#3b244d")
                hover_background Solid("#70458d")
                text_color "#ffffff"
                text_size 21
                text_xalign 0.5
                text_yalign 0.5


################################################################################
## Запуск открытых глав
################################################################################

label ps_replay_day_2:
    $ ps_prepare_chapter(2)
    jump chapter3_second_shift


label ps_replay_day_3:
    $ ps_prepare_chapter(3)
    jump chapter3_day_three


label ps_replay_day_4:
    $ ps_prepare_chapter(4)
    jump chapter4_day_four


label ps_replay_day_5:
    $ ps_prepare_chapter(5)
    jump chapter5_day_five


label ps_replay_day_6:
    $ ps_prepare_chapter(6)
    jump chapter6_day_six


label ps_replay_day_7:
    $ ps_prepare_chapter(7)
    jump chapter7_day_seven


################################################################################
## Исследование — день 2
################################################################################

label ps_trace_d2_break:
    scene bg break_room
    with fade

    $ ps_set_ambience("quiet")

    show newb tired at ps_right
    with dissolve

    n "До запуска линии остаётся девять минут. Лера сидит над сложенным вчетверо листком."

    newb "Я записываю ошибки. Не свои. Вообще все, которые вижу."

    p "Зачем?"

    newb "Если они повторяются, значит, дело не только во мне."

    menu:
        "Помочь превратить записи в понятный чек-лист":
            $ ps_add_route("newbie", 2)
            $ ps_newbie_trust += 2
            $ ps_humanity += 1
            $ ps_record_consequence("Ты помог Новичку отделить свои ошибки от ошибок системы.")

            p "Давай разделим: экран, ячейка, подтверждение. И отдельно — что делала система."

            newb "Так выглядит не как признание вины."
            p "Потому что это не оно."

        "Добавить к записям номера операций":
            $ ps_add_route("newbie", 1)
            $ ps_newbie_trust += 1
            $ ps_efficiency += 1
            $ ps_evidence += 1
            $ ps_record_consequence("Записи Новичка превратились в проверяемый журнал операций.")

            p "Без номеров скажут, что ты неправильно помнишь."
            newb "А с номерами?"
            p "Тогда им придётся придумать что-нибудь сложнее."

    n "Она отрывает половину листка и протягивает тебе. На обороте — время вчерашней передачи участка."

    $ ps_collect_document("handover_note")

    hide newb
    with dissolve
    return


label ps_trace_d2_mezzanine:
    scene bg mezzanine
    with fade

    $ ps_set_ambience("warehouse")

    show vet neutral at ps_left
    with dissolve

    n "Виктор проверяет ограждение у грузового подъёмника. На металлической панели выцарапано: LIFT-09."

    vet "Запомни. Если эта лампа мигает дважды — платформа считает вес неправильно."

    p "Почему её не ремонтируют?"
    vet "Потому что пока она едет."

    menu:
        "Спросить, сколько раз это уже происходило":
            $ ps_add_route("veteran", 2)
            $ ps_evidence += 1
            $ ps_integrity += 1
            $ ps_record_consequence("Виктор рассказал тебе о старой неисправности подъёмника.")

            p "Сколько раз она мигала?"
            vet "Достаточно, чтобы перестать считать."
            p "Я всё равно начну."
            vet "Тогда считай и даты."

        "Проверить аварийную кнопку рядом":
            $ ps_add_route("veteran", 1)
            $ ps_endurance += 1
            $ ps_team_unity += 1
            $ ps_record_consequence("Ты заранее нашёл аварийную кнопку мезонина.")

            n "Кнопка закрыта прозрачной крышкой. Крышка открывается туже, чем должна."

            vet "Хорошо. В опасный момент руки должны помнить быстрее головы."

    hide vet
    with dissolve
    return


label ps_trace_d2_packing:
    scene bg packing_zone
    with fade

    $ ps_set_ambience("warehouse")

    show sv neutral at ps_right
    with dissolve

    n "На упаковке копится очередь нестандартных товаров. Артём один переставляет приоритеты на терминале."

    sv "Раз пришёл — выбирай. Спасти время или освободить безопасный проход."

    menu:
        "Сначала убрать тяжёлые коробки из прохода":
            $ ps_add_route("supervisor", 2)
            $ ps_humanity += 1
            $ ps_team_unity += 1
            $ ps_supervisor_respect += 1
            $ ps_record_consequence("На упаковке ты поставил безопасный проход выше таймера.")

            p "Если кто-то споткнётся, времени потеряем больше."
            sv "Правильный ответ."
            p "А почему тогда спрашивал?"
            sv "Проверял, какой ответ выберешь без подсказки."

        "Перенаправить мелкие заказы и разгрузить очередь":
            $ ps_add_route("supervisor", 1)
            $ ps_efficiency += 2
            $ ps_supervisor_respect += 1
            $ ps_record_consequence("Ты помог Артёму разгрузить очередь без остановки участка.")

            p "Мелкое — на свободный стол. Тяжёлое пока не двигаем."
            sv "Быстро понял схему."
            p "Она несложная."
            sv "Схемы обычно несложные. Люди устают."

    hide sv
    with dissolve
    return


label ps_trace_d2_control:
    scene bg control_room
    with fade

    $ ps_set_ambience("quiet")

    n "Диспетчерская пуста. Один монитор оставлен на журнале передачи смен. В 02:14 участок отмечен жёлтым. Причина остановки удалена, но подпись осталась."

    menu:
        "Сохранить номер передачи и время":
            $ ps_add_route("supervisor", 1)
            $ ps_evidence += 2
            $ ps_integrity += 1
            $ ps_record_consequence("Ты сохранил запись ночной передачи, которую не успели стереть полностью.")

            n "Ты фотографируешь экран. На снимке нет ответа. Зато теперь существует вопрос."

        "Проверить, кто подтвердил передачу":
            $ ps_add_route("supervisor", 2)
            $ ps_supervisor_respect += 1
            $ ps_evidence += 1
            $ ps_record_consequence("В журнале передачи ты нашёл подпись Артёма.")

            n "Подпись принадлежит Артёму. Рядом серым: «Изменено после закрытия смены»."

    $ ps_collect_document("handover_note")
    return


label ps_trace_d2_dock:
    scene bg loading_dock
    with fade

    $ ps_set_ambience("quiet")

    show mem grin at ps_left
    with dissolve

    mem "Добро пожаловать в единственную часть склада, где коробки иногда уезжают."

    p "А люди?"
    mem "Люди возвращаются завтра."

    n "Под колесом пустой тележки лежит сорванная пломба. На ней фиолетовый знак: круг, перечёркнутый тремя линиями."

    mem "Такого сектора у нас нет."

    menu:
        "Сфотографировать пломбу":
            $ ps_add_route("joker", 2)
            $ ps_humor += 1
            $ ps_evidence += 1
            $ ps_record_consequence("На доке вы с Максом нашли пломбу несуществующего сектора.")

            p "Теперь хотя бы есть фотография."
            mem "Отлично. Если исчезнем — у полиции будет очень атмосферная улика."

        "Спрятать пломбу в карман":
            $ ps_add_route("joker", 1)
            $ ps_integrity += 1
            $ ps_record_consequence("Ты сохранил странную фиолетовую пломбу с погрузочного дока.")

            p "Потом разберёмся."
            mem "Фраза человека, который только что поднял начало побочного квеста."

    $ ps_collect_storm_fragment("violet_stamp")

    hide mem
    with dissolve
    return


################################################################################
## Исследование — день 3
################################################################################

label ps_trace_d3_break:
    scene bg break_room
    with fade

    $ ps_set_ambience("quiet")

    show mem serious at ps_left
    with dissolve

    n "Макс сидит перед автоматом с кофе. Стакан пуст, а монеты всё ещё лежат в ладони."

    p "Автомат победил?"
    mem "Я просто забыл, зачем пришёл."

    menu:
        "Сесть рядом и не торопить":
            $ ps_add_route("joker", 2)
            $ ps_humanity += 1
            $ ps_burnout -= 1
            $ ps_record_consequence("Ты позволил Максу несколько минут не поддерживать чужое настроение.")

            n "Вы молчите. Впервые рядом с ним тишина не кажется паузой перед шуткой."

            mem "Спасибо."
            p "За что?"
            mem "Что не спросил второй раз."

        "Купить два кофе и перевести всё в шутку":
            $ ps_add_route("joker", 1)
            $ ps_humor += 2
            $ ps_team_unity += 1
            $ ps_record_consequence("Короткий перерыв вернул Максу голос перед тяжёлой сменой.")

            p "Один тебе. Второй — твоей профессиональной репутации."
            mem "Репутации без сахара."

    hide mem
    with dissolve
    return


label ps_trace_d3_mezzanine:
    scene bg mezzanine
    with fade

    $ ps_set_ambience("warehouse")

    show vet concerned at ps_left
    with dissolve

    n "На корпусе подъёмника свежая наклейка закрывает старую маркировку. Виктор поддевает угол перчаткой."

    vet "Вот. LIFT-09. Проверка просрочена."

    menu:
        "Снять обе маркировки одним кадром":
            $ ps_add_route("veteran", 2)
            $ ps_evidence += 2
            $ ps_integrity += 1
            $ ps_record_consequence("Вы с Виктором сохранили настоящую маркировку подъёмника.")

            p "Старая дата и новая наклейка."
            vet "Так даже специалист из офиса поймёт."

        "Попросить Виктора больше не пользоваться подъёмником":
            $ ps_add_route("veteran", 2)
            $ ps_humanity += 1
            $ ps_team_unity += 1
            $ ps_record_consequence("Ты попросил Виктора не проверять неисправный подъёмник собственным телом.")

            vet "А кто будет?"
            p "Не человек. Пока не починят."
            vet "Слишком разумно для этого здания."

    $ ps_collect_document("lift_marking")

    hide vet
    with dissolve
    return


label ps_trace_d3_packing:
    scene bg packing_zone
    with fade

    $ ps_set_ambience("warehouse")

    show newb worried at ps_right
    with dissolve

    n "Лера держит коробку с двумя разными этикетками."

    newb "ТСД говорит — электроника. На старой наклейке — хрупкое."

    menu:
        "Остановить операцию и проверить карточку товара":
            $ ps_add_route("newbie", 2)
            $ ps_newbie_trust += 2
            $ ps_integrity += 1
            $ ps_record_consequence("Ты подтвердил: сомнение Новичка спасло товар от пересорта.")

            p "Не подтверждай. Если экран спорит с товаром, сначала верим глазам."

            n "В карточке находится вчерашняя массовая замена категории."
            newb "То есть я правильно остановилась?"
            p "Именно."

        "Показать быстрый способ перепривязать этикетку":
            $ ps_add_route("newbie", 1)
            $ ps_newbie_trust += 1
            $ ps_efficiency += 2
            $ ps_record_consequence("Ты научил Новичка исправлять двойную маркировку без потери товара.")

            p "Сканируй внутренний код, потом новую ячейку."
            newb "А старый?"
            p "Останется в истории. В этот раз."

    hide newb
    with dissolve
    return


label ps_trace_d3_control:
    scene bg control_room
    with fade

    $ ps_set_ambience("quiet")

    show sv neutral at ps_right
    with dissolve

    n "Артём закрывает таблицу рейтинга, когда ты входишь."

    p "Моё место — секрет?"
    sv "Нет. Способ расчёта — почти."

    n "Он показывает вес показателей. Скорость учитывается сразу. Помощь другому участку — только после ручного подтверждения."

    menu:
        "Попросить учитывать остановки по безопасности":
            $ ps_add_route("supervisor", 2)
            $ ps_supervisor_respect += 2
            $ ps_integrity += 1
            $ ps_record_consequence("Артём добавил безопасные остановки в ручной отчёт смены.")

            p "Красная кнопка не должна выглядеть как провал."
            sv "Система так не считает."
            p "Тогда отчёт должен считать."
            sv "Запишу."

        "Разобраться, как честно поднять эффективность":
            $ ps_add_route("supervisor", 1)
            $ ps_supervisor_respect += 1
            $ ps_efficiency += 2
            $ ps_record_consequence("Ты изучил рейтинг, не соглашаясь скрывать ошибки ради места.")

            sv "Убирай повторные движения. Не убирай проверки."
            p "Звучит очевидно."
            sv "Поэтому почти никто так не делает."

    hide sv
    with dissolve
    return


label ps_trace_d3_dock:
    scene bg loading_dock
    with fade

    $ ps_set_ambience("quiet")

    show mem grin at ps_left
    with dissolve

    n "За воротами идёт мелкий дождь. Макс считает машины, которые уезжают к городу."

    mem "Пять."
    p "Что пять?"
    mem "Пять грузовиков выбрались. Значит, шанс есть."

    menu:
        "Признаться, что рейтинг уже начал давить":
            $ ps_add_route("joker", 2)
            $ ps_humanity += 1
            $ ps_burnout -= 1
            $ ps_record_consequence("На доке ты впервые вслух признал, что рейтинг меняет тебя.")

            p "Я проверяю место чаще, чем хочу."
            mem "Главное — не начни проверять людей как таблицу."

        "Предложить собственный рейтинг смены":
            $ ps_add_route("joker", 1)
            $ ps_humor += 2
            $ ps_team_unity += 1
            $ ps_record_consequence("Вы с Максом придумали рейтинг вещей, которые система не умеет считать.")

            p "Первое место — тому, кто напомнил другому попить."
            mem "Второе — тому, кто не сказал «это не моя зона»."
            p "Третье — автомату, который иногда выдаёт два кофе."

    hide mem
    with dissolve
    return


################################################################################
## Исследование — день 4
################################################################################

label ps_trace_d4_break:
    scene bg break_room
    with fade

    $ ps_set_ambience("quiet")

    show newb worried at ps_right
    with dissolve

    n "Бланк объяснительной лежит перед Новичком рядом с нетронутым чаем."

    newb "Если подпишу — отстанут?"
    p "Сегодня — может быть."
    newb "А завтра?"

    menu:
        "Разобрать каждую строку вместе":
            $ ps_add_route("newbie", 2)
            $ ps_newbie_trust += 2
            $ ps_integrity += 1
            $ ps_record_consequence("Лера не подписала готовое признание в чужой ошибке.")

            p "Пиши только то, что видела сама. Не их формулировку."
            newb "Тогда лист будет почти пустой."
            p "Это тоже ответ."

        "Предложить собственную формулировку о сбое":
            $ ps_add_route("newbie", 1)
            $ ps_newbie_trust += 1
            $ ps_evidence += 1
            $ ps_record_consequence("В объяснительной Новичка впервые появился системный сбой.")

            p "«Операция прошла после зависания привязки»."
            newb "Они это примут?"
            p "Зато не смогут сказать, что ты признала невнимательность."

    hide newb
    with dissolve
    return


label ps_trace_d4_mezzanine:
    scene bg mezzanine
    with fade

    $ ps_set_ambience("warehouse")

    show vet neutral at ps_left
    with dissolve

    n "Виктор раскладывает распечатки по времени. Семь операций принадлежат Лере; остальные сорок — аккаунту человека, которого сегодня нет."

    vet "Учёт задвоился. Но виноватым назначат того, кто рядом."

    menu:
        "Помочь восстановить цепочку":
            $ ps_add_route("veteran", 2)
            $ ps_evidence += 2
            $ ps_team_unity += 1
            $ ps_record_consequence("Вы с Виктором восстановили разорванную цепочку операций.")

            p "Сначала буфер, потом повторная привязка."
            vet "И сорок единиц возвращаются к старому аккаунту."

        "Попросить Виктора выступить свидетелем":
            $ ps_add_route("veteran", 1)
            $ ps_integrity += 1
            $ ps_humanity += 1
            $ ps_record_consequence("Виктор согласился подтвердить сбой не только в разговоре.")

            vet "Я подпишу."
            p "Это может ударить по тебе."
            vet "По ней уже ударило."

    hide vet
    with dissolve
    return


label ps_trace_d4_packing:
    scene bg packing_zone
    with fade

    $ ps_set_ambience("warehouse")

    n "Под упаковочным столом находится коробка с остатками старых этикеток. Одна из них содержит номер пропавшей партии. Сорок семь единиц ушли в буфер во время общего сбоя."

    menu:
        "Снять полную последовательность кодов":
            $ ps_efficiency += 1
            $ ps_evidence += 2
            $ ps_integrity += 1
            $ ps_record_consequence("Ты связал недостачу с массовым сбоем привязки.")

            n "Номера складываются в простую цепочку. Не кража. Не невнимательность. Ошибка системы, которую оказалось удобнее назвать человеком."

        "Сразу отнести этикетку Новичку":
            $ ps_add_route("newbie", 2)
            $ ps_newbie_trust += 2
            $ ps_humanity += 1
            $ ps_record_consequence("Ты принёс Новичку материальное доказательство её невиновности.")

            newb "Это та партия."
            p "Теперь она существует не только в твоей памяти."

    $ ps_collect_document("account_trace")
    return


label ps_trace_d4_control:
    scene bg control_room
    with fade

    $ ps_set_ambience("quiet")

    n "Камеры показывают склад с задержкой в несколько секунд. На канале V-13 изображение внезапно становится фиолетовым."

    if not persistent.ps_reduce_flashes:
        scene bg control_room
        with hpunch

    n "На один кадр появляется коридор, которого нет на плане. Подпись канала: «СЕКТОР V // ШТОРМОВОЙ ДОПУСК». Потом экран возвращается к обычной ленте."

    menu:
        "Записать время и номер канала":
            $ ps_add_route("joker", 1)
            $ ps_evidence += 1
            $ ps_record_consequence("Камера показала несуществующий сектор V-13.")

            p "03:17. Канал V-13."
            n "На повторе в архиве этого кадра уже нет."

        "Позвать Макса как свидетеля":
            $ ps_add_route("joker", 2)
            $ ps_humor += 1
            $ ps_team_unity += 1
            $ ps_record_consequence("Вы с Максом вдвоём увидели коридор, которого нет на плане.")

            show mem serious at ps_left
            with dissolve

            mem "Я сейчас должен пошутить?"
            p "Лучше запомни."
            mem "Уже."

            hide mem
            with dissolve

    $ ps_collect_storm_fragment("dead_channel")
    return


label ps_trace_d4_dock:
    scene bg loading_dock
    with fade

    $ ps_set_ambience("quiet")

    show sv stern at ps_right
    with dissolve

    n "Артём стоит у закрытых ворот с выключенной рацией."

    sv "Ты хотел спросить, почему готовые объяснительные появляются раньше проверки."
    p "Хотел."
    sv "Потому что закрытый инцидент выглядит лучше открытого."

    menu:
        "Спросить, сколько раз он это подписывал":
            $ ps_add_route("supervisor", 2)
            $ ps_supervisor_respect += 2
            $ ps_integrity += 1
            $ ps_record_consequence("Артём признал, что раньше закрывал похожие инциденты.")

            sv "Достаточно."
            p "Это не число."
            sv "Пока — всё, что могу сказать."

        "Потребовать исправить документ Новичка":
            $ ps_add_route("supervisor", 1)
            $ ps_supervisor_respect += 1
            $ ps_humanity += 1
            $ ps_record_consequence("Ты заставил Артёма убрать готовое признание из дела Леры.")

            sv "Я заберу бланк."
            p "И?"
            sv "Открою проверку привязки аккаунтов."

    hide sv
    with dissolve
    return


################################################################################
## Исследование — день 5
################################################################################

label ps_trace_d5_break:
    scene bg break_room
    with fade

    $ ps_set_ambience("quiet")

    show vet concerned at ps_left
    with dissolve

    n "Виктор затягивает бинт на запястье зубами."

    vet "Не смотри так."
    p "Как?"
    vet "Будто сейчас скажешь разумную вещь."

    menu:
        "Настоять, чтобы он снялся с тяжёлых операций":
            $ ps_add_route("veteran", 2)
            $ ps_humanity += 2
            $ ps_team_unity += 1
            $ ps_veteran_safe = True
            $ ps_record_consequence("Виктор согласился не доказывать опыт через боль.")

            p "Сегодня ты не работаешь с подъёмником."
            vet "Ты мне уже начальник?"
            p "Нет. Поэтому могу попросить как человек."
            vet "Это хуже."

        "Попросить показать, как правильно страховать груз":
            $ ps_add_route("veteran", 1)
            $ ps_endurance += 1
            $ ps_efficiency += 1
            $ ps_record_consequence("Виктор передал тебе приём безопасной страховки груза.")

            vet "Не держишь вес. Держишь направление, в котором он не должен упасть."

    hide vet
    with dissolve
    return


label ps_trace_d5_mezzanine:
    scene bg mezzanine
    with fade

    $ ps_set_ambience("warehouse")

    n "За щитом управления подъёмником застряла сложенная заявка. Статус: «Ожидает остановки участка». Ниже новая строка: «Отменено в связи с производственной необходимостью»."

    menu:
        "Сохранить обе версии заявки":
            $ ps_evidence += 2
            $ ps_integrity += 1
            $ ps_add_route("veteran", 1)
            $ ps_record_consequence("Ты нашёл отменённую заявку на ремонт подъёмника.")

            n "Заявка создана за девять дней до твоей первой смены. Неисправность не была неожиданностью."

        "Передать заявку Артёму при свидетелях":
            $ ps_add_route("supervisor", 2)
            $ ps_supervisor_respect += 1
            $ ps_team_unity += 1
            $ ps_record_consequence("Отменённая заявка на ремонт стала известна всей смене.")

            show sv stern at ps_right
            with dissolve

            p "Она была отменена не техниками."
            sv "Вижу."
            p "Пусть остальные тоже увидят."
            sv "Не убирай."

            hide sv
            with dissolve

    $ ps_collect_document("maintenance_ticket")
    return


label ps_trace_d5_packing:
    scene bg packing_zone
    with fade

    $ ps_set_ambience("warehouse")

    show newb tired at ps_right
    with dissolve

    n "Поток ускорился, и Лера начинает повторять каждое действие вслух."

    newb "Код. Ячейка. Вес. Подтверждение."

    menu:
        "Встать рядом и принять часть очереди":
            $ ps_add_route("newbie", 2)
            $ ps_newbie_trust += 2
            $ ps_team_unity += 1
            $ ps_humanity += 1
            $ ps_record_consequence("Во время перегруза Лера не осталась одна со своей очередью.")

            p "Я беру левую ленту."
            newb "У тебя своя зона."
            p "Теперь у нас общая."

        "Помочь ей выстроить приоритеты":
            $ ps_add_route("newbie", 1)
            $ ps_newbie_trust += 1
            $ ps_efficiency += 2
            $ ps_record_consequence("Лера удержала перегруз, используя собственный порядок действий.")

            p "Сначала тяжёлое в стоп. Потом хрупкое. Остальное ждёт."
            newb "Не всё одновременно."
            p "Никогда всё одновременно."

    hide newb
    with dissolve
    return


label ps_trace_d5_control:
    scene bg control_room
    with fade

    $ ps_set_ambience("quiet")

    show sv stern at ps_right
    with dissolve

    n "На центральном экране две цифры. План: 91%%. Риск перегруза: высокий."

    sv "Если остановлю сейчас, участок не закроет ночь."

    menu:
        "Предложить частичную остановку опасной линии":
            $ ps_add_route("supervisor", 2)
            $ ps_supervisor_respect += 2
            $ ps_efficiency += 1
            $ ps_integrity += 1
            $ ps_record_consequence("Вы с Артёмом нашли схему частичной безопасной остановки.")

            p "Останавливаем подъёмник, не весь участок. Мелкое уходит через левую линию."
            sv "Потеряем четыре процента."
            p "Не человека."

        "Попросить его честно объявить риск смене":
            $ ps_add_route("supervisor", 2)
            $ ps_team_unity += 2
            $ ps_humanity += 1
            $ ps_record_consequence("Артём впервые объявил риск перегруза всей смене.")

            sv "Они начнут спорить."
            p "Зато будут знать, почему мы замедляемся."
            sv "Хорошо. Рацию."

    hide sv
    with dissolve
    return


label ps_trace_d5_dock:
    scene bg loading_dock
    with fade

    $ ps_set_ambience("quiet")

    show mem serious at ps_left
    with dissolve

    n "Макс рисует пальцем схему линий на пыльной двери."

    mem "Если связь ляжет, люди услышат только тех, кто рядом."

    menu:
        "Придумать короткие голосовые команды":
            $ ps_add_route("joker", 2)
            $ ps_humor += 1
            $ ps_team_unity += 2
            $ ps_record_consequence("Вы с Максом заранее придумали команды на случай отказа связи.")

            p "Левая. Буфер. Правая. Стоп."
            mem "Четыре слова."
            p "Главное — в правильном порядке."

        "Распределить, кто кого предупредит":
            $ ps_add_route("joker", 1)
            $ ps_efficiency += 1
            $ ps_team_unity += 2
            $ ps_record_consequence("У смены появилась живая цепочка оповещения.")

            mem "Я беру упаковку."
            p "Я — мезонин."
            mem "А если ничего не случится?"
            p "Тогда зря поговорили пять минут. Переживём."

    hide mem
    with dissolve
    return


################################################################################
## Исследование — день 6
################################################################################

label ps_trace_d6_break:
    scene bg break_room
    with fade

    $ ps_set_ambience("quiet")

    show newb relief at ps_right
    with dissolve

    n "Лера переписывает старую памятку: строку «не ошибаться» зачёркивает и вместо неё пишет «остановиться и проверить»."

    menu:
        "Сказать, что она уже может помогать другим":
            $ ps_add_route("newbie", 2)
            $ ps_newbie_trust += 2
            $ ps_humanity += 1
            $ ps_record_consequence("Лера впервые увидела в себе не проблему, а опору для другого человека.")

            newb "Мне?"
            p "Ты замечаешь то, что опытные давно перестали видеть."

        "Попросить добавить памятку в общий чат":
            $ ps_add_route("newbie", 1)
            $ ps_team_unity += 1
            $ ps_efficiency += 1
            $ ps_record_consequence("Памятка Новичка стала общей инструкцией смены.")

            newb "А если будут смеяться?"
            p "Макс будет. Остальные сохранят."

    hide newb
    with dissolve
    return


label ps_trace_d6_mezzanine:
    scene bg mezzanine
    with fade

    $ ps_set_ambience("quiet")

    n "За старой панелью лежит чёрный пластиковый конверт. На нём тот же знак, что был на пломбе. Внутри — накладная V-13. Пункт назначения: «Штормовой сектор»."

    menu:
        "Сохранить накладную и не сообщать системе":
            $ ps_integrity += 1
            $ ps_evidence += 1
            $ ps_record_consequence("Ты сохранил накладную закрытого сектора V-13.")

            n "При попытке сканирования ТСД отвечает:"
            n "«Объект отсутствует»."

        "Позвать Макса и сверить знак":
            $ ps_add_route("joker", 2)
            $ ps_team_unity += 1
            $ ps_record_consequence("Накладную V-13 теперь помнит не один человек.")

            show mem serious at ps_left
            with dissolve

            mem "Та же пломба."
            p "И тот же несуществующий сектор."
            mem "Значит, существует он очень старательно."

            hide mem
            with dissolve

    $ ps_collect_document("sealed_manifest")
    $ ps_collect_storm_fragment("sealed_manifest")
    return


label ps_trace_d6_packing:
    scene bg packing_zone
    with fade

    $ ps_set_ambience("warehouse")

    show mem grin at ps_left
    with dissolve

    n "Макс наклеивает на пустую коробку этикетку «ЧЕСТНЫЙ ОТЧЁТ»."

    p "Что внутри?"
    mem "Пока воздух."

    menu:
        "Перечислить вслух всё, что нельзя потерять в отчёте":
            $ ps_add_route("joker", 2)
            $ ps_integrity += 1
            $ ps_team_unity += 1
            $ ps_record_consequence("Вы с Максом собрали человеческую версию отчёта.")

            p "Контейнер. Сорок семь единиц. Подъёмник."
            mem "И люди, которых каждый раз хотели вынести за скобки."

        "Спрятать в коробку копии документов":
            $ ps_add_route("joker", 1)
            $ ps_evidence += 2
            $ ps_humor += 1
            $ ps_record_consequence("Копии доказательств пережили подготовку официального отчёта.")

            mem "Архив высочайшей секретности."
            p "Почему коробка из-под печенья?"
            mem "Потому что её никто не отдаст Куратору."

    hide mem
    with dissolve
    return


label ps_trace_d6_control:
    scene bg control_room
    with fade

    $ ps_set_ambience("quiet")

    show sv stern at ps_right
    with dissolve

    n "Артём открывает локальный архив камер. Запись остановки ещё существует в кэше терминала."

    sv "После закрытия отчёта кэш очистится."

    menu:
        "Сделать копию вместе с контрольной суммой":
            $ ps_add_route("supervisor", 2)
            $ ps_evidence += 2
            $ ps_integrity += 1
            $ ps_supervisor_respect += 1
            $ ps_record_consequence("У записи с камеры появилась проверяемая копия.")

            p "Теперь изменение файла будет видно."
            sv "Куратор это понимает."
            p "Поэтому и делаем."

        "Попросить Артёма подписать время выгрузки":
            $ ps_add_route("supervisor", 2)
            $ ps_supervisor_respect += 2
            $ ps_integrity += 2
            $ ps_record_consequence("Артём поставил подпись под копией, которую нельзя назвать слухом.")

            sv "Если подпишу, назад не отойду."
            p "Поэтому я и спрашиваю."
            sv "Давай."

    $ ps_collect_document("camera_copy")

    hide sv
    with dissolve
    return


label ps_trace_d6_dock:
    scene bg loading_dock
    with fade

    $ ps_set_ambience("quiet")

    show vet concerned at ps_left
    with dissolve

    n "Виктор стоит у открытых ворот. Холодный воздух двигает край бинта на его руке."

    vet "После отчёта всё станет либо проще, либо честнее."
    p "Не одно и то же?"
    vet "Почти никогда."

    menu:
        "Пообещать не оставлять его историю без подписи":
            $ ps_add_route("veteran", 2)
            $ ps_integrity += 1
            $ ps_team_unity += 1
            $ ps_record_consequence("Ты пообещал Виктору довести историю подъёмника до конца.")

            vet "Не ради меня."
            p "Ради следующего, кто увидит LIFT-09."

        "Спросить, почему он всё ещё остаётся":
            $ ps_add_route("veteran", 2)
            $ ps_humanity += 1
            $ ps_endurance += 1
            $ ps_record_consequence("Виктор признался, что остаётся из-за людей, а не из-за склада.")

            vet "Потому что кто-то должен был встречать новых."
            p "Теперь не только ты."
            vet "Вот поэтому завтра, может быть, уйду вовремя."

    hide vet
    with dissolve
    return


################################################################################
## Кульминации маршрутов
################################################################################

label ps_route_climax:
    if ps_route_scene_seen:
        return

    $ ps_route_scene_seen = True
    $ ps_route_scene_id = ps_route_target()
    $ ps_unlock_route(ps_route_scene_id)
    $ ps_play_route_motif(ps_route_scene_id)
    show screen ps_cinematic_bars

    if ps_route_scene_id == "newbie":
        scene bg break_room
        with fade

        $ ps_set_ambience("quiet")

        show newb relief at ps_right
        with dissolve

        newb "Я переписала объяснительную. Не так, как они оставили в шаблоне."

        p "Страшно?"
        newb "Да."
        newb "Но раньше мне было страшно даже сказать, что экран завис."

        n "Она протягивает тебе лист. Внизу нет признания в невнимательности. Есть время, номер операции и просьба проверить систему."

        scene cg route_newbie at ps_cg_reveal
        with ps_violet_cut

        $ ps_unlock_cg("route_newbie", notify=True)

        newb "Ты сказал, что ошибка — это событие, а не человек. Сегодня я наконец поверила."

        p "Тогда подпиши своим именем. Не их версией тебя."

        $ ps_newbie_trust += 3
        $ ps_humanity += 2
        $ ps_team_unity += 1
        $ ps_record_consequence("Лера подписала собственную правду вместо готового признания.")
        $ ps_key_choices = ps_key_choices + ["Ты помог Новичку перестать считать себя системной ошибкой."]

    elif ps_route_scene_id == "veteran":
        scene bg loading_dock
        with fade

        $ ps_set_ambience("quiet")

        show vet concerned at ps_left
        with dissolve

        vet "Я снял заявку на дополнительный час."

        p "Ты?"
        vet "Не делай такое лицо. Опытный человек тоже может однажды поступить разумно."

        n "Он снимает бинт. Запястье всё ещё болит, но сегодня на нём нет следов новой нагрузки."

        scene cg route_veteran at ps_cg_reveal
        with ps_violet_cut

        $ ps_unlock_cg("route_veteran", notify=True)

        vet "Раньше думал, что если я остановлюсь, всё рухнет."
        p "И?"
        vet "Ничего. Линия пережила. Люди подхватили."

        p "Значит, ты хорошо их научил."

        $ ps_endurance += 2
        $ ps_integrity += 1
        $ ps_team_unity += 2
        $ ps_veteran_safe = True
        $ ps_record_consequence("Виктор выбрал остановиться раньше, чем работа остановила бы его.")
        $ ps_key_choices = ps_key_choices + ["Виктор позволил команде стать его опорой."]

    elif ps_route_scene_id == "joker":
        scene bg loading_dock
        with fade

        $ ps_set_ambience("quiet")

        show mem serious at ps_left
        with dissolve

        mem "Знаешь, почему я всё время говорю?"
        p "Потому что тишина боится конкуренции?"
        mem "Хорошая версия."

        n "Он смотрит на тёмные окна склада."

        mem "Если люди смеются, я понимаю, что они ещё здесь. А когда никто не отвечает — начинаю считать головы."

        scene cg route_joker at ps_cg_reveal
        with ps_violet_cut

        $ ps_unlock_cg("route_joker", notify=True)

        p "Тогда завтра считай вслух. Но не один."

        mem "Это сейчас был приказ?"
        p "По инструкции."
        mem "Тогда спорить нельзя."

        $ ps_humor += 2
        $ ps_humanity += 1
        $ ps_team_unity += 2
        $ ps_record_consequence("Макс доверил тебе причину, по которой продолжает смеяться.")
        $ ps_key_choices = ps_key_choices + ["Ты услышал серьёзный голос Макса и не заставил его снова спрятаться за шуткой."]

    else:
        scene bg control_room
        with fade

        $ ps_set_ambience("quiet")

        show sv stern at ps_right
        with dissolve

        sv "Я подготовил две версии отчёта."

        p "Удобную и настоящую?"
        sv "Раньше я бы назвал их краткой и полной."

        n "Он кладёт короткую версию в измельчитель. Не включает. Просто оставляет там."

        scene cg route_supervisor at ps_cg_reveal
        with ps_violet_cut

        $ ps_unlock_cg("route_supervisor", notify=True)

        sv "Куратор спросит, кто виноват."
        p "А ты?"
        sv "Отвечу, что руководитель, который ищет имя раньше причины, задаёт неправильный вопрос."

        p "Подпишешь?"
        sv "Подпишу."

        $ ps_supervisor_respect += 3
        $ ps_integrity += 2
        $ ps_team_unity += 1
        $ ps_record_consequence("Артём выбрал полный отчёт и принял ответственность за участок.")
        $ ps_key_choices = ps_key_choices + ["Артём перестал прятать решения за формулировками системы."]

label ps_route_climax_end:
    scene black
    with dissolve

    hide screen ps_cinematic_bars
    $ ps_stop_route_motif()
    $ ps_stop_ambience()
    return


################################################################################
## Скрытая линия — «Фиолетовый Шторм»
################################################################################

label ps_storm_teaser:
    $ persistent.ps_storm_unlocked = True
    $ renpy.save_persistent()
    $ ps_unlock_cg("storm_signal", notify=True)
    $ ps_unlock_achievement("purple_signal")

    scene bg service_corridor
    with fade

    play music "audio/night_shift.mp3" fadein 2.0 loop
    $ ps_set_ambience("service")
    $ ps_play_sfx("radio")
    show screen ps_cinematic_bars

    n "Экран уже должен погаснуть. Но где-то за комнатой отдыха щёлкает реле."

    if not persistent.ps_reduce_flashes:
        scene bg service_corridor
        with hpunch

    n "На телефоне появляется сеть без названия. Один входящий файл. V-13 // НАКЛАДНАЯ ПРИНЯТА."

    scene cg storm_signal at ps_cg_reveal
    with ps_violet_cut

    n "За технической дверью вспыхивает фиолетовый свет. Не складской. Слишком глубокий, будто коридор продолжается намного дальше стены."

    n "На секунду слышен незнакомый голос:"
    n "«Штормовой сектор проснулся»."

    if ps_storm_deep_ready():
        n "Помехи не обрываются. В восстановленном канале появляется вторая строка:"
        n "«BERRY // STORM. ТОЧКА ВХОДА ПОДТВЕРЖДЕНА». Ты не знаешь, что находится по ту сторону двери. Но теперь дверь знает, кто находится по эту."

    centered "ФИОЛЕТОВЫЙ ШТОРМ\n\nСИГНАЛ ПРИНЯТ"

    n "Потом связь исчезает. Утро снаружи остаётся прежним. Но теперь ты знаешь: смена была только первой дверью."

label ps_storm_teaser_end:
    hide screen ps_cinematic_bars
    $ ps_stop_ambience()
    stop music fadeout 2.0
    return
