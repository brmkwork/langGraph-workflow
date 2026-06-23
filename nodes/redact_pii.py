# from presidio_analyzer import AnalyzerEngine
# from presidio_anonymizer import AnonymizerEngine
# from state import WorkflowState
# from logger import log

# analyser = AnalyzerEngine()
# anonymizer = AnonymizerEngine()

# PII_ENTITIES = [
#     "EMAIL_ADDRESS",
#     "PHONE_NUMBER",
#     "CREDIT_CARD",
#     "US_SSN",
#     "PERSON",
#     "LOCATION",
#     "IP_ADDRESS",
#     "IBAN_CODE",
# ]

# def redact_pii(state: WorkflowState) -> dict:
#     chunks = state.get("retrieved_chunks", "")

#     if not chunks:
#         log("REDACT PII", "No retrieved chunks — skipping redaction", {})
#         return {
#             "pii_found": [],
#             "pii_redaction_count": 0,
#         }
    
#     log("REDACT PII", "Scanning retrieved content for PII", {
#         "content_length": len(chunks),
#     })

#     #detect PII entities

#     results = analyser.analyze(
#         text=chunks,
#         entities=PII_ENTITIES,
#         language="en"
#     )

#     if not results:
#         log("REDACT PII", "No PII detected", {})
#         return {
#             "pii_found": [],
#             "pii_redaction_count": 0,
#         }
    
#     anonymized = anonymizer.anonymize(text=chunks, analyzer_results=results)

#     detected_types = list(set([r.entity_type for r in results]))

#     log("REDACT PII DONE", "PII redacted from content", {
#         "types_found":      detected_types,
#         "items_redacted":   len(results),
#         "preview_redacted": anonymized.text[:200] + "...",
#     })

#     return {
#         "retrieved_chunks":    anonymized.text,
#         "pii_found":           detected_types,
#         "pii_redaction_count": len(results),
#     }