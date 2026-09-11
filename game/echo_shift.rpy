# -*- coding: utf-8 -*-

################################################################################
## Purple Shift 1.6 — «Смена помнит»
## Внутренние ветки маршрутов, командные конфликты и глубокое расследование
################################################################################

default ps_route_tendencies = {
    "newbie": {"growth": 0, "shadow": 0},
    "veteran": {"growth": 0, "shadow": 0},
    "joker": {"growth": 0, "shadow": 0},
    "supervisor": {"growth": 0, "shadow": 0},
}
default ps_route_turns_seen = []
default ps_route_resolutions_seen = []
default ps_reactive_echoes_seen = []
default ps_team_conflicts_seen = []
default ps_team_conflict_results = {}

default ps_investigation_chain = []
default ps_investigation_hypothesis = None
default ps_investigation_result = 0
default ps_investigation_complete = False

default ps_storm_mimic_choice = None
default ps_storm_mimic_correct = False
default ps_storm_mimic_seen = False
default ps_zero_shift_seen = False


init 18 python:
    if getattr(persistent, "ps_route_variants", None) is None:
        persistent.ps_route_variants = []

    if getattr(persistent, "ps_true_shift_unlocked", None) is None:
        persistent.ps_true_shift_unlocked = False

    if getattr(persistent, "ps_story_peak_day", None) is None:
        persistent.ps_story_peak_day = 1

    ps_route_variant_catalog = {
        "newbie": {
            "growth": {
                "title": "Собственный голос",
                "short": "самостоятельность",
                "description": "Лера просит о поддержке, но оставляет решение и слова за собой.",
                "accent": "#ff8fd4",
                "track": "audio/live/route_newbie_growth.ogg",
            },
            "shadow": {
                "title": "Чужая опора",
                "short": "зависимость",
                "description": "Лера всё чаще смотрит на тебя раньше, чем успевает услышать себя.",
                "accent": "#bc6f9f",
                "track": "audio/live/route_newbie_shadow.ogg",
            },
        },
        "veteran": {
            "growth": {
                "title": "Опыт просит помощи",
                "short": "доверие",
                "description": "Виктор учится считать остановку частью опыта, а не поражением.",
                "accent": "#ffd786",
                "track": "audio/live/route_veteran_growth.ogg",
            },
            "shadow": {
                "title": "Последний герой",
                "short": "геройство",
                "description": "Виктор продолжает доказывать телом то, что давно знает головой.",
                "accent": "#b89962",
                "track": "audio/live/route_veteran_shadow.ogg",
            },
        },
        "joker": {
            "growth": {
                "title": "Тишина без страха",
                "short": "честность",
                "description": "Макс остаётся рядом, даже когда не может спрятаться за удачной репликой.",
                "accent": "#83ddff",
                "track": "audio/live/route_joker_growth.ogg",
            },
            "shadow": {
                "title": "Шутка вместо ответа",
                "short": "избегание",
                "description": "Макс превращает любой страх в номер, пока никто не успел спросить всерьёз.",
                "accent": "#5b94aa",
                "track": "audio/live/route_joker_shadow.ogg",
            },
        },
        "supervisor": {
            "growth": {
                "title": "Ответственность",
                "short": "ответственность",
                "description": "Артём принимает решения своим именем и не прячет людей за формулировками.",
                "accent": "#86ef9a",
                "track": "audio/live/route_supervisor_growth.ogg",
            },
            "shadow": {
                "title": "Контроль",
                "short": "контроль",
                "description": "Артём защищает смену так жёстко, что перестаёт слышать саму смену.",
                "accent": "#5aa168",
                "track": "audio/live/route_supervisor_shadow.ogg",
            },
        },
    }

    ps_investigation_events = [
        {
            "id": "maintenance",
            "stamp": "ДЕНЬ −9",
            "title": "Отмена ремонта",
            "detail": "Заявку LIFT-09 закрыли без подписи техника.",
            "document": "maintenance_ticket",
            "accent": "#ffd083",
        },
        {
            "id": "rating",
            "stamp": "ДЕНЬ 3",
            "title": "Новый рейтинг",
            "detail": "Табло меняет места людей после каждой операции.",
            "document": None,
            "accent": "#8fa5bf",
        },
        {
            "id": "deleted_log",
            "stamp": "ДЕНЬ 3",
            "title": "Удалённая остановка",
            "detail": "Запись исчезла после ночной синхронизации.",
            "document": "handover_note",
            "accent": "#c99cff",
        },
        {
            "id": "rumor",
            "stamp": "БЕЗ ДАТЫ",
            "title": "Разговор у курилки",
            "detail": "Кто-то слышал, будто Лера перепутала участок.",
            "document": None,
            "accent": "#8fa5bf",
        },
        {
            "id": "account_shift",
            "stamp": "ДЕНЬ 4",
            "title": "Сбой привязки",
            "detail": "Сорок семь товаров прошли через общий буфер.",
            "document": "account_trace",
            "accent": "#ff8fd4",
        },
        {
            "id": "false_report",
            "stamp": "ДЕНЬ 6",
            "title": "Готовая причина",
            "detail": "В отчёте заранее появилась «ошибка сотрудника».",
            "document": "camera_copy",
            "accent": "#86ef9a",
        },
    ]

    ps_investigation_expected = [
        "maintenance",
        "deleted_log",
        "account_shift",
        "false_report",
    ]

    ps_investigation_hypotheses = [
        (
            "employee",
            "ЕДИНИЧНАЯ ОШИБКА",
            "Недостача началась с неверного действия одного сотрудника.",
        ),
        (
            "systemic",
            "СИСТЕМНАЯ ЦЕПОЧКА",
            "Ремонт отменили, запись удалили, а ответственность подготовили заранее.",
        ),
        (
            "storm",
            "ВМЕШАТЕЛЬСТВО V-13",
            "Любое несоответствие объясняется закрытым сектором.",
        ),
    ]

    ps_storm_mimic_messages = [
        {
            "id": "lera",
            "sender": "Лера",
            "time": "06:11",
            "text": "Если завтра снова начнут с готового ответа, я сначала назову время и операцию.",
            "tell": "говорит о собственном действии",
        },
        {
            "id": "viktor",
            "sender": "Виктор",
            "time": "06:12",
            "text": "Бирку не снимай. Сначала фото, потом блокировка, потом разговор.",
            "tell": "держится фактов и порядка",
        },
        {
            "id": "max",
            "sender": "Макс",
            "time": "06:13",
            "text": "Всё нормально. Не ищи меня и никого не пересчитывай. Я уже ушёл один.",
            "tell": "просит именно то, чего Макс боится",
        },
        {
            "id": "artyom",
            "sender": "Артём",
            "time": "06:14",
            "text": "Черновик не подписывай. Я сам назову Морозову причину остановки.",
            "tell": "оставляет решение за собой",
        },
    ]

    def ps_note_story_day(day):
        if day > persistent.ps_story_peak_day:
            persistent.ps_story_peak_day = day
            renpy.save_persistent()

    def ps_route_tendency(route_id, tendency):
        return ps_route_tendencies.get(route_id, {}).get(tendency, 0)

    def ps_route_variant(route_id):
        growth = ps_route_tendency(route_id, "growth")
        shadow = ps_route_tendency(route_id, "shadow")

        if growth == shadow:
            return "growth" if growth > 0 else "undecided"
        return "growth" if growth > shadow else "shadow"

    def ps_route_variant_data(route_id):
        variant = ps_route_variant(route_id)
        if variant == "undecided":
            return {
                "title": "Развилка ещё впереди",
                "short": "не определено",
                "description": "Отношения уже меняются, но смена ещё не знает, во что они превратятся.",
                "accent": "#b9a8c8",
                "track": ps_route_motifs.get(route_id),
            }
        return ps_route_variant_catalog[route_id][variant]

    def ps_route_variant_key(route_id):
        variant = ps_route_variant(route_id)
        return "{}:{}".format(route_id, variant)

    def ps_record_route_tendency(route_id, tendency, amount=1, memory=None):
        global ps_route_tendencies

        tendencies = {
            key: dict(value)
            for key, value in ps_route_tendencies.items()
        }
        route_values = dict(tendencies.get(route_id, {"growth": 0, "shadow": 0}))
        route_values[tendency] = route_values.get(tendency, 0) + amount
        tendencies[route_id] = route_values
        ps_route_tendencies = tendencies

        ps_add_route(route_id, 1)
        if memory:
            ps_add_relationship_memory(memory)

        variant = ps_route_variant(route_id)
        if variant != "undecided" and max(route_values.values()) >= 2:
            variant_key = "{}:{}".format(route_id, variant)
            ps_append_unique_persistent("ps_route_variants", variant_key)

        if len(persistent.ps_route_variants) >= 4:
            ps_unlock_achievement("two_sides")
        if len(persistent.ps_route_variants) >= 8:
            ps_unlock_achievement("all_faces")

    def ps_route_turn_seen(day, route_id):
        return "{}:{}".format(day, route_id) in ps_route_turns_seen

    def ps_mark_route_turn(day, route_id):
        global ps_route_turns_seen
        key = "{}:{}".format(day, route_id)
        if key not in ps_route_turns_seen:
            ps_route_turns_seen = ps_route_turns_seen + [key]

    def ps_mark_team_conflict(day, result_id):
        global ps_team_conflicts_seen
        global ps_team_conflict_results

        if day not in ps_team_conflicts_seen:
            ps_team_conflicts_seen = ps_team_conflicts_seen + [day]

        results = dict(ps_team_conflict_results)
        results[day] = result_id
        ps_team_conflict_results = results

        if len(ps_team_conflicts_seen) >= 4:
            ps_unlock_achievement("team_chemistry")

    def ps_conflict_result(day):
        return ps_team_conflict_results.get(day)

    def ps_investigation_start():
        global ps_investigation_chain
        global ps_investigation_hypothesis
        ps_investigation_chain = []
        ps_investigation_hypothesis = None

    def ps_investigation_add(event_id):
        global ps_investigation_chain
        if event_id in ps_investigation_chain or len(ps_investigation_chain) >= 4:
            return
        ps_investigation_chain = ps_investigation_chain + [event_id]
        ps_play_sfx("paper")
        renpy.restart_interaction()

    def ps_investigation_undo():
        global ps_investigation_chain
        if ps_investigation_chain:
            ps_investigation_chain = ps_investigation_chain[:-1]
            ps_play_sfx("tap")
            renpy.restart_interaction()

    def ps_investigation_reset():
        global ps_investigation_chain
        global ps_investigation_hypothesis
        ps_investigation_chain = []
        ps_investigation_hypothesis = None
        ps_play_sfx("tap")
        renpy.restart_interaction()

    def ps_investigation_event(event_id):
        for event in ps_investigation_events:
            if event["id"] == event_id:
                return event
        return ps_investigation_events[0]

    def ps_investigation_event_confirmed(event):
        document = event.get("document")
        if document is None:
            return False
        return (
            document in ps_trace_clues
            or document in persistent.ps_unlocked_documents
        )

    def ps_investigation_score(chain=None, hypothesis=None):
        chain = list(ps_investigation_chain if chain is None else chain)
        hypothesis = ps_investigation_hypothesis if hypothesis is None else hypothesis

        positions = sum(
            1
            for index, event_id in enumerate(ps_investigation_expected)
            if index < len(chain) and chain[index] == event_id
        )
        links = sum(
            1
            for index in range(min(len(chain) - 1, len(ps_investigation_expected) - 1))
            if chain[index:index + 2] == ps_investigation_expected[index:index + 2]
        )
        hypothesis_score = 2 if hypothesis == "systemic" else 0
        return positions + links + hypothesis_score

    def ps_investigation_ready():
        return len(ps_investigation_chain) == 4 and ps_investigation_hypothesis is not None

    def ps_storm_mimic_message(message_id):
        for message in ps_storm_mimic_messages:
            if message["id"] == message_id:
                return message
        return ps_storm_mimic_messages[0]

    def ps_true_shift_ready():
        return (
            ps_storm_deep_ready()
            and ps_investigation_result >= 9
            and ps_storm_mimic_correct
            and ps_team_unity >= 5
            and not ps_signed_false_report
            and ps_final_ending not in ("employee", "silence")
        )

    def ps_main_menu_art():
        if persistent.ps_true_shift_unlocked and renpy.loadable("images/cg/zero_shift.jpg"):
            return "images/cg/zero_shift.jpg"
        if persistent.ps_storm_decoded and renpy.loadable("images/cg/named_shift.jpg"):
            return "images/cg/named_shift.jpg"
        if persistent.ps_total_runs > 0 and renpy.loadable("images/cg/team_dawn.jpg"):
            return "images/cg/team_dawn.jpg"
        return "images/ui/fon.jpg"

    def ps_main_menu_status():
        if persistent.ps_true_shift_unlocked:
            return "НУЛЕВАЯ СМЕНА ОТКРЫТА"
        if persistent.ps_storm_decoded:
            return "КАНАЛ V-13 ВОССТАНОВЛЕН"
        if persistent.ps_total_runs > 0:
            return "СМЕНА ПОМНИТ ПРОХОЖДЕНИЕ"
        return "ДО НАЧАЛА СМЕНЫ"


