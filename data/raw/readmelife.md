# Remaining life expectancy at different ages - Data package

This data package contains the data that powers the chart ["Remaining life expectancy at different ages"](https://ourworldindata.org/grapher/remaining-life-expectancy-at-different-ages?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website.

## CSV Structure

The high level structure of the CSV file is that each row is an observation for an entity (usually a country or region) and a timepoint (usually a year).

The first two columns in the CSV file are "Entity" and "Code". "Entity" is the name of the entity (e.g. "United States"). "Code" is the OWID internal entity code that we use if the entity is a country or region. For normal countries, this is the same as the [iso alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) code of the entity (e.g. "USA") - for non-standard countries like historical countries these are custom codes.

The third column is either "Year" or "Day". If the data is annual, this is "Year" and contains only the year as an integer. If the column is "Day", the column contains a date string in the form "YYYY-MM-DD".

The remaining columns are the data columns, each of which is a time series. If the CSV data is downloaded using the "full data" option, then each column corresponds to one time series below. If the CSV data is downloaded using the "only selected data visible in the chart" option then the data columns are transformed depending on the chart type and thus the association with the time series might not be as straightforward.

## Metadata.json structure

The .metadata.json file contains metadata about the data package. The "charts" key contains information to recreate the chart, like the title, subtitle etc.. The "columns" key contains information about each of the columns in the csv, like the unit, timespan covered, citation for the data etc..

## About the data

Our World in Data is almost never the original producer of the data - almost all of the data we use has been compiled by others. If you want to re-use data, it is your responsibility to ensure that you adhere to the sources' license and to credit them correctly. Please note that a single time series may have more than one source - e.g. when we stich together data from different time periods by different producers or when we calculate per capita metrics using population data from a second source.

### How we process data at Our World In Data
All data and visualizations on Our World in Data rely on data sourced from one or several original data providers. Preparing this original data involves several processing steps. Depending on the data, this can include standardizing country names and world region definitions, converting units, calculating derived indicators such as per capita measures, as well as adding or adapting metadata such as the name or the description given to an indicator.
[Read about our data pipeline](https://docs.owid.io/projects/etl/)

## Detailed information about each time series


## Life expectancy at birth – totals, period tables – HMD
The period life expectancy at birth among totals, in a given year.
Last updated: October 22, 2025  
Next update: October 2026  
Date range: 1751–2023  
Unit: years  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data

#### Full citation
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data. “Life expectancy at birth – HMD – totals, period tables” [dataset]. Human Mortality Database, “Human Mortality Database”; United Nations, “World Population Prospects” [original data].
Source: Human Mortality Database (2025), UN, World Population Prospects (2024) – processed by Our World In Data

### What you should know about this data
* Period life expectancy is a metric that summarizes death rates across all age groups in one particular year.
* For a given year, it represents the average lifespan for a hypothetical group of people, if they experienced the same age-specific death rates throughout their whole lives as the age-specific death rates seen in that particular year.
* Prior to 1950, we use HMD (2025) data. From 1950 onwards, we use UN WPP (2024) data.

### Sources

#### Human Mortality Database
Retrieved on: 2025-10-22  
Retrieved from: https://www.mortality.org/Data/ZippedDataFiles  

#### United Nations – World Population Prospects
Retrieved on: 2024-12-02  
Retrieved from: https://population.un.org/wpp/downloads/  


## Life expectancy at 10 – totals, period tables – HMD
The remaining period life expectancy at age 10 among totals, in a given year.
Last updated: October 22, 2025  
Next update: October 2026  
Date range: 1751–2023  
Unit: years  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data

#### Full citation
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data. “Life expectancy at 10 – HMD – totals, period tables” [dataset]. Human Mortality Database, “Human Mortality Database”; United Nations, “World Population Prospects” [original data].
Source: Human Mortality Database (2025), UN, World Population Prospects (2024) – processed by Our World In Data

### What you should know about this data
* Period life expectancy is a metric that summarizes death rates across all age groups in one particular year.
* For a given year, it represents the remaining average lifespan for a hypothetical group of people, if they experienced the same age-specific death rates throughout the rest of their lives as the age-specific death rates seen in that particular year.
* This shows the remaining life expectancy among people who have already reached the age 10, using death rates from their age group and older age groups.
* Prior to 1950, we use HMD (2025) data. From 1950 onwards, we use UN WPP (2024) data.

### Sources

#### Human Mortality Database
Retrieved on: 2025-10-22  
Retrieved from: https://www.mortality.org/Data/ZippedDataFiles  

#### United Nations – World Population Prospects
Retrieved on: 2024-12-02  
Retrieved from: https://population.un.org/wpp/downloads/  


## Life expectancy at 15 – totals, period tables – HMD
The remaining period life expectancy at age 15 among totals, in a given year.
Last updated: October 22, 2025  
Next update: October 2026  
Date range: 1751–2023  
Unit: years  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data

#### Full citation
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data. “Life expectancy at 15 – HMD – totals, period tables” [dataset]. Human Mortality Database, “Human Mortality Database”; United Nations, “World Population Prospects” [original data].
Source: Human Mortality Database (2025), UN, World Population Prospects (2024) – processed by Our World In Data

### What you should know about this data
* Period life expectancy is a metric that summarizes death rates across all age groups in one particular year.
* For a given year, it represents the remaining average lifespan for a hypothetical group of people, if they experienced the same age-specific death rates throughout the rest of their lives as the age-specific death rates seen in that particular year.
* This shows the remaining life expectancy among people who have already reached the age 15, using death rates from their age group and older age groups.
* Prior to 1950, we use HMD (2025) data. From 1950 onwards, we use UN WPP (2024) data.

### Sources

#### Human Mortality Database
Retrieved on: 2025-10-22  
Retrieved from: https://www.mortality.org/Data/ZippedDataFiles  

#### United Nations – World Population Prospects
Retrieved on: 2024-12-02  
Retrieved from: https://population.un.org/wpp/downloads/  


## Life expectancy at 25 – totals, period tables – HMD
The remaining period life expectancy at age 25 among totals, in a given year.
Last updated: October 22, 2025  
Next update: October 2026  
Date range: 1751–2023  
Unit: years  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data

#### Full citation
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data. “Life expectancy at 25 – HMD – totals, period tables” [dataset]. Human Mortality Database, “Human Mortality Database”; United Nations, “World Population Prospects” [original data].
Source: Human Mortality Database (2025), UN, World Population Prospects (2024) – processed by Our World In Data

### What you should know about this data
* Period life expectancy is a metric that summarizes death rates across all age groups in one particular year.
* For a given year, it represents the remaining average lifespan for a hypothetical group of people, if they experienced the same age-specific death rates throughout the rest of their lives as the age-specific death rates seen in that particular year.
* This shows the remaining life expectancy among people who have already reached the age 25, using death rates from their age group and older age groups.
* Prior to 1950, we use HMD (2025) data. From 1950 onwards, we use UN WPP (2024) data.

### Sources

#### Human Mortality Database
Retrieved on: 2025-10-22  
Retrieved from: https://www.mortality.org/Data/ZippedDataFiles  

#### United Nations – World Population Prospects
Retrieved on: 2024-12-02  
Retrieved from: https://population.un.org/wpp/downloads/  


## Life expectancy at 45 – totals, period tables – HMD
The remaining period life expectancy at age 45 among totals, in a given year.
Last updated: October 22, 2025  
Next update: October 2026  
Date range: 1751–2023  
Unit: years  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data

#### Full citation
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data. “Life expectancy at 45 – HMD – totals, period tables” [dataset]. Human Mortality Database, “Human Mortality Database”; United Nations, “World Population Prospects” [original data].
Source: Human Mortality Database (2025), UN, World Population Prospects (2024) – processed by Our World In Data

### What you should know about this data
* Period life expectancy is a metric that summarizes death rates across all age groups in one particular year.
* For a given year, it represents the remaining average lifespan for a hypothetical group of people, if they experienced the same age-specific death rates throughout the rest of their lives as the age-specific death rates seen in that particular year.
* This shows the remaining life expectancy among people who have already reached the age 45, using death rates from their age group and older age groups.
* Prior to 1950, we use HMD (2025) data. From 1950 onwards, we use UN WPP (2024) data.

### Sources

#### Human Mortality Database
Retrieved on: 2025-10-22  
Retrieved from: https://www.mortality.org/Data/ZippedDataFiles  

#### United Nations – World Population Prospects
Retrieved on: 2024-12-02  
Retrieved from: https://population.un.org/wpp/downloads/  


## Life expectancy at 65 – totals, period tables – HMD
The remaining period life expectancy at age 65 among totals, in a given year.
Last updated: October 22, 2025  
Next update: October 2026  
Date range: 1751–2023  
Unit: years  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data

#### Full citation
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data. “Life expectancy at 65 – HMD – totals, period tables” [dataset]. Human Mortality Database, “Human Mortality Database”; United Nations, “World Population Prospects” [original data].
Source: Human Mortality Database (2025), UN, World Population Prospects (2024) – processed by Our World In Data

### What you should know about this data
* Period life expectancy is a metric that summarizes death rates across all age groups in one particular year.
* For a given year, it represents the remaining average lifespan for a hypothetical group of people, if they experienced the same age-specific death rates throughout the rest of their lives as the age-specific death rates seen in that particular year.
* This shows the remaining life expectancy among people who have already reached the age 65, using death rates from their age group and older age groups.
* Prior to 1950, we use HMD (2025) data. From 1950 onwards, we use UN WPP (2024) data.

### Sources

#### Human Mortality Database
Retrieved on: 2025-10-22  
Retrieved from: https://www.mortality.org/Data/ZippedDataFiles  

#### United Nations – World Population Prospects
Retrieved on: 2024-12-02  
Retrieved from: https://population.un.org/wpp/downloads/  


## Life expectancy at 80 – totals, period tables – HMD
The remaining period life expectancy at age 80 among totals, in a given year.
Last updated: October 22, 2025  
Next update: October 2026  
Date range: 1751–2023  
Unit: years  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data

#### Full citation
Human Mortality Database (2025); UN, World Population Prospects (2024) – processed by Our World in Data. “Life expectancy at 80 – HMD – totals, period tables” [dataset]. Human Mortality Database, “Human Mortality Database”; United Nations, “World Population Prospects” [original data].
Source: Human Mortality Database (2025), UN, World Population Prospects (2024) – processed by Our World In Data

### What you should know about this data
* Period life expectancy is a metric that summarizes death rates across all age groups in one particular year.
* For a given year, it represents the remaining average lifespan for a hypothetical group of people, if they experienced the same age-specific death rates throughout the rest of their lives as the age-specific death rates seen in that particular year.
* This shows the remaining life expectancy among people who have already reached the age 80, using death rates from their age group and older age groups.
* Prior to 1950, we use HMD (2025) data. From 1950 onwards, we use UN WPP (2024) data.

### Sources

#### Human Mortality Database
Retrieved on: 2025-10-22  
Retrieved from: https://www.mortality.org/Data/ZippedDataFiles  

#### United Nations – World Population Prospects
Retrieved on: 2024-12-02  
Retrieved from: https://population.un.org/wpp/downloads/  


    