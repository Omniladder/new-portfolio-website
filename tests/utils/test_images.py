from src.utils.images import process_image_data, read_image_data, write_image_data


def test_read_image_data_returns_raw_bytes(tmp_path):
    """read_image_data returns a file's exact contents as bytes."""
    image_path = tmp_path / "logo.png"
    image_path.write_bytes(b"\x89PNG raw bytes")

    assert read_image_data(image_path) == b"\x89PNG raw bytes"


def test_process_image_data_is_a_passthrough():
    """process_image_data currently returns its input unchanged."""
    assert process_image_data(b"some image bytes") == b"some image bytes"


def test_write_image_data_writes_bytes_to_file(tmp_path):
    """write_image_data writes the given bytes to the given path."""
    image_path = tmp_path / "logo.png"

    write_image_data(image_path, b"\x89PNG raw bytes")

    assert image_path.read_bytes() == b"\x89PNG raw bytes"


def test_write_image_data_creates_missing_parent_directories(tmp_path):
    """write_image_data creates any missing parent directories first."""
    image_path = tmp_path / "assets" / "logo.png"

    write_image_data(image_path, b"data")

    assert image_path.read_bytes() == b"data"
