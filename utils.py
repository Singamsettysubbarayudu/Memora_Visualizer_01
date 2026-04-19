def parse_input(input_str):
    """Parse a space-separated string of integers."""
    return list(map(int, input_str.strip().split()))


def validate_reference_string(input_str):
    """Validate and return parsed reference string, or raise ValueError."""
    try:
        values = parse_input(input_str)
        if not values:
            raise ValueError("Reference string cannot be empty.")
        return values
    except Exception:
        raise ValueError("Invalid reference string. Use space-separated integers.")


def get_unique_pages(pages):
    """Return count of unique pages in reference string."""
    return len(set(pages))
