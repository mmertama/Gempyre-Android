import sys
import subprocess

project_name = sys.argv[1] if len(sys.argv) > 1 else "TELEX"

subprocess.run(['gradle', 'init', '--type', 'basic', '--dsl', 'groovy', ' --project-name', project_name])

