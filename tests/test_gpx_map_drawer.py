import os
import sys
import tempfile
import pytest

# Add project root to path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from importlib.machinery import SourceFileLoader

# Load module with hyphenated filename
loader = SourceFileLoader("gpx_map_drawer", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gpx-map-drawer.py"))
gpx_map_drawer = loader.load_module()

plot_route = gpx_map_drawer.plot_route
process_file = gpx_map_drawer.process_file
is_valid_hex_color = gpx_map_drawer.is_valid_hex_color

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def fixture_path(name):
    return os.path.join(FIXTURES_DIR, name)


class TestIsValidHexColor:
    def test_valid_6_digit(self):
        assert is_valid_hex_color("#ff0000")
        assert is_valid_hex_color("#FFFFFF")
        assert is_valid_hex_color("#abc123")

    def test_valid_3_digit(self):
        assert is_valid_hex_color("#fff")
        assert is_valid_hex_color("#ABC")

    def test_invalid_no_hash(self):
        assert not is_valid_hex_color("ff0000")

    def test_invalid_wrong_length(self):
        assert not is_valid_hex_color("#ff00")
        assert not is_valid_hex_color("#ff000000")

    def test_invalid_chars(self):
        assert not is_valid_hex_color("#gggggg")

    def test_empty(self):
        assert not is_valid_hex_color("")


class TestPlotRoute:
    def test_simple_track_png(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "output.png")
            result = plot_route(fixture_path("simple_track.gpx"), output_file=output)
            assert result == output
            assert os.path.isfile(output)
            assert os.path.getsize(output) > 0

    def test_simple_track_svg(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "output.svg")
            result = plot_route(fixture_path("simple_track.gpx"), output_file=output, fmt='svg')
            assert result == output
            assert os.path.isfile(output)
            with open(output, 'r') as f:
                content = f.read()
            assert '<svg' in content

    def test_multi_segment(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "output.png")
            result = plot_route(fixture_path("multi_segment.gpx"), output_file=output)
            assert os.path.isfile(output)

    def test_route_only(self):
        """GPX files with only <rte> elements should render successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "output.png")
            result = plot_route(fixture_path("route_only.gpx"), output_file=output)
            assert os.path.isfile(output)

    def test_mixed_track_and_route(self):
        """GPX files with both <trk> and <rte> elements should render."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "output.png")
            result = plot_route(fixture_path("mixed_track_route.gpx"), output_file=output)
            assert os.path.isfile(output)

    def test_straight_horizontal_no_division_by_zero(self):
        """A perfectly horizontal route (lat_range=0) should not crash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "output.png")
            result = plot_route(fixture_path("straight_horizontal.gpx"), output_file=output)
            assert os.path.isfile(output)

    def test_empty_gpx_raises(self):
        """An empty GPX file should raise a ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "output.png")
            with pytest.raises(ValueError, match="No track or route points found"):
                plot_route(fixture_path("empty.gpx"), output_file=output)

    def test_custom_color_and_linewidth(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "output.png")
            result = plot_route(fixture_path("simple_track.gpx"), output_file=output, color='#fc5266', linewidth=5)
            assert os.path.isfile(output)

    def test_default_output_filename(self):
        """When no output_file is given, it should be derived from the input."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy fixture to tmpdir so the output goes there
            import shutil
            src = fixture_path("simple_track.gpx")
            dst = os.path.join(tmpdir, "simple_track.gpx")
            shutil.copy2(src, dst)

            result = plot_route(dst)
            expected = os.path.join(tmpdir, "simple_track.png")
            assert result == expected
            assert os.path.isfile(expected)


class TestProcessFile:
    def test_nonexistent_file(self, capsys):
        process_file("/nonexistent/path/file.gpx")
        captured = capsys.readouterr()
        assert "Input file not found" in captured.out

    def test_non_gpx_extension(self, tmp_path, capsys):
        fake = tmp_path / "data.txt"
        fake.write_text("not gpx")
        process_file(str(fake))
        captured = capsys.readouterr()
        assert "not a GPX file" in captured.out

    def test_successful_processing(self, capsys):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "out.png")
            process_file(fixture_path("simple_track.gpx"), output_file=output)
            captured = capsys.readouterr()
            assert "successfully" in captured.out
            assert os.path.isfile(output)
