FROM python:3.10.6

FROM gorialis/discord.py

WORKDIR /

ENV VIRTUAL_ENV=/opt/venv

RUN python3 -m venv $VIRTUAL_ENV

RUN pip install --upgrade pip

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements-prod.txt .
RUN pip install -r requirements-prod.txt

# Run the application:
COPY . .
CMD ["python", "main.py"]