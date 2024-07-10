FROM python:latest
LABEL authors="maksi"
WORKDIR usr/src
COPY ./src/ /usr/src/
RUN pip install -r /usr/src/requirements.txt
ENV PYTHONPATH="/usr/src"
ENTRYPOINT ["uvicorn", "--factory", "application.api.main:start_app", "--host", "0.0.0.0", "--port", "80"]