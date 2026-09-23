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
    # Dedicated first-launch selector. Keep both languages visible before a
    # preference exists, but do not cover the screen with an oversized panel.
    modal True
    zorder 300

    add Solid("#05020bcc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 760
        padding (44, 36)
        background Solid("#0d0717f2")

        vbox:
            xfill True
            spacing 14

            text "PURPLE SHIFT":
                xalign 0.5
                size 20
                color "#9a75be"
                kerning 4

            text "ЯЗЫК / LANGUAGE":
                xalign 0.5
                size 34
                color "#c99cff"

            text "Выберите язык / Choose your language":
                xalign 0.5
                text_align 0.5
                size 20
                color "#ded2ea"

            null height 12

            hbox:
                xalign 0.5
                spacing 18

                textbutton "РУССКИЙ":
                    action Function(ps_select_language, None)
                    xsize 290
                    ysize 64
                    text_xalign 0.5

                textbutton "ENGLISH":
                    action Function(ps_select_language, "english")
                    xsize 290
                    ysize 64
                    text_xalign 0.5

            null height 6

            text "Язык можно изменить в настройках / Language can be changed in Settings":
                xalign 0.5
                text_align 0.5
                size 16
                color "#9f90b2"