################################################################################
## Экраны расследования и вмешательства V-13
################################################################################

screen ps_deep_investigation_board():
    modal True
    zorder 260

    add "bg control_room" at ps_cinematic_background
    add Solid("#06030be8")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1740
        ysize 970
        padding (42, 30)
        background Solid("#12091ef6")

        vbox:
            spacing 18
            xfill True

            hbox:
                xfill True

                vbox:
                    spacing 4

                    text "ДЕЛО СМЕНЫ // ВОССТАНОВЛЕНИЕ ХРОНОЛОГИИ":
                        color "#d5adff"
                        size 34

                    text "Выстрой четыре события по порядку и назови общую причину.":
                        color "#b9a9c8"
                        size 21

                text "[len(ps_investigation_chain)] / 4":
                    color "#ffffff"
                    size 30
                    xalign 1.0

            hbox:
                spacing 12
                xalign 0.5

                for index in range(4):
                    frame:
                        xsize 395
                        ysize 116
                        padding (16, 12)
                        background Solid("#39234f" if index < len(ps_investigation_chain) else "#1c1423")

                        if index < len(ps_investigation_chain):
                            $ event = ps_investigation_event(ps_investigation_chain[index])
                            vbox:
                                spacing 5
                                text "[index + 1]. [event['stamp']]":
                                    color event["accent"]
                                    size 18
                                text event["title"]:
                                    color "#ffffff"
                                    size 22
                        else:
                            text "[index + 1]. —":
                                color "#6d6375"
                                size 24
                                xalign 0.5
                                yalign 0.5

            grid 3 2:
                spacing 12
                xalign 0.5

                for event in ps_investigation_events:
                    $ selected = event["id"] in ps_investigation_chain
                    $ confirmed = ps_investigation_event_confirmed(event)

                    button:
                        id ("ps_deep_event_" + event["id"])
                        action Function(ps_investigation_add, event["id"])
                        sensitive not selected and len(ps_investigation_chain) < 4
                        xsize 520
                        ysize 154
                        padding (20, 15)
                        background Solid("#21162c" if not selected else "#17121b")
                        hover_background Solid("#49305d")

                        vbox:
                            spacing 5

                            hbox:
                                xfill True
                                text event["stamp"]:
                                    color event["accent"]
                                    size 17
                                text ("ФАКТ" if confirmed else "НЕ ПОДТВЕРЖДЕНО"):
                                    color ("#82e5b7" if confirmed else "#8b7c92")
                                    size 15
                                    xalign 1.0

                            text event["title"]:
                                color ("#ffffff" if not selected else "#625a68")
                                size 23

                            text event["detail"]:
                                color ("#c9bdcf" if not selected else "#625a68")
                                size 18

            hbox:
                spacing 12
                xalign 0.5

                for hypothesis_id, hypothesis_title, hypothesis_detail in ps_investigation_hypotheses:
                    textbutton hypothesis_title:
                        id ("ps_deep_hypothesis_" + hypothesis_id)
                        action SetVariable("ps_investigation_hypothesis", hypothesis_id)
                        xsize 520
                        ysize 78
                        background Solid("#69408b" if ps_investigation_hypothesis == hypothesis_id else "#251832")
                        hover_background Solid("#8154a4")
                        text_color "#ffffff"
                        text_size 20
                        text_xalign 0.5
                        text_yalign 0.5

            hbox:
                spacing 18
                xalign 0.5

                textbutton "ШАГ НАЗАД":
                    id "ps_deep_board_undo"
                    action Function(ps_investigation_undo)
                    sensitive bool(ps_investigation_chain)
                    xsize 260
                    ysize 62
                    background Solid("#33243e")
                    hover_background Solid("#554065")
                    text_color "#ffffff"
                    text_size 20

                textbutton "СБРОСИТЬ":
                    id "ps_deep_board_reset"
                    action Function(ps_investigation_reset)
                    xsize 260
                    ysize 62
                    background Solid("#33243e")
                    hover_background Solid("#554065")
                    text_color "#ffffff"
                    text_size 20

                textbutton "ЗАФИКСИРОВАТЬ ЦЕПОЧКУ":
                    id "ps_deep_board_confirm"
                    action Return()
                    sensitive ps_investigation_ready()
                    xsize 520
                    ysize 62
                    background Solid("#7543a7")
                    hover_background Solid("#9b63d3")
                    insensitive_background Solid("#302738")
                    text_color "#ffffff"
                    text_insensitive_color "#716a77"
                    text_size 21


