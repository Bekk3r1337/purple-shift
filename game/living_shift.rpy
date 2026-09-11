# -*- coding: utf-8 -*-

################################################################################
## Purple Shift 1.5 — «Голоса смены»
## Живая постановка, многослойный звук, осмотры, телефон и линия Шторма
################################################################################

default ps_archive_section = "documents"
default ps_inspection_seen = {}
default ps_inspection_active = None
default ps_inspection_focus = None
default ps_route_afterword_seen = False
default ps_storm_decoder_index = 0
default ps_storm_decoder_errors = 0
default ps_storm_decoder_completed = False


init -11 python:
    renpy.music.register_channel(
        "machine",
        mixer="sfx",
        loop=True,
        stop_on_mute=True,
        tight=True,
    )
    renpy.music.register_channel(
        "weather",
        mixer="sfx",
        loop=True,
        stop_on_mute=True,
        tight=True,
    )
    renpy.music.register_channel(
        "motif",
        mixer="music",
        loop=True,
        stop_on_mute=True,
        tight=True,
    )


init 12 python:
    if getattr(persistent, "ps_inspected_hotspots", None) is None:
        persistent.ps_inspected_hotspots = []

    if getattr(persistent, "ps_storm_decoded", None) is None:
        persistent.ps_storm_decoded = False

    if getattr(persistent, "ps_storm_transmissions", None) is None:
        persistent.ps_storm_transmissions = []

    ps_live_sfx = {
        "scan_ok": "audio/live/scanner_confirm.ogg",
        "scan_error": "audio/live/scanner_warning.ogg",
        "phone_unlock": "audio/live/phone_unlock.ogg",
        "tap": "audio/live/ui_tap.ogg",
        "paper": "audio/live/paper_rustle.ogg",
        "emergency": "audio/live/emergency_press.ogg",
        "radio": "audio/live/radio_burst.ogg",
        "steps": "audio/live/footsteps_concrete.ogg",
    }

    ps_soundscape_catalog = {
        "warehouse": [
            ("ambient", "audio/conveyor_loop.ogg", 0.32),
            ("machine", "audio/live/forklift_distant.ogg", 0.22),
            ("weather", "audio/live/fluorescent_hum.ogg", 0.17),
        ],
        "quiet": [
            ("ambient", "audio/live/breakroom_hum.ogg", 0.30),
            ("machine", "audio/ventilation_loop.ogg", 0.14),
        ],
        "alert": [
            ("ambient", "audio/live/fluorescent_hum.ogg", 0.30),
            ("machine", "audio/conveyor_loop.ogg", 0.28),
            ("weather", "audio/live/storm_whisper.ogg", 0.18),
        ],
        "break": [
            ("ambient", "audio/live/breakroom_hum.ogg", 0.31),
            ("machine", "audio/ventilation_loop.ogg", 0.12),
        ],
        "mezzanine": [
            ("ambient", "audio/ventilation_loop.ogg", 0.28),
            ("machine", "audio/live/forklift_distant.ogg", 0.24),
            ("weather", "audio/live/fluorescent_hum.ogg", 0.13),
        ],
        "packing": [
            ("ambient", "audio/conveyor_loop.ogg", 0.31),
            ("machine", "audio/live/forklift_distant.ogg", 0.20),
            ("weather", "audio/live/fluorescent_hum.ogg", 0.16),
        ],
        "control": [
            ("ambient", "audio/live/fluorescent_hum.ogg", 0.26),
            ("machine", "audio/ventilation_loop.ogg", 0.12),
        ],
        "dock": [
            ("ambient", "audio/live/dock_rain.ogg", 0.36),
            ("machine", "audio/live/forklift_distant.ogg", 0.16),
        ],
        "service": [
            ("ambient", "audio/live/fluorescent_hum.ogg", 0.24),
            ("weather", "audio/live/storm_whisper.ogg", 0.21),
        ],
    }

    ps_route_motifs = {
        "newbie": "audio/live/route_newbie_motif.ogg",
        "veteran": "audio/live/route_veteran_motif.ogg",
        "joker": "audio/live/route_joker_motif.ogg",
        "supervisor": "audio/live/route_supervisor_motif.ogg",
    }

    ps_inspection_catalog = {
        "control_scan": {
            "title": "ДИСПЕТЧЕРСКАЯ // ТИХИЙ ОСМОТР",
            "subtitle": "Выбери минимум две точки. Остальное смена оставит на следующий раз.",
            "background": "images/bg/control_room.jpg",
            "soundscape": "control",
            "hotspots": [
                {
                    "id": "buffer_log",
                    "title": "Буфер B-04",
                    "detail": "В журнале есть сорок семь повторных привязок в одну секунду.",
                    "x": 310,
                    "y": 390,
                    "document": "account_trace",
                    "route": "supervisor",
                    "stat": ("ps_efficiency", 1),
                },
                {
                    "id": "camera_clock",
                    "title": "Часы камеры",
                    "detail": "Видеопоток отстаёт от системного времени на одиннадцать минут.",
                    "x": 1210,
                    "y": 280,
                    "document": "camera_copy",
                    "route": "veteran",
                    "stat": ("ps_evidence", 1),
                },
                {
                    "id": "violet_frequency",
                    "title": "Частота 13.7",
                    "detail": "На отключённом канале остаётся ровная фиолетовая полоса без источника.",
                    "x": 1510,
                    "y": 610,
                    "storm": "violet_frequency",
                    "route": "joker",
                    "stat": ("ps_integrity", 1),
                },
            ],
        },
        "packing_scan": {
            "title": "УПАКОВКА // СЛЕДЫ ОШИБКИ",
            "subtitle": "Найди то, что не попало в служебную формулировку.",
            "background": "images/bg/packing_zone.jpg",
            "soundscape": "packing",
            "hotspots": [
                {
                    "id": "shift_seal",
                    "title": "Сорванная пломба",
                    "detail": "Пломбу меняли после передачи участка, но в журнале этого нет.",
                    "x": 380,
                    "y": 680,
                    "document": "handover_note",
                    "route": "newbie",
                    "stat": ("ps_integrity", 1),
                },
                {
                    "id": "duplicate_label",
                    "title": "Двойная этикетка",
                    "detail": "Один товар получил два маршрута после зависания ТСД.",
                    "x": 990,
                    "y": 430,
                    "route": "supervisor",
                    "stat": ("ps_efficiency", 1),
                },
                {
                    "id": "forgotten_glove",
                    "title": "Перчатка у линии",
                    "detail": "Лера оставила её там, где пыталась одна остановить хвост.",
                    "x": 1500,
                    "y": 690,
                    "route": "newbie",
                    "stat": ("ps_humanity", 1),
                },
            ],
        },
        "lift_scan": {
            "title": "ПОДЪЁМНИК // ПЕРЕД ЗАПУСКОМ",
            "subtitle": "Машина говорит следами износа. Нужно только остановиться и посмотреть.",
            "background": "images/bg/warehouse_inside.jpg",
            "soundscape": "warehouse",
            "hotspots": [
                {
                    "id": "dead_sensor",
                    "title": "Датчик массы",
                    "detail": "Кабель перетёрт там, где его не видно с рабочего прохода.",
                    "x": 880,
                    "y": 270,
                    "document": "lift_marking",
                    "route": "veteran",
                    "stat": ("ps_evidence", 1),
                },
                {
                    "id": "service_tag",
                    "title": "Сервисная бирка",
                    "detail": "Последний осмотр закрыли удалённо через семь минут после заявки.",
                    "x": 1280,
                    "y": 560,
                    "document": "maintenance_ticket",
                    "route": "veteran",
                    "stat": ("ps_integrity", 1),
                },
                {
                    "id": "stop_line",
                    "title": "Красная граница",
                    "detail": "Кнопка доступна, но безопасная линия почти полностью стёрта.",
                    "x": 290,
                    "y": 710,
                    "route": "supervisor",
                    "stat": ("ps_team_unity", 1),
                },
            ],
        },
        "service_scan": {
            "title": "СЛУЖЕБНЫЙ КОРИДОР // НЕТ НА КАРТЕ",
            "subtitle": "Дверь закрыта. Сигнал — нет.",
            "background": "images/bg/service_corridor.jpg",
            "soundscape": "service",
            "hotspots": [
                {
                    "id": "relay_echo",
                    "title": "Реле без питания",
                    "detail": "Щелчки повторяют ритм смены, хотя линия находится в другом корпусе.",
                    "x": 430,
                    "y": 350,
                    "storm": "shift_echo",
                    "route": "joker",
                    "stat": ("ps_evidence", 1),
                },
                {
                    "id": "v13_manifest",
                    "title": "Пломба V-13",
                    "detail": "Номер накладной совпадает с грузом, которого нет в реестре.",
                    "x": 1250,
                    "y": 600,
                    "document": "sealed_manifest",
                    "storm": "sealed_manifest",
                    "route": "supervisor",
                    "stat": ("ps_integrity", 1),
                },
                {
                    "id": "dead_network",
                    "title": "Сеть без имени",
                    "detail": "Телефон видит точку доступа за бетонной дверью. Уровень сигнала максимальный.",
                    "x": 1570,
                    "y": 300,
                    "route": "newbie",
                    "stat": ("ps_humanity", 1),
                },
            ],
        },
    }

    ps_storm_fragment_catalog = [
        ("violet_stamp", "Фиолетовая печать", "Краска реагирует на экран телефона."),
        ("dead_channel", "Мёртвый канал", "Рация отвечает после отключения питания."),
        ("sealed_manifest", "Накладная V-13", "Груз принят сектором, которого нет на карте."),
        ("violet_frequency", "Частота 13.7", "Полоса существует без передатчика."),
        ("shift_echo", "Эхо смены", "Служебное реле повторяет ритм работающей линии."),
        ("camera_guest", "Лишний сотрудник", "Камера видит фигуру, которой нет рядом с линией."),
        ("future_message", "Сообщение из завтра", "V-13 предупреждает об аварии раньше её начала."),
        ("named_shift", "Названная смена", "Отключённое табло перечисляет людей по именам."),
    ]

    ps_storm_decoder_sequence = [
        ("violet", "ФИОЛЕТОВЫЙ КАНАЛ"),
        ("silence", "ПАУЗА"),
        ("echo", "ЭХО СМЕНЫ"),
        ("violet", "ФИОЛЕТОВЫЙ КАНАЛ"),
    ]

    ps_storm_decoder_buttons = [
        ("violet", "13.7 // V"),
        ("silence", "0.0 // ТИШИНА"),
        ("echo", "07.0 // ЭХО"),
    ]

    ps_live_messages = [
        {
            "id": "newbie_followup",
            "day": 5,
            "sender": "Новичок",
            "time": "18:44",
            "preview": "Я сегодня скажу сама.",
            "route": "newbie",
            "requires_route": "newbie",
            "incoming": [
                "Я сегодня скажу сама, если ТСД снова зависнет.",
                "Можешь просто быть рядом. Не вместо меня.",
            ],
            "replies": [
                {
                    "id": "beside",
                    "title": "«Буду рядом. Говорить будешь ты.»",
                    "answer": "Буду рядом. Но говорить будешь ты.",
                    "reaction": "Договорились. Так даже лучше.",
                    "effects": {"ps_newbie_trust": 2, "ps_humanity": 1},
                },
                {
                    "id": "checklist",
                    "title": "«Сначала соберём факты.»",
                    "answer": "Сначала код, время и операция. Потом разговор.",
                    "reaction": "Уже записала шаблон. Свой.",
                    "effects": {"ps_efficiency": 1, "ps_integrity": 1},
                },
            ],
        },
        {
            "id": "veteran_followup",
            "day": 5,
            "sender": "Ветеран",
            "time": "18:39",
            "preview": "Не давай мне лезть одному.",
            "route": "veteran",
            "requires_route": "veteran",
            "incoming": [
                "Если подъёмник снова покажет LIFT-09 — не давай мне лезть одному.",
                "Да, это официальное разрешение остановить старого дурака.",
            ],
            "replies": [
                {
                    "id": "promise",
                    "title": "«Остановлю и тебя, и подъёмник.»",
                    "answer": "Остановлю и тебя, и подъёмник.",
                    "reaction": "Вот теперь можно работать.",
                    "effects": {"ps_team_unity": 1, "ps_endurance": 1},
                },
                {
                    "id": "repair",
                    "title": "«Сначала заявка и блокировка.»",
                    "answer": "Сначала заявка, бирка и блокировка. Без ручного режима.",
                    "reaction": "Наконец кто-то читает опыт как инструкцию.",
                    "effects": {"ps_evidence": 1, "ps_integrity": 1},
                },
            ],
        },
        {
            "id": "joker_followup",
            "day": 5,
            "sender": "Шутник",
            "time": "18:51",
            "preview": "Если я замолчу — пересчитай людей.",
            "route": "joker",
            "requires_route": "joker",
            "incoming": [
                "Если я вдруг замолчу — пересчитай людей.",
                "Это не шутка. Поэтому сообщение автоматически удалится из моей биографии.",
            ],
            "replies": [
                {
                    "id": "together",
                    "title": "«Считать будем вместе.»",
                    "answer": "Считать будем вместе. И вслух.",
                    "reaction": "Ненавижу командную работу. Спасибо.",
                    "effects": {"ps_team_unity": 2, "ps_humor": 1},
                },
                {
                    "id": "honest",
                    "title": "«Можешь не шутить со мной.»",
                    "answer": "Со мной можешь не шутить, если сил нет.",
                    "reaction": "Опасное предложение. Я запомню.",
                    "effects": {"ps_humanity": 1, "ps_humor": 1},
                },
            ],
        },
        {
            "id": "supervisor_followup",
            "day": 5,
            "sender": "Супервайзер",
            "time": "19:03",
            "preview": "Мне нужен второй голос.",
            "route": "supervisor",
            "requires_route": "supervisor",
            "incoming": [
                "Если куратор попросит короткую версию, мне нужен второй голос.",
                "Не поддержка. Свидетель.",
            ],
            "replies": [
                {
                    "id": "facts",
                    "title": "«Буду говорить только по фактам.»",
                    "answer": "Буду говорить по фактам. Даже если они против нас обоих.",
                    "reaction": "Именно поэтому я написал тебе.",
                    "effects": {"ps_supervisor_respect": 2, "ps_integrity": 1},
                },
                {
                    "id": "responsibility",
                    "title": "«Решение всё равно подпишешь ты.»",
                    "answer": "Я принесу доказательства. Ответственность за решение останется твоей.",
                    "reaction": "Справедливо.",
                    "effects": {"ps_evidence": 1, "ps_endurance": 1},
                },
            ],
        },
        {
            "id": "v13_unknown",
            "day": 6,
            "sender": "V-13",
            "time": "--:--",
            "preview": "Смена слышит тебя.",
            "requires_storm_any": True,
            "incoming": [
                "СМЕНА СЛЫШИТ ТЕБЯ.",
                "СОБЕРИ ВОСЕМЬ СЛЕДОВ. НЕ ДОВЕРЯЙ ВРЕМЕНИ НА КАМЕРАХ.",
            ],
            "replies": [
                {
                    "id": "who",
                    "title": "«Кто это?»",
                    "answer": "Кто это и откуда у вас мой номер?",
                    "reaction": "СЕКТОР ПОМНИТ НОМЕР РАНЬШЕ ТЕБЯ.",
                    "effects": {"ps_evidence": 1},
                },
                {
                    "id": "disconnect",
                    "title": "«Отключиться от сети.»",
                    "answer": "Соединение разорвано пользователем.",
                    "reaction": "СОЕДИНЕНИЕ ПРОДОЛЖАЕТСЯ.",
                    "effects": {"ps_endurance": 1},
                },
            ],
        },
    ]

    existing_message_ids = {message["id"] for message in ps_message_catalog}
    for live_message in ps_live_messages:
        if live_message["id"] not in existing_message_ids:
            ps_message_catalog.append(live_message)

    def ps_play_sfx(cue_id):
        path = ps_live_sfx.get(cue_id)
        if path and renpy.loadable(path):
            renpy.sound.play(path)

    def ps_cg_motion(trans, shown_time, animation_time):
        if persistent.ps_reduce_motion:
            trans.zoom = 1.0
            return None

        progress = min(1.0, shown_time / 8.0)
        trans.zoom = 1.055 - 0.055 * progress
        return None if progress >= 1.0 else 0.05

    def ps_background_motion(trans, shown_time, animation_time):
        if persistent.ps_reduce_motion:
            trans.zoom = 1.02
            return None

        progress = min(1.0, shown_time / 12.0)
        trans.zoom = 1.02 + 0.05 * progress
        return None if progress >= 1.0 else 0.05

    def ps_play_route_motif(route_id):
        variant = ps_route_variant(route_id)
        track = ps_route_variant_tracks.get(
            "{}:{}".format(route_id, variant),
            ps_route_motifs.get(route_id),
        )
        if track and renpy.loadable(track):
            renpy.music.set_volume(0.30, delay=0.4, channel="motif")
            renpy.music.play(
                track,
                channel="motif",
                loop=True,
                fadein=1.2,
                if_changed=True,
            )

    def ps_stop_route_motif():
        renpy.music.stop(channel="motif", fadeout=1.2)

    def ps_set_ambience(zone):
        global ps_ambience_zone

        ps_ambience_zone = zone
        for channel in ("ambient", "machine", "weather"):
            renpy.music.stop(channel=channel, fadeout=0.7)

        if not persistent.ps_ambient_enabled:
            return

        for channel, track, volume in ps_soundscape_catalog.get(zone, []):
            if renpy.loadable(track):
                renpy.music.set_volume(volume, delay=0.5, channel=channel)
                renpy.music.play(
                    track,
                    channel=channel,
                    loop=True,
                    fadein=1.0,
                    if_changed=True,
                )

    def ps_stop_ambience():
        global ps_ambience_zone

        ps_ambience_zone = None
        for channel in ("ambient", "machine", "weather"):
            renpy.music.stop(channel=channel, fadeout=1.0)

    def ps_toggle_ambience():
        persistent.ps_ambient_enabled = not persistent.ps_ambient_enabled
        renpy.save_persistent()

        if persistent.ps_ambient_enabled and ps_ambience_zone:
            ps_set_ambience(ps_ambience_zone)
        else:
            for channel in ("ambient", "machine", "weather"):
                renpy.music.stop(channel=channel, fadeout=0.5)

        renpy.restart_interaction()

    def ps_zone_soundscape(zone_id):
        return {
            "break": "break",
            "mezzanine": "mezzanine",
            "packing": "packing",
            "control": "control",
            "dock": "dock",
        }.get(zone_id, "warehouse")

    def ps_available_messages():
        result = []
        current_route = ps_route_target()

        for message in ps_message_catalog:
            if message["day"] > ps_chapter:
                continue
            if message.get("requires_route") not in (None, current_route):
                continue
            if (
                message.get("requires_variant")
                and ps_route_variant(message.get("route")) != message["requires_variant"]
            ):
                continue
            if message.get("requires_storm_any") and not ps_storm_fragments:
                continue
            result.append(message)

        return result

    def ps_unread_message_count():
        return len(
            [
                message
                for message in ps_available_messages()
                if message["id"] not in ps_message_reads
            ]
        )

    def ps_begin_inspection(scene_id):
        global ps_inspection_active
        global ps_inspection_focus
        global ps_inspection_seen

        ps_inspection_active = scene_id
        ps_inspection_focus = None
        inspections = dict(ps_inspection_seen)
        inspections.setdefault(scene_id, [])
        ps_inspection_seen = inspections

    def ps_inspection_items(scene_id):
        return list(ps_inspection_seen.get(scene_id, []))

    def ps_inspect_hotspot(scene_id, hotspot_id):
        global ps_inspection_seen
        global ps_inspection_focus

        inspection = ps_inspection_catalog[scene_id]
        hotspot = next(
            item
            for item in inspection["hotspots"]
            if item["id"] == hotspot_id
        )

        inspected = dict(ps_inspection_seen)
        current = list(inspected.get(scene_id, []))
        is_new = hotspot_id not in current

        if is_new:
            current.append(hotspot_id)
            inspected[scene_id] = current
            ps_inspection_seen = inspected
            ps_append_unique_persistent(
                "ps_inspected_hotspots",
                "{}:{}".format(scene_id, hotspot_id),
            )

            if hotspot.get("document"):
                ps_collect_document(hotspot["document"])
            if hotspot.get("storm"):
                ps_collect_storm_fragment(hotspot["storm"])
            if hotspot.get("route"):
                ps_add_route(hotspot["route"], 1)
            if hotspot.get("stat"):
                variable_name, delta = hotspot["stat"]
                value = getattr(renpy.store, variable_name)
                setattr(renpy.store, variable_name, value + delta)

            ps_play_sfx("paper")

            if len(persistent.ps_inspected_hotspots) >= 8:
                ps_unlock_achievement("observer")
        else:
            ps_play_sfx("tap")

        ps_inspection_focus = hotspot_id
        renpy.restart_interaction()

    def ps_inspection_hotspot(scene_id, hotspot_id):
        return next(
            item
            for item in ps_inspection_catalog[scene_id]["hotspots"]
            if item["id"] == hotspot_id
        )

    def ps_inspection_can_finish(scene_id):
        return len(ps_inspection_items(scene_id)) >= 2

    def ps_storm_fragment_title(fragment_id):
        for item_id, title, description in ps_storm_fragment_catalog:
            if item_id == fragment_id:
                return title
        return "Неизвестный след"

    def ps_storm_pressure():
        base = int(80.0 * len(set(ps_storm_fragments)) / len(ps_storm_fragment_catalog))
        return min(100, base + (20 if persistent.ps_storm_decoded else 0))

    def ps_storm_deep_ready():
        required = {item[0] for item in ps_storm_fragment_catalog}
        return required.issubset(set(ps_storm_fragments)) and persistent.ps_storm_decoded

    def ps_storm_decoder_start():
        global ps_storm_decoder_index
        global ps_storm_decoder_errors

        ps_storm_decoder_index = 0
        ps_storm_decoder_errors = 0

    def ps_storm_decoder_choose(channel_id):
        global ps_storm_decoder_index
        global ps_storm_decoder_errors

        if ps_storm_decoder_index >= len(ps_storm_decoder_sequence):
            return

        expected = ps_storm_decoder_sequence[ps_storm_decoder_index][0]
        if channel_id == expected:
            ps_storm_decoder_index += 1
            ps_play_sfx("scan_ok")
        else:
            ps_storm_decoder_errors += 1
            ps_play_sfx("scan_error")

        renpy.restart_interaction()

    def ps_record_storm_transmission(transmission_id):
        transmissions = list(persistent.ps_storm_transmissions)
        if transmission_id not in transmissions:
            transmissions.append(transmission_id)
            persistent.ps_storm_transmissions = transmissions
            renpy.save_persistent()


