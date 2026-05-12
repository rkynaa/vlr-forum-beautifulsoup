from match_scraper import vct_scraper
import sys
import time

years = [2026, 2025, 2024, 2023]

urlBase = "https://www.vlr.gg"

print(sys.argv, len(sys.argv))

if len(sys.argv) >= 2:
    if sys.argv[1] == '--match-stats' or '--player-stats':
        yearsFocused = None
        if len(sys.argv) == 2:
            yearsFocused = years
        else:
            yearsFocused = sys.argv[2:]

        print(f"Commencing VLR Scraper for {sys.argv[1]} now...", end="\r", flush=True)

        time.sleep(2)

        for year in yearsFocused:
            vctYearUrl = urlBase + "/vct-" + str(year)
            # print(year, vctYearUrl)
            vct_scraper(vctYearUrl, sys.argv)

else:
    for year in years:
        vctYearUrl = urlBase + "/vct-" + str(year)
        print(year, vctYearUrl)