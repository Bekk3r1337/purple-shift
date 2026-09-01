# -*- coding: utf-8 -*-

################################################################################
## Purple Shift 2.1 - живые маршруты
##
## Отдельный модуль для шестого дня, аварийной развязки и восьми маршрутных
## исходов. Новые сюжетные модули больше не привязаны к номеру версии.
################################################################################

default ps21_route_day6_choice = None
default ps21_route_final_action = None
default ps21_route_outcome = None
default ps21_route_memory = []


init 45 python:
    if getattr(persistent, "ps21_route_outcomes", None) is None:
        persistent.ps21_route_outcomes = []

    ps21_route_outcome_catalog = {
        "newbie:growth": (
            "Свой голос",
            "Лера остановила опасный участок сама, а ты не перехватил у неё рацию.",
        ),
        "newbie:shadow": (
            "Голос напрокат",
            "Лера снова дождалась, пока решение за неё произнесёт кто-то другой.",
        ),
        "veteran:growth": (
            "Опыт остановиться",
            "Виктор передал смене главное правило: боль и перегрев не нужно терпеть до аварии.",
        ),
        "veteran:shadow": (
            "Последний на ногах",
            "Виктор снова стал человеком, которого берегут только после того, как он сломался.",
        ),
        "joker:growth": (
            "Без заготовленной шутки",
            "Макс сначала признал страх, а уже потом помог остальным не поддаться панике.",
        ),
        "joker:shadow": (
            "Ведущий остаётся",
            "Смена услышала шутку и не услышала человека, который её произнёс.",
        ),
        "supervisor:growth": (
            "Решение Артёма",
            "Артём остановил линию от своего имени и сам записал причину в журнал.",
        ),
        "supervisor:shadow": (
            "Так распорядились",
            "Артём снова спрятал своё решение между должностью, приказом и общей подписью.",
        ),
    }

    ps21_achievements = [
        (
            "living_voice",
            "Не должность, а человек",
            "Довести один маршрут до личной развязки в аварии.",
        ),
        (
            "eight_living_routes",
            "Восемь способов измениться",
            "Открыть рост и тень всех четырёх маршрутов.",
        ),
    ]

    known_achievement_ids = {item[0] for item in ps_achievement_catalog}
    for achievement_item in ps21_achievements:
        if achievement_item[0] not in known_achievement_ids:
            ps_achievement_catalog.append(achievement_item)

    def ps21_route_variant(route_id=None):
        route_id = route_id or ps_route_target()
        result_to_variant = {
            "newbie_voice": "growth",
            "newbie_shadow": "shadow",
            "veteran_growth": "growth",
            "veteran_shadow": "shadow",
            "joker_growth": "growth",
            "joker_shadow": "shadow",
            "supervisor_growth": "growth",
            "supervisor_shadow": "shadow",
        }
        if ps2_route_crisis_result in result_to_variant:
            return result_to_variant[ps2_route_crisis_result]

        variant = ps_route_variant(route_id)
        return "growth" if variant == "undecided" else variant

    def ps21_route_outcome_key():
        if ps21_route_outcome:
            return ps21_route_outcome
        return "{}:{}".format(ps_route_target(), ps21_route_variant())

    def ps21_route_outcome_data():
        return ps21_route_outcome_catalog.get(
            ps21_route_outcome_key(),
            ("Маршрут продолжается", "Последствие ещё не определилось."),
        )

    def ps21_unlock_route_outcome(outcome_key):
        outcomes = list(persistent.ps21_route_outcomes or [])
        if outcome_key not in outcomes:
            outcomes.append(outcome_key)
            persistent.ps21_route_outcomes = outcomes
            renpy.save_persistent()

        ps_unlock_achievement("living_voice")
        if len(outcomes) >= len(ps21_route_outcome_catalog):
            ps_unlock_achievement("eight_living_routes")