################################################################################
## Живая постановка и кинематографические слои
################################################################################

define ps_violet_cut = Fade(0.12, 0.08, 0.32, color="#43195f")
define ps_alarm_cut = Fade(0.06, 0.04, 0.22, color="#7b101d")

transform ps_cg_reveal:
    xalign 0.5
    yalign 0.5
    zoom 1.055
    alpha 0.0
    ease 0.45 alpha 1.0
    function ps_cg_motion

transform ps_cinematic_background:
    xalign 0.5
    yalign 0.5
    zoom 1.02
    function ps_background_motion

transform ps_phone_arrive:
    alpha 0.0
    yoffset 35
    ease 0.22 alpha 1.0 yoffset 0

transform ps_marker_pulse:
    alpha 0.55
    zoom 0.96
    linear 0.7 alpha 1.0 zoom 1.08
    linear 0.7 alpha 0.55 zoom 0.96
    repeat

transform ps_violet_breathe:
    alpha 0.02
    linear 1.6 alpha 0.10
    linear 1.6 alpha 0.02
    repeat


screen ps_cinematic_bars():
    zorder 95

    frame:
        xfill True
        ysize 72
        ypos 0
        padding (0, 0)
        background Solid("#000000ee")

    frame:
        xfill True
        ysize 72
        yalign 1.0
        padding (0, 0)
        background Solid("#000000ee")

    if not persistent.ps_reduce_flashes:
        add Solid("#6f2b8a18") at ps_violet_breathe


