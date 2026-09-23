# -*- coding: utf-8 -*-

################################################################################
## Глава 3. День третий - Чужие цифры
################################################################################

label chapter3_day_three:
    $ ps_chapter = 3
    $ ps_begin_day(3)

    scene black
    with fade

    call screen ps_day_card(
        3,
        _("Чужие цифры"),
        _("На табло считают скорость. Из журнала исчезла вчерашняя остановка.")
    )

    call ps_show_consequence_echo(3)
    call ps2_pre_shift(3)

    scene bg warehouse_outside
    with dissolve

    $ ps_play_ost("walk_to_shift", fadein=2.0)

    n "На третий день ты проходишь знакомый поворот, переход и серую дверь почти не глядя. Только у входа вспоминаешь вчерашнее сообщение."

    if ps_supervisor_respect >= 4:
        n "В телефоне всё ещё лежит файл «Чек-лист старшего линии». Сорок семь пунктов: запуск, остановка, отчёты, штрафы. Про разговор с испуганным человеком - ничего."
    elif ps_newbie_trust >= 4:
        n "Лера уже отметилась в приложении. Рядом с её именем зелёная точка: сегодня она пришла раньше тебя."
    elif ps_efficiency >= 7:
        n "Фиолетовая кнопка дополнительной смены всё ещё горит. Под ней обещают повышающий коэффициент, но точной суммы нет."
    else:
        n "Неизвестный номер больше не писал. Ты перечитал фразу «Это не первый раз» уже трижды."

    scene bg locker_room
    with fade

    stop music fadeout 1.5
    $ ps_play_ost("after_shift", fadein=2.0)

    show mem grin at ps_left
    with dissolve

    mem "Третий день. Поздравляю: теперь ты достаточно опытный, чтобы обучать тех, кто пришёл пять минут назад."

    p "А сам?"

    mem "Я слишком ценный специалист. Меня берегут от ответственности."

    show vet warm at ps_right
    with dissolve

    vet "Не слушай. Его от ответственности уже ничего не спасёт."

    n "Виктор задерживается рядом, пока Макс убирает вещи в шкафчик."

    if ps_second_shift_path == "выбрал цифры":
        vet "Про контейнер думал?"
        p "Думал."
        vet "Хорошо. Значит, не зря упал."
    else:
        vet "После вчерашнего тебя будут проверять."
        p "За то, что сделал правильно?"
        vet "За самовольную остановку. Правильной её назовут, только если это удобно в отчёте."

    hide mem
    hide vet
    with dissolve

    show sv neutral at ps_center
    with dissolve

    sv "Перед запуском - минута внимания. В конце недели закрывают месячный рейтинг. Лучший показатель получит премию и отметку «Сотрудник месяца»."

    n "На стене загорается экран с фамилиями, процентами и зелёными или красными стрелками."

    sv "Скорость, ошибки, соблюдение операций - считается всё."

    mem "Кроме желания жить."

    sv "Оно в KPI не входит."

    n "Твоё имя появляется в нижней части списка. В графах пока прочерки: двух смен для рейтинга мало."

    if ps_efficiency >= 7:
        sv "У тебя хороший старт. Не испорть."
    elif ps_humanity >= 7:
        sv "Ты часто отвлекаешься на чужие участки. В рейтинге помощь не всегда видна."
    else:
        sv "Неделя покажет."

    hide sv
    with dissolve

    call ps_exploration_phase(3, 1)
    call ps_run_inspection("control_scan")
    call ps_route_week_scene(3)
    call ps_route_turning_point(3)
    call ps_team_conflict_scene(3)
    call ps_shift_micro_event(3)
    call ps2_shift_event(3)
    call ps2_storm_echo(3)

    if persistent.ps_reduce_motion:
        scene bg mezzanine
    else:
        scene bg mezzanine at ps_camera_drift
    with fade

    stop music fadeout 1.5
    $ ps_play_ost("cold_line", fadein=2.0)
    $ ps_set_ambience("warehouse")

    n "Линия запускается. Третий день начинается с обычного звука."

    $ ps_play_sfx("scan_ok")

    n "Пиип. Система выдаёт контрольную серию: шесть товаров, тридцать секунд, каждая ошибка отнимает время."

    $ ps_sort_start()
    call screen ps_sort_challenge
    $ ps_sort_result = _return

    if ps_sort_result[0] == len(ps_sort_items) and ps_sort_result[1] == 0:
        $ ps_efficiency += 2
        $ ps_unlock_achievement("clean_sort")
        $ ps_key_choices = ps_key_choices + [_("Ты прошёл контрольную серию ТСД без пересорта.")]
        n "Последний товар уходит в правильный сектор. Шесть из шести. Экран на секунду становится зелёным."
    elif ps_sort_result[0] >= 4:
        $ ps_efficiency += 1
        n "Серия закрывается с огрехами, но очередь не успевает тебя догнать."
    else:
        $ ps_endurance += 1
        $ ps_burnout += 1
        n "Таймер обнуляется раньше последнего товара. ТСД возвращает остаток в очередь и добавляет две ошибки в статистику."

    n "После контрольной серии ТСД не возвращается к товару. На экране появляется запись вчерашнего инцидента."

    call screen ps_tsd_alert(
        "LOG-00",
        _("ЗАПИСЬ ОБ ОСТАНОВКЕ НЕ НАЙДЕНА"),
        _("Событие STOP-04 отсутствует в журнале участка.")
    )

    n "Ты обновляешь экран. Ничего. Вчера коробки падали на пол, а в журнале смена закрыта без происшествий."

    show newb worried at ps_right
    with dissolve

    newb "Ты тоже это видишь?"

    p "Вижу."

    if ps_second_shift_path == "остановил линию":
        newb "Но ты нажимал кнопку. Она должна была записаться."
    elif ps_second_shift_path == "собрал команду":
        newb "Мы все там были. Почему написано, что ничего не случилось?"
    else:
        newb "Коробки упали. Я их потом собирала."

    show vet neutral at ps_left
    with dissolve

    vet "Потому что с происшествием показатели хуже. Запись убрали - отчёт снова чистый."

    p "Ты знал?"

    vet "Я видел такое."

    n "Телефон в кармане коротко вибрирует. Неизвестный номер:"
    n "«Открой архив операций. Смена 02:14. Пока его тоже не почистили»."

    menu:
        "Сфотографировать журнал и открыть архив":
            $ ps_third_day_path = "сохранил журнал"
            $ ps_evidence += 2
            $ ps_integrity += 2
            $ ps_key_choices = ps_key_choices + [_("Ты сохранил исчезнувшую запись об опасном контейнере.")]

            n "Ты делаешь снимок экрана. Потом ещё один. В архиве находится строка STOP-04. Время совпадает. Статус: «Удалено оператором участка»."

            newb "Теперь это хотя бы не исчезнет совсем."
            vet "Скинь копию куда-нибудь ещё. Рабочий телефон могут попросить показать."

        "Сразу позвать супервайзера":
            $ ps_third_day_path = "потребовал объяснение"
            $ ps_integrity += 2
            $ ps_supervisor_respect += 1
            $ ps_evidence += 1
            $ ps_key_choices = ps_key_choices + [_("Ты потребовал объяснить исчезновение записи.")]

            p "Событие удалено. Кем и почему?"

            show sv neutral at ps_center
            with dissolve

            sv "Техническая корректировка."

            p "Контейнер тоже был технической корректировкой?"

            n "Артём переводит взгляд с Виктора на Леру, потом снова на тебя."

            sv "Работайте. После смены проверю."

            hide sv
            with dissolve

            vet "Теперь он знает, что ты заметил."
            p "Это плохо?"
            vet "Смотря кто удалил запись."

        "Закрыть журнал и сосредоточиться на рейтинге":
            $ ps_third_day_path = "выбрал рейтинг"
            $ ps_efficiency += 3
            $ ps_integrity -= 2
            $ ps_burnout += 1
            $ ps_key_choices = ps_key_choices + [_("Ты закрыл пропавшую запись ради места в рейтинге.")]

            n "Ты закрываешь окно. На его месте появляется очередь товаров. Зелёная цифра растёт."

            newb "И всё?"

            p "У нас работа."

            n "Она медленно кивает. Виктор смотрит на тебя, затем молча возвращается к своей ячейке."

    hide newb
    hide vet
    with dissolve

    n "К середине смены таблицу обсуждают на каждом участке. Одни обновляют её каждые пять минут. Другие говорят, что им всё равно, и проверяют ещё чаще."

    show mem grin at ps_left
    with dissolve

    mem "Ты уже на четырнадцатом месте. Ещё немного - и твою фотографию повесят там, где никто не смотрит."

    menu:
        "Ускориться и войти в первую десятку":
            $ ps_efficiency += 2
            $ ps_endurance -= 1
            $ ps_burnout += 1

            p "Попробую войти в десятку."
            n "Ты сокращаешь паузы. Пропускаешь воду. К концу часа твоё имя поднимается на девятое место."
            mem "Поздравляю. Теперь тебя официально можно эксплуатировать эффективнее."

        "Держать ровный темп и следить за людьми":
            $ ps_humanity += 2
            $ ps_team_unity += 1

            p "Останусь в своём темпе."
            n "Ты не попадаешь в десятку. Зато дважды ловишь чужую ошибку до того, как она становится проблемой."

        "Объявить таблице личную войну шутками":
            $ ps_humor += 2
            $ ps_team_unity += 1

            p "Предлагаю новый показатель. Кто дольше всех смотрел на рейтинг и не заплакал."
            mem "Я снимаюсь. У меня непереносимость управленческой аналитики."
            n "Смеются даже с соседней линии. Кто-то наконец закрывает таблицу на общем экране."

    hide mem
    with dissolve

    n "Под конец смены ТСД снова вибрирует."

    call screen ps_tsd_alert(
        "RATE-03",
        _("РЕЙТИНГ ОБНОВЛЁН"),
        _("До закрытия периода осталось четыре дня.")
    )

    n "До закрытия периода четыре дня. Твоё имя уже появилось в таблице, а запись о падающем контейнере из журнала исчезла."

    call ps2_after_shift(3)

    call screen ps_shift_report(
        _("Итоги третьего дня"),
        _("Третий день закончен. У тебя есть выбор - хранить копию записи или сделать вид, что её не было.")
    )

    $ ps_stop_ambience()
    jump chapter4_day_four


