# -*- coding: utf-8 -*-

################################################################################
## Purple Shift 1.5 — «Голоса смены»
## Имена, характеры, недельные маршруты, рабочие решения и вторжение V-13
################################################################################

default ps_route_week_seen = []
default ps_relationship_memories = []
default ps_shift_plan = None
default ps_shift_plan_history = []
default ps_phone_deferred = []
default ps_phone_muted = []
default ps_storm_intrusions_seen = []
default ps_story_voice_notes = []
default ps_group_chat_choice = None


init 15 python:
    ps_character_profiles = {
        "newbie": {
            "name": "Лера",
            "full_name": "Валерия Мельникова",
            "role": "новичок сортировки",
            "age": "22 года",
            "truth": "Боится не самой ошибки, а того, что чужая формулировка навсегда станет её характеристикой.",
            "need": "Ей нужна не защита вместо неё, а человек, рядом с которым она сможет говорить сама.",
            "avatar": "newb relief",
        },
        "veteran": {
            "name": "Виктор",
            "full_name": "Виктор Савельев",
            "role": "ветеран ночной смены",
            "age": "46 лет",
            "truth": "Он знает склад лучше инструкций и слишком долго считал боль обычной частью опыта.",
            "need": "Ему нужно разрешить другим остановить его раньше, чем привычка снова окажется сильнее тела.",
            "avatar": "vet neutral",
        },
        "joker": {
            "name": "Макс",
            "full_name": "Максим Орлов",
            "role": "сортировщик и голос линии",
            "age": "29 лет",
            "truth": "Шутками он проверяет, отвечает ли ещё смена. Тишина пугает его сильнее любой аварии.",
            "need": "Ему нужен собеседник, рядом с которым не обязательно развлекать всех, чтобы остаться нужным.",
            "avatar": "mem grin",
        },
        "supervisor": {
            "name": "Артём",
            "full_name": "Артём Волков",
            "role": "супервайзер участка",
            "age": "35 лет",
            "truth": "Он вырос из той же линии и теперь каждый день выбирает, кого защищать: людей, цифры или собственное место.",
            "need": "Ему нужен второй голос, который не позволит превратить ответственность в удобную подпись.",
            "avatar": "sv neutral",
        },
    }

    ps_shift_plan_catalog = [
        {
            "id": "rotation",
            "title": "РОТАЦИЯ",
            "subtitle": "Менять позиции каждые сорок минут",
            "detail": "Лера не останется одна на сложном секторе, Виктор не будет постоянно работать у подъёмника, а Макс получит место, откуда слышно всю линию.",
            "accent": "#72d99a",
        },
        {
            "id": "balanced",
            "title": "ПО ОПЫТУ",
            "subtitle": "Каждого поставить туда, где он сильнее",
            "detail": "План будет идти ровнее, но усталость спрячется за привычными движениями.",
            "accent": "#7fcfff",
        },
        {
            "id": "push",
            "title": "РЫВОК",
            "subtitle": "Сильных — на узкие места",
            "detail": "Табло быстро позеленеет. Люди — не обязательно.",
            "accent": "#ff907f",
        },
    ]

    ps_voice_messages = [
        {
            "id": "shift_group",
            "day": 4,
            "sender": "Ночная // общий чат",
            "time": "18:27",
            "preview": "Лера: Я ничего не подписала.",
            "group": True,
            "avatar": "cg team_dawn",
            "status": "4 участника",
            "incoming": [
                "Лера: Я ничего не подписала. Сказала, что дождусь остальных.",
                "Макс: Отлично. Коллективное ожидание официально началось.",
                "Виктор: Скинь номер операции. Без фамилий и лишних слов.",
                "Артём: В диспетчерскую не заходите по одному. Встретимся у линии.",
            ],
            "replies": [
                {
                    "id": "together",
                    "title": "«Разбираем вместе. Никто не остаётся один.»",
                    "answer": "Разбираем вместе. Никто не идёт объясняться в одиночку.",
                    "reaction": "Лера: Тогда я дождусь вас у турникета.",
                    "effects": {"ps_team_unity": 2, "ps_humanity": 1},
                },
                {
                    "id": "facts",
                    "title": "«Нужны лог, время и список операций.»",
                    "answer": "Пришлите лог, время и список операций. Сначала восстановим цепочку.",
                    "reaction": "Артём: Уже выгружаю журнал. Это правильный порядок.",
                    "effects": {"ps_evidence": 1, "ps_efficiency": 1},
                },
            ],
        },
        {
            "id": "lera_voice",
            "day": 3,
            "sender": "Лера",
            "time": "06:11",
            "preview": "Голосовое · 0:18",
            "route": "newbie",
            "requires_route": "newbie",
            "avatar": "newb relief",
            "status": "была недавно",
            "voice_note": "audio/live/route_newbie_motif.ogg",
            "voice_caption": "«Я переписала памятку. Там теперь отдельно мои действия и отдельно то, что сделал ТСД. Так правда спокойнее.»",
            "incoming": [
                "Я всё-таки записала вчерашнюю ошибку. Только теперь это не список того, где я виновата.",
                "Голосовое сообщение · 0:18",
            ],
            "replies": [
                {
                    "id": "proud",
                    "title": "«Вот это уже твоя инструкция.»",
                    "answer": "Вот это уже твоя инструкция, а не признание вины.",
                    "reaction": "Да. И я впервые не боюсь её перечитывать.",
                    "effects": {"ps_newbie_trust": 2, "ps_integrity": 1},
                },
                {
                    "id": "share",
                    "title": "«Покажем её следующему новичку.»",
                    "answer": "Сохрани. Покажем её тому, кто придёт после нас.",
                    "reaction": "После нас. Звучит так, будто мы уже старенькие.",
                    "effects": {"ps_humanity": 1, "ps_team_unity": 1},
                },
            ],
        },
        {
            "id": "viktor_photo",
            "day": 4,
            "sender": "Виктор",
            "time": "06:08",
            "preview": "Фото: старая бирка LIFT-09",
            "route": "veteran",
            "requires_route": "veteran",
            "avatar": "vet neutral",
            "status": "в сети",
            "attachment": "images/cg/route_veteran.jpg",
            "attachment_caption": "Снимок старой сервисной бирки",
            "incoming": [
                "Нашёл старое фото. Эту бирку меняли уже дважды, а дату проверки каждый раз оставляли прежней.",
                "Не пересылай в рабочий чат. Пока просто сохрани оригинал.",
            ],
            "replies": [
                {
                    "id": "backup",
                    "title": "«Сделаю резервную копию.»",
                    "answer": "Сохраню оригинал и копию с датой получения.",
                    "reaction": "Правильно. Память должна жить больше чем в одном телефоне.",
                    "effects": {"ps_evidence": 1, "ps_integrity": 1},
                },
                {
                    "id": "ask",
                    "title": "«Почему ты хранил это один?»",
                    "answer": "Почему ты столько времени хранил это один?",
                    "reaction": "Потому что привык. Это не значит, что правильно.",
                    "effects": {"ps_humanity": 1, "ps_endurance": 1},
                },
            ],
        },
        {
            "id": "max_deleted",
            "day": 4,
            "sender": "Макс",
            "time": "06:13",
            "preview": "Сообщение удалено",
            "route": "joker",
            "requires_route": "joker",
            "avatar": "mem serious",
            "status": "печатает…",
            "incoming": [
                "Сообщение удалено.",
                "Ладно, короткая версия: если сегодня будет совсем не смешно, просто не уходи молча.",
            ],
            "replies": [
                {
                    "id": "stay",
                    "title": "«Не уйду. Но и ты не исчезай в шутках.»",
                    "answer": "Не уйду. Но и ты не исчезай в шутках.",
                    "reaction": "Никаких гарантий. Постараюсь остаться хотя бы между ними.",
                    "effects": {"ps_humor": 1, "ps_team_unity": 2},
                },
                {
                    "id": "call",
                    "title": "«Если накроет — напиши прямо.»",
                    "answer": "Если станет плохо, напиши прямо. Я пойму без шутки.",
                    "reaction": "Вот это уже звучит страшно. Договорились.",
                    "effects": {"ps_humanity": 1, "ps_humor": 1},
                },
            ],
        },
        {
            "id": "irina_note",
            "day": 5,
            "sender": "Артём",
            "time": "18:58",
            "preview": "Черновик расстановки на линию",
            "route": "supervisor",
            "requires_route": "supervisor",
            "avatar": "sv neutral",
            "status": "на смене",
            "attachment": "images/cg/report_pressure.jpg",
            "attachment_caption": "Черновик без подписи",
            "incoming": [
                "Посмотри расстановку до запуска. Если оставить как есть, Виктор снова окажется у подъёмника на всю ночь.",
                "Я могу поменять план, но тогда куратор спросит, почему просела скорость.",
            ],
            "replies": [
                {
                    "id": "rotate",
                    "title": "«Ставим ротацию и записываем причину.»",
                    "answer": "Ставим ротацию. Причину указываем прямо: риск повторения LIFT-09.",
                    "reaction": "Хорошо. Если спросят, отвечать будем вдвоём.",
                    "effects": {"ps_supervisor_respect": 2, "ps_integrity": 1},
                },
                {
                    "id": "own",
                    "title": "«Решение должно быть твоим.»",
                    "answer": "Я скажу, что вижу. Но решение и подпись должны быть твоими.",
                    "reaction": "Так и будет. Спасибо, что не дал спрятаться за тобой.",
                    "effects": {"ps_endurance": 1, "ps_supervisor_respect": 1},
                },
            ],
        },
    ]

    known_message_ids = {message["id"] for message in ps_message_catalog}
    for voice_message in ps_voice_messages:
        if voice_message["id"] not in known_message_ids:
            ps_message_catalog.append(voice_message)

    sender_names = {
        "newbie": "Лера",
        "veteran": "Виктор",
        "joker": "Макс",
        "supervisor": "Артём",
        "newbie_followup": "Лера",
        "veteran_followup": "Виктор",
        "joker_followup": "Макс",
        "supervisor_followup": "Артём",
    }
    for message in ps_message_catalog:
        if message["id"] in sender_names:
            message["sender"] = sender_names[message["id"]]

        route_id = message.get("route")
        if route_id not in ps_character_profiles:
            route_id = {
                "newbie": "newbie",
                "veteran": "veteran",
                "joker": "joker",
                "supervisor": "supervisor",
                "newbie_followup": "newbie",
                "veteran_followup": "veteran",
                "joker_followup": "joker",
                "supervisor_followup": "supervisor",
            }.get(message["id"])

        if "avatar" not in message and route_id in ps_character_profiles:
            message["avatar"] = ps_character_profiles[route_id]["avatar"]

        if "status" not in message:
            message["status"] = "рабочий канал"

    def ps_reveal_character_names():
        global ps_names_revealed
        global ps_newbie_name
        global ps_veteran_name
        global ps_joker_name
        global ps_supervisor_name

        ps_names_revealed = True
        ps_newbie_name = "Лера"
        ps_veteran_name = "Виктор"
        ps_joker_name = "Макс"
        ps_supervisor_name = "Артём"

    def ps_set_curator_name():
        global ps_curator_name
        ps_curator_name = "Морозов"

    def ps_character_profile(route_id):
        return ps_character_profiles.get(route_id, ps_character_profiles["newbie"])

    def ps_character_display_name(route_id):
        if not ps_names_revealed:
            return {
                "newbie": ps_newbie_name,
                "veteran": ps_veteran_name,
                "joker": ps_joker_name,
                "supervisor": ps_supervisor_name,
            }.get(route_id, "Сотрудник")
        return ps_character_profile(route_id)["name"]

    def ps_add_relationship_memory(text):
        global ps_relationship_memories
        if text not in ps_relationship_memories:
            ps_relationship_memories = ps_relationship_memories + [text]

    def ps_route_scene_seen(day, route_id):
        return "{}:{}".format(day, route_id) in ps_route_week_seen

    def ps_mark_route_scene(day, route_id):
        global ps_route_week_seen
        key = "{}:{}".format(day, route_id)
        if key not in ps_route_week_seen:
            ps_route_week_seen = ps_route_week_seen + [key]

    def ps_apply_shift_plan(plan_id):
        global ps_shift_plan
        global ps_shift_plan_history
        global ps_humanity
        global ps_endurance
        global ps_efficiency
        global ps_team_unity
        global ps_burnout

        ps_shift_plan = plan_id
        ps_shift_plan_history = ps_shift_plan_history + [plan_id]

        if plan_id == "rotation":
            ps_humanity += 1
            ps_endurance += 1
            ps_team_unity += 2
            ps_efficiency -= 1
        elif plan_id == "balanced":
            ps_efficiency += 2
            ps_team_unity += 1
            ps_burnout += 1
        else:
            ps_efficiency += 3
            ps_team_unity -= 1
            ps_burnout += 2

    def ps_play_story_voice(message_id):
        global ps_story_voice_notes
        message = ps_message_data(message_id)
        track = message.get("voice_note")
        if track and renpy.loadable(track):
            renpy.music.play(track, channel="motif", loop=False, fadein=0.25)
        if message_id not in ps_story_voice_notes:
            ps_story_voice_notes = ps_story_voice_notes + [message_id]
        renpy.restart_interaction()

    def ps_defer_message(message_id):
        global ps_phone_deferred
        if message_id not in ps_phone_deferred:
            ps_phone_deferred = ps_phone_deferred + [message_id]
            ps_record_consequence(
                "Ты отложил ответ в чате. Для собеседника пауза тоже стала ответом."
            )
        renpy.notify("Ответ отложен")
        renpy.restart_interaction()

    def ps_message_avatar(message):
        if message.get("avatar"):
            return message["avatar"]
        if message["id"] == "v13_unknown":
            return "cg storm_signal"
        return None

    def ps_message_status(message):
        if message["id"] == "v13_unknown":
            return "источник не определён"
        return message.get("status", "рабочий канал")


