# -*- coding: utf-8 -*-

################################################################################
## Purple Shift 1.8 — «Свои люди»
## Живые сцены команды, бытовые события и память недели
##
## Purple Shift 1.9 — «После шума»
## Единая панель смены, доступность, новые CG и технический ремастер
################################################################################

default ps_human_moments_seen = []
default ps_micro_events_seen = []
default ps_human_memory_log = []
default ps_shift_temperature = 0
default ps_memory_wall_choice = None
default ps_last_checkpoint_choice = None


image cg human_break = "images/cg/human_break.jpg"
image cg memory_wall = "images/cg/memory_wall.jpg"
image cg last_checkpoint = "images/cg/last_checkpoint.jpg"


transform ps_memory_reveal:
    xalign 0.5
    yalign 0.5
    zoom 1.055
    alpha 0.0
    matrixcolor TintMatrix("#eadcff") * SaturationMatrix(0.94)
    ease 0.8 zoom 1.015 alpha 1.0


init 25 python:
    if getattr(persistent, "ps_choice_insight", None) is None:
        persistent.ps_choice_insight = False

    if getattr(persistent, "ps_high_contrast", None) is None:
        persistent.ps_high_contrast = False

    if getattr(persistent, "ps_quiet_interface", None) is None:
        persistent.ps_quiet_interface = False

    if getattr(persistent, "ps_human_memories", None) is None:
        persistent.ps_human_memories = []

    ps_remaster_cgs = [
        ("human_break", "Пять минут без должностей", "images/cg/human_break.jpg"),
        ("memory_wall", "Что запомнила смена", "images/cg/memory_wall.jpg"),
        ("last_checkpoint", "После проходной", "images/cg/last_checkpoint.jpg"),
    ]

    known_cg_ids = {item[0] for item in ps_cg_catalog}
    for cg_item in ps_remaster_cgs:
        if cg_item[0] not in known_cg_ids:
            ps_cg_catalog.append(cg_item)

    ps_remaster_documents = [
        (
            "human_roster",
            "Табель с человеческими пометками",
            "Рядом с номерами смены от руки записано, кто боится высоты, кому нельзя перегружать кисть и кто всегда забывает поесть.",
        ),
        (
            "memory_wall",
            "Стена одной недели",
            "Факты, решения и имена собраны рядом: происшествие больше нельзя отделить от людей, которые его пережили.",
        ),
    ]

    known_document_ids = {item[0] for item in ps_document_catalog}
    for document_item in ps_remaster_documents:
        if document_item[0] not in known_document_ids:
            ps_document_catalog.append(document_item)

    ps_remaster_achievements = [
        (
            "ordinary_people",
            "Пять минут без должностей",
            "Остаться с командой, когда разговор больше ничего не решает.",
        ),
        (
            "small_stops",
            "Маленькие остановки",
            "Не пройти мимо трёх бытовых событий смены.",
        ),
        (
            "memory_wall",
            "Помнить целиком",
            "Собрать стену недели из фактов и человеческих последствий.",
        ),
        (
            "after_noise",
            "После шума",
            "Дойти с командой до последней развилки за проходной.",
        ),
    ]

    known_achievement_ids = {item[0] for item in ps_achievement_catalog}
    for achievement_item in ps_remaster_achievements:
        if achievement_item[0] not in known_achievement_ids:
            ps_achievement_catalog.append(achievement_item)

    ps_remaster_messages = [
        {
            "id": "shift_kettle",
            "day": 3,
            "sender": "Смена",
            "time": "05:26",
            "preview": "Чайник снова выключили раньше времени.",
            "incoming": [
                "Чайник снова выключили раньше времени. Макс обвиняет автоматику, Виктор — Макса.",
                "Лера просит никого не включать его пустым. Артём неожиданно прислал инструкцию из двух слов: «Налей воду».",
            ],
            "replies": [
                {
                    "id": "bring_water",
                    "title": "«Принесу бутылку. Без служебной записки.»",
                    "answer": "Принесу воду. И давайте хотя бы чайник не превращать в расследование.",
                    "reaction": "Макс: поздно, дело уже передано в отдел особо горячих кружек.",
                    "effects": {"ps_humor": 1, "ps_team_unity": 1},
                },
            ],
        },
        {
            "id": "shift_photo",
            "day": 5,
            "sender": "Смена",
            "time": "06:11",
            "preview": "На общем фото опять не хватает одного человека.",
            "incoming": [
                "На общем фото опять не хватает того, кто держал телефон.",
                "Лера предлагает поставить таймер. Виктор предлагает считать отсутствующего официально присутствующим.",
            ],
            "replies": [
                {
                    "id": "timer",
                    "title": "«Ставьте таймер. В этот раз будут все.»",
                    "answer": "Ставьте таймер. Десять секунд хватит, чтобы никто не остался за кадром.",
                    "reaction": "Лера: сохраню оригинал. Даже если Макс моргнёт.",
                    "effects": {"ps_humanity": 1, "ps_team_unity": 1},
                },
            ],
        },
        {
            "id": "shift_gate",
            "day": 7,
            "sender": "Смена",
            "time": "07:09",
            "preview": "У проходной ждём пять минут.",
            "incoming": [
                "У проходной ждём пять минут. Без повестки и без обязательного присутствия.",
                "Кто успеет — просто дойдём до остановки вместе.",
            ],
            "replies": [
                {
                    "id": "coming",
                    "title": "«Иду. Не начинайте финал без меня.»",
                    "answer": "Иду. Не начинайте финальную сцену без меня.",
                    "reaction": "Макс: режиссёр просил передать, что бюджет на второй дубль закончился.",
                    "effects": {"ps_humor": 1, "ps_team_unity": 1},
                },
            ],
        },
    ]

    known_message_ids = {message["id"] for message in ps_message_catalog}
    for message_item in ps_remaster_messages:
        if message_item["id"] not in known_message_ids:
            ps_message_catalog.append(message_item)

    def ps_record_human_memory(memory_id, description, temperature=1):
        global ps_human_memory_log
        global ps_shift_temperature

        if memory_id not in ps_human_memory_log:
            ps_human_memory_log = ps_human_memory_log + [memory_id]
            ps_shift_temperature += temperature
            ps_record_consequence(description)

        memories = list(getattr(persistent, "ps_human_memories", []) or [])
        if memory_id not in memories:
            memories.append(memory_id)
            persistent.ps_human_memories = memories
            renpy.save_persistent()

    def ps_mark_human_scene(scene_id):
        global ps_human_moments_seen
        if scene_id not in ps_human_moments_seen:
            ps_human_moments_seen = ps_human_moments_seen + [scene_id]

    def ps_mark_micro_event(event_id):
        global ps_micro_events_seen
        if event_id not in ps_micro_events_seen:
            ps_micro_events_seen = ps_micro_events_seen + [event_id]
        if len(ps_micro_events_seen) >= 3:
            ps_unlock_achievement("small_stops")

    def ps_shift_pulse_title():
        if ps_shift_temperature >= 6 and ps_team_unity >= 5:
            return "Люди держат смену вместе"
        if ps_shift_temperature >= 3:
            return "Должности начинают становиться именами"
        if ps_burnout >= 7:
            return "Шум стал громче людей"
        return "Смена пока присматривается к тебе"

    def ps_shift_pulse_caption():
        if not ps_human_memory_log:
            return "Значимые мелочи появятся здесь после разговоров и бытовых остановок."
        return "Запомнено человеческих моментов: {}. Последние решения возвращаются не только цифрами, но и поведением команды.".format(len(ps_human_memory_log))

    def ps_toggle_choice_insight():
        persistent.ps_choice_insight = not persistent.ps_choice_insight
        renpy.save_persistent()
        renpy.restart_interaction()

    def ps_toggle_high_contrast():
        persistent.ps_high_contrast = not persistent.ps_high_contrast
        renpy.save_persistent()
        renpy.restart_interaction()

    def ps_toggle_quiet_interface():
        persistent.ps_quiet_interface = not persistent.ps_quiet_interface
        renpy.save_persistent()
        renpy.restart_interaction()

    def ps_remaster_panel_color(alpha="f4"):
        return "#08050d{}".format(alpha) if persistent.ps_high_contrast else "#160d22{}".format(alpha)

    def ps_choice_hint(text):
        if persistent.ps_choice_insight:
            return "  //  {}".format(text)
        return ""