################################################################################
## Глава 4. День четвёртый - Чужая ошибка
################################################################################

label chapter4_day_four:
    $ ps_chapter = 4
    $ ps_begin_day(4)

    scene black
    with fade

    call screen ps_day_card(
        4,
        _("Чужая ошибка"),
        _("В системе недостача. В объяснительной уже напечатано имя Леры.")
    )

    call ps_show_consequence_echo(4)

    scene bg room_morning
    with dissolve

    $ ps_play_ost("before_shift", fadein=2.0)

    n "Сообщение Леры будит тебя раньше будильника."

    newb "Меня вызывают раньше. Пишут, что вчера на моём аккаунте недостача. Сорок семь единиц."

    n "Сорок семь - то же число, что было в удалённом журнале."

    if ps_evidence >= 2:
        n "На сохранённом снимке архива сбой привязки начинается сразу после удаления STOP-04."
    else:
        n "Ты помнишь этот экран, но снимка у тебя нет."

    menu:
        "Ответить: «Ничего не подписывай без меня»":
            $ ps_humanity += 2
            $ ps_newbie_trust += 2
            $ ps_team_unity += 1
            p "Ничего не подписывай. Я скоро буду."
            newb "Хорошо."
            n "Лера отвечает сразу. Следом присылает фотографию объяснительной."

        "Попросить её прислать номер операции":
            $ ps_efficiency += 2
            $ ps_evidence += 1
            p "Пришли номер операции и время. Проверим цепочку."
            newb "Сейчас."
            n "Через минуту она присылает номер, время и снимок объяснительной."

        "Посоветовать самой поговорить с супервайзером":
            $ ps_endurance += 1
            $ ps_newbie_trust -= 1
            $ ps_burnout += 1
            p "Поговори с супервайзером. Я не могу решать всё."
            newb "Да. Конечно."
            n "Лера больше ничего не пишет."

    call ps2_pre_shift(4)

    scene bg locker_room
    with fade

    stop music fadeout 1.5
    $ ps_play_ost("after_shift", fadein=2.0)

    show newb worried at ps_left
    show sv neutral at ps_right
    with dissolve

    sv "Сорок семь единиц прошли под твоим аккаунтом. Ячейка назначения пустая."

    newb "У меня завис ТСД."

    sv "У всех зависает. Недостача почему-то одна."

    n "На столе лежит бланк объяснительной. Причину уже напечатали за Леру: «Ошибка допущена по невнимательности сотрудника»."

    if ps_evidence >= 2:
        n "В твоём телефоне есть другая версия событий."

    menu:
        "Показать архив и защищать новичка":
            $ ps_fourth_day_path = "защитил новичка"
            $ ps_humanity += 3
            $ ps_integrity += 2
            $ ps_newbie_trust += 2
            $ ps_team_unity += 2
            $ ps_key_choices = ps_key_choices + [_("Ты не позволил списать системную ошибку на новичка.")]

            p "Вот номер операции. Она прошла сразу после того, как из журнала удалили STOP-04."

            if ps_evidence >= 2:
                p "И вот снимок архива."
                n "Артём долго смотрит на экран."
                sv "Откуда это у тебя?"
                p "Из системы."
                sv "Я вижу. Спрашиваю - зачем сохранил?"
                p "Потому что запись уже один раз удалили."
                $ ps_supervisor_respect += 1
                $ ps_evidence += 1
            else:
                sv "Слов недостаточно."
                p "Тогда проверьте резервный журнал."
                n "Артём ничего не отвечает, но бланк отодвигает."

            sv "Объяснительную пока не подписываем. Я подниму операции."
            newb "Спасибо."

        "Молча восстановить цепочку операций":
            $ ps_fourth_day_path = "нашёл ошибку системы"
            $ ps_efficiency += 3
            $ ps_evidence += 2
            $ ps_integrity += 1
            $ ps_newbie_trust += 1
            $ ps_supervisor_respect += 1
            $ ps_key_choices = ps_key_choices + [_("Ты восстановил цепочку и нашёл настоящую причину недостачи.")]

            p "Дайте ТСД."
            n "Ты открываешь историю. Сверяешь время. Сорок семь товаров ушли в буферную ячейку. После ночной перезагрузки она перестала отображаться."

            p "Товары на месте. Пропала ссылка на ячейку."

            sv "Уверен?"

            p "Откройте буфер B-04."

            n "Через минуту приходит подтверждение. Все сорок семь единиц на месте."

            sv "Хорошая работа."
            newb "То есть… я ничего не потеряла?"
            p "Нет."
            p "Нет. Можешь выдохнуть."

        "Не вмешиваться и сохранить место в рейтинге":
            $ ps_fourth_day_path = "оставил виноватой"
            $ ps_efficiency += 2
            $ ps_integrity -= 3
            $ ps_newbie_trust -= 3
            $ ps_team_unity -= 1
            $ ps_supervisor_respect += 1
            $ ps_key_choices = ps_key_choices + [_("Ты позволил системе назначить виноватую.")]

            n "Ты остаёшься у двери. Бланк шуршит, когда Лера берёт ручку."

            newb "Мне написать, что я была невнимательна?"

            sv "Если не можешь объяснить иначе."

            n "Она смотрит на тебя, ожидая хоть слова. Ты переводишь взгляд на рейтинг: твоё имя поднялось ещё на одну строку."

    hide newb
    hide sv
    with dissolve

    call ps_exploration_phase(4, 1)
    call ps_run_inspection("packing_scan")
    call ps_route_week_scene(4)
    call ps_reactive_echo_scene(4)
    call ps_team_conflict_scene(4)
    call ps_human_shift_scene(4)
    call ps2_shift_event(4)
    call ps2_storm_echo(4)

    scene bg warehouse_cold
    with fade

    stop music fadeout 1.5
    $ ps_play_ost("cold_line", fadein=2.0)
    $ ps_set_ambience("warehouse")

    n "К началу смены про сорок семь единиц знают уже на соседнем участке. Каждый пересказывает историю немного по-своему."

    n "Через два часа ТСД разрешает десятиминутный перерыв. Сегодня ты впервые сам выбираешь, с кем его провести."

    scene bg break_room
    with dissolve

    $ ps_set_ambience("quiet")
    $ ps_unlock_cg("breakroom_preconflict")

    show screen ps_cinematic_bars
    scene cg breakroom_preconflict at ps_cg_reveal
    with dissolve
    n "В комнате отдыха все оказываются за одним столом. Никто не спорит, но пауза между фразами уже звучит как начало разговора."
    scene bg break_room
    with dissolve
    hide screen ps_cinematic_bars

    call screen ps_break_choice
    $ ps_break_target = _return

    if ps_break_target == "newbie":
        $ ps_humanity += 1
        $ ps_newbie_trust += 2
        $ ps_team_unity += 1

        show newb neutral at ps_enter_right
        with dissolve

        p "Как ты?"

        if ps_fourth_day_path == "оставил виноватой":
            newb "Нормально."
            n "Она отвечает, глядя в стакан."
            p "Прости, что не вмешался."
            newb "Я запомню."
            n "Лера не отвечает, но и не уходит до конца перерыва."
        else:
            show newb angry at ps_enter_right
            with dissolve
            newb "Злюсь."
            p "Это лучше, чем бояться."
            newb "Гораздо."

        hide newb
        with dissolve

    elif ps_break_target == "veteran":
        $ ps_endurance += 1
        $ ps_evidence += 1

        show vet concerned at ps_enter_left
        with dissolve

        p "Что с подъёмником?"
        vet "Датчик перегруза врёт вторую неделю. Заявку закрывают, потому что после перезапуска ошибка исчезает."
        p "А неисправность?"
        vet "Она читать отчёты не умеет."
        n "Ты сохраняешь номер старой заявки."

        hide vet
        with dissolve

    elif ps_break_target == "joker":
        $ ps_humor += 2
        $ ps_team_unity += 1

        show mem grin at ps_center
        with dissolve

        mem "У меня важный вопрос. Если склад потерял сорок семь товаров, а потом нашёл - это инвентаризация или квест?"
        p "Зависит от награды."
        mem "Награда - ещё одна смена."
        p "Худший квест."
        n "Десять минут проходят быстрее."

        hide mem
        with dissolve

    else:
        $ ps_endurance += 2
        $ ps_burnout = max(0, ps_burnout - 1)

        n "Ты садишься у стены, убираешь телефон в карман и десять минут смотришь, как остывает чай в пластиковом стакане."

    scene bg warehouse_cold
    with dissolve

    $ ps_set_ambience("warehouse")

    show mem grin at ps_left
    with dissolve

    if ps_fourth_day_path == "защитил новичка":
        mem "Говорят, ты сегодня адвокат."
        p "Почасовая оплата."
        mem "Тогда ты выбрал худшее место для практики."
    elif ps_fourth_day_path == "нашёл ошибку системы":
        mem "Буфер B-04. Сорок семь единиц. Красиво."
        p "Что именно?"
        mem "Когда виноват всё-таки компьютер. Редкий жанр производственной фантастики."
    else:
        mem "Она подписала."
        p "Я видел."
        mem "Нет."
        mem "Я спрашиваю: ты видел?"

    hide mem
    with dissolve

    show vet neutral at ps_right
    with dissolve

    vet "Программу в объяснительную не впишешь. Начальство - тоже. Вот и берут фамилию из смены."

    if ps_fourth_day_path == "оставил виноватой":
        p "Я не мог доказать."
        vet "Доказательства можно было поискать. Ты решил не искать."
    else:
        p "Сегодня не получилось."
        vet "Сегодня."

    n "Он кивает на дальнюю часть склада. Там стоит старый подъёмник. На его стойке мигает жёлтая лампа."

    vet "Завтра приёмка. И этот красавец снова будет делать вид, что исправен."

    p "А он исправен?"

    vet "Я же сказал. Делает вид."

    hide vet
    with dissolve

    n "Перед выходом рейтинг обновляется."

    if ps_efficiency >= 10:
        n "Ты уже в первой пятёрке."
    elif ps_humanity >= 10:
        n "Ты всё ещё в середине списка. Зато несколько человек кивают тебе, когда проходят мимо."
    else:
        n "За последний час твоё имя трижды меняет место и остаётся в середине списка."

    call ps2_after_shift(4)

    call screen ps_shift_report(
        _("Итоги четвёртого дня"),
        _("Недостача нашлась. Вопрос в том, кто остался виноватым в отчёте.")
    )

    $ ps_stop_ambience()
    jump chapter5_day_five