################################################################################
## Имена вместо должностей
################################################################################

label ps_team_names:
    if ps_names_revealed:
        return

    scene bg break_room
    with fade

    $ ps_set_ambience("break")

    show newb relief at ps_right
    show mem grin at ps_left
    with dissolve

    newb "Мы второй день рядом работаем, а всё ещё зовём друг друга по должностям. Если так пойдёт дальше, я навсегда останусь Новичком."
    newb "Я Лера. Валерия, если кто-то вдруг решит оформить на меня очередную служебку."
    $ ps_newbie_name = "Лера"

    mem "Макс. Просто Макс. «Шутник» — это должность без доплаты и права на отпуск."
    $ ps_joker_name = "Макс"

    show vet neutral at ps_center
    with dissolve

    vet "Виктор."
    $ ps_veteran_name = "Виктор"

    mem "Ты мог хотя бы фамилию добавить. Для торжественности."
    vet "Савельев. Теперь торжественно иди переодеваться."

    show sv neutral at ps_righter
    with dissolve

    sv "Артём Волков. Раз уж у нас вечер знакомств — закончите его до запуска линии."
    $ ps_supervisor_name = "Артём"

    p "А я — [ps_player_name]."
    newb "Вот. Уже немного меньше похоже, будто нас выдали вместе с терминалами."

    $ ps_names_revealed = True
    $ ps_add_relationship_memory("Вы перестали быть должностями и назвали друг другу имена.")
    $ ps_unlock_achievement("names")
    $ ps_unlock_cg("team_names")

    hide newb
    hide mem
    hide vet
    hide sv
    with dissolve

    show screen ps_cinematic_bars
    scene cg team_names at ps_cg_reveal
    with ps_violet_cut
    pause 1.1
    hide screen ps_cinematic_bars
    return


