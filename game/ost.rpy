# -*- coding: utf-8 -*-

################################################################################
## Purple Shift - optional Suno OST layer
##
## New tracks live in game/audio/ost/. Until a generated track is added, every
## cue falls back to the existing soundtrack so the game remains fully playable.
################################################################################

init -5 python:
    ps_ost_catalog = {
        "main_theme": {
            "path": "audio/ost/01_purple_shift_main.mp3",
            "fallback": "audio/menu_theme.mp3",
            "title": "Purple Shift",
        },
        "before_shift": {
            "path": "audio/ost/02_before_shift.mp3",
            "fallback": "audio/home_ambient.mp3",
            "title": "До смены",
        },
        "city_night": {
            "path": "audio/ost/03_city_after_midnight.mp3",
            "fallback": "audio/city_night.mp3",
            "title": "Город после полуночи",
        },
        "walk_to_shift": {
            "path": "audio/ost/04_walk_to_shift.mp3",
            "fallback": "audio/night_walk.mp3",
            "title": "Дорога на смену",
        },
        "ordinary_shift": {
            "path": "audio/ost/05_ordinary_shift.mp3",
            "fallback": "audio/night_shift.mp3",
            "title": "Обычная смена",
        },
        "cold_line": {
            "path": "audio/ost/06_cold_line.mp3",
            "fallback": "audio/warehouse_chill.mp3",
            "title": "Холодная линия",
        },
        "after_shift": {
            "path": "audio/ost/07_after_shift.mp3",
            "fallback": "audio/after_shift_ambient.mp3",
            "title": "После смены",
        },
        "v13_memory": {
            "path": "audio/ost/08_v13_memory.mp3",
            "fallback": "audio/warehouse_chill.mp3",
            "title": "V-13 // Память",
        },
        "human_pressure": {
            "path": "audio/ost/09_human_pressure.mp3",
            "fallback": "audio/after_shift_ambient.mp3",
            "title": "Давление",
        },
        "red_button": {
            "path": "audio/ost/10_red_button.mp3",
            "fallback": "audio/warehouse_chill.mp3",
            "title": "Красная кнопка",
        },
        "purple_intrusion": {
            "path": "audio/ost/11_purple_intrusion.mp3",
            "fallback": "audio/night_shift.mp3",
            "title": "Фиолетовое вмешательство",
        },
        "seven_days_later": {
            "path": "audio/ost/12_seven_days_later.mp3",
            "fallback": "audio/after_shift_ambient.mp3",
            "title": "Семь дней спустя",
        },
        "opening_song": {
            "path": "audio/ost/13_shift_remembers.mp3",
            "fallback": "audio/menu_theme.mp3",
            "title": "Смена помнит",
        },
        "ending_song": {
            "path": "audio/ost/14_afterglow.mp3",
            "fallback": "audio/after_shift_ambient.mp3",
            "title": "После света",
        },
    }

    def ps_ost_path(track_id):
        data = ps_ost_catalog.get(track_id)
        if not data:
            return None
        preferred = data["path"]
        return preferred if renpy.loadable(preferred) else data["fallback"]

    def ps_play_ost(track_id, fadein=1.5, loop=True, fadeout=0.8):
        path = ps_ost_path(track_id)
        if not path:
            return
        renpy.music.play(
            path,
            channel="music",
            loop=loop,
            fadeout=fadeout,
            fadein=fadein,
            if_changed=True,
        )

    def ps_stop_ost(fadeout=1.5):
        renpy.music.stop(channel="music", fadeout=fadeout)


# The main menu automatically upgrades to the new theme as soon as its file is
# dropped into game/audio/ost/.
init 20 python:
    _ps_menu_theme = ps_ost_path("main_theme")
    if _ps_menu_theme:
        config.main_menu_music = _ps_menu_theme


# Register generated OST entries in the in-game music archive only when the
# actual files exist. This avoids locked placeholder entries before generation.
init 50 python:
    if "ps_music_catalog" in globals():
        _known_music_ids = {item[0] for item in ps_music_catalog}
        for _track_id, _data in ps_ost_catalog.items():
            if _track_id in ("opening_song", "ending_song") and renpy.loadable(_data["path"]):
                _catalog_id = "ost_" + _track_id
                if _catalog_id not in _known_music_ids:
                    ps_music_catalog.append(
                        (_catalog_id, _data["title"], _data["path"], 1)
                    )