################################################################################
## Осмотр локаций
################################################################################

screen ps_inspection_hotspots(scene_id):
    modal True
    zorder 250

    $ inspection = ps_inspection_catalog[scene_id]
    $ inspected = ps_inspection_items(scene_id)

    if persistent.ps_reduce_motion:
        add inspection["background"]
    else:
        add inspection["background"] at ps_cinematic_background

    add Solid("#08030ab0")

    frame:
        xpos 45
        ypos 35
        xsize 930
        padding (28, 20)
        background Solid("#12091eea")

        vbox:
            spacing 7

            text inspection["title"]:
                color "#e0b5ff"
                size 31

            text inspection["subtitle"]:
                color "#c4b3d1"
                size 20

            text "Осмотрено: [len(inspected)] / 2":
                color ("#8ff0b1" if len(inspected) >= 2 else "#ffd176")
                size 21

    for hotspot in inspection["hotspots"]:
        $ hotspot_seen = hotspot["id"] in inspected

        textbutton ("✓" if hotspot_seen else "◎"):
            action Function(
                ps_inspect_hotspot,
                scene_id,
                hotspot["id"],
            )
            pos (hotspot["x"], hotspot["y"])
            xsize 78
            ysize 78
            background Solid("#3f7c58dd" if hotspot_seen else "#6d3d88dd")
            hover_background Solid("#9b63bd")
            text_color "#ffffff"
            text_size 43
            text_xalign 0.5
            text_yalign 0.5
            at ps_marker_pulse

    frame:
        xalign 0.5
        yalign 1.0
        yoffset -34
        xsize 1460
        ysize 190
        padding (30, 22)
        background Solid("#100819f2")

        hbox:
            spacing 26
            xfill True

            vbox:
                spacing 8
                xsize 1020

                if ps_inspection_focus:
                    $ focused = ps_inspection_hotspot(scene_id, ps_inspection_focus)

                    text focused["title"]:
                        color "#ffffff"
                        size 29

                    text focused["detail"]:
                        color "#cbbbd6"
                        size 22
                else:
                    text "Выбери отмеченную точку":
                        color "#ffffff"
                        size 29

                    text "Каждый осмотр может открыть документ, улику или новую сторону персонажа.":
                        color "#cbbbd6"
                        size 22

            textbutton "ЗАВЕРШИТЬ ОСМОТР":
                id "ps_inspection_finish"
                action Return(inspected)
                sensitive ps_inspection_can_finish(scene_id)
                xalign 1.0
                yalign 0.5
                xsize 340
                ysize 66
                background Solid(
                    "#3f7755"
                    if ps_inspection_can_finish(scene_id)
                    else "#302936"
                )
                hover_background Solid("#5ca776")
                insensitive_background Solid("#302936")
                text_color "#ffffff"
                text_insensitive_color "#746b7b"
                text_size 21
                text_xalign 0.5
                text_yalign 0.5


