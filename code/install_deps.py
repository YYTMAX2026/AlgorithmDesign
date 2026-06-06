
import subprocess, sys
r = subprocess.run(
    [sys.executable, '-m', 'pip', 'install', 'matplotlib', 'openpyxl', '--quiet'],
    capture_output=True, text=True
)
print('STDOUT:', r.stdout)
print('STDERR:', r.stderr)
print('RC:', r.returncode)