screen ps_shift_pulse():
    modal True
    zorder 290

    key "K_q" action Hide("ps_shift_pulse")
    add Solid("#020104e8")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1420
        ysize 880
        padding (54, 42)
        background Solid(ps_remaster_panel_color())

        vbox:
            spacing 20
            xfill True

            hbox:
                xfill True

                vbox:
                    spacing 4
                    text "СМЕНА // ДЕНЬ [ps_chapter]":
                        color "#b68be7"
                        size 22
                        kerning 3
                    text ps_shift_pulse_title():
                        color "#ffffff"
                        size 43

                textbutton "ЗАКРЫТЬ  [[Q]":
                    id "ps_shift_pulse_close"
                    action Hide("ps_shift_pulse")
                    xalign 1.0
                    xsize 240
                    ysize 58
                    background Solid("#43285b")
                    hover_background Solid("#704397")
                    text_color "#ffffff"
                    text_size 20

            if not persistent.ps_quiet_interface:
                text ps_shift_pulse_caption():
                    color "#cfc2d8"
                    size 23
                    xmaximum 1180

            grid 3 2:
                spacing 16
                xalign 0.5

                use ps_remaster_metric("КОМАНДА", ps_team_unity, "#82e5b7")
                use ps_remaster_metric("ЧЕСТНОСТЬ", ps_integrity, "#d5a6ff")
                use ps_remaster_metric("УЛИКИ", ps_evidence, "#7fd9ff")
                use ps_remaster_metric("ВЫГОРАНИЕ", ps_burnout, "#e58d99")
                use ps_remaster_metric("ТЕПЛО СМЕНЫ", ps_shift_temperature, "#ffd083")
                use ps_remaster_metric("ОТКРЫТО CG", len(persistent.ps_unlocked_cgs), "#ff91d2", 22)

            frame:
                xfill True
                padding (26, 20)
                background Solid("#21142fe8" if not persistent.ps_high_contrast else "#000000")

                vbox:
                    spacing 9
                    text "ВЕДУЩИЙ МАРШРУТ // [ps_route_title(ps_route_target())]":
                        color "#d5b6ff"
                        size 26
                    text ps_person_route_memory(ps_route_target()):
                        color "#ddd4e3"
                        size 21
                    text "Личных исходов открыто: [len(persistent.ps21_route_outcomes)] / 8":
                        color "#a99ab4"
                        size 18
                    if ps_human_memory_log and not persistent.ps_quiet_interface:
                        text "Последние человеческие следы: [', '.join(ps_human_memory_log[-3:])]":
                            color "#aa9bb5"
                            size 18

            hbox:
                spacing 14
                xalign 0.5

                textbutton "ТЕЛЕФОН":
                    action [Hide("ps_shift_pulse"), Show("ps_phone")]
                    xsize 300
                    ysize 60
                    background Solid("#5d3581")
                    hover_background Solid("#8752b6")
                    text_color "#ffffff"
                    text_size 22

                textbutton "ИНТЕРФЕЙС":
                    id "ps_remaster_settings_open"
                    action Show("ps_remaster_settings")
                    xsize 340
                    ysize 60
                    background Solid("#3c2d49")
                    hover_background Solid("#604873")
                    text_color "#ffffff"
                    text_size 22


