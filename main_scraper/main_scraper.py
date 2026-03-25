from match_scraper import vct_scraper
import sys

years = [2024, 2025, 2026]

urlBase = "https://www.vlr.gg"

print(sys.argv, len(sys.argv))

if len(sys.argv) >= 3:
    if sys.argv[1] == '--match-year':
        yearsFocused = sys.argv[2:]
        for year in yearsFocused:
            vctYearUrl = urlBase + "/vct-" + year
            # print(year, vctYearUrl)
            vct_scraper(vctYearUrl)

else:
    for year in years:
        vctYearUrl = urlBase + "/vct-" + str(year)
        print(year, vctYearUrl)