# -*- coding: utf-8 -*-

################################################################################
## Персонажи и изображения
################################################################################

default ps_player_name = "Сотрудник"
default ps_newbie_name = "Новичок"
default ps_veteran_name = "Ветеран"
default ps_joker_name = "Шутник"
default ps_supervisor_name = "Супервайзер"
default ps_curator_name = "Куратор"
default ps_names_revealed = False

define p = DynamicCharacter("ps_player_name", color="#c8a2ff")
define sv = DynamicCharacter("ps_supervisor_name", color="#7CFF7C")
define n = Character(None)
define vet = DynamicCharacter("ps_veteran_name", color="#ffd27a")
define mem = DynamicCharacter("ps_joker_name", color="#7ad7ff")
define newb = DynamicCharacter("ps_newbie_name", color="#ff7ad7")
define cur = DynamicCharacter("ps_curator_name", color="#ff9d66")

image bg mainmenu = Solid("#120a1f")
image ps_bg_base = Solid("#0c0614")
image ps_bg_purple = Solid("#1b0f2a")
image ps_bg_soft = Solid("#120a1f")

image bg room_morning = "images/bg/room_morning.jpg"
image bg room_night = "images/bg/room_night.jpg"
image bg stairwell = "images/bg/stairwell.jpg"
image bg street_night = "images/bg/street_night.jpg"
image bg warehouse_outside = "images/bg/warehouse_outside.jpg"
image bg warehouse_inside = "images/bg/warehouse_inside.jpg"
image bg warehouse_alert = "images/bg/warehouse_alert.jpg"
image bg warehouse_cold = "images/bg/warehouse_cold.jpg"
image bg control_room = "images/bg/control_room.jpg"
image bg locker_room = "images/bg/locker_room.jpg"
image bg break_room = "images/bg/break_room.jpg"
image bg mezzanine = "images/bg/mezzanine.jpg"
image bg packing_zone = "images/bg/packing_zone.jpg"
image bg loading_dock = "images/bg/loading_dock.jpg"
image bg service_corridor = "images/bg/service_corridor.jpg"
image bg black = "images/bg/bg_black.jpg"

image cg emergency_stop = "images/cg/emergency_stop.jpg"
image cg report_pressure = "images/cg/report_pressure.jpg"
image cg team_dawn = "images/cg/team_dawn.jpg"
image cg route_newbie = "images/cg/route_newbie.jpg"
image cg route_veteran = "images/cg/route_veteran.jpg"
image cg route_joker = "images/cg/route_joker.jpg"
image cg route_supervisor = "images/cg/route_supervisor.jpg"
image cg storm_signal = "images/cg/storm_signal.jpg"
image cg team_names = "images/cg/team_names.jpg"
image cg shift_plan = "images/cg/shift_plan.jpg"
image cg monitor_guest = "images/cg/monitor_guest.jpg"
image cg future_message = "images/cg/future_message.jpg"
image cg named_shift = "images/cg/named_shift.jpg"

image sv neutral = "images/ch/super1.png"
image sv stern = "images/ch/super_stern.png"
image sv conflicted = "images/ch/super_conflicted.png"
image newb worried = "images/ch/nov1.png"
image newb tired = "images/ch/nov2.png"
image newb relief = "images/ch/nov_relief.png"
image newb determined = "images/ch/nov_determined.png"
image vet neutral = "images/ch/vet1.png"
image vet concerned = "images/ch/vet_concerned.png"
image vet injured = "images/ch/vet_injured.png"
image mem grin = "images/ch/mem1.png"
image mem serious = "images/ch/mem_serious.png"
image mem open = "images/ch/mem_open.png"
image cur = "images/ch/curator.png"

