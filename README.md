# Hacktivity Disclosed Reports Notifier
This project is a Python-based tool that monitors HackerOne's hacktivity feed for newly disclosed vulnerability reports and sends notifications to a Google Chat. It aims to keep security teams and interested parties informed about the latest publicly disclosed vulnerabilities.

## Key Features:
- **Automated Monitoring:** Fetches the latest disclosed reports from the HackerOne API every 3 hours using a scheduled cron job inside a Docker container.
- **Change Detection:** Compares fetched data with previously stored entries to identify newly disclosed reports since the last check.
- **Google Chat Integration:** Sends a customized Google Chat message for each new report, featuring:

## Purpose:
By automating the monitoring and notification process, this tool ensures that teams are promptly alerted about new vulnerabilities affecting various programs. This facilitates quicker response times and enhances overall security awareness.

## Setup:
0. Add the required environment variable values in `Dockerfile`
   - H1_USER_NAME
   - H1_API_TOKEN
   - GOOGLE_CHAT_WEBHOOK_URL
2. `git clone https://github.com/RAltai/H1-Hacktivity-Notifier`
3. `docker build -t h1_hacktivity_bot:1.0 src/`
4. `docker run -itd --name h1_hacktivity_bot h1_hacktivity_bot:1.0`
