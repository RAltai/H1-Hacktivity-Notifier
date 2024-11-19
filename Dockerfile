FROM python:3.9

ENV H1_USER_NAME="H1_USER_NAME" \
    H1_API_TOKEN="H1_API_TOKEN" \
    GOOGLE_CHAT_WEBHOOK_URL="GOOGLE_CHAT_WEBHOOK_URL"

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    nano \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN cp /app/hacktivity-cron /etc/cron.d/hacktivity-cron
RUN crontab /etc/cron.d/hacktivity-cron
RUN touch /var/log/cron.log

RUN chmod 0644 /etc/cron.d/hacktivity-cron
RUN printenv | sed 's/^/export /' > /app/container_env.sh
RUN chmod 600 /app/container_env.sh
RUN chmod +x /app/run.sh

CMD ["cron", "-f"]