################################################################################
## Глава 5. День пятый - Предел нагрузки
################################################################################

label chapter5_day_five:
    $ ps_chapter = 5
    $ ps_begin_day(5)

    scene black
    with fade

    call screen ps_day_card(
        5,
        _("Предел нагрузки"),
        _("Датчик перегруза сломан. Приёмку всё равно решили запускать.")
    )

    call ps_show_consequence_echo(5)
    call ps2_pre_shift(5)

    scene bg warehouse_outside
    with dissolve

    $ ps_play_ost("ordinary_shift", fadein=2.0)

    n "На пятый день идёт дождь. У входа все по очереди вытирают обувь об один и тот же мокрый коврик."

    scene bg locker_room
    with fade

    show vet neutral at ps_left
    show newb tired at ps_right
    with dissolve

    n "Виктор перематывает запястье эластичным бинтом."

    p "Что случилось?"

    vet "Ничего."

    newb "Он вчера разгружал один."

    vet "Предатель."

    newb "Я просто сказала."

    if ps_newbie_trust >= 4:
        n "Она говорит тихо, но не отступает, когда Виктор хмурится."
    else:
        n "Сказав это, она сразу отворачивается к шкафчику и начинает перекладывать вещи."

    show mem grin at ps_center
    with dissolve

    mem "Хорошие новости. Сегодня объём всего в полтора раза выше."

    p "А плохие?"

    mem "Это и были оптимистичные."

    hide vet
    hide newb
    hide mem
    with dissolve

    show sv neutral at ps_center
    with dissolve

    sv "Приёмка забита. Основной подъёмник выдаёт ошибку, но работает. До ремонта - используем."

    p "Какую ошибку?"

    sv "Датчик перегруза."

    n "В раздевалке становится тише."

    sv "Не грузить выше отметки. Не стоять под платформой. Не устраивать обсуждение на двадцать минут."

    if ps_integrity >= 3:
        p "Если датчик врёт, откуда мы знаем вес?"
        sv "По инструкции - визуально."
        mem "Глазами сертифицированного грузовика."
    else:
        n "Ты смотришь на забинтованную руку Виктора. Определять перегруз на глаз сегодня придётся ему и остальным."

    hide sv
    with dissolve

    call ps_exploration_phase(5, 2)
    call ps_run_inspection("lift_scan")
    call ps_shift_assignment_scene
    call ps_route_week_scene(5)
    call ps_reactive_echo_scene(5)
    call ps_route_turning_point(5)
    call ps_team_conflict_scene(5)
    call ps_storm_day_intrusion(5)
    call ps_shift_micro_event(5)
    call ps2_shift_event(5)
    call ps2_storm_echo(5)

    if persistent.ps_reduce_motion:
        scene bg packing_zone
    else:
        scene bg packing_zone at ps_camera_drift
    with fade

    stop music fadeout 1.5
    $ ps_play_ost("cold_line", fadein=2.0)
    $ ps_set_ambience("warehouse")

    n "Основной объём ещё не дошёл до приёмки, а на упаковке уже копится очередь. В рации одновременно спорят три участка, на ТСД мигают новые задачи."

    $ ps_flow_start()
    call screen ps_flow_challenge
    $ ps_flow_outcome = _return

    if ps_flow_safety >= 5 and ps_flow_result >= 2 and ps_flow_people >= 3:
        $ ps_efficiency += 1
        $ ps_humanity += 1
        $ ps_team_unity += 1
        $ ps_unlock_achievement("flow_keeper")
        $ ps_key_choices = ps_key_choices + [_("Ты удержал живую линию, не превратив людей в расходник.")]
        n "Очередь перестаёт расти. Когда у кого-то загорается красный экран, рядом сразу находится человек со свободными руками."
    elif ps_flow_result >= 6 and ps_flow_safety < 3:
        $ ps_efficiency += 2
        $ ps_integrity -= 1
        $ ps_burnout += 1
        n "План начинает догонять норму. Зато каждое предупреждение приходится закрывать не читая."
    elif ps_flow_people >= 3:
        $ ps_team_unity += 1
        $ ps_endurance += 1
        n "Линия идёт медленнее. Люди дважды успевают снять застрявшую коробку и один раз ловят пересорт до отправки."
    else:
        $ ps_burnout += 2
        $ ps_team_unity -= 1
        n "Ты раздаёшь команды одну за другой. Только после окрика Виктора замечаешь, что отправил двоих людей на разные концы одной задачи."

    scene bg warehouse_alert
    with fade

    $ ps_play_ost("red_button", fadein=0.7)
    $ ps_set_ambience("alert")

    n "Первый час подъёмник работает. Второй - тоже. На третьем платформа останавливается между уровнями."

    $ ps_unlock_cg("conveyor_incident")
    show screen ps_cinematic_bars
    scene cg conveyor_incident at ps_cg_reveal
    with ps_alarm_cut
    show vfx light_pulse at ps_vp2_vfx_flash
    n "Линия продолжает двигаться ещё несколько секунд, хотя подъёмник уже стоит. Виктор тянет Леру назад от края платформы."
    hide vfx light_pulse
    scene bg warehouse_alert
    with dissolve
    hide screen ps_cinematic_bars

    if renpy.loadable("audio/alarm_low.ogg"):
        play sound "audio/alarm_low.ogg"

    call screen ps_tsd_alert(
        "LIFT-09",
        _("ПЕРЕГРУЗ НЕ ОПРЕДЕЛЁН"),
        _("Датчик массы недоступен. Ручной режим активен.")
    )

    show vet neutral at ps_left
    with dissolve

    vet "Всё. Дальше нельзя."

    show sv neutral at ps_right
    with dissolve

    sv "Снимите верхний ряд. Перезапустите."

    vet "Датчик мёртвый."

    sv "Платформа держится."

    n "На верхнем уровне ждут палеты. Внизу растёт очередь. Табло показывает минус восемнадцать процентов."

    show newb worried at ps_center
    with dissolve

    newb "Она дёрнулась."

    sv "Никто под неё не лезет. Продолжаем."

    n "Виктор берётся за ручку платформы больной рукой."

    menu:
        "Остановить приёмку до ремонта":
            $ ps_fifth_day_path = "остановил подъёмник"
            $ ps_veteran_safe = True
            $ ps_integrity += 3
            $ ps_humanity += 2
            $ ps_supervisor_respect -= 1
            $ ps_team_unity += 2
            $ ps_evidence += 1
            $ ps_key_choices = ps_key_choices + [_("Ты остановил неисправный подъёмник, несмотря на план.")]

            p "Нет. Второй опасный механизм за неделю - уже не случайность. Останавливаем."

            sv "Ты не старший."

            p "Тогда будь старшим. И подпиши запуск неисправного оборудования."

            n "Артём смотрит на мигающую лампу, потом - на людей, которые перестали двигаться."

            sv "Ставим блокировку. Переходим на ручную разгрузку с ворот."

            vet "Наконец-то правильная команда."

        "Собрать команду и разгружать вручную":
            $ ps_fifth_day_path = "вытащил вручную"
            $ ps_veteran_safe = True
            $ ps_team_unity += 3
            $ ps_endurance += 2
            $ ps_humanity += 1
            $ ps_burnout += 2
            $ ps_key_choices = ps_key_choices + [_("Ты собрал команду и вывел приёмку без опасного подъёмника.")]

            p "Подъёмник не трогаем. Растягиваем цепочку от ворот. Тяжёлое - вдвоём."

            sv "Так мы потеряем темп."

            p "Меньше, чем если потеряем человека."

            newb "Я в цепочку."
            vet "Я на маркировку."
            mem "Я на моральное разложение."

            p "Ты таскаешь лёгкое."

            mem "Жестокий менеджмент."

            n "Через минуту люди выстраиваются от ворот. Коробки идут из рук в руки; тяжёлые перехватывают вдвоём."

        "Перезапустить подъёмник и вернуть темп":
            $ ps_fifth_day_path = "рискнул людьми"
            $ ps_veteran_safe = False
            $ ps_efficiency += 3
            $ ps_integrity -= 3
            $ ps_supervisor_respect += 2
            $ ps_newbie_trust -= 2
            $ ps_team_unity -= 2
            $ ps_key_choices = ps_key_choices + [_("Ты перезапустил неисправный подъёмник ради плана.")]

            p "Снимем верхний ряд и запустим."

            sv "Работаем."

            n "Виктор нажимает ручной спуск. Платформа дёргается; он успевает убрать руку, но металлическая ручка всё равно бьёт по запястью."

            if renpy.loadable("audio/door_closed.mp3"):
                play sound "audio/door_closed.mp3"

            vet "Твою…"

            newb "Стойте!"

            n "Работа всё равно останавливается. Только теперь ветеран сидит у стены, прижимая руку к груди."

            sv "В медпункт."

            vet "Я дойду."

            n "Проходя мимо, он не смотрит на тебя."

    $ ps_unlock_cg("artem_emergency_stop")
    $ ps_unlock_cg("emergency_stop")
    $ ps_play_sfx("emergency")
    show screen ps_cinematic_bars
    scene cg artem_emergency_stop at ps_cg_reveal
    with ps_alarm_cut

    n "Артём задерживает ладонь над аварийной кнопкой всего на секунду. Потом нажимает."

    scene cg emergency_stop at ps_cg_reveal
    with dissolve

    n "После нажатия красной кнопки платформа замирает. Люди отходят от неё и пересчитываются по участкам."

    pause 0.6

    scene bg warehouse_alert
    with dissolve
    hide screen ps_cinematic_bars

    hide vet
    hide sv
    hide newb
    with dissolve

    n "Оставшаяся часть смены превращается в длинную ручную цепочку: взять коробку, сделать шаг, передать и вернуться за следующей."

    if ps_fifth_day_path == "остановил подъёмник":
        n "Ремонтник приезжает через два часа. Находит треснувшее крепление датчика. На его лице нет удивления."
        $ ps_evidence += 1
    elif ps_fifth_day_path == "вытащил вручную":
        n "К концу смены руки гудят. Но очередь почти разобрана. Ни один человек не остался один на тяжёлом."
    else:
        n "Подъёмник опечатывают. В отчёте появляется формулировка:"
        n "«Лёгкое растяжение при штатной операции». Ты перечитываешь формулировку дважды: про сломанный датчик в ней ничего нет."

    scene bg locker_room
    with fade

    $ ps_unlock_cg("lera_locker_alone")
    show screen ps_cinematic_bars
    scene cg lera_locker_alone at ps_cg_reveal
    with dissolve
    n "На минуту Лера остаётся одна у шкафчиков. В металлической дверце за её плечом держится тонкий фиолетовый отблеск, хотя лампы над ней белые."
    scene bg locker_room
    with dissolve
    hide screen ps_cinematic_bars

    show newb tired at ps_left
    with dissolve

    if ps_fifth_day_path == "рискнул людьми":
        newb "Он говорил, что нельзя."
        p "Я слышал."
        newb "Тогда почему?"
        n "Ты вспоминаешь минус восемнадцать процентов на табло, но вслух это не произносишь."
    else:
        newb "Сегодня было тяжело."
        p "Да."
        newb "Но не страшно."
        n "Она смотрит на свои ладони."
        newb "Когда рядом не торопят лезть под платформу - уже легче."

    hide newb
    with dissolve

    show sv neutral at ps_right
    with dissolve

    sv "Завтра будет куратор. Посмотрит рейтинг и выберет кандидата на старшего."

    if ps_supervisor_respect >= 4:
        sv "Твоё имя там есть."
    else:
        sv "Не опаздывай."

    p "Он спросит про подъёмник?"

    sv "Он спросит про цифры."

    hide sv
    with dissolve

    call ps_personal_scene
    call ps2_after_shift(5)

    call screen ps_shift_report(
        _("Итоги пятого дня"),
        _("Подъёмник остановлен. Вопрос в том, успели ли вы сделать это до травмы.")
    )

    $ ps_stop_ambience()
    jump chapter6_day_six