################################################################################
## Маршрутные сцены на протяжении недели
################################################################################

label ps_route_week_scene(day):
    $ ps_week_route = ps_route_target()

    if ps_route_scene_seen(day, ps_week_route):
        return

    $ ps_mark_route_scene(day, ps_week_route)
    $ ps_play_route_motif(ps_week_route)

    if day == 2:
        scene bg break_room
        with fade

        if ps_week_route == "newbie":
            show newb worried at ps_right
            with dissolve
            n "Перед запуском Лера прячет сложенный лист под перчатку. На нём в две колонки записаны ошибки: слева её действия, справа — то, что делал ТСД."
            newb "Я больше не хочу писать просто «ошиблась». Это слово ничего не объясняет, зато очень удобно остаётся рядом с фамилией."
            p "Тогда фиксируй шаги. Где нажала, что увидела и что произошло после."
            newb "Поможешь проверить? Не исправлять за меня — просто проверить."
            p "Договорились."
            $ ps_newbie_trust += 1
            $ ps_add_route("newbie", 1)
            $ ps_add_relationship_memory("Лера попросила не спасать её, а проверить факты рядом.")
            hide newb

        elif ps_week_route == "veteran":
            show vet neutral at ps_left
            with dissolve
            n "Виктор задерживается у двери и разминает кисть, думая, что ты не заметишь. Движение короткое, слишком привычное."
            p "Давно болит?"
            vet "Давно — это не диагноз. На работе удобно говорить «привык» и не разбираться."
            p "Если сегодня начнёт сильнее, скажешь."
            vet "Если скажу, отправишь отдыхать?"
            p "Хотя бы переставлю с тяжёлого."
            vet "Ладно. Один раз попробуем сделать по-умному."
            $ ps_add_route("veteran", 1)
            $ ps_add_relationship_memory("Виктор впервые разрешил заметить свою боль.")
            hide vet

        elif ps_week_route == "joker":
            show mem serious at ps_left
            with dissolve
            n "Макс стоит у автомата с водой и не шутит уже целую минуту. Без привычной улыбки он выглядит не старше, а просто уставшим."
            p "Ты всегда столько говоришь?"
            mem "Только когда вокруг слишком тихо. Если люди отвечают, значит, я ещё не остался один на линии."
            p "А если не отвечают?"
            mem "Тогда я говорю громче. Очень здоровая система."
            p "Сегодня можешь иногда молчать. Я всё равно рядом."
            mem "Опасное предложение, [ps_player_name]. Ещё привыкну."
            $ ps_add_route("joker", 1)
            $ ps_add_relationship_memory("Макс признался, что шутками проверяет, остались ли люди рядом.")
            hide mem

        else:
            show sv neutral at ps_right
            with dissolve
            n "Артём сверяет расстановку людей и дважды меняет Лере участок, прежде чем оставить первый вариант."
            p "Почему вернул обратно?"
            sv "Потому что на безопасном месте просядет план. А если оставить там, где быстро, — просядет человек."
            p "Ты ведь раньше сам стоял на линии."
            sv "Именно поэтому слишком хорошо понимаю оба ответа."
            p "Тогда выбери тот, который сможешь объяснить ей в лицо."
            sv "Неприятный совет. Полезный."
            $ ps_supervisor_respect += 1
            $ ps_add_route("supervisor", 1)
            $ ps_add_relationship_memory("Артём признал, что ещё помнит линию по эту сторону табло.")
            hide sv

    elif day == 3:
        scene bg mezzanine
        with fade

        if ps_week_route == "newbie":
            show newb tired at ps_right
            with dissolve
            newb "В рейтинге напротив меня уже красная стрелка. Смешно: система ещё почти ничего обо мне не знает, но ухудшение уже нашла."
            p "Красная стрелка знает только разницу между двумя числами. Она не знает, почему ты остановилась и что успела заметить."
            newb "Значит, придётся говорить громче неё."
            $ ps_newbie_trust += 1
            $ ps_add_route("newbie", 1)
            hide newb

        elif ps_week_route == "veteran":
            show vet concerned at ps_left
            with dissolve
            vet "Раньше на этом участке работал Денис. Быстрый был, пока однажды не решил, что боль в спине можно закрыть обезболивающим и ещё одной сменой."
            p "Что с ним стало?"
            vet "Ушёл. Но не тогда, когда хотел, а когда уже не смог вернуться. Я всё время вспоминаю его только после того, как сам делаю ту же глупость."
            p "Теперь буду напоминать до."
            $ ps_endurance += 1
            $ ps_add_route("veteran", 1)
            hide vet

        elif ps_week_route == "joker":
            show mem serious at ps_left
            with dissolve
            mem "Знаешь, что смешнее рейтинга? Я вчера поднялся на четыре места, потому что человек из соседней смены уволился."
            p "Это вообще не смешно."
            mem "Вот и я не придумал концовку. Ненавижу материал, который работает без меня."
            p "Можно не превращать всё в материал."
            mem "Можно. Но тогда придётся признать, что меня это задело."
            $ ps_humanity += 1
            $ ps_add_route("joker", 1)
            hide mem

        else:
            show sv stern at ps_right
            with dissolve
            sv "Рейтинг считают так, чтобы помощь другому участку выглядела потерей времени. Я могу вручную подтвердить её, если замечу."
            p "А если не заметишь?"
            sv "Значит, человек сделал правильно и получил за это красную стрелку."
            p "Тебя устраивает такой ответ?"
            sv "Нет. Поэтому я показываю тебе, где система врёт ещё до отчёта."
            $ ps_integrity += 1
            $ ps_add_route("supervisor", 1)
            hide sv

    elif day == 4:
        scene bg locker_room
        with fade

        if ps_week_route == "newbie":
            show newb worried at ps_right
            with dissolve
            newb "Они будут задавать вопрос так, будто ответ уже написан: «Почему вы допустили недостачу?» Что мне говорить?"
            menu:
                "Дать Лере говорить самой и остаться рядом":
                    $ ps_newbie_trust += 2
                    $ ps_humanity += 1
                    $ ps_add_route("newbie", 2)
                    p "Начни с того, что видела сама. Я буду рядом и подключусь, если тебя попытаются перебить."
                    newb "Хорошо. Тогда это будет мой ответ, а не твоя защита."
                    $ ps_add_relationship_memory("Ты не заговорил вместо Леры и помог ей защитить себя самой.")
                "Сразу взять разговор на себя":
                    $ ps_newbie_trust += 1
                    $ ps_evidence += 1
                    p "Я объясню цепочку операций. Тебе не придётся отбиваться одной."
                    newb "Спасибо. Только не дай им решить, что я вообще ничего не понимаю."
            hide newb

        elif ps_week_route == "veteran":
            show vet neutral at ps_left
            with dissolve
            vet "Когда-то я подписал похожую бумагу. Не потому что был виноват — просто хотел домой и думал, что одна подпись ничего не изменит."
            p "Изменила?"
            vet "Следующую проверку начали с фразы: «Вы уже признавали нарушения». Бумаги хорошо помнят то, что люди подписывают от усталости."
            p "Сегодня никто не будет спешить домой такой ценой."
            $ ps_integrity += 1
            $ ps_add_route("veteran", 2)
            hide vet

        elif ps_week_route == "joker":
            show mem serious at ps_left
            with dissolve
            mem "Я уже придумал семь шуток про сорок семь пропавших товаров. Ни одну не скажу при Лере."
            p "Почему?"
            mem "Потому что если все засмеются, ей придётся улыбнуться вместе с нами. А потом никто не заметит, что ей страшно."
            p "Ты замечаешь больше, чем показываешь."
            mem "Не распространяй. Репутация пострадает."
            $ ps_team_unity += 1
            $ ps_add_route("joker", 2)
            hide mem

        else:
            show sv stern at ps_right
            with dissolve
            n "Артём показывает тебе готовую служебную записку. В графе причины уже стоит «ошибка сотрудника», хотя разбор ещё не начался."
            sv "Это прислали сверху. От меня ждут подпись до конца смены."
            p "А от Леры — согласие с тем, что уже решили."
            sv "Да."
            p "И что ты сделаешь?"
            sv "Впервые за долгое время не подпишу документ только потому, что так быстрее."
            $ ps_supervisor_respect += 2
            $ ps_add_route("supervisor", 2)
            $ ps_add_relationship_memory("Артём показал тебе документ, который должен был молча подписать.")
            hide sv

    elif day == 5:
        scene bg packing_zone
        with fade

        if ps_week_route == "newbie":
            show newb relief at ps_right
            with dissolve
            newb "Сегодня, если ТСД снова выдаст ошибку, я скажу сама. Не жди, пока начну паниковать."
            p "Что мне делать?"
            newb "Быть рядом. И не забирать терминал, пока я не попрошу."
            p "Принято."
            $ ps_newbie_trust += 2
            $ ps_add_route("newbie", 1)
            hide newb

        elif ps_week_route == "veteran":
            show vet concerned at ps_left
            with dissolve
            vet "Если увидишь, что я снова лезу к подъёмнику вручную, останови. Даже если начну рассказывать, что делал так сто раз."
            p "А ты начнёшь?"
            vet "Обязательно. Опыт очень убедительно оправдывает глупость."
            p "Тогда я тоже буду убедительным."
            $ ps_endurance += 1
            $ ps_add_route("veteran", 1)
            hide vet

        elif ps_week_route == "joker":
            show mem serious at ps_left
            with dissolve
            n "Во время короткой остановки Макс машинально считает людей у линии. На четвёртом сбивается и начинает заново."
            p "Все на месте."
            mem "Знаю. Просто иногда мозг не верит, пока не пересчитает сам."
            p "Давай вместе."
            mem "Четыре человека, один супервайзер и один подозрительно заботливый коллега. Сходится."
            $ ps_team_unity += 1
            $ ps_add_route("joker", 1)
            hide mem

        else:
            show sv neutral at ps_right
            with dissolve
            sv "Сегодня людей меньше, а план оставили прежний. Есть три варианта: спрятать риск, спрятать отставание или честно показать оба."
            p "Третий вариант хотя бы не требует врать."
            sv "Зато требует объяснять. Останешься рядом, когда начнут спрашивать?"
            p "Если решение примешь ты — останусь."
            $ ps_supervisor_respect += 1
            $ ps_add_route("supervisor", 1)
            hide sv

    elif day == 7:
        scene bg warehouse_alert
        with ps_alarm_cut

        if ps_week_route == "newbie":
            show newb relief at ps_right
            with dissolve
            newb "В первый день я смотрела на тебя, потому что не знала, что делать. Сейчас знаю. Но всё равно хочу, чтобы ты был рядом."
            p "Буду. Только решение примем вместе."
            newb "Так даже лучше."
            $ ps_newbie_trust += 1
            hide newb

        elif ps_week_route == "veteran":
            show vet concerned at ps_left
            with dissolve
            vet "Я всю неделю учил тебя вовремя останавливаться. Теперь моя очередь послушать собственный совет."
            p "Справишься?"
            vet "Если начну геройствовать — напомни про старого дурака."
            p "Про какого именно?"
            vet "Вот поэтому ты мне и нравишься."
            $ ps_team_unity += 1
            hide vet

        elif ps_week_route == "joker":
            show mem serious at ps_left
            with dissolve
            mem "Сейчас будет момент, когда мне захочется пошутить и сделать вид, что всё нормально."
            p "Можешь не делать."
            mem "Тогда скажу прямо: мне страшно. Но уходить одному страшнее."
            p "Один и не пойдёшь."
            $ ps_team_unity += 1
            hide mem

        else:
            show sv stern at ps_right
            with dissolve
            sv "Через минуту мне придётся отдать приказ. Если он будет неправильным — останови меня."
            p "При всех?"
            sv "Особенно при всех. Мне больше не нужен человек, который просто подтверждает мои решения."
            p "Тогда говори."
            $ ps_supervisor_respect += 1
            hide sv

    stop motif fadeout 1.0
    with dissolve
    return


