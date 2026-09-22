# -*- coding: utf-8 -*-

################################################################################
## Visual Pass 2 - generated art integration
################################################################################

# Extra cinematic CGs.
image cg breakroom_preconflict = "images/cg/breakroom_preconflict.jpg"
image cg conveyor_incident = "images/cg/conveyor_incident.jpg"
image cg artem_curator_private = "images/cg/artem_curator_private.jpg"
image cg lera_locker_alone = "images/cg/lera_locker_alone.jpg"
image cg first_impossible_reflection = "images/cg/first_impossible_reflection.jpg"
image cg max_terminal_night = "images/cg/max_terminal_night.jpg"
image cg viktor_protective_moment = "images/cg/viktor_protective_moment.jpg"
image cg empty_shift_aftershock = "images/cg/empty_shift_aftershock.jpg"
image cg artem_emergency_stop = "images/cg/artem_emergency_stop.jpg"
image cg team_after_gates = "images/cg/team_after_gates.jpg"

# Full-screen transparent anomaly plates.
image vfx violet_seam = "images/vfx/violet_seam.png"
image vfx glitch_overlay = "images/vfx/glitch_overlay.png"
image vfx light_pulse = "images/vfx/light_pulse.png"
image vfx memory_fracture = "images/vfx/memory_fracture.png"
image vfx terminal_interference = "images/vfx/terminal_interference.png"


################################################################################
## VFX transforms
################################################################################

transform ps_vp2_vfx_flash:
    alpha 0.0
    linear 0.10 alpha 0.82
    pause 0.12
    linear 0.42 alpha 0.0

transform ps_vp2_vfx_soft:
    alpha 0.0
    linear 0.18 alpha 0.50
    pause 0.35
    linear 0.50 alpha 0.0

transform ps_vp2_vfx_memory:
    alpha 0.0
    linear 0.12 alpha 0.62
    pause 0.45
    linear 0.60 alpha 0.0

transform ps_vp2_terminal_breathe:
    alpha 0.22
    linear 1.4 alpha 0.36
    linear 1.2 alpha 0.20
    repeat


################################################################################
## Gallery registration
################################################################################

init 45 python:
    ps_vp2_cgs = [
        ("breakroom_preconflict", "Перед разговором", "images/cg/breakroom_preconflict.jpg"),
        ("conveyor_incident", "Линия идёт неправильно", "images/cg/conveyor_incident.jpg"),
        ("artem_curator_private", "Разговор за закрытой дверью", "images/cg/artem_curator_private.jpg"),
        ("lera_locker_alone", "После тяжёлой смены", "images/cg/lera_locker_alone.jpg"),
        ("first_impossible_reflection", "Отражение опоздало", "images/cg/first_impossible_reflection.jpg"),
        ("max_terminal_night", "Экран после полуночи", "images/cg/max_terminal_night.jpg"),
        ("viktor_protective_moment", "Шаг назад", "images/cg/viktor_protective_moment.jpg"),
        ("empty_shift_aftershock", "После сигнала", "images/cg/empty_shift_aftershock.jpg"),
        ("artem_emergency_stop", "Красная кнопка - Артём", "images/cg/artem_emergency_stop.jpg"),
        ("team_after_gates", "За воротами", "images/cg/team_after_gates.jpg"),
    ]

    if "ps_cg_catalog" in globals():
        known_cg_ids = {item[0] for item in ps_cg_catalog}
        for cg_item in ps_vp2_cgs:
            if cg_item[0] not in known_cg_ids:
                ps_cg_catalog.append(cg_item)


################################################################################
## Reusable UI overlay
################################################################################

screen ps_vp2_terminal_fx(strength=0.30):
    add Transform("images/ui/v2/terminal_overlay.png", alpha=strength)
    add Transform("images/vfx/terminal_interference.png", alpha=(strength * 0.55)) at ps_vp2_terminal_breathe