screen ps21_route_result_card():
    modal True
    zorder 305

    $ ps21_result_title, ps21_result_description = ps21_route_outcome_data()

    add Solid("#030105e8")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1180
        padding (62, 48)
        background Solid("#170c22f7")

        vbox:
            spacing 20
            xfill True

            text "ЛИЧНАЯ РАЗВЯЗКА":
                color "#aa82cf"
                size 22
                kerning 4
                xalign 0.5

            text ps21_result_title:
                color "#ffffff"
                size 46
                xalign 0.5

            text ps21_result_description:
                color "#d2c6d9"
                size 25
                xalign 0.5
                text_align 0.5
                xmaximum 980

            textbutton "ПРОДОЛЖИТЬ":
                id "ps21_route_result_continue"
                action Return(True)
                xalign 0.5
                xsize 360
                ysize 66
                background Solid("#72409d")
                hover_background Solid("#9a61d2")
                text_color "#ffffff"
                text_size 23


################################################################################
## Шестой день: личный разговор вместо короткой проверки показателей
################################################################################

label ps21_route_night_scene:
    $ ps21_route = ps_route_target()
    $ ps21_route_day6_choice = None

    scene bg break_room
    with fade

    if ps21_route == "newbie":
        show newb determined at ps_center
        with dissolve

        newb "Я весь день ждала удобного момента сказать про линию. Потом поняла: если станет опасно, удобного момента уже не будет."
        p "Что ты хочешь сделать завтра?"
        newb "Сказать «стоп» сразу. И не смотреть на Артёма, чтобы понять, разрешили мне или нет."

        menu:
            "Договориться, что она останавливает участок сама":
                $ ps21_route_day6_choice = "voice"
                $ ps2_route_crisis_result = "newbie_voice"
                $ ps2_apply(ps_newbie_trust=2, ps2_team_trust=2, ps2_resolve=1)
                $ ps_record_route_tendency("newbie", "growth", 2, "Лера попросила не разрешение, а поддержку рядом.")
                $ ps2_record_decision(6, "после смены", "lera_voice", "Не перехватывать рацию", "Лера готовится остановить опасную линию своим решением.")
                p "Хорошо. Ты называешь причину и даёшь стоп. Я проверяю, чтобы команду услышали."
                newb "Вот. Так нормально. Рядом, а не вместо меня."

            "Пообещать, что завтра всё скажешь за неё":
                $ ps21_route_day6_choice = "cover"
                $ ps2_route_crisis_result = "newbie_shadow"
                $ ps2_apply(ps_newbie_trust=1, ps2_team_fear=1, ps2_team_fracture=1)
                $ ps_record_route_tendency("newbie", "shadow", 2, "Ты снова стал голосом Леры вместо неё самой.")
                $ ps2_record_decision(6, "после смены", "lera_cover", "Говорить за Леру", "Завтрашнее решение снова зависит от того, окажешься ли ты рядом.")
                p "Если что-то начнётся, сразу зови меня. Я разберусь с Артёмом и куратором."
                newb "А если тебя отправят в другой сектор? Ладно. Завтра разберёмся."

        hide newb

    elif ps21_route == "veteran":
        show vet injured at ps_center
        with dissolve

        vet "Перчатка сегодня не виновата. Я ещё утром понял, что кисть не держит нагрузку. Просто решил дотянуть. По старой привычке."
        p "До чего? До конца смены или до медпункта на погрузчике?"
        vet "Вот за такие вопросы я новичков и не люблю. Быстро учитесь."

        menu:
            "Попросить Виктора завтра самому объявить предел":
                $ ps21_route_day6_choice = "teach_stop"
                $ ps2_route_crisis_result = "veteran_growth"
                $ ps2_apply(ps_endurance=1, ps2_team_aid=2, ps2_team_trust=1)
                $ ps_record_route_tendency("veteran", "growth", 2, "Виктор согласился показать команде, когда работу нужно остановить.")
                $ ps2_record_decision(6, "после смены", "victor_stop", "Передать опыт остановки", "Виктор больше не выдаёт терпение за единственный профессиональный навык.")
                p "Завтра твой опыт нужен не для того, чтобы терпеть дольше всех. Скажи нам первым, когда хватит."
                vet "С непривычки могу сказать слишком рано."
                p "Переживём семь минут простоя. Вторую руку тебе никто не выдаст."

            "Сказать, что без него смена всё равно не справится":
                $ ps21_route_day6_choice = "pillar"
                $ ps2_route_crisis_result = "veteran_shadow"
                $ ps2_apply(ps_endurance=2, ps2_team_fear=1, ps2_fatigue=1)
                $ ps_record_route_tendency("veteran", "shadow", 2, "Команда снова попросила Виктора быть крепче собственного тела.")
                $ ps2_record_decision(6, "после смены", "victor_pillar", "Оставить Виктора опорой", "Виктор выйдет в финальную смену с больной рукой, потому что остальные рассчитывают на него.")
                p "Завтра без тебя будет хуже. Хотя бы помоги пройти последний день."
                vet "Помогу. Только потом не удивляйся, почему старики молчат о боли. Нас обычно спрашивают совсем о другом."

        hide vet

    elif ps21_route == "joker":
        show mem open at ps_center
        with dissolve

        mem "Я сегодня три раза пошутил про подъёмник. Один раз даже смешно. А потом понял, что не помню, что хотел сказать до шутки."
        p "Попробуй сейчас. Зрителей нет."
        mem "Мне страшно, что завтра начнётся паника, и все опять посмотрят на меня: ну давай, развлекай."

        menu:
            "Договориться: сначала честная фраза, потом юмор":
                $ ps21_route_day6_choice = "honest_first"
                $ ps2_route_crisis_result = "joker_growth"
                $ ps2_apply(ps_humanity=1, ps2_team_trust=2, ps2_resolve=1)
                $ ps_record_route_tendency("joker", "growth", 2, "Макс разрешил себе говорить серьёзно, не отказываясь от юмора.")
                $ ps2_record_decision(6, "после смены", "max_honest", "Сначала сказать честно", "В финальной смене Макс попробует назвать страх до того, как превратит его в шутку.")
                p "Если станет страшно, так и говоришь. Потом можешь украсть мою реплику и спасти эфир."
                mem "Отвратительный план. Слишком мало возможностей спрятаться за харизмой."

            "Попросить его любой ценой удержать настроение":
                $ ps21_route_day6_choice = "keep_show"
                $ ps2_route_crisis_result = "joker_shadow"
                $ ps2_apply(ps_humor=2, ps2_team_fear=-1, ps2_team_fracture=1)
                $ ps_record_route_tendency("joker", "shadow", 2, "Ты попросил Макса снова сыграть ведущего, даже если ему самому станет страшно.")
                $ ps2_record_decision(6, "после смены", "max_show", "Не останавливать выступление", "Команда получит привычного Макса. На разговор с настоящим снова не останется времени.")
                p "Если все поплывут, вытащи их шуткой. Ты умеешь."
                mem "Умею. Записываю: человек временно недоступен, ведущий работает без выходных."

        hide mem

    else:
        show sv conflicted at ps_center
        with dissolve

        sv "Морозов завтра будет на связи лично. Если участок встанет, решение запишут на меня. Не на регламент и не на общий чат."
        p "Тебя пугает остановка или то, что нельзя будет сослаться на приказ?"
        sv "Оба варианта. Второй сильнее, чем хотелось бы."

        menu:
            "Потребовать, чтобы он назвал решение своим":
                $ ps21_route_day6_choice = "own_name"
                $ ps2_route_crisis_result = "supervisor_growth"
                $ ps2_apply(ps_supervisor_respect=2, ps_integrity=1, ps2_team_trust=1)
                $ ps_record_route_tendency("supervisor", "growth", 2, "Артём согласился отвечать за решение собственным именем.")
                $ ps2_record_decision(6, "после смены", "artem_name", "Решение от своего имени", "В аварии Артём не сможет спрятать выбор внутри формулировки «так распорядились».")
                p "Тогда завтра говоришь прямо: «Я остановил линию, потому что людям было опасно». Без «нам поручили»."
                sv "И если ошибусь, это тоже будет моё. Понял."

            "Предложить общую подпись, чтобы разделить удар":
                $ ps21_route_day6_choice = "shared_cover"
                $ ps2_route_crisis_result = "supervisor_shadow"
                $ ps2_apply(ps_team_unity=1, ps2_team_aid=1, ps2_team_fracture=1)
                $ ps_record_route_tendency("supervisor", "shadow", 2, "Общая подпись снова позволила Артёму не называть собственное решение.")
                $ ps2_record_decision(6, "после смены", "artem_cover", "Спрятаться в общей подписи", "У Артёма появился союзник, но не появилась личная ответственность.")
                p "Запишем решение общим. Если начнут искать виноватого, подпишусь рядом."
                sv "Так проще провести документ. И проще потом не помнить, кто на самом деле решил."

        hide sv

    $ ps21_route_memory = ps21_route_memory + ["Шестой день: {}".format(ps21_route_day6_choice)]
    return