label ps_run_inspection(scene_id):
    $ ps_begin_inspection(scene_id)
    $ ps_set_ambience(ps_inspection_catalog[scene_id]["soundscape"])
    call screen ps_inspection_hotspots(scene_id)
    $ ps_inspection_result = _return
    $ ps_record_consequence(
        "Ты остановился и осмотрел участок, вместо того чтобы пройти мимо следов."
    )
    return


################################################################################
## Телефон: дело V-13
################################################################################

screen ps_storm_signal_panel():
    vbox:
        spacing 18
        xfill True

        hbox:
            xfill True

            vbox:
                spacing 4

                text "ДЕЛО V-13":
                    color "#e0b5ff"
                    size 34

                text "Источник сигнала не определён":
                    color "#9685a7"
                    size 20

            text "СИНХРОНИЗАЦИЯ [ps_storm_pressure()]%":
                color ("#dc8cff" if ps_storm_pressure() < 100 else "#ff8fed")
                size 24
                xalign 1.0
                yalign 0.5

        bar:
            value StaticValue(ps_storm_pressure(), 100)
            xmaximum 1320
            ymaximum 16
            left_bar Solid("#a54fe0")
            right_bar Solid("#36213e")

        hbox:
            spacing 16

            frame:
                xsize 610
                ysize 525
                padding (22, 18)
                background Solid("#120b1ddd")

                viewport:
                    mousewheel True
                    draggable True
                    scrollbars "vertical"

                    vbox:
                        spacing 10
                        xfill True

                        text "НАЙДЕННЫЕ СЛЕДЫ":
                            color "#917ca8"
                            size 20

                        for fragment_id, fragment_title, fragment_desc in ps_storm_fragment_catalog:
                            $ fragment_open = fragment_id in ps_storm_fragments

                            frame:
                                xfill True
                                padding (17, 12)
                                background Solid(
                                    "#3a2250"
                                    if fragment_open
                                    else "#1c1720"
                                )

                                vbox:
                                    spacing 4

                                    text (fragment_title if fragment_open else "НЕИЗВЕСТНЫЙ СЛЕД"):
                                        color ("#ddaaff" if fragment_open else "#625a69")
                                        size 22

                                    text (fragment_desc if fragment_open else "Нет данных"):
                                        color ("#b9a8c7" if fragment_open else "#554f59")
                                        size 18

            frame:
                xsize 720
                ysize 525
                padding (24, 18)
                background Solid("#120b1ddd")

                vbox:
                    spacing 13
                    xfill True

                    text "ВОССТАНОВЛЕННЫЙ КАНАЛ":
                        color "#917ca8"
                        size 20

                    if persistent.ps_storm_decoded:
                        text "V-13 // СМЕНА ПРИНЯТА":
                            color "#f0c8ff"
                            size 29

                        text "«Сектор просыпается не после аварии. Авария происходит, когда сектор пытается проснуться.»":
                            color "#ffffff"
                            size 23
                            text_align 0.0

                        text "Координаты повреждены. Метка назначения: BERRY // STORM.":
                            color "#c29cd6"
                            size 20
                    elif len(ps_storm_fragments) >= 2:
                        text "Канал найден, но последовательность ещё не восстановлена.":
                            color "#d4c2dc"
                            size 24

                        text "Слушай помехи во время последней смены.":
                            color "#9f8cab"
                            size 20
                    else:
                        text "Недостаточно данных для синхронизации.":
                            color "#7c7184"
                            size 24

                    null height 12

                    textbutton "ПРОСЛУШАТЬ ПОМЕХИ":
                        action Play(
                            "weather",
                            "audio/live/storm_whisper.ogg",
                            loop=True,
                            fadein=0.6,
                        )
                        xsize 360
                        ysize 56
                        background Solid("#55306c")
                        hover_background Solid("#8150a0")
                        text_color "#ffffff"
                        text_size 19
                        text_xalign 0.5
                        text_yalign 0.5

                    textbutton "ОСТАНОВИТЬ СИГНАЛ":
                        action Stop("weather", fadeout=0.6)
                        xsize 360
                        ysize 52
                        background Solid("#3d293f")
                        hover_background Solid("#654263")
                        text_color "#ffffff"
                        text_size 18
                        text_xalign 0.5
                        text_yalign 0.5


