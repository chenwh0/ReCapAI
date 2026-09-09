import pytest
from docx import Document
from pypdf import PdfReader

from backend.services.document_export import *
from backend.models.schemas import RecapaiFormat, Sentiment

def make_test_recap():
    return RecapaiFormat(
        key_points=["Project requires GPU hardware", "Potentially access to cloud architecture"],
        summary="This lecture discussed the requirements for final project.",
        tasks=["Team member consolidation", "Access cloud infrastructure"],
        sentiment=Sentiment(
            sentiment_label="Positive",
            explanation="The lecture presents the project requirements in a constructive manner."
        )   
    )


# Test export_recap()
def test_export_recap_unsupported():
    recap = make_test_recap()
    with pytest.raises(ValueError, match="Unsupported export type"):
        export_recap(recap, ".xlsx")

def test_export_recap_txt(monkeypatch):
    recap = make_test_recap()
    called = False
    def fake_save_as_txt(recap):
        nonlocal called 
        called = True
        return "test.txt"
    monkeypatch.setattr("backend.services.document_export.save_as_txt", fake_save_as_txt)
    result = export_recap(recap, ".txt")
    assert called
    assert result == "test.txt"

# Test save_as_txt()
def test_save_as_txt(tmp_path):
    recap = make_test_recap()
    file_path = save_as_txt(recap, file_path=tmp_path, file_name="test_recap")
    assert file_path.exists()
    assert file_path.suffix == ".txt"
    content = file_path.read_text(encoding="utf-8")

    assert recap.summary in content
    assert recap.key_points[0] in content
    assert recap.key_points[1] in content
    assert recap.tasks[0] in content
    assert recap.tasks[1] in content
    assert recap.sentiment.sentiment_label in content
    assert recap.sentiment.explanation in content 

# Test save_as_docx()
def test_save_as_docx(tmp_path):
    recap = make_test_recap()
    file_path = save_as_docx(recap, file_path=tmp_path, file_name="test_recap")
    assert file_path.exists()
    assert file_path.suffix == ".docx"

    doc = Document(file_path)
    content = "\n".join(paragraph.text for paragraph in doc.paragraphs)

    assert recap.summary in content
    assert recap.key_points[0] in content
    assert recap.key_points[1] in content
    assert recap.tasks[0] in content
    assert recap.tasks[1] in content
    assert recap.sentiment.sentiment_label in content
    assert recap.sentiment.explanation in content 

# Test save_as_pdf()
def test_save_as_pdf(tmp_path):
    recap = make_test_recap()
    file_path = save_as_pdf(recap, file_path=tmp_path, file_name="test_recap")
    assert file_path.exists()
    assert file_path.suffix == ".pdf"

    reader = PdfReader(file_path)
    content = "\n".join(page.extract_text() for page in reader.pages)
    
    assert recap.summary in content
    assert recap.key_points[0] in content
    assert recap.key_points[1] in content
    assert recap.tasks[0] in content
    assert recap.tasks[1] in content
    assert recap.sentiment.sentiment_label in content
    assert recap.sentiment.explanation in content 