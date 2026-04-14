# Sun Protection Alert

I recently discovered that sun protection is only needed when UV indices are above 2. Coming from Brazil, I've never thought of it, so I just applied sunscreen every day, and stayed in the shade whenever possible (it's so hot as well, there's no other choice lol). In Berlin, I kept the same habit, but it's a very different situation from back home: during winter, the UV-index stays at 0-1. It's only in spring that we start to see it reaching 3-4, but only for a couple of hours a day. I started tracking it through my phone's weather app, but found the process a bit tedious, with too many clicks and scrolls to find the information. That's why I decided to create **a script in Python that fetches the daily UV index forecast for Berlin and sends an email alert when sun protection is needed.**

## What it does

Every morning, the script:

1. Fetches today's hourly UV index forecast for Berlin from the [Open-Meteo API](https://open-meteo.com/), which is free, no API key required
2. Checks which hours have a UV index above 2 (the threshold recommended by the [WHO](https://www.who.int/news-room/questions-and-answers/item/radiation-the-ultraviolet-(uv)-index) for sun protection)
3. If any such hours exist, calculates the peak UV level and maps it to a risk category (moderate / high / very high / extreme) based on the WHO UV index scale
4. Sends an email summarising the risk window, peak index, and SPF advice for the day

If UV stays at 2 or below all day, it sends a "no sunscreen needed" message instead.

## Current status

The script is complete and automated. It runs daily via GitHub Actions and delivers the alert by email (Gmail SMTP).

## Stack

- **Python 3.11**
- **[Open-Meteo API](https://open-meteo.com/)** — UV index forecast data (free, no account needed)
- **Gmail SMTP** — email delivery
- **GitHub Actions** — daily scheduling and hosting

## Project structure

```
uv_alert.py       # main script
.env              # local credentials (ignored by git)
.github/
  workflows/
    uv_alert.yml  # GitHub Actions workflow
```

## Future improvements

- Allow friends and family (Berlin) to get notifications.
- Use DWD (Deutscher Wetterdienst) data instead of Open-Meteo for more accurate local UV readings
- Expand to friends and family in Brazil: make the location configurable instead of hardcoded to Berlin
- Add Google Calendar integration to block out high-UV windows.
- Create a web app for it, so other users may subscribe to alerts.