screen ps_storm_mimic():
    modal True
    zorder 270

    add Solid("#030106f2")
    add "images/cg/mimic_message.jpg" at ps_cinematic_background:
        alpha 0.24
    add Solid("#7d34a838") at ps_signal_breathe

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1450
        ysize 900
        padding (52, 38)
        background Solid("#100817f2")

        vbox:
            spacing 20
            xfill True

            text "V-13 // ОДИН ИЗ ГОЛОСОВ НЕ ПРИНАДЛЕЖИТ ЧЕЛОВЕКУ":
                color "#db9cff"
                size 33
                xalign 0.5

            text "Сравни не стиль сообщения, а то, чего каждый человек боится и чему научился за неделю.":
                color "#c1b2cb"
                size 21
                text_align 0.5
                xalign 0.5

            vbox:
                spacing 12
                xfill True

                for message in ps_storm_mimic_messages:
                    button:
                        id ("ps_mimic_" + message["id"])
                        action SetVariable("ps_storm_mimic_choice", message["id"])
                        xfill True
                        ysize 130
                        padding (24, 17)
                        background Solid("#542a70" if ps_storm_mimic_choice == message["id"] else "#21142c")
                        hover_background Solid("#62377c")

                        vbox:
                            spacing 7

                            hbox:
                                xfill True
                                text message["sender"]:
                                    color "#ffffff"
                                    size 24
                                text message["time"]:
                                    color "#927fa1"
                                    size 19
                                    xalign 1.0

                            text message["text"]:
                                color "#d8cede"
                                size 21

            textbutton "ОТМЕТИТЬ ПОДДЕЛКУ":
                id "ps_mimic_confirm"
                action Return(ps_storm_mimic_choice)
                sensitive ps_storm_mimic_choice is not None
                xalign 0.5
                xsize 480
                ysize 68
                background Solid("#6d37a0")
                hover_background Solid("#9656d0")
                insensitive_background Solid("#2d2633")
                text_color "#ffffff"
                text_size 24


