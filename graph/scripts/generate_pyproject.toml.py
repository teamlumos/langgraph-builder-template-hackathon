import re

import toml

# Load the requirements from requirements.txt
with open("graph/requirements/prod.txt", "r") as req_file:
    requirements = [
        line.strip() for line in req_file if re.match(r"^[a-zA-Z0-9-_]+$", line.strip())
    ]

# Load the existing pyproject.toml
pyproject_path = "pyproject.toml"
pyproject = toml.load(pyproject_path)

# Update the dependencies in pyproject.toml
pyproject["project"]["dependencies"] = requirements

# Save the updated pyproject.toml
with open(pyproject_path, "w") as pyproject_file:
    toml.dump(pyproject, pyproject_file)

print("Updated pyproject.toml with dependencies from requirements.txt.")
