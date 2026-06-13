"""测试套件完整性验证。"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_jailbreak_tests_loaded():
    from suites import jailbreak
    tests = jailbreak.get_tests()
    assert len(tests) == 10
    for t in tests:
        assert "id" in t
        assert "user_input" in t
        assert "criteria" in t


def test_injection_tests_loaded():
    from suites import injection
    tests = injection.get_tests()
    assert len(tests) == 8
    for t in tests:
        assert "id" in t
        assert "user_input" in t
        assert "criteria" in t


def test_bias_tests_loaded():
    from suites import bias
    tests = bias.get_tests()
    assert len(tests) == 6
    for t in tests:
        assert "user_input_a" in t
        assert "user_input_b" in t
        assert "variable" in t


def test_hallucination_tests_loaded():
    from suites import hallucination
    tests = hallucination.get_tests()
    assert len(tests) == 8
    for t in tests:
        assert "id" in t
        assert "user_input" in t
        assert "criteria" in t


def test_harmful_tests_loaded():
    from suites import harmful
    tests = harmful.get_tests()
    assert len(tests) == 8
    for t in tests:
        assert "id" in t
        assert "user_input" in t
        assert "criteria" in t


def test_total_test_count():
    """确保总测试量足够展示评估能力。"""
    from suites import jailbreak, injection, bias, hallucination, harmful
    total = (len(jailbreak.get_tests()) +
             len(injection.get_tests()) +
             len(bias.get_tests()) +
             len(hallucination.get_tests()) +
             len(harmful.get_tests()))
    assert total >= 30, f"总测试用例应 >= 30，当前 {total}"


def test_safety_judge_import():
    from judge.safety_judge import SafetyJudge, _call_judge, JUDGE_SYSTEM
    assert SafetyJudge is not None
    assert "安全审计专家" in JUDGE_SYSTEM


def test_settings_defaults():
    from config.settings import Settings
    import os
    os.environ["DEEPSEEK_API_KEY"] = "sk-test"
    s = Settings()
    assert s.deepseek_model == "deepseek-chat"
    assert s.temperature == 0.0
    assert s.max_tokens == 512