################################################################################
## Рабочее взаимодействие: расстановка смены
################################################################################

screen ps_shift_assignment():
    modal True
    zorder 255

    add "bg control_room" at ps_cinematic_background
    add Solid("#07030bd0")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1540
        ysize 850
        padding (55, 42)
        background Solid("#12091ef2")

        vbox:
            spacing 24
            xfill True

            text "РАССТАНОВКА // ЛЮДЕЙ МЕНЬШЕ, ПЛАН ПРЕЖНИЙ":
                color "#e0b5ff"
                size 35
                xalign 0.5

            text "Выбери не красивую схему, а цену, которую смена сможет выдержать.":
                color "#c8b9d3"
                size 22
                xalign 0.5

            hbox:
                spacing 18
                xalign 0.5

                for plan in ps_shift_plan_catalog:
                    button:
                        id ("ps_shift_plan_" + plan["id"])
                        action Return(plan["id"])
                        xsize 445
                        ysize 555
                        padding (28, 26)
                        background Solid("#251532ee")
                        hover_background Solid("#422458")

                        vbox:
                            spacing 18
                            xfill True

                            text plan["title"]:
                                color plan["accent"]
                                size 34
                                xalign 0.5

                            text plan["subtitle"]:
                                color "#ffffff"
                                size 23
                                xalign 0.5
                                text_align 0.5

                            null height 12

                            text plan["detail"]:
                                color "#c6b7cf"
                                size 21
                                text_align 0.0

                            null height 18

                            if plan["id"] == "rotation":
                                text "ЛЮДИ +2  ·  УСТАЛОСТЬ −1  ·  ТЕМП −1":
                                    color "#72d99a"
                                    size 18
                                    xalign 0.5
                            elif plan["id"] == "balanced":
                                text "ТЕМП +2  ·  ЛЮДИ +1  ·  УСТАЛОСТЬ +1":
                                    color "#7fcfff"
                                    size 18
                                    xalign 0.5
                            else:
                                text "ТЕМП +3  ·  ЛЮДИ −1  ·  УСТАЛОСТЬ +2":
                                    color "#ff907f"
                                    size 18
                                    xalign 0.5


