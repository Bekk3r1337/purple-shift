# -*- coding: utf-8 -*-

################################################################################
## Совместимость сохранений
##
## Все последующие изменения состояния проходят через этот модуль. Старые
## сохранения 1.x и 2.0 получают новые поля без необходимости начинать заново.
################################################################################

define ps_latest_save_schema = 21
default ps_save_schema = 21


init -5 python:
    if getattr(persistent, "ps_latest_save_schema", None) is None:
        persistent.ps_latest_save_schema = 21

    def ps_migrate_loaded_save():
        defaults = {
            "ps21_route_day6_choice": None,
            "ps21_route_final_action": None,
            "ps21_route_outcome": None,
            "ps21_route_memory": [],
            "ps_save_schema": ps_latest_save_schema,
        }

        for field_name, default_value in defaults.items():
            if not hasattr(renpy.store, field_name):
                value = list(default_value) if isinstance(default_value, list) else default_value
                setattr(renpy.store, field_name, value)

        if getattr(persistent, "ps21_route_outcomes", None) is None:
            persistent.ps21_route_outcomes = []

        renpy.store.ps_save_schema = ps_latest_save_schema
        persistent.ps_latest_save_schema = ps_latest_save_schema
        renpy.save_persistent()

    if ps_migrate_loaded_save not in config.after_load_callbacks:
        config.after_load_callbacks.append(ps_migrate_loaded_save)
