from .services.transcription import transcribe_audio
from .services.llm_analysis import llm_analyze
from .services.document_export import export_recap
from .models.schemas import RecapResult


class RecapPipeline:
    def recap(self, audio_filepath: str, assemblyai_key: str, model_name: str, export_type: str) -> RecapResult:
        transcript = transcribe_audio(audio_filepath, assemblyai_key)
        result = llm_analyze(transcript, model_name)
        output_filepath = export_recap(result, export_type)
        return RecapResult(recap=result, output_filepath=output_filepath)