################################################################################
## Декодирование Шторма
################################################################################

screen ps_storm_decoder():
    modal True
    zorder 260

    add Solid("#08020bef")
    add "bg service_corridor":
        alpha 0.28

    if ps_storm_decoder_index >= len(ps_storm_decoder_sequence):
        timer 0.25 action Return(True)

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1320
        ysize 790
        padding (52, 42)
        background Solid("#16091ff5")

        vbox:
            spacing 24
            xfill True

            text "V-13 // ВОССТАНОВЛЕНИЕ КАНАЛА":
                color "#efa9ff"
                size 35
                xalign 0.5

            text "Повтори последовательность, которую ты слышал в помехах":
                color "#cfbfd8"
                size 23
                xalign 0.5

            hbox:
                spacing 12
                xalign 0.5

                for sequence_index, sequence_item in enumerate(ps_storm_decoder_sequence):
                    $ sequence_done = sequence_index < ps_storm_decoder_index
                    $ sequence_current = sequence_index == ps_storm_decoder_index

                    frame:
                        xsize 285
                        ysize 112
                        padding (12, 10)
                        background Solid(
                            "#356c56"
                            if sequence_done
                            else "#713b8d"
                            if sequence_current
                            else "#2b2031"
                        )

                        vbox:
                            spacing 5
                            xalign 0.5
                            yalign 0.5

                            text "[sequence_index + 1]":
                                color "#bbaac4"
                                size 18
                                xalign 0.5

                            text sequence_item[1]:
                                color "#ffffff"
                                size 20
                                xalign 0.5
                                text_align 0.5

            null height 10

            hbox:
                spacing 18
                xalign 0.5

                for channel_id, channel_title in ps_storm_decoder_buttons:
                    textbutton channel_title:
                        action Function(ps_storm_decoder_choose, channel_id)
                        xsize 370
                        ysize 150
                        background Solid("#443052")
                        hover_background Solid("#8150a0")
                        text_color "#ffffff"
                        text_size 25
                        text_xalign 0.5
                        text_yalign 0.5

            hbox:
                xfill True

                text "Совпадений: [ps_storm_decoder_index] / [len(ps_storm_decoder_sequence)]":
                    color "#8de8b0"
                    size 23

                text "Ошибки: [ps_storm_decoder_errors]":
                    color "#ff8794"
                    size 23
                    xalign 1.0

            textbutton "РАЗОРВАТЬ СОЕДИНЕНИЕ":
                id "ps_storm_decoder_exit"
                action Return(False)
                xalign 0.5
                xsize 390
                ysize 58
                background Solid("#4a273e")
                hover_background Solid("#75405f")
                text_color "#ffffff"
                text_size 19
                text_xalign 0.5
                text_yalign 0.5