################################################################################
## Седьмой день: маршрут меняет саму аварийную сцену
################################################################################

label ps21_route_finale_setup:
    $ ps21_route = ps_route_target()
    $ ps21_variant = ps21_route_variant(ps21_route)

    if ps21_route == "newbie":
        show newb determined at ps_right
        with dissolve
        if ps21_variant == "growth":
            newb "Рацию беру я. Если датчик снова уйдёт в красное, называю сектор и останавливаю его сразу."
            p "Я рядом. Команду не забираю."
        else:
            newb "Скажи только заранее, где тебя искать. Я не хочу снова бегать по складу за человеком, который может разрешить мне остановку."
        hide newb

    elif ps21_route == "veteran":
        show vet injured at ps_left
        with dissolve
        if ps21_variant == "growth":
            vet "Правая лента греется ещё до запуска. Я отмечу температуру и не дам вам спорить с датчиком."
        else:
            vet "Руку забинтовал. Не смотри так. Последний день доработаю, а там разберёмся."
        hide vet

    elif ps21_route == "joker":
        show mem open at ps_center
        with dissolve
        if ps21_variant == "growth":
            mem "План такой: если мне страшно, я говорю, что мне страшно. Потом уже импровизирую. Ты свидетель этого безумия."
        else:
            mem "Сегодня я снова отвечаю за моральный дух. Свой моральный дух принесу в следующем обновлении."
        hide mem

    else:
        show sv conflicted at ps_left
        with dissolve
        if ps21_variant == "growth":
            sv "Журнал открыт на моём имени. Если дам стоп, запись останется моей. Ничего не исправляй потом."
        else:
            sv "Я подготовил общий протокол. Если придётся остановиться, решение будет коллективным. Формально."
        hide sv

    return


