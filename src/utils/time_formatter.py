"""
Time formatting utilities for TPlayer application.
"""


def format_time(milliseconds: int) -> str:
    """Format time in milliseconds to MM:SS format.
    
    Args:
        milliseconds: Time in milliseconds
        
    Returns:
        Formatted time string in MM:SS format
    """
    if milliseconds < 0:
        return "00:00"
        
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    
    return f"{minutes:02d}:{seconds:02d}"


def format_time_detailed(milliseconds: int) -> str:
    """Format time in milliseconds to HH:MM:SS format.
    
    Args:
        milliseconds: Time in milliseconds
        
    Returns:
        Formatted time string in HH:MM:SS format
    """
    if milliseconds < 0:
        return "00:00:00"
        
    seconds = milliseconds // 1000
    minutes = seconds // 60
    hours = minutes // 60
    
    seconds = seconds % 60
    minutes = minutes % 60
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def get_time_components(milliseconds: int) -> tuple:
    """Get time components from milliseconds.
    
    Args:
        milliseconds: Time in milliseconds
        
    Returns:
        Tuple of (hours, minutes, seconds)
    """
    if milliseconds < 0:
        return (0, 0, 0)
        
    seconds = milliseconds // 1000
    minutes = seconds // 60
    hours = minutes // 60
    
    seconds = seconds % 60
    minutes = minutes % 60
    
    return (hours, minutes, seconds) 