label ps_shift_assignment_scene:
    $ ps_set_ambience("control")

    show sv neutral at ps_right
    with dissolve

    sv "В ночной не вышли трое. Куратор план не снял и попросил «распределить ресурс». Я предпочитаю слово «люди»."
    p "Кто где стоит сейчас?"
    sv "Лера на сложной упаковке, Виктор у подъёмника, Макс закрывает два схода. Если ничего не менять, табло будет довольно примерно час."

    call screen ps_shift_assignment
    $ ps_apply_shift_plan(_return)

    if ps_shift_plan == "rotation":
        p "Делаем ротацию. Каждые сорок минут меняемся, сложные позиции никто не тащит всю ночь."
        sv "План просядет на запуске."
        p "Зато через четыре часа у нас всё ещё будут люди, способные его выполнять."
        sv "Записываю причиной снижение риска. Без красивых формулировок."
        $ ps_record_consequence("Ты выбрал ротацию и отказался прятать безопасность за быстрым стартом.")
    elif ps_shift_plan == "balanced":
        p "Расставляем по опыту, но через час проверяем каждого лично. Не по табло."
        sv "Компромисс."
        p "Нет. Просто решение, которое придётся пересмотреть, если люди начнут уставать."
        sv "Хорошо. Через час встречаемся у линии."
        $ ps_record_consequence("Ты распределил смену по опыту и взял на себя повторную проверку людей.")
    else:
        p "Сильных ставим на узкие места. Сначала выбиваем хвост."
        sv "Быстро. И опасно."
        p "Знаю."
        sv "Тогда не делай вид, что цена появилась без нашего решения."
        $ ps_record_consequence("Ты выбрал рывок и сознательно поставил темп выше запаса людей.")

    hide sv
    with dissolve
    $ ps_unlock_cg("shift_plan")
    show screen ps_cinematic_bars
    scene cg shift_plan at ps_cg_reveal
    with ps_violet_cut
    pause 0.9
    hide screen ps_cinematic_bars
    $ ps_unlock_achievement("planner")
    return


