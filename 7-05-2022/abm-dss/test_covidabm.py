import covid_abm as cv
import defaults as df

main = cv.Main(df.covid_params)
main.run_simulation()