label ps21_route_emergency_payoff:
    $ ps21_route = ps_route_target()
    $ ps21_route_final_action = None

    if ps_final_choice == "уйти":
        $ ps21_route_final_action = "walked_out"
        $ ps21_route_outcome = "{}:{}".format(ps21_route, ps21_route_variant(ps21_route))
        n "У проходной телефон вибрирует один раз. Сообщение приходит от человека, с которым ты провёл больше всего времени за эту неделю. Ты не отвечаешь на ходу, но и не удаляешь его."
        call screen ps21_route_result_card
        return

    if ps21_route == "newbie":
        show newb determined at ps_right
        with dissolve
        newb "Дальний сход снова принимает коробки после стопа. Там двое, рация у меня. Решаем сейчас."
        menu:
            "Оставить команду Лере и прикрыть эвакуацию":
                $ ps21_route_final_action = "own_voice"
                $ ps21_route_outcome = "newbie:growth"
                $ ps2_apply(ps_newbie_trust=2, ps_team_unity=1, ps2_team_trust=1)
                $ ps_record_route_tendency("newbie", "growth", 2)
                newb "Дальний сход, стоп. Два человека выходят через погрузку. Повторяю: это Лера, я останавливаю сектор."
                n "Её слышат с первого раза. Ты остаёшься у прохода и считаешь тех, кто выходит."

            "Забрать рацию и отдать команду самому":
                $ ps21_route_final_action = "borrowed_voice"
                $ ps21_route_outcome = "newbie:shadow"
                $ ps2_apply(ps_newbie_trust=-1, ps2_team_fear=1, ps2_team_fracture=1)
                $ ps_record_route_tendency("newbie", "shadow", 2)
                p "Дай сюда. Дальний сход, немедленный стоп!"
                n "Команду выполняют. Лера молча проверяет людей и больше не просит рацию обратно."
        hide newb

    elif ps21_route == "veteran":
        show vet injured at ps_left
        with dissolve
        vet "Температура правого привода растёт. Ещё минута, и стоп будет уже не нашим решением."
        menu:
            "Доверить Виктору объявить техническую остановку":
                $ ps21_route_final_action = "teach_limit"
                $ ps21_route_outcome = "veteran:growth"
                $ ps2_apply(ps_endurance=1, ps_integrity=1, ps2_team_aid=2)
                $ ps_record_route_tendency("veteran", "growth", 2)
                vet "Правый привод - стоп. Причина: перегрев. Время записал. Никто туда не возвращается до проверки."
                n "Он не добавляет привычное «я посмотрю сам». Вместо этого передаёт ключ блокировки Артёму."

            "Попросить Виктора отключить привод вручную":
                $ ps21_route_final_action = "last_pillar"
                $ ps21_route_outcome = "veteran:shadow"
                $ ps2_apply(ps_endurance=1, ps_burnout=2, ps2_team_fear=1)
                $ ps_record_route_tendency("veteran", "shadow", 2)
                p "Ты знаешь шкаф лучше всех. Отключи вручную, пока автоматика не вернулась."
                vet "Знаю. Поэтому опять иду я."
                n "Он прячет больную кисть под второй перчаткой и уходит к приводу."
        hide vet

    elif ps21_route == "joker":
        show mem open at ps_center
        with dissolve
        mem "На дальнем секторе люди не двигаются. Я могу пошутить, но сначала честно: я сам сейчас еле соображаю."
        menu:
            "Принять честность и вместе дать простые команды":
                $ ps21_route_final_action = "person_first"
                $ ps21_route_outcome = "joker:growth"
                $ ps2_apply(ps_humanity=1, ps_humor=1, ps2_team_trust=2)
                $ ps_record_route_tendency("joker", "growth", 2)
                p "Тогда без выступления. Считаем вслух и выводим по двое."
                mem "Спасибо. А шутку оставим для автобуса, если он опять не придёт."

            "Попросить Макса срочно разрядить панику":
                $ ps21_route_final_action = "host_first"
                $ ps21_route_outcome = "joker:shadow"
                $ ps2_apply(ps_humor=2, ps2_team_fear=-1, ps2_team_fracture=1)
                $ ps_record_route_tendency("joker", "shadow", 2)
                p "Они тебя слушают. Сделай что-нибудь, пока страх не разошёлся дальше."
                mem "Добро пожаловать на экскурсию «Как выйти со склада раньше плана». Проходим по двое и не теряем экскурсовода."
                n "Люди двигаются. Макс улыбается ровно до тех пор, пока последний не проходит мимо."
        hide mem

    else:
        show sv conflicted at ps_left
        with dissolve
        sv "Морозов требует вернуть линию. Решение об остановке ещё можно записать как общий технический сбой."
        menu:
            "Попросить Артёма оставить в журнале своё решение":
                $ ps21_route_final_action = "own_decision"
                $ ps21_route_outcome = "supervisor:growth"
                $ ps2_apply(ps_supervisor_respect=2, ps_integrity=2, ps2_team_trust=1)
                $ ps_record_route_tendency("supervisor", "growth", 2)
                sv "Записываю: «Я, Артём Волков, остановил участок из-за угрозы людям». Время и датчики приложены."
                cur "Волков, ты понимаешь, что подписываешь?"
                sv "Теперь - да."

            "Согласиться оформить решение как коллективное":
                $ ps21_route_final_action = "shared_excuse"
                $ ps21_route_outcome = "supervisor:shadow"
                $ ps2_apply(ps_team_unity=1, ps_integrity=-1, ps2_team_fracture=2)
                $ ps_record_route_tendency("supervisor", "shadow", 2)
                p "Пиши общим. Сейчас не время подставляться одному."
                sv "«Коллективное решение в условиях отсутствия связи». Удобно: ни одного имени и ни одного виноватого."
        hide sv

    $ ps21_route_memory = ps21_route_memory + ["Финал: {}".format(ps21_route_final_action)]
    call screen ps21_route_result_card
    return


