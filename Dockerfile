# Budget Buddy container image
# DEMO TODO (Module 3 - DevOps): this Dockerfile is intentionally incomplete.
# Use Copilot to finish it so the app runs in a container.
#
# Suggested goals for the live demo:
#   - choose a slim Python base image
#   - set a working directory
#   - install dependencies from requirements-test.txt (or a runtime requirements file)
#   - copy the application code
#   - set the default command to run the app

FROM python:3.13-slim

WORKDIR /app

COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

COPY . .

CMD ["python", "main.py"]
