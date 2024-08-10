FROM python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
COPY Girlclass.py .
COPY dblogic.py .
ENV TZ=Europe/Moscow
CMD python3 main.py