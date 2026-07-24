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
