import re


def extract_results(response_text: str):
    gad7_pattern = r"GAD-7:\*+\s(\d/\d/\d/\d/\d/\d/\d)"
    phq9_pattern = r"PHQ-9:\*+\s(\d/\d/\d/\d/\d/\d/\d/\d/\d)"

    gad7_match = re.search(gad7_pattern, response_text)
    gad7_result = gad7_match.group(1) if gad7_match else None

    phq9_match = re.search(phq9_pattern, response_text)
    phq9_result = phq9_match.group(1) if phq9_match else None

    return gad7_result, phq9_result