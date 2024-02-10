{% docs __overview__ %}
# SpaceX - Starlink Satellite Launch Data

## Overview
This dbt project focuses on modeling data related to SpaceX's Starlink satellite launches. Starlink is a database containing information about the launches of Starlink satellites up until 2022. The purpose of this project is to clean and transform the raw Starlink data to create a model that can be used to make predictions about future launches.

## Sources
- **Source:** `starlink`
- **Description:** The `starlink` table contains information about launches of Starlink satellites until 2022. This data serves as the primary source for this dbt project.

## Models
- **Description:** The `starlink_prediction` model is responsible for cleaning and transforming the Starlink data. It prepares the data in a format that can be used to make predictions about future satellite launches. This model is essential for forecasting and analyzing trends in Starlink satellite deployments.

## Documentation
- **Tests:** Implemented
- **Description:** The Starlink Prediction model has been thoroughly documented to provide insights into its purpose, usage, and underlying logic. Additionally, tests have been implemented to ensure the accuracy and reliability of the model's transformations.

## Prediction
### Historical Data 
- Number of SpaceX launches of starlink satellites, so far: 68
- Number of satellites launched so far: 5297

### Prediction by when SpaceX will reach 42000 satellites with number of launches it will take:
- Estimated number of launches needed to reach 42,000 Starlink satellites: 471
- The date by when Spacex will launch 42000 Starlink satellites is predicted to be approximately: 2049-12-30!!

The above prediction is made using the historical data of Starlink launches in the SpaceX API. 
For more detailed information about SpaceX API, 
- Read: https://github.com/r-spacex/SpaceX-API/blob/master/docs/README.md
{% enddocs %}