screen ps_route_variant_card(route_id):
    modal True
    zorder 250

    $ profile = ps_character_profile(route_id)
    $ state = ps_route_variant_data(route_id)

    add Solid("#06030ddd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1120
        padding (64, 44)
        background Solid("#160c25f5")

        vbox:
            spacing 18
            xfill True

            text "МАРШРУТ ИЗМЕНИЛСЯ":
                color "#a98fbd"
                size 21
                kerning 4
                xalign 0.5

            text profile["name"]:
                color "#ffffff"
                size 46
                xalign 0.5

            text state["title"]:
                color state["accent"]
                size 39
                xalign 0.5

            text state["description"]:
                color "#d8cede"
                size 25
                text_align 0.5
                xalign 0.5
                xmaximum 900

            hbox:
                spacing 60
                xalign 0.5

                text "ОПОРА [ps_route_tendency(route_id, 'growth')]":
                    color "#88e5b6"
                    size 22

                text "ДАВЛЕНИЕ [ps_route_tendency(route_id, 'shadow')]":
                    color "#e58d99"
                    size 22

            textbutton "ПРОДОЛЖИТЬ":
                id "ps_variant_continue"
                action Return()
                xalign 0.5
                xsize 410
                ysize 66
                background Solid("#7142a1")
                hover_background Solid("#9a61d2")
                text_color "#ffffff"
                text_size 24


################################################################################
## Внутренние развилки четырёх маршрутов
################################################################################

label ps_route_turning_point(day):
    if day not in (3, 5):
        return

    $ ps_turn_route = ps_route_target()

    if ps_route_turn_seen(day, ps_turn_route):
        return

    $ ps_mark_route_turn(day, ps_turn_route)
    $ ps_play_route_motif(ps_turn_route)

    if day == 3:
        scene bg break_room
        with fade

        if ps_turn_route == "newbie":
            show newb worried at ps_right
            with dissolve

            n "Перед разговором о рейтинге Лера несколько раз проговаривает первую фразу. Каждый раз начинает увереннее и всё равно обрывает себя на середине."
            newb "Если я снова застряну, что ты сделаешь?"

            menu:
                "Попросить её начать самой и вмешаться только при необходимости":
                    $ ps_record_route_tendency("newbie", "growth", 2, "Ты оставил Лере право на собственный голос, не убирая поддержку.")
                    $ ps_newbie_trust += 2
                    $ ps_humanity += 1
                    p "Начнёшь ты. Если тебя перебьют — я верну разговор к твоим словам, но не буду говорить вместо тебя."
                    newb "То есть ошибиться в формулировке мне тоже разрешается?"
                    p "Особенно в своей."
                    newb "Хорошо. Тогда не подсказывай раньше времени."

                "Предложить дать знак и сразу взять разговор на себя":
                    $ ps_record_route_tendency("newbie", "shadow", 2, "Ты пообещал Лере забрать трудный разговор при первом признаке страха.")
                    $ ps_newbie_trust += 1
                    $ ps_efficiency += 1
                    p "Посмотри на меня — и я продолжу. Не будем давать им время задавить тебя."
                    newb "Спасибо. Только я тогда, наверное, опять ничего не скажу."
                    p "Сейчас важнее результат."
                    n "Лера кивает слишком быстро, будто разрешение молчать оказалось удобнее, чем она ожидала."

            hide newb

        elif ps_turn_route == "veteran":
            show vet concerned at ps_left
            with dissolve

            n "Виктор держит кружку двумя руками. Когда думает, что ты отвернулся, переносит её в левую — правое запястье снова отзывается болью."
            vet "Не смотри так. До конца смены дотяну."

            menu:
                "Попросить сообщить о боли Артёму сейчас":
                    $ ps_record_route_tendency("veteran", "growth", 2, "Виктор впервые сообщил о боли до того, как она остановила его сама.")
                    $ ps_endurance += 1
                    $ ps_team_unity += 1
                    p "Не надо дотягивать. Скажи Артёму сейчас, пока это ещё решение, а не эвакуация."
                    vet "Двадцать лет опыта, а докладывать приходится о запястье."
                    p "Значит, опыт наконец пригодился вовремя."
                    vet "Ладно. Идём вместе, но говорить буду я."

                "Согласиться закончить участок и никому не говорить":
                    $ ps_record_route_tendency("veteran", "shadow", 2, "Ты помог Виктору скрыть боль ради конца участка.")
                    $ ps_efficiency += 1
                    $ ps_burnout += 1
                    p "Закроем участок и поменяемся до следующего запуска. Артёму пока не скажем."
                    vet "Вот это деловой разговор."
                    n "Он улыбается с облегчением. Не потому, что стало легче, а потому, что ему снова разрешили не останавливаться."

            hide vet

        elif ps_turn_route == "joker":
            show mem serious at ps_left
            with dissolve

            n "Макс сидит напротив и крутит бумажный стакан. Обычно к этому моменту он успевает дать стакану имя и должность. Сегодня — ничего."
            mem "Ты сейчас обязан спросить, почему я молчу. По сценарию."

            menu:
                "Остаться рядом без требования развлекать тебя":
                    $ ps_record_route_tendency("joker", "growth", 2, "Макс понял, что рядом с тобой тишину не нужно немедленно чинить шуткой.")
                    $ ps_humanity += 1
                    $ ps_team_unity += 1
                    p "Не обязан. Можем просто досидеть перерыв."
                    mem "А если будет неловко?"
                    p "Значит, две минуты будет неловко."
                    n "Макс ставит стакан на стол. Тишина не становится приятной, но хотя бы перестаёт быть аварией."

                "Попросить его вернуть настроение команде":
                    $ ps_record_route_tendency("joker", "shadow", 2, "Ты попросил Макса снова стать голосом комнаты, когда ему самому хотелось тишины.")
                    $ ps_humor += 2
                    p "Народ скис. Дай им что-нибудь своё, пока все не начали слушать вентиляцию."
                    mem "Значит, артист всё-таки нужен."
                    n "Через минуту из комнаты снова слышен смех. Только Макс смеётся на долю секунды позже остальных."

            hide mem

        else:
            show sv stern at ps_right
            with dissolve

            n "Артём показывает тебе список ручных исправлений. Внизу четыре его подписи и ни одного имени человека, чьё решение он исправлял."
            sv "Если оставить фамилии, начнут таскать людей по кабинетам. Я закрыл всё собой."

            menu:
                "Потребовать назвать решения своими именами":
                    $ ps_record_route_tendency("supervisor", "growth", 2, "Артём согласился объяснять свои решения, а не молча закрывать их должностью.")
                    $ ps_integrity += 1
                    $ ps_supervisor_respect += 1
                    p "Закрыть собой — не то же самое, что объяснить. Люди должны знать, что именно ты решил за них."
                    sv "И получить право спорить?"
                    p "Иначе это не защита."
                    sv "Неприятно. Но да. На планёрке скажу сам."

                "Предложить жёстче контролировать решения команды":
                    $ ps_record_route_tendency("supervisor", "shadow", 2, "Ты поддержал контроль Артёма как самый быстрый способ защитить смену.")
                    $ ps_efficiency += 1
                    $ ps_supervisor_respect += 1
                    p "Тогда не оставляй пространство для случайных решений. Один порядок, одна ответственность."
                    sv "Меньше ошибок."
                    p "И меньше вопросов."
                    n "Артём убирает список в папку. Впервые за разговор он выглядит спокойнее."

            hide sv

    else:
        scene bg packing_zone
        with fade

        if ps_turn_route == "newbie":
            show newb tired at ps_right
            with dissolve

            newb "В диспетчерской снова приготовили формулировку. Если пойду одна, голос может дрогнуть. Если пойдёшь первым ты, они опять решат, что я ничего не понимаю."

            menu:
                "Отдать Лере документы и войти следом":
                    $ ps_record_route_tendency("newbie", "growth", 2, "Лера первой вошла в диспетчерскую с собственной хронологией.")
                    $ ps_newbie_trust += 2
                    $ ps_integrity += 1
                    p "Документы несёшь ты. Начинаешь с времени операции. Я войду следом и останусь рядом."
                    newb "Не впереди?"
                    p "Не впереди."
                    newb "Тогда пошли, пока я не придумала причину передумать."

                "Войти первым и представить её версию":
                    $ ps_record_route_tendency("newbie", "shadow", 2, "Ты снова представил версию Леры раньше, чем она смогла сказать её сама.")
                    $ ps_evidence += 1
                    $ ps_newbie_trust += 1
                    p "Я начну с журналов и объясню цепочку. Ты подтвердишь детали."
                    newb "Хорошо. Так безопаснее."
                    n "Она отдаёт тебе папку. Вместе с ней — право решить, какие слова прозвучат первыми."

            hide newb

        elif ps_turn_route == "veteran":
            show vet concerned at ps_left
            with dissolve

            vet "Бирку повесили, но ручной режим оставили. Могу показать, как закончить партию без датчика. Потом точно блокируем."

            menu:
                "Попросить Виктора самому передать ключ блокировки":
                    $ ps_record_route_tendency("veteran", "growth", 2, "Виктор собственными руками передал ключ от неисправного подъёмника.")
                    $ ps_veteran_safe = True
                    $ ps_team_unity += 1
                    p "Нет. Передай ключ Артёму сам. Не мне и не технику — сам."
                    vet "Чтобы потом не забрать обратно?"
                    p "Чтобы остановка тоже стала твоим опытом."
                    vet "Убедил. Но торжественную речь отменяем."

                "Попросить показать ручной режим в последний раз":
                    $ ps_record_route_tendency("veteran", "shadow", 2, "Виктор снова доказал полезность через опасный ручной запуск.")
                    $ ps_efficiency += 2
                    $ ps_burnout += 1
                    p "Покажи один раз. Закрываем партию и сразу блокируем."
                    vet "Один раз — любимая единица измерения плохих привычек."
                    n "Он уже тянется к панели, пока произносит это."

            hide vet

        elif ps_turn_route == "joker":
            show mem serious at ps_left
            with dissolve

            mem "Я пересчитал людей три раза. Все на месте, но мозг требует четвёртый. Можно я просто пошучу, и мы сделаем вид, что это нормально?"

            menu:
                "Пересчитать вместе и спросить прямо, страшно ли ему":
                    $ ps_record_route_tendency("joker", "growth", 2, "Макс впервые назвал страх раньше, чем успел превратить его в шутку.")
                    $ ps_team_unity += 2
                    $ ps_humanity += 1
                    p "Сначала пересчитаем вместе. Потом ты скажешь, чего именно боишься."
                    mem "Вот так сразу? Без разогрева?"
                    p "Без."
                    mem "Боюсь, что однажды не досчитаюсь и никто даже не заметит, когда это случилось."

                "Подыграть и вернуть привычную шутку":
                    $ ps_record_route_tendency("joker", "shadow", 2, "Ты помог Максу снова спрятать тревогу в знакомом номере.")
                    $ ps_humor += 2
                    p "Четвёртая проверка платная. С каждого по одному печенью."
                    mem "Наконец разумный регламент."
                    n "Макс улыбается. Проверять людей он всё равно не прекращает."

            hide mem

        else:
            show sv neutral at ps_right
            with dissolve

            sv "Перед запуском я хочу запретить любые ручные решения без моего подтверждения. После прошлой ночи это единственный способ удержать линию."

            menu:
                "Потребовать право команды остановить опасную операцию":
                    $ ps_record_route_tendency("supervisor", "growth", 2, "Артём оставил каждому право сказать «стоп» без разрешения должности.")
                    $ ps_team_unity += 2
                    $ ps_supervisor_respect += 1
                    p "Команда должна иметь право остановить опасную операцию без ожидания твоего ответа. Иначе ты один отвечаешь быстрее, чем один человек способен увидеть."
                    sv "Будут лишние остановки."
                    p "Зато ни одна не станет запрещённой."
                    sv "Хорошо. Стоп — общий. Запуск — через меня."

                "Поддержать единый центр управления":
                    $ ps_record_route_tendency("supervisor", "shadow", 2, "Ты помог Артёму собрать все решения смены в одних руках.")
                    $ ps_efficiency += 2
                    $ ps_supervisor_respect += 1
                    p "После аварии импровизация опаснее задержки. Все решения идут через тебя."
                    sv "Тогда мне нужен доступ ко всем терминалам."
                    p "Получишь."
                    n "Порядок становится идеальным. Люди — чуть тише."

            hide sv

    with dissolve
    $ ps_play_route_motif(ps_turn_route)
    call screen ps_route_variant_card(ps_turn_route)
    $ ps_stop_route_motif()
    return


################################################################################
## Конфликты людей, которые существуют не только рядом с героем
################################################################################

label ps_team_conflict_scene(day):
    if day in ps_team_conflicts_seen:
        return

    if day == 3:
        scene bg break_room
        with fade
        show newb worried at ps_right
        show mem grin at ps_left
        with dissolve

        mem "Красная стрелка рядом с Лерой — просто система наконец выбрала фирменный цвет тревоги."
        newb "Можешь хотя бы раз не делать из меня объявление для всей комнаты?"
        mem "Я хотел, чтобы стало легче."
        newb "Тебе стало."

        menu:
            "Дать Лере договорить, а Макса попросить услышать ответ":
                $ ps_mark_team_conflict(3, "listen")
                $ ps_record_route_tendency("newbie", "growth", 1)
                $ ps_record_route_tendency("joker", "growth", 1)
                $ ps_team_unity += 2
                p "Макс, подожди. Лера ещё не закончила."
                newb "Если я смеюсь вместе со всеми, это не всегда значит, что мне смешно. Иногда просто не хочется портить вам перерыв."
                mem "Понял. Прости. Без второй попытки пошутить."

            "Поддержать шутку, чтобы снять напряжение":
                $ ps_mark_team_conflict(3, "laugh")
                $ ps_record_route_tendency("newbie", "shadow", 1)
                $ ps_record_route_tendency("joker", "shadow", 1)
                $ ps_humor += 1
                $ ps_team_unity -= 1
                p "Зато стрелка честная. У меня внутри такая же."
                mem "Вот, уже командная символика."
                n "Комната смеётся. Лера тоже улыбается, но больше в разговор не возвращается."

            "Резко оборвать Макса":
                $ ps_mark_team_conflict(3, "cut")
                $ ps_record_route_tendency("newbie", "growth", 1)
                $ ps_record_route_tendency("joker", "shadow", 1)
                $ ps_integrity += 1
                p "Хватит. Не каждый чужой страх обязан становиться твоим материалом."
                mem "Принял."
                n "Он замолкает. Лера благодарно смотрит на тебя, но легче в комнате не становится."

        hide newb
        hide mem

    elif day == 4:
        scene bg locker_room
        with fade
        show newb worried at ps_right
        show sv stern at ps_left
        with dissolve

        sv "Я начну разговор. Сначала журнал, потом Лера подтвердит последовательность."
        newb "Я могу начать сама."
        sv "Можешь. Но если они зададут вопрос неправильно, у нас не будет второй первой фразы."

        menu:
            "Попросить Артёма сначала выслушать Леру":
                $ ps_mark_team_conflict(4, "lera_first")
                $ ps_record_route_tendency("newbie", "growth", 1)
                $ ps_record_route_tendency("supervisor", "growth", 1)
                $ ps_team_unity += 2
                p "Пусть начинает Лера. Если формулировку исказят, тогда подключишься ты."
                sv "Рискованно."
                newb "Зато это будет мой риск."
                sv "Хорошо. Я не перебиваю."

            "Согласиться с планом Артёма":
                $ ps_mark_team_conflict(4, "artyom_first")
                $ ps_record_route_tendency("newbie", "shadow", 1)
                $ ps_record_route_tendency("supervisor", "shadow", 1)
                $ ps_evidence += 1
                p "Начинай с журналов. Нам нельзя потерять разговор из-за первой формулировки."
                sv "Именно."
                newb "Тогда скажите, когда мне можно будет говорить."

            "Самому представить общую версию":
                $ ps_mark_team_conflict(4, "player_first")
                $ ps_record_route_tendency("newbie", "shadow", 1)
                $ ps_record_route_tendency("supervisor", "shadow", 1)
                $ ps_efficiency += 1
                $ ps_team_unity -= 1
                p "Начну я. У меня вся хронология, и меня пока не записали в виноватые."
                sv "Практично."
                n "Лера ничего не говорит. Артём тоже. Решение принято быстрее, чем они успели договориться между собой."

        hide newb
        hide sv

    elif day == 5:
        $ ps_unlock_cg("team_conflict")
        show screen ps_cinematic_bars
        scene cg team_conflict at ps_cg_reveal
        with ps_alarm_cut
        pause 0.7
        hide screen ps_cinematic_bars

        scene bg packing_zone
        with dissolve
        show vet concerned at ps_left
        show sv stern at ps_right
        with dissolve

        vet "Ручной режим работает. Я закрою остаток и потом отдам ключ."
        sv "Нет. Ты отдашь ключ сейчас."
        vet "А ты закроешь остаток чем — должностной инструкцией?"
        sv "Если понадобится, остановлю участок."

        menu:
            "Остановить участок и записать причину вместе":
                $ ps_mark_team_conflict(5, "record_stop")
                $ ps_record_route_tendency("veteran", "growth", 1)
                $ ps_record_route_tendency("supervisor", "growth", 1)
                $ ps_team_unity += 2
                $ ps_integrity += 1
                p "Останавливаем. Виктор передаёт ключ, Артём записывает LIFT-09 причиной. Оба ставите имена."
                vet "Чтобы никто не оказался крайним?"
                sv "Чтобы решение не исчезло."

            "Дать Виктору закончить одну партию под контролем Артёма":
                $ ps_mark_team_conflict(5, "last_batch")
                $ ps_record_route_tendency("veteran", "shadow", 1)
                $ ps_record_route_tendency("supervisor", "shadow", 1)
                $ ps_efficiency += 2
                $ ps_burnout += 1
                p "Одна партия. Артём стоит у панели, Виктор не подходит к механизму. После — полная блокировка."
                vet "Договорились."
                sv "Мне не нравится."
                p "Мне тоже. Поэтому это не станет новой нормой."

            "Поддержать приказ Артёма без обсуждения":
                $ ps_mark_team_conflict(5, "obey")
                $ ps_record_route_tendency("veteran", "shadow", 1)
                $ ps_record_route_tendency("supervisor", "shadow", 1)
                $ ps_supervisor_respect += 1
                $ ps_team_unity -= 1
                p "Ключ Артёму. Сейчас."
                vet "Уже двое начальников. Удобно."
                n "Он отдаёт ключ. Останавливается механизм, но спор остаётся работать внутри смены."

        hide vet
        hide sv

    elif day == 6:
        scene bg service_corridor
        with fade
        show newb tired at ps_left
        show mem serious at ps_center
        show vet concerned at ps_right
        with dissolve

        newb "Мы зайдём вместе."
        vet "Нет. Если придём толпой, Морозов назовёт это давлением."
        mem "А если по одному, он назовёт это четырьмя удобными версиями."
        newb "Тогда что делать?"

        menu:
            "Собрать одну хронологию, но дать каждому говорить за себя":
                $ ps_mark_team_conflict(6, "shared_timeline")
                $ ps_record_route_tendency("newbie", "growth", 1)
                $ ps_record_route_tendency("veteran", "growth", 1)
                $ ps_record_route_tendency("joker", "growth", 1)
                $ ps_record_route_tendency("supervisor", "growth", 1)
                $ ps_team_unity += 3
                $ ps_integrity += 1
                p "Сверяем время и документы вместе. В кабинете каждый говорит только о том, что видел сам."
                vet "Не хор. Последовательность."
                newb "И никто не заканчивает чужое предложение."
                mem "Это явно было адресовано мне. Согласен."

            "Взять общий разговор на себя":
                $ ps_mark_team_conflict(6, "player_voice")
                $ ps_record_route_tendency("newbie", "shadow", 1)
                $ ps_record_route_tendency("veteran", "shadow", 1)
                $ ps_record_route_tendency("joker", "shadow", 1)
                $ ps_evidence += 2
                p "Дайте мне материалы. Я изложу общую версию, чтобы он не растащил её на противоречия."
                newb "А мы?"
                p "Подтвердите, если спросят."
                n "Папка становится тяжелее. Команда — тише."

            "Попросить всех говорить отдельно":
                $ ps_mark_team_conflict(6, "separate")
                $ ps_endurance += 1
                $ ps_team_unity -= 2
                p "По одному. Так ни у кого не будет причины говорить, что мы договорились."
                vet "Логично."
                mem "И очень удобно тому, кто задаёт вопросы."
                n "Никто не спорит дальше. Это не означает, что все согласились."

        hide newb
        hide mem
        hide vet

    else:
        return

    with dissolve
    return


################################################################################
## Возвращение конкретных решений в последующие дни
################################################################################

label ps_reactive_echo_scene(day):
    if day in ps_reactive_echoes_seen:
        return

    $ ps_reactive_echoes_seen = ps_reactive_echoes_seen + [day]

    if day == 4:
        scene bg mezzanine
        with dissolve

        if ps_second_shift_path == "остановил линию":
            show sv neutral at ps_right
            with dissolve
            sv "После твоей остановки люди начали раньше сообщать о заторах. Цифры просели на три минуты, зато сегодня никто не полез разгребать контейнер руками."
            p "В отчёте это тоже видно?"
            sv "Теперь — да. Я добавил отдельную причину: «остановлено сотрудником до происшествия»."
            $ ps_record_consequence("Первая остановка стала для смены разрешением замечать риск раньше аварии.")
            hide sv
        elif ps_second_shift_path == "позвал команду":
            show newb relief at ps_right
            with dissolve
            newb "Сегодня у контейнера никто не спрашивал, кто виноват. Сначала позвали людей. Кажется, один раз тоже может стать привычкой."
            $ ps_team_unity += 1
            hide newb
        else:
            show vet concerned at ps_left
            with dissolve
            vet "Вчера мы вытянули норму. Сегодня контейнер поставили на тот же участок и добавили скорость. Система тоже умеет учиться — только не тому."
            $ ps_burnout += 1
            hide vet

    elif day == 5:
        scene bg control_room
        with dissolve

        if ps_conflict_result(4) == "lera_first":
            show newb relief at ps_right
            with dissolve
            newb "Вчера я начала сама. Сегодня в служебной записке впервые есть моя фраза, а не пересказ начальника."
            $ ps_newbie_trust += 1
            hide newb
        elif ps_conflict_result(4) in ("artyom_first", "player_first"):
            show newb worried at ps_right
            with dissolve
            newb "Мне прислали протокол. Там написано, что я «подтвердила изложенную версию». Формально правда. Только моей версии там нет."
            $ ps_record_consequence("За Леру снова сказали правильные слова, но её собственных слов в протоколе не осталось.")
            hide newb

    elif day == 6:
        scene bg break_room
        with dissolve

        if ps_shift_plan == "rotation":
            show vet neutral at ps_left
            show newb relief at ps_right
            with dissolve
            vet "Ротация сработала. Рука ноет меньше, чем обычно."
            newb "А я впервые дошла до конца смены и не перестала понимать, что сканирую."
            $ ps_team_unity += 1
            hide vet
            hide newb
        elif ps_shift_plan == "balanced":
            show sv neutral at ps_right
            with dissolve
            sv "План закрыли. Виктор после смены не смог сразу снять перчатку. В отчёте обе строки зелёные."
            p "Значит, проверять людей через час было поздно."
            $ ps_burnout += 1
            hide sv
        elif ps_shift_plan == "push":
            show mem serious at ps_left
            with dissolve
            mem "Хвост выбили за сорок минут. Потом два часа никто не разговаривал — берегли дыхание. Табло было в восторге."
            $ ps_team_unity -= 1
            hide mem

    elif day == 7:
        scene bg locker_room
        with dissolve
        $ ps_echo_route = ps_route_target()
        $ ps_echo_state = ps_route_variant_data(ps_echo_route)

        if ps_echo_route == "newbie":
            show newb relief at ps_right
            with dissolve
            if ps_route_variant("newbie") == "growth":
                newb "Сегодня не жди от меня сигнала. Если что-то будет не так, я скажу первой. Ты всё равно услышишь."
            else:
                newb "Перед запуском скажи, куда мне встать и что отвечать, если вызовут. Когда ты уже решил, у меня хотя бы не дрожат руки."
            hide newb
        elif ps_echo_route == "veteran":
            show vet concerned at ps_left
            with dissolve
            if ps_route_variant("veteran") == "growth":
                vet "Ключ от подъёмника у Артёма. Странное чувство: впервые пришёл на смену и заранее знаю, чего делать не буду."
            else:
                vet "Если линия встанет, сначала зови меня. После финала можете читать лекции про безопасность сколько угодно."
            hide vet
        elif ps_echo_route == "joker":
            show mem serious at ps_left
            with dissolve
            if ps_route_variant("joker") == "growth":
                mem "Мне страшно. Всё, сказал. Теперь можем работать без обязательной шутки в конце."
            else:
                mem "Последняя смена! Сегодня шутки бесплатные, паника по подписке, исчезновения только после согласования."
            hide mem
        else:
            show sv stern at ps_right
            with dissolve
            if ps_route_variant("supervisor") == "growth":
                sv "Общий стоп доступен каждому. Если ошибётесь — разберём. Если промолчите — разбирать может быть уже нечего."
            else:
                sv "Никаких решений без моего подтверждения. Сегодня я отвечаю за каждый запуск и каждую остановку."
            hide sv

        $ ps_record_consequence("Маршрут {} вошёл в состояние «{}».".format(ps_character_display_name(ps_echo_route), ps_echo_state["title"]))

    return


################################################################################
## Дело смены и поддельный голос
################################################################################

label ps_deep_investigation_scene:
    $ ps_investigation_start()
    $ ps_unlock_cg("evidence_timeline")

    show screen ps_cinematic_bars
    scene cg evidence_timeline at ps_cg_reveal
    with ps_violet_cut

    n "Факты уже лежат в папке. Но Морозов будет смотреть не на толщину, а на разрывы между страницами. Ты раскладываешь события по времени."

    hide screen ps_cinematic_bars
    call screen ps_deep_investigation_board

    $ ps_investigation_result = ps_investigation_score()
    $ ps_investigation_complete = True

    scene bg control_room
    with dissolve
    show sv stern at ps_right
    show cur at ps_left
    with dissolve

    if ps_investigation_result >= 9:
        $ ps_evidence += 3
        $ ps_integrity += 2
        $ ps_supervisor_respect += 1
        $ ps_unlock_achievement("chain_of_cause")
        $ ps_record_consequence("Ты доказал не одну ошибку, а последовательность решений, сделавших её неизбежной.")
        p "Ремонт отменили за девять дней до нашей смены. Остановку удалили после синхронизации. Недостачу провели через общий буфер. И только потом подготовили причину про сотрудника."
        cur "Ты называешь это системой?"
        p "Я называю это хронологией. Система — ваше слово."
        sv "Все четыре события подтверждаются независимо."
    elif ps_investigation_result >= 5:
        $ ps_evidence += 1
        $ ps_integrity += 1
        p "Часть событий связана. Но между удалённой записью и готовым отчётом остаётся разрыв."
        cur "Разрыв, в который вы поместили удобное объяснение."
        sv "Или место, где нам не дали доступ к журналу."
        n "Дело не рассыпается, но теперь каждую недостающую минуту придётся защищать отдельно."
    else:
        $ ps_supervisor_respect -= 1
        $ ps_burnout += 1
        p "Все события выглядят подозрительно."
        cur "Подозрение — не последовательность. Вы принесли четыре отдельных тревоги и назвали их причиной."
        n "На доске много линий. Ни одна не выдерживает первого прямого вопроса."

    hide sv
    hide cur
    with dissolve
    return


label ps_storm_mimic_scene:
    if ps_storm_mimic_seen or len(ps_storm_fragments) < 4:
        return

    $ ps_storm_mimic_seen = True
    $ ps_storm_mimic_choice = None
    $ ps_unlock_cg("mimic_message")
    $ ps_set_ambience("service")
    $ ps_play_sfx("radio")

    show screen ps_cinematic_bars
    scene cg mimic_message at ps_cg_reveal
    with ps_violet_cut

    n "Телефон показывает четыре сообщения с разницей в одну минуту. Все отправлены с настоящих контактов. Но одно просит человека сделать именно то, чего он боялся всю неделю."

    hide screen ps_cinematic_bars
    call screen ps_storm_mimic
    $ ps_storm_mimic_choice = _return
    $ ps_storm_mimic_correct = ps_storm_mimic_choice == "max"

    if ps_storm_mimic_correct:
        $ ps_evidence += 1
        $ ps_unlock_achievement("human_voice")
        $ ps_record_consequence("Ты узнал подделку V-13 не по словам, а по тому, чему Макс успел научиться рядом с вами.")
        n "Ты нажимаешь на сообщение Макса. Его время меняется первым: 06:13 превращается в --:--. Текст распадается на отдельные буквы. Под ними появляется новая строка: «ГОЛОС ОПРЕДЕЛЁН ПО ПАМЯТИ СМЕНЫ»."
        mem "Я бы никогда не попросил никого не считать людей. Даже подделывать меня надо внимательнее."
    else:
        $ ps_burnout += 1
        $ ps_record_consequence("V-13 заставил тебя усомниться в настоящем голосе одного из людей смены.")
        $ ps_mimic_person = ps_storm_mimic_message(ps_storm_mimic_choice)
        n "Отмеченное сообщение гаснет. Через секунду возвращается с обычным временем и отметкой «прочитано». Настоящий автор отвечает коротко: «Это был я». Поддельный голос остаётся в списке."

    return


################################################################################
## Восемь вариантов разрешения маршрутов и истинный посткредитный эпизод
################################################################################

label ps_route_resolution_scene:
    $ ps_resolution_route = ps_route_target()
    $ ps_resolution_variant = ps_route_variant(ps_resolution_route)

    if ps_resolution_variant == "undecided":
        $ ps_record_route_tendency(ps_resolution_route, "growth", 1, "Смена сохранила незавершённый маршрут как осторожный шаг к доверию.")
        $ ps_resolution_variant = ps_route_variant(ps_resolution_route)

    $ ps_resolution_key = "{}:{}".format(ps_resolution_route, ps_resolution_variant)

    if ps_resolution_key in ps_route_resolutions_seen:
        return

    $ ps_route_resolutions_seen = ps_route_resolutions_seen + [ps_resolution_key]
    $ ps_play_route_motif(ps_resolution_route)
    $ ps_unlock_cg("route_crossroads")

    show screen ps_cinematic_bars
    if ps_resolution_variant == "growth":
        scene cg route_crossroads at ps_growth_grade
    else:
        scene cg route_crossroads at ps_shadow_grade
    with ps_violet_cut
    pause 0.7
    hide screen ps_cinematic_bars

    if ps_resolution_route == "newbie":
        scene bg control_room
        with dissolve
        show newb relief at ps_close_right
        with dissolve
        if ps_resolution_variant == "growth":
            newb "Я уже отправила свою хронологию. Не тебе на проверку — сразу в дело."
            p "Страшно?"
            newb "Да. Но теперь страх хотя бы не пишет за меня."
            $ ps_add_relationship_memory("Лера отправила собственную версию без просьбы переписать её слова.")
        else:
            newb "Я написала черновик. Посмотришь и отправишь от своего имени? Твоим словам поверят быстрее."
            p "А твоим?"
            newb "Моим я пока верю только после тебя."
            n "Это звучит как доверие. И как предупреждение о цене такого доверия."
        hide newb

    elif ps_resolution_route == "veteran":
        scene bg loading_dock
        with dissolve
        show vet concerned at ps_close_left
        with dissolve
        if ps_resolution_variant == "growth":
            vet "Я поставил себя на выходной. Сам. Без твоего приказа и без справки после падения."
            p "Склад переживёт?"
            vet "Теперь это его проблема."
            $ ps_add_relationship_memory("Виктор выбрал остановку раньше, чем тело выбрало её за него.")
        else:
            vet "После финального запуска уйду. До него не трогай меня и не смотри на руку."
            p "Ты ведь сам просил остановить тебя."
            vet "Просил. А теперь прошу дать закончить. Видишь, какой я последовательный."
            n "Он улыбается, уже заранее прощая себе очередное исключение."
        hide vet

    elif ps_resolution_route == "joker":
        scene bg break_room
        with dissolve
        show mem serious at ps_close_left
        with dissolve
        if ps_resolution_variant == "growth":
            mem "Я не придумал, как сделать это смешным. Поэтому скажу как есть: если вы уйдёте, я не хочу оставаться здесь один."
            p "Вот и не оставайся."
            mem "Невероятно короткий сценарий. Работает лучше моих."
            $ ps_add_relationship_memory("Макс попросил остаться без единой защитной шутки.")
        else:
            mem "После смены устрою прощальный стендап. Тема вечера: «Как потерять всех коллег и всё равно закрыть план»."
            p "Макс."
            mem "Не сейчас. Если перестану говорить, придётся услышать ответ."
            n "Он улыбается слишком широко. Ты уже умеешь различать этот сигнал."
        hide mem

    else:
        scene bg control_room
        with dissolve
        show sv stern at ps_close_right
        with dissolve
        if ps_resolution_variant == "growth":
            sv "Я открыл общий стоп всем терминалам. После смены за это придётся отвечать."
            p "Своим именем?"
            sv "Артём Волков. Без должности в начале строки."
            $ ps_add_relationship_memory("Артём подписал решение своим именем и оставил смене право остановиться.")
        else:
            sv "До конца смены все команды идут через меня. Даже если я ошибусь, линия хотя бы ошибётся один раз, а не четырьмя разными способами."
            p "А если тебя не будет рядом?"
            sv "Значит, никто ничего не запускает."
            n "Он построил идеальную защиту. Проблема только в том, что внутри неё почти не осталось чужой воли."
        hide sv

    call screen ps_route_variant_card(ps_resolution_route)
    $ ps_stop_route_motif()
    return


label ps_zero_shift:
    if ps_zero_shift_seen or not ps_true_shift_ready():
        return

    $ ps_zero_shift_seen = True
    $ persistent.ps_true_shift_unlocked = True
    $ renpy.save_persistent()
    $ ps_unlock_cg("zero_shift", notify=True)
    $ ps_collect_document("zero_roster")
    $ ps_unlock_achievement("zero_shift")
    $ ps_record_storm_transmission("zero_shift")

    scene bg black
    with fade
    stop music fadeout 2.0
    $ ps_set_ambience("service")

    centered "ПОСЛЕ ТИТРОВ\n\nНУЛЕВАЯ СМЕНА"

    scene bg service_corridor
    with fade

    n "Проходная уже закрыла вашу неделю, но телефон показывает незавершённую операцию. Время начала — 00:00. Время окончания отсутствует. В карточке нет номера сотрудника. Только строка: «СМЕНА 0 // НЕ ПЕРЕДАНА»."

    show newb relief at ps_left
    show mem serious at ps_center
    show vet concerned at ps_right
    with dissolve

    newb "Сообщение пришло всем. На этот раз текст одинаковый."
    vet "Значит, либо настоящее, либо научилось не ошибаться."
    mem "Очень успокаивающий выбор из двух вариантов."

    hide newb
    hide mem
    hide vet
    show sv stern at ps_right
    with dissolve

    sv "Я нашёл старый журнал. До введения ночного рейтинга здесь была смена, которую выводили между закрытием одного отчётного дня и началом другого."
    p "Нулевая?"
    sv "В документах её нет. Но все отменённые заявки проходили через её код. V-13 был не сектором. Сначала это был номер смены."

    $ ps_play_sfx("radio")
    n "За бетонной дверью щёлкает реле. По очереди загораются пять индикаторов — ровно столько, сколько людей стоит в коридоре."

    show screen ps_cinematic_bars
    scene cg zero_shift at ps_cg_reveal
    with ps_violet_cut

    n "На старом табло появляются фамилии сотрудников, которых давно нет в графике. Последняя строка остаётся пустой, пока ты не подходишь ближе. Система вписывает твоё имя и задаёт первый вопрос без готового ответа: «КТО ПЕРЕДАСТ ЭТУ СМЕНУ?»"

    if ps_conflict_result(6) == "shared_timeline":
        p "Мы. По очереди. Каждый — только то, что видел сам."
        n "Четыре голоса за спиной отвечают не одновременно, но одним решением."
    else:
        p "Сначала открой дверь."
        n "Замок отвечает зелёным светом. Это не согласие. Скорее приглашение продолжить спор с другой стороны."

    centered "PURPLE SHIFT\n\nНУЛЕВАЯ СМЕНА ОТКРЫТА"

    hide screen ps_cinematic_bars
    $ ps_stop_ambience()
    return