screen ps_remaster_metric(title, value, accent, maximum=12):
    frame:
        xsize 410
        ysize 116
        padding (20, 15)
        background Solid("#20152be8" if not persistent.ps_high_contrast else "#000000")

        vbox:
            spacing 9
            hbox:
                xfill True
                text title:
                    color "#c8bbd0"
                    size 18
                text "[value]":
                    color accent
                    size 24
                    xalign 1.0
            bar:
                value StaticValue(max(0, min(value, maximum)), maximum)
                xmaximum 365
                ymaximum 14
                left_bar Solid(accent)
                right_bar Solid("#4c4054")


screen ps_remaster_settings():
    modal True
    zorder 310

    add Solid("#020104dd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1040
        padding (54, 42)
        background Solid(ps_remaster_panel_color())

        vbox:
            spacing 20
            xfill True

            text "ДОСТУПНОСТЬ И ОТОБРАЖЕНИЕ":
                color "#d2a7ff"
                size 35
                xalign 0.5

            text "Настройки сохраняются между прохождениями и не меняют условия финалов.":
                color "#bfb1c6"
                size 21
                xalign 0.5

            use ps_remaster_toggle(
                "ПОЯСНЕНИЯ К ВЫБОРАМ",
                "Показывать рядом с новыми решениями их смысл, но не точные очки.",
                persistent.ps_choice_insight,
                Function(ps_toggle_choice_insight),
                "ps_remaster_choice_insight",
            )
            use ps_remaster_toggle(
                "ВЫСОКИЙ КОНТРАСТ",
                "Затемнить панели и усилить разделение текста и фона.",
                persistent.ps_high_contrast,
                Function(ps_toggle_high_contrast),
                "ps_remaster_high_contrast",
            )
            use ps_remaster_toggle(
                "ТИХИЙ ИНТЕРФЕЙС",
                "Скрыть лишний статусный шум на новых экранах.",
                persistent.ps_quiet_interface,
                Function(ps_toggle_quiet_interface),
                "ps_remaster_quiet_interface",
            )

            textbutton "ГОТОВО":
                id "ps_remaster_settings_close"
                action Hide("ps_remaster_settings")
                xalign 0.5
                xsize 360
                ysize 64
                background Solid("#7040a0")
                hover_background Solid("#9a61d2")
                text_color "#ffffff"
                text_size 23


screen ps_remaster_toggle(title, description, enabled, action, button_id):
    button:
        id button_id
        action action
        xfill True
        ysize 116
        padding (24, 17)
        background Solid("#43285b" if enabled else "#21172a")
        hover_background Solid("#58376e")

        hbox:
            spacing 22
            xfill True
            vbox:
                spacing 5
                text title:
                    color "#ffffff"
                    size 24
                text description:
                    color "#c7bacd"
                    size 18
            text ("ВКЛ" if enabled else "ВЫКЛ"):
                color ("#8ee3bc" if enabled else "#8d8195")
                size 24
                xalign 1.0
                yalign 0.5


################################################################################
## 1.8 — сцены, в которых команда существует не только ради основного сюжета
################################################################################

label ps_human_shift_scene(day):
    $ ps_human_scene_id = "human_day_{}".format(day)
    if ps_human_scene_id in ps_human_moments_seen:
        return

    if day == 2:
        $ ps_mark_human_scene(ps_human_scene_id)

        scene bg break_room
        with fade

        show newb relief at ps_left
        show vet neutral at ps_right
        show mem grin at ps_center
        with dissolve

        n "Перерыв уже закончился, но никто не встаёт первым. Лера медленно сворачивает пустой пакет из-под печенья, Виктор греет ладони о давно остывшую кружку, а Макс смотрит на часы так, будто ждёт от них официального разрешения ещё немного побыть людьми."
        mem "У нас осталось четыре минуты незаконной обычной жизни. Предложения?"
        vet "Не произноси слово «незаконной» рядом с камерой. Она впечатлительная."
        newb "Можно просто ничего не решать? Хотя бы эти четыре минуты."

        menu:
            "Спросить, кем они бывают после смены[ps_choice_hint('узнать людей вне склада')]":
                $ ps_record_human_memory("разговор вне склада", "Ты впервые спросил команду не о работе, а о жизни после проходной.", 2)
                $ ps_humanity += 1
                $ ps_team_unity += 1
                p "А после проходной вы кто? Не Новичок, Ветеран и Шутник. Просто вы."
                n "Вопрос оказывается сложнее любого кода ошибки. Виктор первым признаётся, что чинит старый мотоцикл, который уже три года не заводится. Лера учится фотографировать город до рассвета. Макс пишет заметки и никому их не показывает."
                mem "Вот и познакомились. Про тебя, кстати, вопрос остаётся открытым."

            "Оставить четыре минуты без разговора[ps_choice_hint('дать команде безопасную тишину')]":
                $ ps_record_human_memory("общая тишина", "Вы разделили тишину, которую не пришлось срочно заполнять задачами.", 1)
                $ ps_endurance += 1
                $ ps_burnout = max(0, ps_burnout - 1)
                p "Давайте ничего. Четыре минуты — это не так много."
                n "Никто не спорит. За стеной продолжает греметь склад, но здесь шум впервые не требует ответа. Когда Артём заглядывает в комнату, он молча прикрывает дверь обратно."

        hide newb
        hide vet
        hide mem
        return

    if day == 4:
        $ ps_mark_human_scene(ps_human_scene_id)
        $ ps_unlock_cg("human_break", True)

        show screen ps_cinematic_bars
        scene cg human_break at ps_memory_reveal
        with ps_violet_cut

        n "В комнате отдыха впервые собираются все четверо. Не для планёрки и не потому, что случилась авария. Просто чайник закипел ровно тогда, когда у каждого нашлось пять свободных минут."
        n "Разговор перескакивает с автобусов на дешёвый кофе, с кофе — на первую зарплату, а потом почему-то на то, кто хуже всех умеет притворяться, будто не устал. Побеждает Виктор. Он требует пересчёта."

        menu:
            "Остаться до конца разговора[ps_choice_hint('поставить человеческий момент выше темпа')]":
                $ ps_record_human_memory("пять минут без должностей", "Ты остался на пять минут, в которых никто ничего от тебя не требовал.", 2)
                $ ps_team_unity += 2
                $ ps_humanity += 1
                $ ps_unlock_achievement("ordinary_people")
                p "Линия переживёт ещё две минуты без нас."
                sv "Если кто-то спросит, я этого не слышал."
                mem "Поздно. Это уже самая человечная служебная записка недели."

            "Мягко вернуть разговор к предстоящей смене[ps_choice_hint('сохранить тепло, но не терять контроль')]":
                $ ps_record_human_memory("честная планёрка", "Ты не оборвал разговор, но помог команде вместе назвать, чего она боится перед запуском.", 1)
                $ ps_efficiency += 1
                $ ps_integrity += 1
                p "Пока все здесь: давайте по одному страху перед запуском. Не отчёт — просто чтобы знать."
                n "Шутки заканчиваются не сразу, но каждый всё-таки называет одну вещь. Артём записывает их на обратной стороне старого графика и не просит подписываться."

        hide screen ps_cinematic_bars
        return

    if day == 6:
        $ ps_mark_human_scene(ps_human_scene_id)
        $ ps_unlock_cg("memory_wall", True)
        $ ps_collect_document("memory_wall")

        show screen ps_cinematic_bars
        scene cg memory_wall at ps_memory_reveal
        with ps_violet_cut

        n "К концу шестого дня доска перестаёт быть схемой происшествия. Между кодами ошибок появляются имена, рядом со временем остановки — заметка о руке Виктора, возле удалённого журнала — фотография Леры, которую система едва не назначила причиной сбоя."
        sv "Для проверки это лишнее."
        newb "Для проверки — может быть. Для правды — нет."

        menu:
            "Оставить на доске факты и человеческие последствия[ps_choice_hint('собрать полную память недели')]":
                $ ps_memory_wall_choice = "whole"
                $ ps_record_human_memory("полная стена недели", "Вы отказались отделять техническую причину от человеческой цены.", 2)
                $ ps_evidence += 1
                $ ps_integrity += 1
                $ ps_team_unity += 1
                $ ps_unlock_achievement("memory_wall")
                p "Пусть проверяющий увидит не только момент сбоя, но и то, что было до него и осталось после."
                sv "Тогда это уже не приложение к отчёту."
                p "Это и есть отчёт."

            "Снять личные пометки и сохранить их отдельной копией[ps_choice_hint('защитить людей, не потеряв память')]":
                $ ps_memory_wall_choice = "protected"
                $ ps_record_human_memory("защищённая копия недели", "Личные последствия не попали в официальный файл, но остались у команды.", 1)
                $ ps_evidence += 1
                $ ps_supervisor_respect += 1
                p "В официальной версии оставим проверяемое. Всё личное сфотографируем и сохраним отдельно — без фамилий в чужих руках."
                newb "Главное, чтобы отдельно не означало забыто."
                p "Не будет."

        hide screen ps_cinematic_bars
        return

    return


label ps_shift_micro_event(day):
    $ ps_event_id = "micro_day_{}".format(day)
    if ps_event_id in ps_micro_events_seen:
        return

    if day == 3:
        $ ps_mark_micro_event(ps_event_id)
        scene bg warehouse_inside
        with dissolve

        n "У пустой тележки лежит чужая бутылка воды. На крышке маркером написана только буква «В». Виктор уже ушёл на дальнюю линию и, конечно, скажет, что не хотел пить."

        menu:
            "Отнести бутылку Виктору[ps_choice_hint('заметить человека раньше проблемы')]":
                $ ps_record_human_memory("бутылка Виктора", "Ты принёс Виктору воду до того, как усталость стала ещё одной неисправностью.", 1)
                $ ps_humanity += 1
                $ ps_veteran_safe = True
                p "Забыл своё оборудование."
                vet "Это вода."
                p "Сегодня — оборудование."

            "Поставить бутылку у общей рации[ps_choice_hint('сделать заботу частью порядка')]":
                $ ps_record_human_memory("вода у рации", "Вода появилась там, где её нельзя было не заметить.", 1)
                $ ps_efficiency += 1
                $ ps_team_unity += 1
                n "Через десять минут бутылка исчезает. Виктор ничего не говорит, но позже у рации появляется ещё одна — уже для Леры."
        return

    if day == 5:
        $ ps_mark_micro_event(ps_event_id)
        scene bg packing_zone
        with dissolve

        n "На упаковке заканчиваются перчатки нужного размера. Можно дотянуть до конца партии в неудобных или остановить участок на семь минут и сходить за коробкой. Табло уже считает отставание."

        menu:
            "Остановить участок и принести подходящие перчатки[ps_choice_hint('безопасность важнее семи минут')]":
                $ ps_record_human_memory("семь минут на перчатки", "Вы потеряли семь минут и не потеряли право работать безопасно.", 1)
                $ ps_team_unity += 1
                $ ps_integrity += 1
                $ ps_burnout = max(0, ps_burnout - 1)
                p "Стоп на семь минут. Табло переживёт. Руки у нас запасных не имеют."

            "Перераспределить людей с подходящими перчатками[ps_choice_hint('решить проблему без опасной спешки')]":
                $ ps_record_human_memory("тихая перестановка", "Команда сама перестроилась, пока коробку с перчатками несли со склада.", 1)
                $ ps_efficiency += 1
                $ ps_team_unity += 1
                sv "Без рывков. Кто меняется местами — говорит вслух."
                n "Семь минут всё равно теряются, но впервые никто не делает вид, будто их можно выиграть чужим дискомфортом."
        return

    if day == 7:
        $ ps_mark_micro_event(ps_event_id)
        $ ps_collect_document("human_roster")
        scene bg locker_room
        with dissolve

        n "На внутренней стороне шкафчика висит старый табель. Кто-то дописывал рядом с номерами короткие вещи: «боится высоты», «не давать таскать одной», «после четырёх утра забывает поесть»."

        menu:
            "Сфотографировать табель для команды[ps_choice_hint('сохранить неофициальную память')]":
                $ ps_record_human_memory("человеческий табель", "Ты сохранил табель, в котором люди описаны заботой, а не производительностью.", 2)
                $ ps_humanity += 1
                $ ps_team_unity += 1
                n "В архив попадает документ, который никогда не примут как доказательство. Возможно, поэтому он говорит о смене точнее остальных."

            "Переписать важные пометки в общий план безопасности[ps_choice_hint('превратить заботу в работающий порядок')]":
                $ ps_record_human_memory("забота как регламент", "Человеческие пометки стали частью общего плана безопасности без имён и диагнозов.", 1)
                $ ps_integrity += 1
                $ ps_supervisor_respect += 1
                n "Ты убираешь имена, оставляешь ограничения и добавляешь одно правило: любой может попросить замену без объяснений перед всей сменой."
        return

    return


################################################################################
## 1.9 — последний визуальный акцент после рассчитанного финала
################################################################################

label ps_last_checkpoint_scene:
    if ps_last_checkpoint_choice is not None:
        return

    $ ps_unlock_cg("last_checkpoint", True)
    $ ps_unlock_achievement("after_noise")

    show screen ps_cinematic_bars
    scene cg last_checkpoint at ps_memory_reveal
    with ps_violet_cut

    n "За проходной дождь уже закончился. До автобусов можно идти двумя дорогами: короткой вдоль забора или длинной через освещённую остановку. Никто не торопится выбирать первым."
    mem "Вот теперь официально всё. Дальше у каждого своя ветка сюжета."
    vet "Ты можешь хотя бы однажды не называть обычную дорогу веткой сюжета?"
    newb "Не может. Но вопрос всё равно правильный: вместе или по домам?"

    menu:
        "Пойти длинной дорогой вместе[ps_choice_hint('оставить финалу человеческое послесловие')]":
            $ ps_last_checkpoint_choice = "together"
            $ ps_record_human_memory("длинная дорога вместе", "После финала вы выбрали дорогу, на которой разговор успевал закончиться сам.", 2)
            p "Автобусы всё равно не раньше чем через десять минут. Пойдём длинной."
            sv "Это неэффективно."
            mem "Запишите дату: Артём только что согласился на неэффективное."
            sv "Я ещё не согласился."
            n "Но идёт вместе со всеми."

        "Попрощаться здесь, не обесценивая неделю[ps_choice_hint('дать каждому право уйти своим путём')]":
            $ ps_last_checkpoint_choice = "separate"
            $ ps_record_human_memory("честное прощание", "Вы разошлись без обещаний навсегда остаться одной командой.", 1)
            p "Дальше каждый своей дорогой. Но не так, будто этой недели не было."
            newb "Хорошо. Тогда без «ещё увидимся», если не знаем."
            vet "Увидимся или нет — номера друг у друга есть. Этого достаточно."

    hide screen ps_cinematic_bars
    return