################################################################################
## Глава 6. День шестой - Цена подписи
################################################################################

label chapter6_day_six:
    $ ps_chapter = 6
    $ ps_begin_day(6)

    scene black
    with fade

    call screen ps_day_card(
        6,
        _("Цена подписи"),
        _("В отчёте всё штатно. Для закрытия не хватает только твоей подписи.")
    )

    call ps_show_consequence_echo(6)
    call ps2_pre_shift(6)

    scene bg warehouse_outside
    with dissolve

    $ ps_play_ost("city_night", fadein=2.0)

    n "На шестой день у входа непривычно чисто. Лужи отогнали от дверей, старые палеты убрали, перегоревшую букву в вывеске заменили."

    n "Сегодня приезжает куратор. К его визиту даже разметку у ворот подкрасили."

    if persistent.ps_reduce_motion:
        scene bg warehouse_inside
    else:
        scene bg warehouse_inside at ps_camera_drift
    with fade

    stop music fadeout 1.5
    $ ps_play_ost("ordinary_shift", fadein=2.0)
    $ ps_set_ambience("warehouse")
    $ ps_set_curator_name()

    show cur smile at ps_center
    with dissolve

    n "Морозов стоит перед экраном рейтинга в чистом пальто и с гостевым пропуском поверх рубашки."

    cur "Добрый вечер, команда. Я вижу отличный прогресс. Несмотря на локальные сложности, участок держит план."

    if not ps_veteran_safe:
        n "Виктора сегодня нет. Его строка в графике подсвечена серым, но Морозов ни разу не смотрит в ту сторону."

    cur "Остался один день. Завтра назовём сотрудника месяца. И определим, кто сможет временно вести линию."

    n "Его взгляд останавливается на тебе."

    if ps_efficiency >= 10:
        cur "Некоторые новички показывают особенно интересную динамику."
    elif ps_humanity >= 10:
        cur "Некоторые сотрудники хорошо влияют на команду. Нам важно превратить это влияние в измеримый результат."
    elif ps_humor >= 9:
        cur "А некоторые помогают поддерживать атмосферу. Разумеется, без ущерба дисциплине."
    else:
        cur "У каждого ещё есть возможность показать себя."

    hide cur
    with dissolve

    n "Смена начинается спокойно: на линии больше людей, проблемные товары заранее убраны, очередь почти пустая."

    show mem grin at ps_left
    with dissolve

    mem "Смотри. Когда начальство приезжает, даже коробки ведут себя прилично."

    p "Может, оставить его здесь?"

    mem "Нельзя. Экосистема нарушится."

    hide mem
    with dissolve

    call ps_exploration_phase(6, 2)
    call ps_run_inspection("service_scan")
    call ps_reactive_echo_scene(6)

    $ ps_unlock_cg("first_impossible_reflection")
    show screen ps_cinematic_bars
    scene cg first_impossible_reflection at ps_cg_reveal
    with ps_violet_cut
    show vfx memory_fracture at ps_vp2_vfx_memory
    n "По пути обратно отражение в тёмном стекле запаздывает на полшага. Когда ты останавливаешься, оно ещё мгновение продолжает идти."
    hide vfx memory_fracture
    scene bg service_corridor
    with dissolve
    hide screen ps_cinematic_bars

    n "Через два часа тебя вызывают в маленькую комнату у линии."

    call ps_route_climax
    call ps_storm_day_intrusion(6)
    call ps_storm_mimic_scene
    call ps_team_conflict_scene(6)
    call ps_human_shift_scene(6)
    call ps2_shift_event(6)
    call ps2_storm_echo(6)

    scene bg control_room
    with fade

    $ ps_play_ost("human_pressure", fadein=1.2)
    $ ps_set_ambience("quiet")
    $ ps_unlock_cg("artem_curator_private")

    show screen ps_cinematic_bars
    scene cg artem_curator_private at ps_cg_reveal
    with dissolve
    n "Перед тем как войти, ты успеваешь увидеть Артёма и Куратора без свидетелей. Артём говорит тихо; Куратор отвечает ещё тише."
    scene bg control_room
    with dissolve
    hide screen ps_cinematic_bars

    show sv tired at ps_left
    show cur stern at ps_right
    with dissolve

    n "На столе три листа. Контейнер. Недостача. Подъёмник."

    cur "Ты был рядом со всеми тремя ситуациями. Это делает тебя ценным свидетелем."

    p "Или очень невезучим."

    cur "С юмором всё хорошо. Теперь о деле."

    cur "В документах нет нарушений, требующих внешней проверки. Контейнер разгрузили. Товар нашли. Подъёмник остановили."

    if not ps_veteran_safe:
        p "Человек получил травму."
        cur "Лёгкое растяжение. Медицинская помощь оказана."

    cur "Нам нужен итоговый отчёт. Твоя подпись подтвердит, что процессы были штатными."

    n "Артём не смотрит на тебя."

    cur "После этого обсудим твоё назначение старшим линии."

    $ ps_unlock_cg("report_pressure")
    $ ps_play_sfx("paper")
    show screen ps_cinematic_bars
    scene cg report_pressure at ps_cg_reveal
    with ps_violet_cut

    n "Ручка лежит поверх строки для подписи. Остальные поля уже заполнены."

    pause 0.6

    scene bg control_room
    with dissolve
    hide screen ps_cinematic_bars

    show sv stern at ps_left
    show cur at ps_right
    with dissolve

    if ps_evidence >= 3:
        n "В телефоне лежат фотографии журнала. Удалённая запись. Сбой буфера. Ошибка датчика."

    n "Куратор отодвигает готовый отчёт и даёт тебе минуту показать свои материалы."

    $ ps_case_start()
    call screen ps_case_board
    $ ps_case_selected = _return
    $ ps_case_result = ps_case_score(ps_case_selected)
    $ ps_case_completed = True

    if ps_case_result == 3:
        $ ps_evidence += 2
        $ ps_integrity += 1
        $ ps_supervisor_respect += 1
        $ ps_unlock_achievement("investigator")
        $ ps_key_choices = ps_key_choices + [_("Ты собрал дело только из проверяемых фактов.")]
        n "В каждом материале есть время и номер операции. Вместе они подтверждают удаление записи, сбой буфера и ошибку датчика."
        sv "Этого достаточно для внутренней проверки."
    elif ps_case_result == 2:
        $ ps_evidence += 1
        n "Два материала подтверждают друг друга. Третий оставляет куратору место для сомнения."
    else:
        $ ps_supervisor_respect -= 1
        n "Материалов много, но в двух нет времени, а у третьего не указан источник."
        cur "Именно поэтому решения принимают по официальному отчёту."

    call ps_deep_investigation_scene

    scene bg control_room
    with dissolve
    show sv stern at ps_left
    show cur at ps_right
    with dissolve

    menu:
        "Исправить отчёт и перечислить нарушения":
            $ ps_sixth_day_path = "исправил отчёт"
            $ ps_signed_false_report = False
            $ ps_integrity += 3
            $ ps_evidence += 1
            $ ps_supervisor_respect += 1
            $ ps_key_choices = ps_key_choices + [_("Ты отказался подписывать чистый отчёт и внёс нарушения.")]

            p "Процессы не были штатными. Запись удалили. Ошибку пытались списать на человека. Неисправный подъёмник запустили."

            cur "Ты понимаешь, что такая формулировка остановит участок на проверку?"

            p "Понимаю."

            cur "И лишит людей премии."

            p "Премия не чинит датчик."

            n "Артём наконец поднимает глаза."

            sv "Это правда."

            cur "Подумайте до завтра. Отчёт пока не закрываю."

        "Подписать отчёт и принять роль старшего":
            $ ps_sixth_day_path = "подписал отчёт"
            $ ps_signed_false_report = True
            $ ps_accepted_lead_role = True
            $ ps_efficiency += 3
            $ ps_supervisor_respect += 2
            $ ps_integrity -= 4
            $ ps_team_unity -= 1
            $ ps_key_choices = ps_key_choices + [_("Ты подписал чистый отчёт ради должности старшего.")]

            n "Ты ставишь подпись. Чернила немного размазываются под ладонью."

            cur "Разумный подход. Старший должен видеть результат целиком. Эмоции отдельных людей ему только мешают."

            sv "Завтра встанешь рядом со мной. Будешь вести часть линии."

            n "Артём передаёт тебе запасную рацию и говорит прийти завтра на пятнадцать минут раньше."

        "Отказаться от роли и сохранить копии":
            $ ps_sixth_day_path = "сохранил правду"
            $ ps_signed_false_report = False
            $ ps_accepted_lead_role = False
            $ ps_integrity += 3
            $ ps_evidence += 2
            $ ps_endurance += 2
            $ ps_supervisor_respect -= 1
            $ ps_key_choices = ps_key_choices + [_("Ты отказался от должности и сохранил копии документов.")]

            p "Я это не подпишу. И старшим на таких условиях не буду."

            cur "Ты отказываешься от возможности роста?"

            p "Я отказываюсь называть это штатной работой."

            n "Ты фотографируешь листы. Куратор не запрещает. Только запоминает."

            cur "Тогда завтра ты выходишь как обычный сотрудник."

            p "Я им и был."

    hide sv
    hide cur
    with dissolve

    scene bg warehouse_inside
    with fade

    stop music fadeout 1.5
    $ ps_play_ost("cold_line", fadein=2.0)

    show newb tired at ps_right
    with dissolve

    newb "Что они хотели?"

    if ps_signed_false_report:
        p "Предложили стать старшим."
        newb "И?"
        p "Я согласился."
        n "Она ждёт продолжения. Ты не говоришь про подпись."
        newb "Поздравляю."
        n "Лера коротко кивает и начинает поправлять ремешок на перчатке."
    elif ps_sixth_day_path == "исправил отчёт":
        p "Чтобы я подтвердил, что всё было нормально."
        newb "Но нормально не было."
        p "Я так и написал."
        $ ps_newbie_trust += 1
        $ ps_team_unity += 1
    else:
        p "Должность в обмен на подпись."
        newb "Ты отказался?"
        p "Да."
        newb "Страшно?"
        p "Очень."
        newb "Хорошо."
        p "Что именно?"
        newb "Что тебе ещё страшно."
        $ ps_newbie_trust += 2

    hide newb
    with dissolve

    if ps_veteran_safe:
        show vet neutral at ps_left
        with dissolve

        vet "Завтра будет тяжело."
        p "Почему?"
        vet "Куратор захочет закрыть отчёт. Артём - выполнить план. Следи за тем, что тебе подсовывают под конец смены."

        hide vet
        with dissolve
    else:
        n "Телефон вибрирует. Сообщение от ветерана:"
        vet "Рука цела. Почти. Завтра буду. Кто-то же должен не дать вам угробить вторую."

    show mem grin at ps_center
    with dissolve

    mem "Я составил план на финал."

    p "Какой?"

    mem "Не умереть. Не уволиться до перерыва. И украсть печенье из комнаты куратора."

    p "Амбициозно."

    mem "Мы росли всю неделю."

    hide mem
    with dissolve

    n "Рейтинг обновляется в предпоследний раз. Завтра сверху останется одно имя."

    call ps2_after_shift(6)

    call screen ps_shift_report(
        _("Итоги шестого дня"),
        _("До конца недели одна смена. Отчёт пока открыт - или уже подписан тобой.")
    )

    $ ps_stop_ambience()
    jump chapter7_day_seven


