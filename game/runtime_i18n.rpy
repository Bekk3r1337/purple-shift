# Runtime localization for dynamic strings stored in saves and Python data.
# These values are not Ren'Py dialogue blocks, so they need translation at render time.

init -5 python:
    PS_RUNTIME_EN = {
        "до смены": "before shift",
        "в смене": "during shift",
        "после смены": "after shift",
        "Замечать людей": "Notice the People",
        "Собрать факты": "Collect the Facts",
        "Удержать результат": "Protect the Output",
        "Сохранить себя": "Protect Yourself",
        "Перехватить движение": "Stop the Motion",
        "Предупредить голосом": "Warn Her",
        "Проверить вручную": "Check Manually",
        "Пропустить и запомнить": "Let It Pass and Remember",
        "Разделить результат": "Share the Result",
        "Оспорить рейтинг": "Challenge the Ranking",
        "Остановить подпись": "Stop the Signature",
        "Оставить примечание": "Leave a Note",
        "Заблокировать подъёмник": "Lock Out the Lift",
        "Рискнуть последней разгрузкой": "Risk One Last Unload",
        "Приложить историю": "Attach the History",
        "Обменять подпись на ремонт": "Trade a Signature for Repairs",
        "Оставить честную запись": "Leave an Honest Record",
        "Не ставить оценку": "Leave No Rating",
        "Разобрать момент": "Talk It Through",
        "Отложить разговор": "Postpone the Conversation",
        "Спросить без шутки": "Ask Without a Joke",
        "Сохранить людей": "Remember the People",
        "Сохранить копию": "Keep a Copy",
        "Уничтожить копию": "Destroy the Copy",
        "Записать боль вовремя": "Record the Pain in Time",
        "Взять чужую нагрузку": "Take Someone Else's Load",
        "Ты заранее оставил внимание для тех, кого таблица не показывает.": "You made room in advance for the people the ranking never shows.",
        "Ты решил не спорить с системой без памяти и доказательств.": "You decided not to argue with the system without records and evidence.",
        "Ты поставил темп впереди сомнений. Смена это почувствовала.": "You put pace ahead of doubt. The shift felt it.",
        "Ты признал, что у тебя тоже есть предел, даже если его нет в регламенте.": "You admitted that you have a limit too, even if the rules do not list one.",
        "Ты потерял несколько операций, но Лера запомнила, что её безопасность заметили раньше ошибки.": "You lost several operations, but Lera remembered that someone noticed her safety before her mistake.",
        "Ты сохранил участок, но в твоём голосе Лера услышала тот же приказ, что слышит от системы.": "You kept the section moving, but Lera heard the same kind of order in your voice that she hears from the system.",
        "План просел, зато у коробки появилась история, которую нельзя стереть одной кнопкой.": "The target slipped, but the box gained a history that cannot be erased with one click.",
        "Ты сохранил цифру, но оставил проблему следующему участку.": "You preserved the number and passed the problem on to the next section.",
        "Твоё место в рейтинге опустилось, зато помощь перестала быть невидимой хотя бы для команды.": "Your ranking dropped, but at least the team could finally see the help that the system ignored.",
        "Ты сделал помощь предметом официального спора. Теперь система знает, кто задал вопрос.": "You turned that help into an official dispute. Now the system knows who asked the question.",
        "Лера не стала удобным именем для системной ошибки. Теперь проверка касается всех.": "Lera did not become a convenient name for a system error. Now the review involves everyone.",
        "Документ закрыли вовремя. Лера запомнила, что закрыли его всё равно на ней.": "The document was closed on time. Lera remembered that it was still closed on her name.",
        "Сорок минут стали видимой потерей. Возможная травма так и не стала фактом.": "Forty minutes became a visible loss. A possible injury never became a fact.",
        "Поставка закрылась вовремя. После неё никто не назвал тишину облегчением.": "The delivery closed on time. Afterward, nobody called the silence relief.",
        "Инцидент перестал быть единичным. Вместе с ним видимой стала цена прежнего молчания.": "The incident stopped looking isolated. With it, the cost of earlier silence became visible.",
        "Подъёмник починят. Документы навсегда скажут, что проблемы не было.": "The lift will be repaired. The paperwork will forever say there was never a problem.",
        "Ты сохранил собственную версию произошедшего - вместе со страхом и растерянностью.": "You kept your own version of what happened, including the fear and confusion.",
        "Ты отказался превращать прожитую смену в ещё одну цифру.": "You refused to turn the shift you lived through into one more number.",
        "Лера услышала честное признание: ты тоже не был уверен.": "Lera heard an honest admission: you were not sure either.",
        "Вы оба получили передышку. Разговор остался долгом следующего дня.": "You both got a breather. The conversation remained a debt for the next day.",
        "Макс впервые признался: шутки помогают ему заглушить страх, пока тот не заговорил первым.": "For the first time, Max admitted that jokes help him drown out fear before it speaks first.",
        "В памяти телефона осталась смена без процентов и мест.": "Your phone kept a memory of the shift without percentages or rankings.",
        "Документ, который должен был исчезнуть, стал частью хронологии.": "A document that was supposed to disappear became part of the timeline.",
        "Ты защитил Леру от документа и лишил команду одного доказательства.": "You protected Lera from the document and cost the team one piece of evidence.",
        "Виктор впервые не оставил травму на потом. Смена потеряла красивую статистику без происшествий.": "For the first time, Viktor did not leave the injury for later. The shift lost its clean incident-free statistics.",
        "Виктор получил передышку. Твой собственный предел стал ближе.": "Viktor got a breather. Your own limit moved closer.",
    }

    def ps_language_is_english():
        return (
            getattr(renpy.game.preferences, "language", None) == "english"
            or getattr(persistent, "ps_language_code", None) == "english"
        )

    def ps_default_player_name():
        return "Employee" if ps_language_is_english() else "Сотрудник"

    def ps_runtime_text(value):
        if value is None:
            return ""
        if not ps_language_is_english():
            return value
        return PS_RUNTIME_EN.get(value, _(value))
