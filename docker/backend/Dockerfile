ARG PYTHON_VERSION

FROM bitnami/python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN groupadd -r api \
  && useradd --no-log-init -r -g api api

WORKDIR /api
COPY ./requirements.txt .

RUN python -m venv $VIRTUAL_ENV \
  && pip install --upgrade pip \
  && pip install -r requirements.txt

USER api
CMD ["uvicorn", "main:api", "--host", "0.0.0.0"]
