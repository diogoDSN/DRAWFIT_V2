# Create builder image to install unecessary packages in instalation
FROM python:3.11-slim AS venv_builder

# Install packages for venv instalation
RUN apt-get update && \
    apt-get install -y libpq-dev gcc

# Create venv and activate it
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install requirements into virtual environment
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Create final image
FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy venv from builder and activate it
COPY --from=venv_builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /drawfit

COPY . .

RUN pip install -e .

CMD ["python", "src/drawfit/Drawfit.py"]