label ps_storm_interference:
    if len(ps_storm_fragments) < 2:
        return

    $ ps_play_sfx("radio")
    $ ps_set_ambience("service")

    if not persistent.ps_reduce_flashes:
        scene bg warehouse_alert
        with ps_violet_cut

    n "Среди аварийных команд появляется ещё один ритм. Он не идёт из рации. Телефон сам открывает канал V-13."

    $ ps_storm_decoder_start()
    call screen ps_storm_decoder
    $ ps_storm_decoder_completed = _return

    if ps_storm_decoder_completed:
        $ persistent.ps_storm_decoded = True
        $ ps_record_storm_transmission("sector_wakeup")
        $ ps_unlock_achievement("storm_decoder")
        $ ps_evidence += 1
        $ ps_integrity += 1
        $ ps_record_consequence("Ты восстановил скрытый канал V-13 во время аварии.")

        n "Последний тон совпадает. Помехи складываются в человеческий голос. «Сектор просыпается не после аварии». «Авария начинается, когда сектор просыпается»."
    else:
        $ ps_burnout += 1
        n "Ты разрываешь соединение. Но последний импульс продолжает вибрировать в корпусе телефона."

    $ ps_set_ambience("alert")
    return


################################################################################
## Личные послесловия маршрутов
################################################################################

