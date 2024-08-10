FROM python:3.11
COPY requirements.txt /dockerimage
RUN pip install -r requirements.txt
COPY main.py .
COPY Girlclass.py .
COPY dblogic.py .
ENV TZ=Europe/Moscow
CMD python main.py