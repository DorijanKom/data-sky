def convert_bytes_to_human_readable(bytes_size):
    # Define conversion factors
    KB = 1024
    MB = KB * 1024

    if bytes_size < KB:
        return f"{bytes_size} B"
    elif bytes_size < MB:
        return f"{bytes_size / KB:.2f} KB"
    else:
        return f"{bytes_size / MB:.2f} MB"