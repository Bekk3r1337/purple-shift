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
image bg room_night = Transform(
    "images/bg/room_morning.jpg",
    matrixcolor=TintMatrix("#7770aa") * BrightnessMatrix(-0.35)
)
image bg stairwell = "images/bg/stairwell.jpg"
image bg street_night = "images/bg/street_night.jpg"
image bg warehouse_outside = "images/bg/warehouse_outside.jpg"
image bg warehouse_inside = "images/bg/warehouse_inside.jpg"
image bg warehouse_alert = Transform(
    "images/bg/warehouse_inside.jpg",
    matrixcolor=TintMatrix("#b984d6") * BrightnessMatrix(-0.12)
)
image bg warehouse_cold = Transform(
    "images/bg/warehouse_inside.jpg",
    matrixcolor=TintMatrix("#87a7c7") * BrightnessMatrix(-0.22)
)
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

# Curated OVERDRIVE art. Every image has a safe fallback so the script stays
# playable even before the generated file is promoted from art_output.
image newb neutral = ConditionSwitch(
    "renpy.loadable('images/ch/nov_neutral.png')", "images/ch/nov_neutral.png",
    "True", "images/ch/nov_relief.png",
)
image newb angry = ConditionSwitch(
    "renpy.loadable('images/ch/nov_angry.png')", "images/ch/nov_angry.png",
    "True", "images/ch/nov_determined.png",
)
image newb scared = ConditionSwitch(
    "renpy.loadable('images/ch/nov_scared.png')", "images/ch/nov_scared.png",
    "True", "images/ch/nov1.png",
)

image vet tired = ConditionSwitch(
    "renpy.loadable('images/ch/vet_tired.png')", "images/ch/vet_tired.png",
    "True", "images/ch/vet_concerned.png",
)
image vet warm = ConditionSwitch(
    "renpy.loadable('images/ch/vet_warm.png')", "images/ch/vet_warm.png",
    "True", "images/ch/vet1.png",
)

image mem nervous = ConditionSwitch(
    "renpy.loadable('images/ch/mem_nervous.png')", "images/ch/mem_nervous.png",
    "True", "images/ch/mem_serious.png",
)
image mem angry = ConditionSwitch(
    "renpy.loadable('images/ch/mem_angry.png')", "images/ch/mem_angry.png",
    "True", "images/ch/mem_serious.png",
)

image sv tired = ConditionSwitch(
    "renpy.loadable('images/ch/super_tired.png')", "images/ch/super_tired.png",
    "True", "images/ch/super_conflicted.png",
)
image sv soft = ConditionSwitch(
    "renpy.loadable('images/ch/super_soft.png')", "images/ch/super_soft.png",
    "True", "images/ch/super_conflicted.png",
)

image cur stern = ConditionSwitch(
    "renpy.loadable('images/ch/curator_stern.png')", "images/ch/curator_stern.png",
    "True", "images/ch/curator.png",
)
image cur smile = ConditionSwitch(
    "renpy.loadable('images/ch/curator_smile.png')", "images/ch/curator_smile.png",
    "True", "images/ch/curator.png",
)

image bg warehouse_storm = ConditionSwitch(
    "renpy.loadable('images/bg/warehouse_storm.jpg')", "images/bg/warehouse_storm.jpg",
    "True", "images/bg/warehouse_inside.jpg",
)
image bg control_room_storm = ConditionSwitch(
    "renpy.loadable('images/bg/control_room_storm.jpg')", "images/bg/control_room_storm.jpg",
    "True", "images/bg/control_room.jpg",
)

image cg team_break_cinematic = ConditionSwitch(
    "renpy.loadable('images/cg/team_break_cinematic.jpg')", "images/cg/team_break_cinematic.jpg",
    "True", "images/cg/human_break.jpg",
)
image cg v13_false_memory = ConditionSwitch(
    "renpy.loadable('images/cg/v13_false_memory.jpg')", "images/cg/v13_false_memory.jpg",
    "True", "images/cg/memory_wall.jpg",
)
image cg zero_shift_v2 = ConditionSwitch(
    "renpy.loadable('images/cg/zero_shift_v2.jpg')", "images/cg/zero_shift_v2.jpg",
    "True", "images/cg/zero_shift.jpg",
)
image cg storm_first_contact = ConditionSwitch(
    "renpy.loadable('images/cg/storm_first_contact.jpg')", "images/cg/storm_first_contact.jpg",
    "True", "images/cg/storm_signal.jpg",
)


################################################################################
## Позиции персонажей
################################################################################

init python:
    import math

    def ps_character_breathe(trans, shown_time, animation_time):
        if persistent.ps_reduce_motion:
            trans.yoffset = 5
            return None

        trans.yoffset = 3 + math.sin(shown_time * 2.4) * 3
        return 0.05


transform ps_center:
    xalign 0.5
    yalign 1.0
    yoffset 5
    zoom 0.60
    subpixel True
    function ps_character_breathe

transform ps_left:
    xalign 0.22
    yalign 1.0
    yoffset 5
    zoom 0.60
    subpixel True
    function ps_character_breathe

transform ps_right:
    xalign 0.75
    yalign 1.0
    yoffset 5
    zoom 0.65
    subpixel True
    function ps_character_breathe

transform ps_righter:
    xalign 0.55
    yalign 1.0
    yoffset 5
    zoom 0.65
    subpixel True
    function ps_character_breathe

transform ps_breathe_bg:
    alpha 0.03
    linear 3.0 alpha 0.08
    linear 3.0 alpha 0.03
    repeat

transform ps_vignette_soft:
    alpha 0.25