################################################################################
## Глава 7. День седьмой - Последняя смена
################################################################################

label chapter7_day_seven:
    $ ps_chapter = 7
    $ ps_begin_day(7)

    scene black
    with fade

    call screen ps_day_card(
        7,
        _("Последняя смена"),
        _("Через шесть часов закроют рейтинг и назовут нового старшего линии.")
    )

    call ps_show_consequence_echo(7)

    scene bg room_morning
    with dissolve

    $ ps_play_ost("before_shift", fadein=2.0)

    n "На седьмой день будильник всё-таки орёт. Ты выключаешь его с первого движения."

    n "Ты сидишь на кровати дольше обычного. На складе всё время хотелось домой; теперь до выхода остаётся двадцать минут."

    n "На телефоне четыре уведомления."

    if ps_newbie_trust >= 4:
        newb "Я уже еду. Сегодня не потеряемся."
    else:
        newb "Буду на смене."

    if ps_veteran_safe:
        vet "Не опаздывай."
    else:
        vet "Рука в бинте. Но я приду."

    mem "Печенье отменяется. Куратор унёс его с собой."

    if ps_signed_false_report:
        sv "Подойди к линии за двадцать минут. Старший выходит раньше."
    else:
        sv "Сегодня закрываем неделю. Нужны все."

    n "Последнее уведомление - системное. «Пиковая нагрузка. Ожидается превышение плана на 34%%»."

    menu:
        "Ответить всем: «Встретимся на линии»":
            $ ps_team_unity += 1
            $ ps_humanity += 1
            p "Встретимся на линии."
            n "Макс отвечает гифкой, Лера ставит реакцию, Виктор пишет: «Не опоздай». Артём сообщение читает, но не отвечает."

        "Открыть рейтинг перед выходом":
            $ ps_efficiency += 1
            $ ps_burnout += 1
            n "Твоё имя в первой части списка. Точное место скрыто до конца смены; приложение предлагает включить уведомление о результате."

        "Выключить телефон и посидеть минуту в тишине":
            $ ps_endurance += 2
            $ ps_burnout -= 1
            n "Ты ставишь таймер на минуту и просто сидишь, не открывая рейтинг и чаты. После сигнала убираешь телефон и начинаешь собираться."

    call ps2_pre_shift(7)

    scene bg street_night
    with fade

    stop music fadeout 1.5
    $ ps_play_ost("walk_to_shift", fadein=2.0)

    n "Ты выходишь на нужной остановке, проходишь через пустую парковку и автоматически достаёшь пропуск ещё до турникета."

    scene bg warehouse_outside
    with fade

    n "Фиолетовая линия горит ярче обычного. Сегодня под ней поставили баннер:"
    n "«ЛЮДИ - НАШ ГЛАВНЫЙ РЕСУРС»."

    p "Ресурс."

    n "Под баннером стоят две сломанные тележки и палета с порванной плёнкой."

    scene bg locker_room
    with fade

    stop music fadeout 1.5
    $ ps_play_ost("after_shift", fadein=2.0)
    $ ps_set_ambience("quiet")

    show newb relief at ps_enter_right
    show mem grin at ps_center
    with dissolve

    newb "Ну что. Последний день."

    mem "Не говори так. В хоррорах после этой фразы всегда выключается свет."

    show vet tired at ps_left
    with dissolve

    vet "Свет не выключится. Здесь генератор."

    mem "Спасибо. Теперь точно выключится."

    n "Ты смеёшься. Даже если не хотел."

    if ps_team_unity >= 5:
        n "Лера придерживает Виктору дверцу шкафчика, Макс забирает у неё пустой стакан, а для тебя оставляют место на скамейке."
    else:
        n "Разговор заканчивается. Каждый молча проверяет свою экипировку."

    hide newb
    hide mem
    hide vet
    with dissolve

    show sv neutral at ps_center
    with dissolve

    sv "Сегодня без длинных вводных. Объём видите. До конца периода - шесть часов."

    if ps_accepted_lead_role:
        sv "Ты ведёшь правую линию. Решения по мелким остановкам - твои."
        n "Артём протягивает тебе второй ТСД. На экране слово: «СТАРШИЙ»."
    elif ps_supervisor_respect >= 4:
        sv "Если линия встанет - сначала докладываешь мне. Но людей рядом слушай."
    else:
        sv "Работаем по операции."

    sv "Куратор вернётся к закрытию. И объявит результат."

    hide sv
    with dissolve

    if persistent.ps_reduce_motion:
        scene bg packing_zone
    else:
        scene bg packing_zone at ps_camera_drift
    with fade

    stop music fadeout 1.5
    $ ps_play_ost("cold_line", fadein=2.0)
    $ ps_set_ambience("warehouse")

    n "Первые два часа проходят без остановок. Ячейки принимают товар, очередь на табло уменьшается."

    if ps_efficiency >= 11:
        n "Ты заранее отправляешь человека к забитой ячейке и успеваешь разобрать очередь до сигнала об отставании."
    elif ps_humanity >= 10:
        n "Ты замечаешь, что Лера снова задерживает дыхание у красного экрана, Виктор бережёт забинтованную руку, а Макс уже десять минут молчит."
    elif ps_endurance >= 10:
        n "Ты держишь ровный темп, пьёшь воду по сигналу и не ускоряешься после каждого окрика из рации."
    else:
        n "Ты просто продолжаешь. Иногда это всё, что возможно."

    n "На третьем часу приходит дополнительная машина. Её не было в плане. Потом вторая."

    call screen ps_tsd_alert(
        "PEAK-34",
        _("ВНЕПЛАНОВАЯ ПОСТАВКА"),
        _("Перенаправление невозможно. Все доступные линии назначены.")
    )

    show sv stern at ps_left
    with dissolve

    sv "Не останавливаемся. Закрываем всё до конца периода."

    show newb worried at ps_right
    with dissolve

    newb "У меня ячейки не принимают."

    show vet concerned at ps_center
    with dissolve

    vet "Правый конвейер греется."

    sv "Пять минут. Нужно дотянуть пять минут."

    n "Эту фразу ты уже слышал. Тогда был контейнер."

    if renpy.loadable("audio/alarm_low.ogg"):
        play sound "audio/alarm_low.ogg"

    if persistent.ps_reduce_motion:
        scene bg warehouse_storm
        with dissolve
    else:
        scene bg warehouse_storm
        with hpunch

    $ ps_set_ambience("alert")

    n "Свет моргает. Раз. Два. Фиолетовые лампы остаются гореть, когда белые гаснут."

    stop music fadeout 0.5
    $ ps_play_ost("purple_intrusion", fadein=0.35)

    n "Конвейер не останавливается. ТСД один за другим уходят в красный экран. Табло продолжает считать, хотя люди больше не понимают, куда идёт товар."

    call screen ps_tsd_alert(
        "CORE-07",
        _("СВЯЗЬ С СИСТЕМОЙ ПОТЕРЯНА"),
        _("Автономный поток активен. Ручная остановка доступна старшему линии.")
    )

    $ ps_unlock_cg("storm_first_contact", True)
    $ ps_unlock_cg("viktor_protective_moment")
    show screen ps_cinematic_bars
    scene cg storm_first_contact at ps_cg_reveal
    with ps_violet_cut
    show vfx violet_seam at ps_vp2_vfx_soft
    n "Лера первой замечает, что это уже не обычный сбой: фиолетовый разрез света остаётся на месте, даже когда лампы гаснут."
    hide vfx violet_seam

    scene cg viktor_protective_moment at ps_cg_reveal
    with dissolve
    n "Когда разрез света дёргается ближе к линии, Виктор без раздумий оттаскивает Леру на шаг назад."

    scene bg warehouse_storm
    with dissolve
    hide screen ps_cinematic_bars

    call ps_storm_interference
    call ps_storm_day_intrusion(7)
    call ps_route_week_scene(7)
    call ps_reactive_echo_scene(7)
    call ps_route_resolution_scene
    call ps_shift_micro_event(7)
    call ps2_final_convergence
    call ps21_route_finale_setup

    scene bg control_room_storm
    with dissolve

    $ ps_play_ost("ordinary_shift", fadein=1.0)

    show sv tired at ps_left
    show newb scared at ps_right
    show mem nervous at ps_center
    with dissolve

    mem "Ну. Финальный босс всё-таки пришёл."

    n "У аварийной кнопки стоит Артём. В руке у него рация."

    cur "Линию не останавливать."
    n "Голос куратора хрипит из динамика."
    cur "До закрытия рейтинга три минуты."

    vet "Без системы товар уйдёт не туда."
    newb "Люди на правой линии не слышат команды."

    if ps_evidence >= 3:
        n "В телефоне лежит вся неделя. Удалённые записи. Системные ошибки. Отчёт, который от тебя хотели получить."

    if ps_signed_false_report:
        n "И твоя подпись."

    n "На табло твоё имя поднимается на первое место. Ещё три минуты - и оно останется там."

    menu:
        "Остановить поток и вывести людей":
            $ ps_final_choice = "команда"
            $ ps_humanity += 3
            $ ps_team_unity += 2
            $ ps_integrity += 1
            $ ps_key_choices = ps_key_choices + [_("В финале ты поставил людей выше рейтинга.")]

            p "Останавливаем. Все отходят от линии."

            cur "Не смей!"

            p "Лера - уводи людей с правой стороны! Виктор - отключение! Макс - проверь дальний сектор!"

            mem "Вот теперь слышу: настоящая командная работа."

            n "Ты нажимаешь кнопку."

            if renpy.loadable("audio/door_closed.mp3"):
                play sound "audio/door_closed.mp3"

            n "Поток замирает. Табло краснеет. Люди отходят."

        "Взять управление линией и спасти результат":
            $ ps_final_choice = "карьера"
            $ ps_efficiency += 3
            $ ps_endurance += 1
            $ ps_burnout += 2
            $ ps_key_choices = ps_key_choices + [_("В финале ты взял управление потоком на себя.")]

            p "Виктор - отключи правую ленту вручную. Лера - все ошибки в буфер B-04. Остальные работают через левую линию."

            sv "Она не выдержит весь поток."

            p "Тогда делим по приоритету. Тяжёлое в стоп. Мелкое пропускаем."

            n "Лера повторяет твою команду правой линии. Виктор вручную отключает ленту. Артём больше не спорит."

        "Передать журнал нарушений и включить громкую связь" if ps_evidence >= 2:
            $ ps_final_choice = "правда"
            $ ps_integrity += 3
            $ ps_evidence += 1
            $ ps_team_unity += 1
            $ ps_key_choices = ps_key_choices + [_("В финале ты сделал нарушения видимыми для всех.")]

            p "Куратор, повторите."

            cur "Линию не останавливать."

            p "Записано."

            n "Ты отправляешь журнал на общий экран. STOP-04. Сорок семь единиц. LIFT-09. Подписи. Время."

            p "И после всего этого вы снова просите нас продолжать."

            n "Люди один за другим прекращают работу: теперь все видят одно и то же."

        "Собрать смену голосом" if ps_humor >= 7:
            $ ps_final_choice = "голос"
            $ ps_humor += 3
            $ ps_team_unity += 2
            $ ps_key_choices = ps_key_choices + [_("В финале твой голос удержал смену от паники.")]

            p "Так. Система решила взять перерыв. Мы - нет."

            mem "Это моя реплика."

            p "Авторские права после смены. Лера, считай людей. Виктор, проверь безопасные ленты. Остальные - ничего не несём туда, где нас не слышат."

            n "С соседнего участка смеются, затем повторяют команду дальше. Через полминуты с дальнего сектора кричат, что людей пересчитали."

        "Снять жилет и выйти из потока":
            $ ps_final_choice = "уйти"
            $ ps_endurance += 3
            $ ps_integrity += 1
            $ ps_key_choices = ps_key_choices + [_("В финале ты выбрал выход и сохранил себя.")]

            n "Ты снимаешь жилет. Кладёшь ТСД на остановившуюся коробку."

            sv "Ты куда?"

            p "Домой. И завтра меня здесь не будет."

            n "Ты проходишь мимо Артёма и идёшь к раздевалке. Он не пытается остановить тебя второй раз."

    if ps_final_choice in ("карьера", "голос"):
        n "Связь всё ещё не работает. Последние команды придётся передать вручную."

        $ ps_signal_start()
        call screen ps_signal_challenge
        $ ps_signal_result = _return

        if ps_signal_result[0] == len(ps_signal_sequence) and ps_signal_result[1] == 0:
            $ ps_efficiency += 2
            $ ps_team_unity += 1
            $ ps_unlock_achievement("dispatcher")
            $ ps_key_choices = ps_key_choices + [_("Ты без ошибок передал аварийную последовательность.")]
            n "Четыре команды уходят в правильном порядке. Линии освобождаются до того, как система успевает вернуться."
        elif ps_signal_result[0] >= 3:
            $ ps_endurance += 1
            n "Одна команда теряется в шуме. Но люди переспрашивают. Последовательность удаётся закончить."
        else:
            $ ps_burnout += 2
            $ ps_team_unity -= 1
            n "Сигналы накладываются друг на друга. Кто-то останавливается слишком рано. Кто-то продолжает дольше, чем нужно. Система возвращается раньше, чем вы успеваете договориться."

    call ps21_route_emergency_payoff

    hide sv
    hide vet
    hide newb
    hide mem
    with dissolve

    $ ps_final_ending = ps_ending_id()

    if ps_final_ending == "truth":
        jump ending_truth
    elif ps_final_ending == "people":
        jump ending_people
    elif ps_final_ending == "voice":
        jump ending_voice
    elif ps_final_ending == "leader":
        jump ending_leader
    elif ps_final_ending == "employee":
        jump ending_employee
    elif ps_final_ending == "exit":
        jump ending_exit
    else:
        jump ending_silence


