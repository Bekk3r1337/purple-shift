# -*- coding: utf-8 -*-

################################################################################
## Автоматические проверки Ren'Py 8.5+
################################################################################

testsuite purple_shift:

    setup:
        $ _test.timeout = 60.0
        $ _test.transition_timeout = 0.1

    teardown:
        exit


    testcase first_choice_effect:
        $ ps_efficiency = 0
        run Jump("mindset_work")
        skip fast until label leaving_home

        assert eval (ps_efficiency == 1)


    testcase route_calculation:
        $ ps_humanity = 5
        $ ps_endurance = 2
        $ ps_efficiency = 1
        $ ps_humor = 0

        assert eval (ps_route_name() == "Человек в потоке")


    testcase custom_screens:
        run Show(
            "ps_tsd_alert",
            code="TEST-01",
            message="ПРОВЕРКА ТСД",
            hint="Тестовый экран."
        )

        pause until screen "ps_tsd_alert"
        assert id "ps_tsd_accept"
        run Hide("ps_tsd_alert")

        run Show(
            "ps_shift_report",
            title="Проверка итогов",
            subtitle="Тестовый экран."
        )

        pause until screen "ps_shift_report"
        assert id "ps_report_continue"
        run Hide("ps_shift_report")

        run Show(
            "ps_final_report",
            title="Проверка финала",
            subtitle="Тестовый экран."
        )

        pause until screen "ps_final_report"
        assert id "ps_final_continue"
        run Hide("ps_final_report")

        run Show(
            "ps_day_card",
            day=3,
            title="Проверка дня",
            subtitle="Тестовый экран."
        )

        pause until screen "ps_day_card"
        assert id "ps_day_start"
        run Hide("ps_day_card")

        run Show("ps_phone")
        pause until screen "ps_phone"
        assert id "ps_phone_close"
        run Hide("ps_phone")

        run Show("ps_phone", initial_tab="messages")
        pause until screen "ps_phone"
        assert id "ps_phone_messages_tab"
        run Hide("ps_phone")

        run Show("ps_break_choice")
        pause until screen "ps_break_choice"
        assert id "ps_break_newbie"
        run Hide("ps_break_choice")

        run Show("ps_director_settings")
        pause until screen "ps_director_settings"
        assert id "ps_director_close"
        run Hide("ps_director_settings")

        $ persistent.ps_minigame_assist = True
        $ ps_flow_start()
        run Show("ps_flow_challenge")
        pause until screen "ps_flow_challenge"
        assert id "ps_flow_safety"
        run Hide("ps_flow_challenge")

        $ ps_case_start()
        run Show("ps_case_board")
        pause until screen "ps_case_board"
        assert id "ps_case_confirm"
        run Hide("ps_case_board")

        run Show("ps_ending_epilogue", ending_id="truth")
        pause until screen "ps_ending_epilogue"
        assert id "ps_epilogue_continue"
        run Hide("ps_ending_epilogue")
        $ persistent.ps_minigame_assist = False


    testcase full_week_labels:
        assert eval (renpy.has_label("chapter3_day_three"))
        assert eval (renpy.has_label("chapter4_day_four"))
        assert eval (renpy.has_label("chapter5_day_five"))
        assert eval (renpy.has_label("chapter6_day_six"))
        assert eval (renpy.has_label("chapter7_day_seven"))
        assert eval (renpy.has_label("ending_common"))


    testcase all_final_endings:
        $ ps_final_choice = "правда"
        $ ps_evidence = 4
        $ ps_integrity = 4
        $ ps_signed_false_report = False
        assert eval (ps_ending_id() == "truth")

        $ ps_final_choice = "команда"
        $ ps_humanity = 12
        $ ps_team_unity = 6
        $ ps_newbie_trust = 5
        assert eval (ps_ending_id() == "people")

        $ ps_final_choice = "голос"
        $ ps_humor = 10
        $ ps_team_unity = 5
        assert eval (ps_ending_id() == "voice")

        $ ps_final_choice = "карьера"
        $ ps_efficiency = 12
        $ ps_supervisor_respect = 5
        $ ps_signed_false_report = False
        assert eval (ps_ending_id() == "leader")

        $ ps_final_choice = "карьера"
        $ ps_signed_false_report = True
        assert eval (ps_ending_id() == "employee")

        $ ps_final_choice = "уйти"
        $ ps_signed_false_report = False
        assert eval (ps_ending_id() == "exit")

        $ ps_final_choice = "команда"
        $ ps_humanity = 0
        $ ps_team_unity = 0
        $ ps_newbie_trust = 0
        assert eval (ps_ending_id() == "silence")


    testcase interactive_systems:
        $ ps_sort_start()
        $ ps_sort_choose("light")
        assert eval (ps_sort_index == 1)
        assert eval (ps_sort_score == 1)

        $ ps_sort_choose("tech")
        assert eval (ps_sort_mistakes == 1)
        assert eval (ps_sort_time == 27)

        $ ps_signal_start()
        $ ps_signal_choose("left")
        $ ps_signal_choose("buffer")
        assert eval (ps_signal_index == 2)
        assert eval (ps_signal_score == 2)

        $ ps_signal_choose("stop")
        assert eval (ps_signal_mistakes == 1)
        assert eval (ps_signal_time == 17)

        assert eval (renpy.loadable("images/ch/curator.png"))
        assert eval (renpy.loadable("images/bg/control_room.jpg"))


    testcase director_systems:
        $ ps_phone_replies = {}
        $ ps_humanity = 0
        $ ps_newbie_trust = 0
        $ ps_reply_message("newbie", "support")

        assert eval (ps_phone_replies["newbie"] == "support")
        assert eval (ps_humanity == 1)
        assert eval (ps_newbie_trust == 2)

        $ ps_flow_start()
        $ ps_flow_choose("safety")
        assert eval (ps_flow_index == 1)
        assert eval (ps_flow_safety == 2)

        $ ps_flow_choose("result")
        assert eval (ps_flow_index == 2)
        assert eval (ps_flow_result == 2)
        assert eval (ps_flow_mistakes == 0)

        $ ps_case_start()
        $ ps_case_toggle("terminal")
        $ ps_case_toggle("camera")
        $ ps_case_toggle("lift")
        assert eval (len(ps_case_selected) == 3)
        assert eval (ps_case_score(ps_case_selected) == 3)

        $ ps_case_toggle("camera")
        $ ps_case_toggle("rumor")
        assert eval (ps_case_score(ps_case_selected) == 2)


    testcase director_assets:
        assert eval (renpy.loadable("images/bg/break_room.jpg"))
        assert eval (renpy.loadable("images/bg/mezzanine.jpg"))
        assert eval (renpy.loadable("images/bg/packing_zone.jpg"))
        assert eval (renpy.loadable("images/bg/loading_dock.jpg"))

        assert eval (renpy.loadable("images/ch/mem_serious.png"))
        assert eval (renpy.loadable("images/ch/vet_concerned.png"))
        assert eval (renpy.loadable("images/ch/super_stern.png"))
        assert eval (renpy.loadable("images/ch/nov_relief.png"))

        assert eval (renpy.loadable("images/cg/emergency_stop.jpg"))
        assert eval (renpy.loadable("images/cg/report_pressure.jpg"))
        assert eval (renpy.loadable("images/cg/team_dawn.jpg"))

        assert eval (renpy.loadable("audio/scan_soft.ogg"))
        assert eval (renpy.loadable("audio/error_soft.ogg"))
        assert eval (renpy.loadable("audio/phone_vibrate.ogg"))
        assert eval (renpy.loadable("audio/radio_click.ogg"))
        assert eval (renpy.loadable("audio/conveyor_loop.ogg"))
        assert eval (renpy.loadable("audio/ventilation_loop.ogg"))
        assert eval (renpy.loadable("audio/alarm_low.ogg"))


    testsuite incident_paths:

        testcase every_incident_outcome:
            parameter incident_label = [
                "chapter3_incident_stop",
                "chapter3_incident_team",
                "chapter3_incident_norm",
            ]

            run Jump(incident_label)
            skip fast until label chapter3_after_incident

            assert eval (ps_second_shift_path != "не определён")


    testsuite ending_paths:

        testcase every_ending_scene:
            parameter ending_label = [
                "ending_truth",
                "ending_people",
                "ending_voice",
                "ending_leader",
                "ending_employee",
                "ending_exit",
                "ending_silence",
            ]

            run Jump(ending_label)
            skip fast until label ending_common

            assert eval (renpy.has_label(ending_label))
