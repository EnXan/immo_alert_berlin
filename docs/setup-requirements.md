# Environment Setup Requirements

This file documents pre-run environment checks required by the CI pipeline.

## Required Variables

| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token for notifications |
| `TELEGRAM_CHANNEL_ID` | Target channel or group ID |
| `AWS_CREDENTIALS` | AWS credentials for log storage |

## Validation

Run `cat .env` to verify all variables are present before executing the crawler.