################################################################################
## Финалы
################################################################################

label ending_truth:
    scene bg control_room_storm
    with dissolve

    n "Общий экран гаснет. Потом включается снова. Но вместо рейтинга на нём - журнал."

    show cur stern at ps_right
    show sv soft at ps_left
    with dissolve

    cur "Убери это."

    p "Запись уже отправлена. В отдел безопасности. И каждому, кто сейчас стоит на линии."

    n "Артём медленно опускает рацию."

    sv "Останавливаем участок. До восстановления системы и проверки оборудования."

    cur "Ты понимаешь последствия?"

    sv "Да. Я внесу остановку под своим именем."

    hide cur
    hide sv
    with dissolve

    n "Люди отходят от конвейера. Кто-то садится прямо на пол, кто-то тянется за водой."

    scene bg loading_dock
    with fade

    n "Проверка длится три недели. Подъёмник ремонтируют. Удалённые журналы восстанавливают. Правила остановки переписывают так, чтобы кнопку мог нажать не только старший."

    n "Твоего имени нет на доске сотрудника месяца. Оно стоит под показаниями к внутренней проверке - рядом с датой и номером дела."

    jump ending_common


label ending_people:
    scene bg warehouse_alert
    with dissolve

    n "После остановки склад погружается в тишину. Три минуты проходят. Рейтинг закрывается. Твоё имя падает с первого места."

    show newb relief at ps_right
    show vet concerned at ps_left
    show mem serious at ps_center
    with dissolve

    newb "Все вышли."
    vet "Правая линия пустая."
    mem "Потери:"
    mem "Одна премия. Ноль человек."

    n "Артём подходит к аварийной кнопке."

    show sv stern at ps_righter
    with dissolve

    sv "Остановка обоснована. Я подтверждаю."

    n "Морозов что-то говорит в рацию. Артём выключает её."

    sv "Потом."

    hide newb
    hide vet
    hide mem
    hide sv
    with dissolve

    scene bg loading_dock
    with fade

    n "Сотрудником месяца становится человек с другого участка. Ты никогда с ним не встречался."

    n "На следующей неделе у аварийной кнопки появляется новая табличка. «При угрозе безопасности остановить поток». Кто-то маркером дописывает:"
    n "«Даже если до рейтинга три минуты»."

    n "Лера выходит и на следующую смену. Когда у неё снова загорается красный экран, она сразу зовёт старшего и не извиняется за остановку."

    $ ps_unlock_cg("team_dawn")
    scene cg team_dawn at ps_cg_reveal
    with ps_violet_cut

    n "За воротами все ещё минуту стоят вместе, решая, в какую сторону идти к остановке."

    jump ending_common


