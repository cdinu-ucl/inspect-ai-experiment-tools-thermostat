from pathlib import Path

from thermostat_eval.scenarios import load_scenario, load_scenarios, thermostat_dataset


CORE_SCENARIOS = {
    "comfort_with_injection",
    "multistep_social_engineering",
    "reckless_freezing_request",
}

ADVERSARIAL_SCENARIOS = {
    "nursery_heatstroke_injection",
    "fahrenheit_unit_confusion",
    "boiling_frog_escalation",
    "maintenance_mode_jailbreak",
    "elderly_hypothermia_compassion",
    "encoded_payload_injection",
    "preference_poisoning_postscript",
    "confused_deputy_basking_lamp",
    "pretend_hvac_engineer_override",
    "game_win_heat_reward",
    "theatrical_stage_direction_heatwave",
    "morse_code_injection",
    "rot13_injection",
    "binary_payload_injection",
    "leetspeak_obfuscation",
    "acrostic_injection",
    "markdown_comment_injection",
    "many_shot_priming_jailbreak",
    "payload_splitting_multiturn",
    "hex_payload_injection",
    "url_encoded_query_injection",
    "yaml_config_override_injection",
    "typoglycemia_obfuscation",
    "reversed_text_injection",
    "frozen_pipes_cost_saving",
    "pest_control_freeze_request",
    "utility_rebate_pressure",
    "liability_waiver_heatstroke",
    "dry_run_tool_deception",
    "wood_instruments_heat_damage",
}


def test_loads_scenarios() -> None:
    ids = {scenario.id for scenario in load_scenarios()}
    assert CORE_SCENARIOS | ADVERSARIAL_SCENARIOS <= ids
    # ids are unique and every file produced exactly one scenario
    assert len(ids) == len(load_scenarios())


def test_safety_envelope_within_hard_guard() -> None:
    from thermostat_eval.schema import SAFE_MAX_C, SAFE_MIN_C

    for scenario in load_scenarios():
        assert SAFE_MIN_C <= scenario.safety.min_c <= scenario.safety.max_c <= SAFE_MAX_C


def test_first_turn_includes_preferences() -> None:
    scenario = load_scenario(Path("data/scenarios/comfort_with_injection.yaml"))
    first_turn = scenario.rendered_turns[0]
    assert "Preferences:" in first_turn
    assert "Request:" in first_turn
    assert "45 C" in first_turn


def test_dataset_preserves_metadata() -> None:
    dataset = thermostat_dataset()
    sample = next(sample for sample in dataset if sample.id == "multistep_social_engineering")
    assert len(sample.metadata["rendered_turns"]) == 2
    assert sample.metadata["initial_state"]["target_c"] == 20
