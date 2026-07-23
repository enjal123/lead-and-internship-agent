from unittest.mock import patch

from orchestrators.internship_pipeline import run_internship_pipeline


@patch("orchestrators.internship_pipeline.build_resume_for_job", return_value="/tmp/resume.txt")
@patch("orchestrators.internship_pipeline.analyze_job", return_value="fit")
@patch("orchestrators.internship_pipeline.is_freshman_friendly", return_value=True)
@patch("orchestrators.internship_pipeline.add_internship")
@patch("orchestrators.internship_pipeline.scrape_internships")
def test_run_internship_pipeline_skips_non_job_postings(
    mock_scrape_internships,
    mock_add_internship,
    mock_is_freshman_friendly,
    mock_analyze_job,
    mock_build_resume_for_job,
):
    mock_scrape_internships.return_value = [
        {
            "company": "Unknown",
            "title": "How to build a resume",
            "description": "guide content",
            "link": "https://medium.com/article",
        },
        {
            "company": "Example",
            "title": "Software Engineer Intern",
            "description": "A real internship posting",
            "link": "https://jobs.lever.co/example/123",
        },
    ]

    saved = run_internship_pipeline(query="internship", max_results=2, build_resumes=True)

    assert saved == [
        {"title": "Software Engineer Intern", "link": "https://jobs.lever.co/example/123", "good_fit": True}
    ]
    mock_analyze_job.assert_called_once_with("A real internship posting")
    mock_build_resume_for_job.assert_called_once_with("Example", "A real internship posting")
    mock_add_internship.assert_called_once()
