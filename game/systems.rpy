# -*- coding: utf-8 -*-

################################################################################
## Состояние истории
################################################################################

default ps_humanity = 0
default ps_endurance = 0
default ps_efficiency = 0
default ps_humor = 0

default ps_newbie_trust = 0
default ps_supervisor_respect = 0

default ps_first_shift_path = "не определён"
default ps_second_shift_path = "не определён"
default ps_key_choices = []
default ps_chapter = 1


init python:
    def ps_clamp(value, low=0, high=12):
        return max(low, min(high, value))

    def ps_route_name():
        scores = [
            ("Человек в потоке", ps_humanity),
            ("Опора смены", ps_endurance),
            ("Тащер системы", ps_efficiency),
            ("Голос в шуме", ps_humor),
        ]

        scores.sort(key=lambda item: item[1], reverse=True)
        return scores[0][0]

    def ps_route_description():
        route = ps_route_name()

        descriptions = {
            "Человек в потоке": "Ты замечаешь людей раньше, чем цифры.",
            "Опора смены": "Ты умеешь выдержать давление и не рассыпаться.",
            "Тащер системы": "Ты быстро понимаешь правила и умеешь давать результат.",
            "Голос в шуме": "Ты не даёшь смене отнять у людей способность улыбаться.",
        }

        return descriptions[route]


################################################################################
## Экран итогов смены
################################################################################

screen ps_stat_card(title, value, accent):
    frame:
        xsize 500
        ysize 110
        background Solid("#24143bea")
        padding (24, 14)

        vbox:
            spacing 10

            hbox:
                xfill True

                text title:
                    color "#efeaff"
                    size 28

                text "[value]":
                    color accent
                    size 28
                    xalign 1.0

            bar:
                value StaticValue(ps_clamp(value), 12)
                xmaximum 450
                ymaximum 18
                left_bar Solid(accent)
                right_bar Solid("#49345f")


screen ps_shift_report(title, subtitle):
    modal True
    zorder 200

    add Solid("#07030ddd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1260
        ysize 940
        padding (70, 48)
        background Solid("#150a26f5")

        vbox:
            spacing 20
            xfill True

            text title:
                color "#c8a2ff"
                size 52
                xalign 0.5

            text subtitle:
                color "#d8c7ff"
                size 27
                xalign 0.5
                text_align 0.5

            null height 4

            grid 2 2:
                spacing 22
                xalign 0.5

                use ps_stat_card("Человечность", ps_humanity, "#ff86c8")
                use ps_stat_card("Выносливость", ps_endurance, "#7fd9ff")
                use ps_stat_card("Эффективность", ps_efficiency, "#8dff9b")
                use ps_stat_card("Юмор", ps_humor, "#ffd36f")

            frame:
                xfill True
                ysize 120
                padding (28, 18)
                background Solid("#201033dd")

                vbox:
                    spacing 8

                    text "[ps_route_name()]":
                        color "#ffffff"
                        size 34
                        xalign 0.5

                    text "[ps_route_description()]":
                        color "#cbbce3"
                        size 25
                        xalign 0.5

            if ps_key_choices:
                vbox:
                    spacing 7

                    text "Что смена запомнила:":
                        color "#a98fcf"
                        size 23

                    for choice in ps_key_choices[-3:]:
                        text "• [choice]":
                            color "#e7ddf7"
                            size 23

            textbutton "ПРОДОЛЖИТЬ":
                id "ps_report_continue"
                action Return()
                xalign 0.5
                xsize 420
                ysize 68
                background Solid("#6c3aa8")
                hover_background Solid("#9b5ee0")
                text_color "#ffffff"
                text_size 28
                text_xalign 0.5
                text_yalign 0.5


################################################################################
## Экран ТСД
################################################################################

screen ps_tsd_alert(code, message, hint):
    modal True
    zorder 210

    add Solid("#050208cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1050
        ysize 620
        padding (64, 54)
        background Solid("#15151cf7")

        vbox:
            spacing 30
            xfill True

            text "ТСД // [code]":
                color "#b8ffca"
                size 32
                xalign 0.5

            frame:
                xfill True
                ysize 190
                padding (35, 30)
                background Solid("#090b0ddd")

                text message:
                    color "#ffffff"
                    size 40
                    text_align 0.5
                    xalign 0.5
                    yalign 0.5

            text hint:
                color "#aeb5ba"
                size 25
                text_align 0.5
                xalign 0.5

            textbutton "ПРИНЯТЬ":
                id "ps_tsd_accept"
                action Return()
                xalign 0.5
                xsize 380
                ysize 72
                background Solid("#245f39")
                hover_background Solid("#348d50")
                text_color "#ffffff"
                text_size 29
                text_xalign 0.5
                text_yalign 0.5
