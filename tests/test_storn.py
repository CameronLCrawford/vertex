import subprocess
import pytest
import yaml

with open("tests/storn_test_cases.yaml", "r") as file:
    test_cases = yaml.safe_load(file)

def run_storn_test(program_name):
    program_path = f"tests/storn/{program_name}.stn"
    assembly_path = "out/test.vtx"
    rom_path = "roms/test"
    subprocess.run([
        "python",
        "compile_storn.py",
        program_path,
        assembly_path
    ], check=True)
    subprocess.run([
        "python",
        "assemble_vtx.py",
        assembly_path,
        rom_path
    ], check=True)
    result = subprocess.run(
        ["./out/vertex", "roms/control", rom_path],
        capture_output=True,
        text=True,
        timeout=2,
    )
    return result.stdout + result.stderr

@pytest.mark.parametrize("test_case", test_cases, ids=[tc["program"] for tc in test_cases])
def test_storn(test_case):
    program = test_case["program"]
    expected_outputs = test_case["expected_output"]
    if isinstance(expected_outputs, str):
        expected_outputs = [expected_outputs]
    output = run_storn_test(program)
    for expected_output in expected_outputs:
        assert expected_output in output, f"Test {program} failed!"
