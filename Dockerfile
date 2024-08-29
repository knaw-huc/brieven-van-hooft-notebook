FROM python:3.10-slim

WORKDIR /usr/src

COPY requirements.txt .
COPY brieven-van-hooft-notebook.py .

RUN pip install --break-system-packages -r requirements.txt
EXPOSE 8080

CMD ["marimo","run","brieven-van-hooft-notebook.py", "--host", "0.0.0.0", "-p", "8080" ]
