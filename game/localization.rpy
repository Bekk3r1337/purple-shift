# Purple Shift localization bootstrap.
# Russian is the source language (Ren'Py "None"), English is an alternate language.

default persistent.ps_language_chosen = False
default persistent.ps_language_code = "russian"

init python:
    def ps_select_language(language):
        """
        Switch the active Ren'Py language and remember that the player made
        an explicit choice. Pass None for the source Russian script.
        """
        persistent.ps_language_chosen = True
        persistent.ps_language_code = "english" if language == "english" else "russian"
        renpy.change_language(language, force=True, rebuild=True)
        renpy.save_persistent()
        renpy.restart_interaction()


screen ps_language_gate():
    # Dedicated first-launch screen. It deliberately covers the main menu
    # instead of appearing as a dialog on top of navigation.
    modal True
    zorder 1000

    add "images/ui/v2/main_menu_bg.jpg"
    add "images/ui/v2/main_menu_overlay.png"
    add Solid("#05020bd9")

    # Quiet framing lines keep the selector in the Purple Shift visual language
    # without turning it into a giant modal window.
    add Solid("#9f5be0") xpos 318 ypos 255 xsize 1284 ysize 2 alpha 0.55
    add Solid("#6f399e") xpos 474 ypos 820 xsize 972 ysize 1 alpha 0.45

    vbox:
        xalign 0.5
        yalign 0.43
        xsize 1100
        spacing 14

        text "PURPLE SHIFT":
            xalign 0.5
            size 30
            kerning 7
            color "#8e6baa"

        text "ВЫБЕРИТЕ ЯЗЫК / SELECT LANGUAGE":
            xalign 0.5
            text_align 0.5
            size 45
            color "#d5a8ff"

        text "Язык интерфейса и истории можно изменить позже в настройках.\nYou can change the interface and story language later in Settings.":
            xalign 0.5
            text_align 0.5
            size 21
            color "#c6b8d4"
            line_spacing 5

        null height 34

        hbox:
            xalign 0.5
            spacing 24

            button:
                action Function(ps_select_language, None)
                xsize 390
                ysize 104
                background Solid("#12091dcc")
                hover_background Solid("#50236fe8")

                fixed:
                    xfill True
                    yfill True
                    add Solid("#a65dec") xpos 0 ypos 0 xsize 5 ysize 104
                    text "РУССКИЙ":
                        xalign 0.5
                        yalign 0.43
                        size 28
                        color "#ffffff"
                    text "Оригинал":
                        xalign 0.5
                        yalign 0.73
                        size 16
                        color "#a997bd"

            button:
                action Function(ps_select_language, "english")
                xsize 390
                ysize 104
                background Solid("#12091dcc")
                hover_background Solid("#50236fe8")

                fixed:
                    xfill True
                    yfill True
                    add Solid("#a65dec") xpos 385 ypos 0 xsize 5 ysize 104
                    text "ENGLISH":
                        xalign 0.5
                        yalign 0.43
                        size 28
                        color "#ffffff"
                    text "Full localization":
                        xalign 0.5
                        yalign 0.73
                        size 16
                        color "#a997bd"

        null height 18

        text "RU  /  EN":
            xalign 0.5
            size 15
            kerning 5
            color "#776786"