label ps_route_afterword:
    if ps_route_afterword_seen:
        return

    $ ps_route_afterword_seen = True
    $ ps_afterword_route = ps_route_scene_id or ps_route_target()
    $ ps_play_route_motif(ps_afterword_route)

    show screen ps_cinematic_bars

    if ps_afterword_route == "newbie":
        scene bg break_room
        with fade

        show newb relief at ps_enter_right
        with dissolve

        newb "Знаешь, что изменилось?"
        p "Что?"
        newb "Теперь, когда система пишет красным, я сначала читаю. А уже потом решаю, виновата ли я вообще."
        p "Хорошая привычка."
        newb "Я оставлю её следующей новенькой."

        hide newb

    elif ps_afterword_route == "veteran":
        scene bg loading_dock
        with fade

        show vet concerned at ps_enter_left
        with dissolve

        vet "Я записался к врачу."
        p "Добровольно?"
        vet "Не порть исторический момент. Смена переживёт один мой выходной."
        p "А ты?"
        vet "Вот это и проверю."

        hide vet

    elif ps_afterword_route == "joker":
        scene bg loading_dock
        with fade

        show mem serious at ps_enter_left
        with dissolve

        mem "Пересчитал."
        p "Кого?"
        mem "Всех. Сегодня никто не исчез между отчётом и проходной."
        p "Можно снова шутить."
        mem "Через минуту. Я хочу запомнить тишину нормальной."

        hide mem

    else:
        scene bg control_room
        with fade

        show sv stern at ps_enter_right
        with dissolve

        sv "Я отправил полный отчёт."
        p "Что ответили?"
        sv "Что формулировка создаёт репутационные риски."
        p "А ты?"
        sv "Что неисправный подъёмник создаёт риски быстрее. Первый раз написал это без чужого имени."

        hide sv

label ps_route_afterword_end:
    with dissolve
    hide screen ps_cinematic_bars
    $ ps_stop_route_motif()
    return
