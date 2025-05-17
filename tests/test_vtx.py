import subprocess
import pytest
import yaml

with open("tests/vtx_test_cases.yaml", "r") as file:
    test_cases = yaml.safe_load(file)

def run_vtx_test(program_name):
    program_path = f"tests/vtx/{program_name}.vtx"
    rom_path = "roms/test"
    subprocess.run(
        ["python", "assemble_vtx.py", program_path, "-o", rom_path],
        check=True
    )
    result = subprocess.run(
        ["./out/vertex", "roms/control", rom_path],
        capture_output=True,
        text=True,
        timeout=2,
    )
    return result.stdout + result.stderr

@pytest.mark.parametrize("test_case", test_cases, ids=[tc["program"] for tc in test_cases])
def test_vtx(test_case):
    program = test_case["program"]
    expected_outputs = test_case["expected_output"]
    if isinstance(expected_outputs, str):
        expected_outputs = [expected_outputs]
    output = run_vtx_test(program)
    for expected_output in expected_outputs:
        assert expected_output in output, f"Test {program} failed!"
