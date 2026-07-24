# -*- coding: utf-8 -*-

################################################################################
## Персонажи и изображения
################################################################################

define p = Character("Сотрудник", color="#c8a2ff")
define sv = Character("Супервайзер", color="#7CFF7C")
define n = Character(None)
define vet = Character("Ветеран", color="#ffd27a")
define mem = Character("Шутник", color="#7ad7ff")
define newb = Character("Новичок", color="#ff7ad7")
define cur = Character("Куратор", color="#ff9d66")

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
image bg locker_room = "images/bg/locker_room.jpg"
image bg black = "images/bg/bg_black.jpg"

image sv neutral = "images/ch/super1.png"
image newb worried = "images/ch/nov1.png"
image newb tired = "images/ch/nov2.png"
image vet neutral = "images/ch/vet1.png"
image mem grin = "images/ch/mem1.png"
image cur = Transform(
    "images/ch/super1.png",
    matrixcolor=TintMatrix("#ffb078") * BrightnessMatrix(-0.08)
)


################################################################################
## Позиции персонажей
################################################################################

transform ps_center:
    xalign 0.5
    yalign 1.0
    yoffset 5
    zoom 0.60

transform ps_left:
    xalign 0.22
    yalign 1.0
    yoffset 5
    zoom 0.60

transform ps_right:
    xalign 0.75
    yalign 1.0
    yoffset 5
    zoom 0.65

transform ps_righter:
    xalign 0.55
    yalign 1.0
    yoffset 5
    zoom 0.65

transform ps_breathe_bg:
    alpha 0.03
    linear 3.0 alpha 0.08
    linear 3.0 alpha 0.03
    repeat

transform ps_vignette_soft:
    alpha 0.25
