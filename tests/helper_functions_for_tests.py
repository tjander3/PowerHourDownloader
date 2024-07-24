import os


def get_file_size(file_path):
    return os.path.getsize(file_path)


def compare_file_sizes(video1_path, video2_path, tolerance=0.01):
    size1 = get_file_size(video1_path)
    size2 = get_file_size(video2_path)

    size_diff = abs(size1 - size2)
    avg_size = (size1 + size2) / 2

    percentage_diff = size_diff / avg_size

    if percentage_diff <= tolerance:
        print("File sizes are within 1% of each other.")
        return True
    else:
        print(f"File sizes differ by more than 1%: {percentage_diff * 100:.2f}%")
        return False