################################################################################
## Восемь коротких, но самостоятельных маршрутных эпилогов
################################################################################

label ps21_route_epilogue:
    $ ps21_outcome = ps21_route_outcome_key()
    $ ps21_unlock_route_outcome(ps21_outcome)

    if ps21_outcome == "newbie:growth":
        show newb determined at ps_center
        with dissolve
        n "Через неделю Лера присылает фотографию нового журнала остановок. Первая запись сделана её рукой. В графе «кто дал команду» стоит фамилия без исправлений."
        newb "Меня потом трясло минут двадцать. Но в следующий раз я хотя бы знаю, что голос работает."
        hide newb

    elif ps21_outcome == "newbie:shadow":
        show newb tired at ps_center
        with dissolve
        n "Лера переводится на соседний участок и первым делом спрашивает, кто там имеет право дать стоп. Твоего имени в списке нет."
        newb "Я справлюсь. Просто сначала пойму, к кому бежать, если что."
        hide newb

    elif ps21_outcome == "veteran:growth":
        show vet injured at ps_center
        with dissolve
        n "Виктор приходит без рабочей формы и проводит короткий разбор для смены. На доске всего три пункта: температура, боль и право остановиться."
        vet "Если опыт учит только терпеть, это плохой опыт. Можете записать, я второй раз не повторю."
        hide vet

    elif ps21_outcome == "veteran:shadow":
        show vet concerned at ps_center
        with dissolve
        n "Виктор отвечает на сообщения коротко. Рука восстанавливается медленнее, чем он обещал. В чате уже спрашивают, когда он вернётся и снова возьмёт тяжёлый сектор."
        hide vet

    elif ps21_outcome == "joker:growth":
        show mem open at ps_center
        with dissolve
        n "Макс присылает голосовое без музыки и монтажа. Первые десять секунд он просто дышит, потом рассказывает, что записался к врачу из-за бессонницы. В конце всё-таки шутит. На этот раз не вместо разговора."
        hide mem

    elif ps21_outcome == "joker:shadow":
        show mem grin at ps_center
        with dissolve
        n "В общем чате появляется новый мем про аварийную кнопку. Его пересылают даже из дневной смены. На личное сообщение Макс отвечает реакцией и больше ничего не пишет."
        hide mem

    elif ps21_outcome == "supervisor:growth":
        show sv conflicted at ps_center
        with dissolve
        n "Артёма снимают со смены на время проверки, но его запись остаётся в журнале. Он не просит удалить фамилию и не заменяет «я остановил» на безличное «произошла остановка»."
        sv "Должность могут вернуть. Решение уже не отмотаешь, и это нормально."
        hide sv

    else:
        show sv stern at ps_center
        with dissolve
        n "В итоговом протоколе двадцать три строки и ни одного имени. Артём получает копию, читает её дважды и отправляет в архив без комментария."
        hide sv

    return