# Curated OVERDRIVE art.
# Register optional assets from Python so Ren'Py lint does not treat
# not-yet-promoted generated files as hard missing dependencies.
init -5 python:
    def ps_optional_art(preferred, fallback):
        def _pick(st, at):
            path = preferred if renpy.loadable(preferred) else fallback
            return renpy.displayable(path), None
        return renpy.display.layout.DynamicDisplayable(_pick)

    renpy.image("newb neutral", ps_optional_art("images/ch/nov_neutral.png", "images/ch/nov_relief.png"))
    renpy.image("newb angry", ps_optional_art("images/ch/nov_angry.png", "images/ch/nov_determined.png"))
    renpy.image("newb scared", ps_optional_art("images/ch/nov_scared.png", "images/ch/nov1.png"))

    renpy.image("vet tired", ps_optional_art("images/ch/vet_tired.png", "images/ch/vet_concerned.png"))
    renpy.image("vet warm", ps_optional_art("images/ch/vet_warm.png", "images/ch/vet1.png"))

    renpy.image("mem nervous", ps_optional_art("images/ch/mem_nervous.png", "images/ch/mem_serious.png"))
    renpy.image("mem angry", ps_optional_art("images/ch/mem_angry.png", "images/ch/mem_serious.png"))

    renpy.image("sv tired", ps_optional_art("images/ch/super_tired.png", "images/ch/super_conflicted.png"))
    renpy.image("sv soft", ps_optional_art("images/ch/super_soft.png", "images/ch/super_conflicted.png"))

    renpy.image("cur stern", ps_optional_art("images/ch/curator_stern.png", "images/ch/curator.png"))
    renpy.image("cur smile", ps_optional_art("images/ch/curator_smile.png", "images/ch/curator.png"))

    renpy.image("bg warehouse_storm", ps_optional_art("images/bg/warehouse_storm.jpg", "images/bg/warehouse_inside.jpg"))
    renpy.image("bg control_room_storm", ps_optional_art("images/bg/control_room_storm.jpg", "images/bg/control_room.jpg"))

    renpy.image("cg team_break_cinematic", ps_optional_art("images/cg/team_break_cinematic.jpg", "images/cg/human_break.jpg"))
    renpy.image("cg v13_false_memory", ps_optional_art("images/cg/v13_false_memory.jpg", "images/cg/memory_wall.jpg"))
    renpy.image("cg zero_shift_v2", ps_optional_art("images/cg/zero_shift_v2.jpg", "images/cg/zero_shift.jpg"))
    renpy.image("cg storm_first_contact", ps_optional_art("images/cg/storm_first_contact.jpg", "images/cg/storm_signal.jpg"))

init 35 python:
    ps_curated_cgs = [
        ("team_break_cinematic", "Пять минут вместе", "images/cg/team_break_cinematic.jpg"),
        ("v13_false_memory", "Лишний человек", "images/cg/v13_false_memory.jpg"),
        ("zero_shift_v2", "Нулевая смена - ремастер", "images/cg/zero_shift_v2.jpg"),
        ("storm_first_contact", "Первый разрез Шторма", "images/cg/storm_first_contact.jpg"),
    ]

    if "ps_cg_catalog" in globals():
        known_cg_ids = {item[0] for item in ps_cg_catalog}
        for cg_item in ps_curated_cgs:
            if cg_item[0] not in known_cg_ids:
                ps_cg_catalog.append(cg_item)


################################################################################
## Позиции персонажей
################################################################################

init python:
    import math

    def ps_character_breathe(trans, shown_time, animation_time):
        # Do not overwrite the transform's baseline. This function used to
        # force yoffset every frame, which cancelled all grounding fixes.
        return None


transform ps_center:
    xalign 0.5
    yalign 1.0
    yoffset 360
    zoom 0.71
    subpixel True
    function ps_character_breathe

transform ps_left:
    xalign 0.23
    yalign 1.0
    yoffset 360
    zoom 0.71
    subpixel True
    function ps_character_breathe

transform ps_right:
    xalign 0.77
    yalign 1.0
    yoffset 360
    zoom 0.73
    subpixel True
    function ps_character_breathe

transform ps_righter:
    xalign 0.60
    yalign 1.0
    yoffset 360
    zoom 0.73
    subpixel True
    function ps_character_breathe

transform ps_breathe_bg:
    alpha 0.03
    linear 3.0 alpha 0.08
    linear 3.0 alpha 0.03
    repeat

transform ps_vignette_soft:
    alpha 0.25
