from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from langchain_core.tools import tool
from logger import log

analyzer   = AnalyzerEngine()
anonymizer = AnonymizerEngine()

PII_ENTITIES = [
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "CREDIT_CARD",
    "US_SSN",
    "PERSON",
    "LOCATION",
    "IP_ADDRESS",
    "IBAN_CODE",
    "DATE_TIME",
    "NRP",
    "MEDICAL_LICENSE",
    "URL",
]


@tool
def pii_guardrail_tool(text: str) -> str:
    """
    Scans text for personally identifiable information (PII) such
    as names, emails, phone numbers, credit cards, IBANs, IP
    addresses, and locations — then redacts them before the content
    is used in a response. Use this whenever you retrieve content
    from a file or external source that might contain sensitive or
    personal data. Always call this on retrieved file content before
    generating a response from it.
    """
    log("PII GUARDRAIL", "Scanning content for PII", {
        "content_length": len(text),
    })

    results = analyzer.analyze(
        text=text,
        entities=PII_ENTITIES,
        language="en",
    )

    if not results:
        log("PII GUARDRAIL", "No PII detected — content is clean", {})
        return text

    anonymized     = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
    )
    detected_types = list(set([r.entity_type for r in results]))

    log("PII GUARDRAIL DONE", "PII redacted from content", {
        "types_found":    detected_types,
        "items_redacted": len(results),
        "preview":        anonymized.text[:200] + "...",
    })

    return anonymized.text

guardrail = {
    "name":        "pii_redaction",
    "kind":        "guardrail",
    "description": "Scans and redacts PII from retrieved content before it reaches the response",
    "tool":        pii_guardrail_tool,
}