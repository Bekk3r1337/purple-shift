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
