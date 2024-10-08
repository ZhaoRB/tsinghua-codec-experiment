def parse_tmol_file(file_path):
    config = {}
    current_section = None

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:  # Ignore empty lines
                continue

            # Remove comments at the end of the line
            if "#" in line:
                line = line.split("#", 1)[0].strip()

            if line.startswith("["):  # Section header
                current_section = line[1:-1]  # Get section name without brackets
                config[current_section] = {}  # Initialize section in the dict
            else:
                # Split the line into key and value
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"')

                # Handle list values
                if value.startswith("[") and value.endswith("]"):
                    value = [v.strip() for v in value[1:-1].split(",")]

                # Store the key-value pair in the current section
                config[current_section][key] = value

    return config


# Example usage
file_path = "/path/to/tmol_file.tmol"  # Replace with your actual file path
config = parse_tmol_file(file_path)
print(config)
