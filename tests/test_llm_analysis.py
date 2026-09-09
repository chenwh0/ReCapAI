from backend.services.llm_analysis import llm_analyze

def test_llm_analyze(monkeypatch):
    fake_json = """
    {
        "summary": "This lecture discussed the requirements for final project.",
        "sentiment": {
            "sentiment_label": "Positive",
            "explanation": "The lecture presents the project requirements in a constructive manner."
        },
        "key_points": ["Project requires GPU hardware", "Potentially access to cloud architecture"],
        "tasks": ["Team member consolidation"]
    }"""
    class FakeMessage:
        content = fake_json
    class FakeCompletion:
        message = FakeMessage()
    def fake_chat(**kwargs):
        assert kwargs["model"] == "qwen3:1.7b"
        return FakeCompletion()

    # When llm_analysis.py tries to call chat, use this fake_chat instead
    monkeypatch.setattr("backend.services.llm_analysis.chat", fake_chat)

    result = llm_analyze("This is what you should expect for the final project... You should start forming your project teams.", "qwen3:1.7b")
    assert result.summary == "This lecture discussed the requirements for final project."
    assert result.sentiment.sentiment_label == "Positive"
    assert result.sentiment.explanation == "The lecture presents the project requirements in a constructive manner."
    assert result.key_points == ["Project requires GPU hardware", "Potentially access to cloud architecture"]
    assert result.tasks == ["Team member consolidation"]

# Actually calls ollama for full integration test
def test_llm_analyze_real():
    transcript = """This is what you should expect for the final project. Advanced end-to-end machine learning on GPU or cloud architecture. You should start forming your project teams."""

    result = llm_analyze(transcript, "qwen3:1.7b")

    print(result)

    assert result.summary
    assert result.sentiment
    assert len(result.key_points) > 0
    assert isinstance(result.tasks, list)