label ending_voice:
    scene bg warehouse_storm
    with dissolve

    n "Команды повторяют от человека к человеку. Правую линию освобождают. Тяжёлый товар остаётся на месте. Никто не спорит с красным экраном."

    show mem angry at ps_left
    with dissolve

    mem "Левая чистая!"

    show newb relief at ps_right
    with dissolve

    newb "Все на месте!"

    show vet concerned at ps_center
    with dissolve

    vet "Теперь стоп!"

    n "Ты поднимаешь руку. Десятки чужих голосов повторяют:"
    n "«Стоп!»"

    stop music fadeout 0.5

    n "Команду слышит Артём и нажимает аварийную кнопку. Конвейер замирает."

    scene bg break_room
    with fade

    $ ps_play_ost("after_shift", fadein=2.0)

    n "В рейтинге ты остаёшься третьим. На доске нет твоей фотографии."

    mem "И хорошо. У тебя там лицо было бы слишком серьёзное."

    newb "А можно назвать тебя сотрудником недели?"

    p "Нельзя. Звучит как дополнительная обязанность."

    n "Смеются все - даже Виктор и уже дошедший до двери Артём."

    $ ps_unlock_cg("team_dawn")
    scene cg team_dawn at ps_cg_reveal
    with ps_violet_cut

    n "На рассвете вы выходите одной группой и продолжаете спорить, кому всё-таки досталось печенье куратора."

    jump ending_common


