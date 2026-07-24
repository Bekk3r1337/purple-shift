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


    testcase desktop_quick_menu:
        assert eval (renpy.substitute(ps_quick_phone_label) == "Телефон [P]")


    testcase trace_map_screen:
        run Show("ps_warehouse_map", day=2, remaining=1)
        pause until screen "ps_warehouse_map"
        assert id "ps_map_break"
        run Hide("ps_warehouse_map")


    testcase trace_archive_screen:
        $ ps_archive_section = "documents"
        run Show("ps_phone", initial_tab="archive")
        pause until screen "ps_phone"
        assert id "ps_phone_archive_tab"
        assert id "ps_archive_documents"
        click id "ps_archive_cgs"
        assert eval (ps_archive_section == "cgs")
        click id "ps_archive_music"
        assert eval (ps_archive_section == "music")
        click id "ps_archive_routes"
        assert eval (ps_archive_section == "routes")
        click id "ps_archive_documents"
        assert eval (ps_archive_section == "documents")
        run Hide("ps_phone")


    testcase living_phone_signal:
        run Show("ps_phone", initial_tab="signal")
        pause until screen "ps_phone"
        assert id "ps_phone_signal_tab"
        run Hide("ps_phone")


    testcase living_inspection_screen:
        $ ps_begin_inspection("control_scan")
        run Show("ps_inspection_hotspots", scene_id="control_scan")
        pause until screen "ps_inspection_hotspots"
        assert id "ps_inspection_finish"
        run Hide("ps_inspection_hotspots")


    testcase trace_gallery_screen:
        run Show("ps_gallery_viewer", asset_id="route_newbie")
        pause until screen "ps_gallery_viewer"
        assert id "ps_gallery_close"
        run Hide("ps_gallery_viewer")


    testcase trace_chapter_screen:
        run Show("ps_chapter_select_content")
        pause until screen "ps_chapter_select_content"
        assert id "ps_chapter_1"
        run Hide("ps_chapter_select_content")


    testcase full_week_labels:
        assert eval (renpy.has_label("chapter3_day_three"))
        assert eval (renpy.has_label("chapter4_day_four"))
        assert eval (renpy.has_label("chapter5_day_five"))
        assert eval (renpy.has_label("chapter6_day_six"))
        assert eval (renpy.has_label("chapter7_day_seven"))
        assert eval (renpy.has_label("ending_common"))
        assert eval (renpy.has_label("ps_exploration_phase"))
        assert eval (renpy.has_label("ps_route_climax"))
        assert eval (renpy.has_label("ps_storm_teaser"))
        assert eval (renpy.has_label("ps_run_inspection"))
        assert eval (renpy.has_label("ps_storm_interference"))
        assert eval (renpy.has_label("ps_route_afterword"))
        assert eval (renpy.has_label("ps_route_afterword_end"))


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


    testcase trace_systems:
        $ ps_exploration_visits = {}
        $ ps_route_points = {"newbie": 0, "veteran": 0, "joker": 0, "supervisor": 0}
        $ ps_storm_fragments = []
        $ ps_consequence_log = []
        $ ps_newbie_trust = 0
        $ ps_evidence = 0
        $ ps_integrity = 0
        $ ps_humor = 0
        $ ps_team_unity = 0
        $ ps_supervisor_respect = 0
        $ ps_efficiency = 0

        $ ps_record_visit(2, "break")
        $ ps_record_visit(2, "mezzanine")
        assert eval (ps_day_zone_visits(2) == ["break", "mezzanine"])

        $ ps_add_route("newbie", 3)
        assert eval (ps_route_points["newbie"] == 3)
        assert eval (ps_route_target() == "newbie")

        $ ps_record_consequence("Тестовый след.")
        $ ps_record_consequence("Тестовый след.")
        assert eval (ps_consequence_log == ["Тестовый след."])

        $ ps_collect_storm_fragment("violet_stamp")
        $ ps_collect_storm_fragment("dead_channel")
        $ ps_collect_storm_fragment("sealed_manifest")
        assert eval (ps_storm_ready())

        assert eval (ps_zone_event_label(4, "control") == "ps_trace_d4_control")
        assert eval (0 <= ps_completion_percent() <= 100)


    testcase trace_labels:
        assert eval (renpy.has_label("ps_trace_d2_break"))
        assert eval (renpy.has_label("ps_trace_d2_mezzanine"))
        assert eval (renpy.has_label("ps_trace_d2_packing"))
        assert eval (renpy.has_label("ps_trace_d2_control"))
        assert eval (renpy.has_label("ps_trace_d2_dock"))
        assert eval (renpy.has_label("ps_trace_d3_break"))
        assert eval (renpy.has_label("ps_trace_d3_mezzanine"))
        assert eval (renpy.has_label("ps_trace_d3_packing"))
        assert eval (renpy.has_label("ps_trace_d3_control"))
        assert eval (renpy.has_label("ps_trace_d3_dock"))
        assert eval (renpy.has_label("ps_trace_d4_break"))
        assert eval (renpy.has_label("ps_trace_d4_mezzanine"))
        assert eval (renpy.has_label("ps_trace_d4_packing"))
        assert eval (renpy.has_label("ps_trace_d4_control"))
        assert eval (renpy.has_label("ps_trace_d4_dock"))
        assert eval (renpy.has_label("ps_trace_d5_break"))
        assert eval (renpy.has_label("ps_trace_d5_mezzanine"))
        assert eval (renpy.has_label("ps_trace_d5_packing"))
        assert eval (renpy.has_label("ps_trace_d5_control"))
        assert eval (renpy.has_label("ps_trace_d5_dock"))
        assert eval (renpy.has_label("ps_trace_d6_break"))
        assert eval (renpy.has_label("ps_trace_d6_mezzanine"))
        assert eval (renpy.has_label("ps_trace_d6_packing"))
        assert eval (renpy.has_label("ps_trace_d6_control"))
        assert eval (renpy.has_label("ps_trace_d6_dock"))


    testcase trace_assets:
        assert eval (renpy.loadable("images/bg/service_corridor.jpg"))
        assert eval (renpy.loadable("images/cg/route_newbie.jpg"))
        assert eval (renpy.loadable("images/cg/route_veteran.jpg"))
        assert eval (renpy.loadable("images/cg/route_joker.jpg"))
        assert eval (renpy.loadable("images/cg/route_supervisor.jpg"))
        assert eval (renpy.loadable("images/cg/storm_signal.jpg"))


    testcase living_shift_systems:
        $ ps_inspection_seen = {}
        $ ps_storm_fragments = []
        $ ps_route_points = {"newbie": 0, "veteran": 0, "joker": 0, "supervisor": 0}
        $ ps_evidence = 0
        $ ps_integrity = 0
        $ ps_begin_inspection("control_scan")
        $ ps_inspect_hotspot("control_scan", "buffer_log")
        $ ps_inspect_hotspot("control_scan", "violet_frequency")

        assert eval (ps_inspection_can_finish("control_scan"))
        assert eval ("violet_frequency" in ps_storm_fragments)
        assert eval (ps_route_points["supervisor"] == 1)
        assert eval (ps_route_points["joker"] == 1)

        $ ps_storm_decoder_start()
        $ ps_storm_decoder_choose("violet")
        $ ps_storm_decoder_choose("silence")
        $ ps_storm_decoder_choose("echo")
        $ ps_storm_decoder_choose("violet")

        assert eval (ps_storm_decoder_index == len(ps_storm_decoder_sequence))
        assert eval (ps_storm_decoder_errors == 0)
        assert eval (0 <= ps_storm_pressure() <= 100)


    testcase living_shift_audio:
        assert eval (renpy.loadable("audio/live/fluorescent_hum.ogg"))
        assert eval (renpy.loadable("audio/live/breakroom_hum.ogg"))
        assert eval (renpy.loadable("audio/live/forklift_distant.ogg"))
        assert eval (renpy.loadable("audio/live/dock_rain.ogg"))
        assert eval (renpy.loadable("audio/live/storm_whisper.ogg"))
        assert eval (renpy.loadable("audio/live/footsteps_concrete.ogg"))
        assert eval (renpy.loadable("audio/live/scanner_confirm.ogg"))
        assert eval (renpy.loadable("audio/live/scanner_warning.ogg"))
        assert eval (renpy.loadable("audio/live/phone_unlock.ogg"))
        assert eval (renpy.loadable("audio/live/ui_tap.ogg"))
        assert eval (renpy.loadable("audio/live/paper_rustle.ogg"))
        assert eval (renpy.loadable("audio/live/emergency_press.ogg"))
        assert eval (renpy.loadable("audio/live/radio_burst.ogg"))
        assert eval (renpy.loadable("audio/live/route_newbie_motif.ogg"))
        assert eval (renpy.loadable("audio/live/route_veteran_motif.ogg"))
        assert eval (renpy.loadable("audio/live/route_joker_motif.ogg"))
        assert eval (renpy.loadable("audio/live/route_supervisor_motif.ogg"))


    testcase living_shift_messages:
        $ ps_chapter = 6
        $ ps_route_points = {"newbie": 10, "veteran": 0, "joker": 0, "supervisor": 0}
        $ ps_storm_fragments = ["violet_stamp"]
        $ ps_available_ids = [message["id"] for message in ps_available_messages()]

        assert eval ("newbie_followup" in ps_available_ids)
        assert eval ("veteran_followup" not in ps_available_ids)
        assert eval ("v13_unknown" in ps_available_ids)


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


    testsuite route_paths:

        testcase every_route_climax:
            parameter route_id = [
                "newbie",
                "veteran",
                "joker",
                "supervisor",
            ]

            $ ps_route_scene_seen = False
            $ ps_route_points = {
                "newbie": 0,
                "veteran": 0,
                "joker": 0,
                "supervisor": 0,
            }
            $ ps_route_points[route_id] = 10

            run Jump("ps_route_climax")
            skip fast until label ps_route_climax_end

            assert eval (ps_route_scene_id == route_id)


    testsuite route_afterwords:

        testcase every_route_afterword:
            parameter route_id = [
                "newbie",
                "veteran",
                "joker",
                "supervisor",
            ]

            $ ps_route_afterword_seen = False
            $ ps_route_scene_id = route_id

            run Jump("ps_route_afterword")
            skip fast until label ps_route_afterword_end

            assert eval (ps_route_afterword_seen)


    testsuite storm_path:

        testcase secret_post_credit:
            $ ps_storm_fragments = [
                "violet_stamp",
                "dead_channel",
                "sealed_manifest",
            ]

            run Jump("ps_storm_teaser")
            skip fast until label ps_storm_teaser_end

            assert eval (persistent.ps_storm_unlocked)


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