################################################################################
## Фиолетовый Шторм вмешивается в обычные сцены
################################################################################

label ps_storm_day_intrusion(day):
    if not ps_storm_fragments:
        return

    if day in ps_storm_intrusions_seen:
        return

    $ ps_storm_intrusions_seen = ps_storm_intrusions_seen + [day]
    $ ps_set_ambience("service")
    $ ps_play_sfx("radio")

    if day == 5:
        $ ps_unlock_cg("monitor_guest")
        show screen ps_cinematic_bars
        scene cg monitor_guest at ps_cg_reveal
        with ps_violet_cut

        n "На одном из мониторов открывается камера упаковки. Изображение отстаёт на несколько секунд: ты видишь, как сам входишь в кадр, хотя стоишь в диспетчерской."
        n "Следом появляется ещё одна фигура в фиолетовой форме. Она идёт рядом, но на настоящей линии проход пуст."

        if ps_route_target() == "supervisor":
            show sv stern at ps_right
            with dissolve
            sv "Эта камера отключена с прошлого месяца."
            p "Тогда кто сейчас смотрит на нас?"
            sv "Не знаю. И впервые не собираюсь писать в отчёте, что это «техническая корректировка»."
            hide sv
        else:
            p "Ты это тоже видишь?"
            n "Человек рядом отвечает не сразу. За это время фигура на экране успевает повернуть голову прямо к камере."

        hide screen ps_cinematic_bars
        $ ps_collect_storm_fragment("camera_guest")
        $ ps_add_relationship_memory("Камера показала лишнего сотрудника рядом с тобой.")

    elif day == 6:
        $ ps_unlock_cg("future_message")
        show screen ps_cinematic_bars
        scene cg future_message at ps_cg_reveal
        with ps_violet_cut

        n "Телефон вибрирует до того, как приходит сообщение. На экране стоит завтрашняя дата и одна строка: «[ps_player_name], не позволяй им запускать линию после общего стопа»."
        n "Через секунду дата становится сегодняшней, а сообщение исчезает из списка. В уведомлениях остаётся только пустое место."

        hide screen ps_cinematic_bars
        $ ps_collect_storm_fragment("future_message")
        $ ps_add_relationship_memory("V-13 прислал предупреждение из времени, которое ещё не наступило.")

    elif day == 7:
        $ ps_unlock_cg("named_shift")
        show screen ps_cinematic_bars
        scene cg named_shift at ps_cg_reveal
        with ps_alarm_cut

        n "Во время общего сбоя табло по очереди выводит имена людей на линии: ЛЕРА. ВИКТОР. МАКС. АРТЁМ."
        n "Последним появляется твоё имя — [ps_player_name]. Под ним не номер участка, а короткое сообщение: «СМЕНА УЗНАЛА ТЕБЯ»."

        if ps_route_target() == "newbie":
            newb "Раньше система видела во мне только ошибку. Почему сейчас она знает наши имена?"
        elif ps_route_target() == "veteran":
            vet "Не отвечай ей. Всё, что зовёт тебя по имени из выключенного табло, может подождать."
        elif ps_route_target() == "joker":
            mem "Я хотел пошутить, но, кажется, оно именно этого и ждёт."
        else:
            sv "Отключаем табло физически. Если система хочет говорить — пусть сначала переживёт выдернутый кабель."

        hide screen ps_cinematic_bars
        $ ps_collect_storm_fragment("named_shift")
        $ ps_unlock_achievement("known_by_storm")

    return
