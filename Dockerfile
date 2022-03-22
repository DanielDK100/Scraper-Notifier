FROM python:3.8

WORKDIR /var/www/Scraper-Notifier

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/var/www/Scraper-Notifier"

CMD ["python3", "scraper_notifier/scheduler.py"]
