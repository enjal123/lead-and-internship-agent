from unittest.mock import patch


@patch("agents.outreach_agent.ask_ai", return_value="Subject: hi\n\nBody text")
def test_generate_outreach_does_not_raise_keyerror(mock_ask_ai):
    """
    Regression test: the original generate_outreach() only passed
    business_name into OUTREACH_EMAIL_PROMPT.format(...), but the
    template also requires business_type, website, and website_issues --
    calling it with defaults for those should no longer raise KeyError.
    """
    from agents.outreach_agent import generate_outreach

    result = generate_outreach(business_name="Joe's Pizza")
    assert result == "Subject: hi\n\nBody text"
    mock_ask_ai.assert_called_once()


@patch("agents.scoring_agent.ask_ai", return_value="Score: 8/10, strong lead")
def test_score_lead_parses_number_from_sentence(mock_ask_ai):
    """
    Regression test: the original code did int(response.strip()), which
    breaks whenever the LLM adds any surrounding text instead of a bare
    integer.
    """
    from agents.scoring_agent import score_lead

    assert score_lead("some analysis") == 8


@patch("agents.scoring_agent.ask_ai", return_value="unclear, hard to say")
def test_score_lead_handles_unparseable_response(mock_ask_ai):
    from agents.scoring_agent import score_lead

    assert score_lead("some analysis") == 0
