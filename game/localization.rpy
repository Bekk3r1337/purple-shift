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
    # First-launch gate. The bilingual copy is intentionally not translated:
    # both choices must remain understandable before a language is selected.
    button:
        xfill True
        yfill True
        background Solid("#030106f2")
        action NullAction()

    frame:
        xalign 0.5
        yalign 0.5
        xsize 920
        padding (58, 48)
        background Solid("#0d0717f5")

        vbox:
            xfill True
            spacing 18

            text "ЯЗЫК / LANGUAGE":
                xalign 0.5
                size 42
                color "#c99cff"

            text "Выберите язык интерфейса и текста / Choose your language":
                xalign 0.5
                text_align 0.5
                size 24
                color "#ded2ea"

            null height 16

            hbox:
                xalign 0.5
                spacing 28

                textbutton "РУССКИЙ":
                    action Function(ps_select_language, None)
                    xsize 330
                    ysize 78
                    text_xalign 0.5

                textbutton "ENGLISH (BETA)":
                    action Function(ps_select_language, "english")
                    xsize 330
                    ysize 78
                    text_xalign 0.5

            null height 4

            text "Язык можно изменить позже в настройках. / You can change it later in Settings.":
                xalign 0.5
                text_align 0.5
                size 19
                color "#a997bd"
