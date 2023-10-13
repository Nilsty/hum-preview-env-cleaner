# Humanitec Preview Environment Cleaner
The Humanitec preview environment cleaner can be configured to clean up application environments matching a regex and of a certain age in days.
Using this in a cron job enables users to clean up older preview environments to save on resources and potentially costs.

# Configuration
The configuration can be done via the following environment variables:
| ENV VARIABLE | EXAMPLE | DESCRIPTION | DEFAULT VALUE |
|---|---|---|---|
| HUMANITEC_URL | `https://api.humanitec.io` | Url of the Humanitec API | `https://api.humanitec.io` |
| HUMANITEC_TOKEN | `token-example-NnZmqTHXBNmScDeYcQ_Ipp` | Humanitec API token (excluding the Bearer prefix) | None |
| HUMANITEC_APP | `my-app-id` | The Humanitec app id | None |
| HUMANITEC_ENV_REGEX | `preview-.*` | A regex to match the full Humanitec environment id | None |
| HUMANITEC_ENV_MAX_AGE_DAYS | `3.5` | A float number to define the maximum age in days of your environment | `7` |

