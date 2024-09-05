FROM python:3.10-slim

WORKDIR /usr/src

COPY requirements.txt .
COPY brieven-van-hooft-notebook.py .

RUN pip install --break-system-packages stam marimo==0.8.3 polars-lts-cpu natsort
EXPOSE 8080

ENV MARIMO_OUTPUT_MAX_BYTES=40_000_000

CMD ["marimo","run","brieven-van-hooft-notebook.py", "--host", "0.0.0.0", "-p", "8080" ]
