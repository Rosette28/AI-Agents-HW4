from graphify_agent.services.instrumentation import Instrumentation


def test_instrumentation_counts():
    inst = Instrumentation()

    inst.log_llm_call()
    inst.log_file_read()
    inst.log_iteration()

    result = inst.finalize()

    assert result["llm_calls"] == 1
    assert result["files_read"] == 1
    assert result["iterations"] == 1