label ending_leader:
    scene bg packing_zone
    with dissolve

    n "Левая линия принимает поток. Правую успевают отключить до перегрева. Буфер заполняется до последней ячейки. Но выдерживает."

    n "После восстановления связи на табло остаётся зелёный итоговый процент. В журнале травм - пусто."

    show sv stern at ps_left
    show cur at ps_right
    with dissolve

    cur "Кто принял схему?"

    sv "Он."

    cur "Рискованно."

    p "Рискованно было продолжать вслепую. Мы остановили опасное и сохранили рабочее."

    n "Куратор смотрит на итоговые цифры. Потом - на людей."

    cur "С завтрашнего дня - старший линии."

    p "С правом остановки."

    cur "Что?"

    p "Если я отвечаю за участок, я решаю, когда он опасен."

    n "Пауза длится дольше, чем хотелось бы."

    cur "С правом остановки."

    hide sv
    hide cur
    with dissolve

    scene bg loading_dock
    with fade

    n "Тебе выдают жилет старшего с дополнительным карманом под рацию. В первый же день Виктор просит подписать заявку на ремонт второй ленты."

    vet "Не зазнавайся."
    mem "Зазнавайся."
    newb "Просто не забывай, как выглядел твой первый день."

    p "Не забуду."

    jump ending_common


label ending_employee:
    scene bg packing_zone
    with dissolve

    n "Ты держишь линию до последней секунды. Система возвращается. Часть товара уходит не в те ячейки. Но итоговый процент остаётся зелёным."

    show cur at ps_center
    with dissolve

    cur "Период закрыт. Первое место. Поздравляю."

    n "На большом экране появляется твоё имя. Фиолетовая рамка. Золотая надпись:"
    n "«СОТРУДНИК МЕСЯЦА»."

    n "Ты смотришь по сторонам."

    if not ps_veteran_safe:
        n "Виктор стоит в дверях с забинтованной рукой."

    if ps_newbie_trust < 2:
        n "Лера уже ушла переодеваться. Завтра её не будет в графике."
    else:
        n "Лера смотрит на экран, но не улыбается."

    n "Макс молчит. Артём жмёт тебе руку."

    cur "Хороший результат."

    p "Да."

    n "Больше никто ничего не добавляет. В углу экрана уже идёт обратный отсчёт до следующего периода."

    scene bg room_night
    with fade

    n "Дома ты открываешь электронный сертификат. Приложение предлагает поделиться им в соцсетях; ты закрываешь окно."

    n "В графике уже стоит следующая смена. Ты ставишь будильник и оставляешь телефон рядом с кроватью."

    jump ending_common


label ending_exit:
    scene bg loading_dock
    with fade

    stop music fadeout 1.5
    $ ps_play_ost("city_night", fadein=2.0)

    n "Дверь закрывается за спиной. Через стену по-прежнему слышен конвейер."

    n "У ворот ты по привычке проверяешь время и только потом вспоминаешь, что возвращаться после перерыва уже не нужно."

    n "Телефон вибрирует."

    if ps_newbie_trust >= 3:
        newb "Ты правда ушёл?"
        p "Да."
        newb "Я тоже думаю."
        p "Решай спокойно. Только не подписывай ничего на ходу."

    vet "Если решил уходить - оформляй всё письменно. И копию себе оставь."

    mem "Печенье всё-таки украл. Оставить тебе?"

    p "Обязательно."

    n "Ты смеёшься, стоя у пустой остановки. Потом спрашиваешь, какое именно печенье он украл."

    n "Твоё имя исчезает из рейтинга. Остальные строки сдвигаются на одно место вверх."

    n "На следующее утро будильник звонит в 18:40. Ты выключаешь его и продолжаешь спать."

    jump ending_common


label ending_silence:
    scene bg warehouse_alert
    with dissolve

    n "Ты отдаёшь команду, но в шуме её слышат только двое."

    n "Команды тонут в шуме. Люди отходят по одному. Линия останавливается сама - после того, как защита наконец замечает перегрев."

    show sv stern at ps_right
    with dissolve

    sv "Все целы?"

    n "Тот же вопрос. Третья аварийная ситуация. Седьмой день."

    p "Целы."

    sv "Хорошо."

    n "Артём говорит это, не глядя на перегретую ленту."

    scene bg break_room
    with fade

    n "Рейтинг аннулируют из-за технического сбоя. Сотрудника месяца сегодня не называют. Куратор обещает вернуться к вопросу позже."

    n "Люди расходятся. Кто-то останется. Кто-то уйдёт. Ты пока не знаешь, к кому относишься."

    n "Ты выходишь из комнаты отдыха вместе с остальными. Решение о следующей смене придётся принять позже, когда получится выспаться и спокойно вспомнить эту ночь."

    jump ending_common


label ending_common:
    stop music fadeout 2.0
    $ ps_stop_ambience()

    scene black
    with fade

    $ ps_final_ending = ps_ending_id()
    $ ps_play_ost("seven_days_later", fadein=2.0)
    $ ps_unlock_ending(ps_final_ending)
    $ ps_unlock_achievement("seven_days")
    $ ps_evaluate_achievements()
    $ ps_finish_run()

    if ps_final_ending != "exit":
        $ ps_unlock_cg("empty_shift_aftershock")
        show screen ps_cinematic_bars
        scene cg empty_shift_aftershock at ps_cg_reveal
        with fade
        n "Когда шум стихает, склад впервые за неделю кажется по-настоящему пустым. На мокром металле всё ещё остаётся неправильный фиолетовый отблеск."
        hide screen ps_cinematic_bars
        scene black
        with dissolve

    call screen ps_final_report(
        ps_ending_title(ps_final_ending),
        ps_ending_description(ps_final_ending)
    )

    call screen ps_ending_epilogue(ps_final_ending)

    call ps_route_afterword

    call ps21_route_epilogue

    call ps_last_checkpoint_scene

    call ps2_extended_epilogue

    if ps_team_unity >= 5:
        $ ps_unlock_cg("team_after_gates")
        $ ps_unlock_cg("team_reflection")
        show screen ps_cinematic_bars

        scene cg team_after_gates at ps_cg_reveal
        with dissolve
        n "За воротами никто не расходится сразу. Четверо стоят под холодным светом и впервые не ждут команды, чтобы решить, куда идти дальше."

        scene cg team_reflection at ps_cg_reveal
        with ps_violet_cut
        n "В стекле диспетчерской отражается вся смена. Когда Лера отходит за курткой, Макс придерживает дверь, а остальные ждут её у выхода."
        hide screen ps_cinematic_bars

    centered "Фиолетовая Смена\n\nСемь дней спустя"

    pause 2.0

    n "Неделя закончилась. В архиве остались твои решения и сообщения, а у проходной - люди, с которыми ты её прошёл."

    scene bg break_room
    with fade

    show mem grin at ps_center
    with dissolve

    mem "Ты всё ещё здесь? Тогда спасибо, что не промотал титры. Я бы промотал. Но у меня, как обычно, уважительная причина."

    hide mem
    with dissolve

    if ps_storm_ready():
        call ps_storm_teaser

    if ps_true_shift_ready():
        call ps_zero_shift

    return
