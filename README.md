# ELT Pipeline for Starlink Prediction

## Overview

This repository contains an ELT (Extract, Load, Transform) pipeline designed to predict Starlink satellite launches. The pipeline is implemented using Meltano, a data integration platform, and consists of several steps to configure the pipeline, extract data from the SpaceX API, load it into a PostgreSQL database, perform data transformation using dbt (data build tool), and generate documentation.

## How to run this pipeline

#### There are two different ways to run the pipeline and see the prediction
1. Github Actions (preferred)

2. Shell Script (Has prerequisite dependencies)

> Since the Github Actions is the deployment mode in production, I would prefer running the pipeline using it. 

> To run the pipeline locally, you can use the shell script. 

## Usage - Github Actions

To run the ELT pipeline and predict Starlink launches:

1. Navigate to the GitHub Actions tab and selecting the workflow run `ELT Pipeline for Starlink Prediction`

2. Click on `Run Workflow`

3. Once the workflow is triggered, click on the workflow execution and build to see the steps being executed. 


### Check `Run the prediction script!` block in Github Actions job to see the final output.

## Usage - Shell Script
### Prerequisites
1. Install Python
- Python 3.9 or above

2. Create a virtual environment in python
- Run `python3 -m venv meltano_env`
- Run `source meltano_env/bin/activate`
3. Install Docker and start Docker service

### Running the shell script - execute_pipeline.sh
1. Clone the repo :) 

2. cd into `starlink_assignment` folder. 

3. Make sure the shell script is executable:
- Run `chmod u+x execute_pipeline.sh` 

4. Finally run: `./execute_pipeline.sh`

5. The prediction will be displayed in the terminal. 
> This will take a couple mins to complete, sit back and relax!

- The output will be displayed in terminal. After 10 seconds, a DBT document will open on your browser with the results. 

## Implementation details
### Custom Extractor for SpaceX API 
- I've implemented a custom extractor `tap-spacexapi` to fetch SpaceX API data of starlink launches. 
- API endpoint: `https://api.spacexdata.com/v4/starlink`
- Since this is a Meltano project on its own, I've decoupled the extractor from my ELT pipeline code to make it easier to update and maintain this tap.


### Postgres Data loader

#### Prerequisite: Docker 
- To configure the `target-postgres` loader, Docker is a prerequisite. 
- I've setup a `docker-compose.yml` to create a docker container with postgres running on it. 

#### target-postgres loader
- I've configured a Meltano project to build my ELT pipeline. 

- Next, I've installed the `target-postgres` loader to load the data from API.

- Added configs like database and user credentials

## Postgres DBT transformer
- I've configured and installed the `dbt-postgres` utility to transform the data in postgres. 

- I've created a new schema via configs to store the transformed data on which prediction is done. 

- I've encountered a bug in `dbt-postgres` utility. As a workaround, I've written a Python script to fix it.

- I've raised this issue to Meltano and couple PRs to fix the issue in the meltano repo. 

- > Issue: https://github.com/meltano/meltano/issues/8391

- > PR: https://github.com/meltano/meltano/issues/8391

- > PR: https://github.com/meltano/edk/pull/206

- Exciting times indeed!

## Meltano jobs
- To run the meltano ELT pipeline in order, I've configured meltano jobs.

- For easy debugging and maintenance, I've split the pipeline execution into different jobs

- `extract_and_load_data` - Extracts data from SpaceX API and ingests into `postgres.tap-spacexapi.starlink` table. 

- `transform_data` - Transforms the data in the `starlink` table (mentioned above) using dbt. 

- > Finally the transformed data is ingested to `postgres.analytics.starlink_prediction` table. This will be used to make the predictions. 

- `dbt_tests` - Runs dbt tests on data to ensure integrity of the data in final table `starlink_prediction`.

- `generate_dbt_docs` - Runs the dbt docs generate command to display the document I've created. 

## Making the prediction! :) 
- Finally, The result of all the effort, to answer this question. 

> When will there be 42,000 Starlink satellites in orbit, and how many launches will it take to get there?

- I've created a python script `prediction.py` within the `starlink_prediction` folder to make the prediction.

- This script uses the transformed data in the final table `starlink_prediction`, loads data into a CSV. Implements linear regression and prediction methods to fetch the answer to both the questions. 

## Prediction results
### Historical Data 
- Number of SpaceX launches of starlink satellites, so far: 68
- Number of satellites launched so far: 5297

#### Prediction by when SpaceX will reach 42000 satellites with number of launches it will take:
- Estimated number of launches needed to reach 42,000 Starlink satellites: `471`

- The date by when Spacex will launch 42000 Starlink satellites is predicted to be approximately: `2049-12-30` !



## Documentation
- I've used `dbt-docs` to serve documentation

- I've added description for each column of the `starlink_prediction` table, and an overview page. 

- The document can be accessed by running `meltano invoke dbt-postgres:docs-serve`

## Deployment in Production
- I've used Github Actions to run the entire setup, ELT pipeline and the final prediction script.






## Workflow File

The workflow file (`workflow.yml`) defines the automation process for executing the ELT pipeline. It is triggered manually through GitHub Actions and runs on an Ubuntu latest environment. The workflow consists of the following steps:

1. **Checkout Repository**: Clones the repository to the workflow runner.

2. **Configure ELT Pipeline**: Configures the Meltano ELT pipeline for Starlink prediction, including copying configuration files and installing Python dependencies.

3. **Add Custom SpaceX API Extractor**: Adds the custom extractor `tap-spacexapi` to extract data from the SpaceX API.

4. **Start Docker Container with Postgres**: Starts a local Docker container with a PostgreSQL database for data loading.

5. **Add Postgres Loader**: Adds the loader `target-postgres` to load extracted data into the PostgreSQL database.

6. **Add dbt-postgres Utility**: Adds the utility `dbt-postgres` for further data transformation and analysis using dbt.

7. **Fix Bug in dbt-postgres**: Fixes any bugs or issues related to the dbt-postgres utility.

8. **Add Meltano Jobs to run the pipeline**: Adds Meltano jobs for the ELT pipeline, specifying tasks for data extraction, transformation, testing, and documentation generation.

9. **Run the ELT Pipeline**: Executes the ELT pipeline by running Meltano jobs for data extraction, transformation, testing, and documentation generation.

10. **Run the Prediction Script**: Executes the prediction script (`prediction.py`) to predict Starlink launches.


## Improvement plans!
#### 1. Publish my custom extractor `tap-spacexapi` to PyPI. 
- I will publish my custom extractor to PyPI. 

- With my extractor published, we can do a pip install in the meltano project to access it instead of having the extractor in this codebase. 


#### 2. Better forecasting logic for 42000 launches. 
- As mentioned in the assignment instructions, I did assume we have a team of Analysts to predict the launches once the data is available. 

- Nevertheless, I've tried to make a decent prediction using Linear regression and forecasting methods.

- We can try other ML models to improve accuracy of the prediction.

#### 3. Github Secrets for all passwords
- Ideally in production, we must store them in Github Secrets and reference them in the Github Actions workflow. 

- This would require admin priveleges to add these secrets to repository settings. But this will be my top priority if I push my code to production!


#### 4. Unit tests for prediction.py 
- I will right more unit tests, implement exception handling for the python file that does the prediction of starlink launches.

#### 5. Data quality, data cleaning
- The SpaceX API data does have inconsistencies.

- I've implemented checks in DBT to filter `NULL` values and discard irrelevant records. 

- However, we can enforce strict data quality checks on the API data during data extraction and loading itself. 

#### 6. Dashboard to track starlink satellite launches  
- This would be a cool feature I'd like to implement using data visualization tools like Metabase, Redash or Chartbrew. 

- This will help to track the satellite launches in realtime using a dashboard. 

- I would refresh the data in this dashboard every week or so to fetch data from API and get latest info on the launches. 

#### 7. Documentation and code improvements
- I will add a detailed doc of my implementation for anyone to try building this project from scratch. 

- Add more Comments, docstrings wherever required. 

- Fix warnings

> This was a great exercise to work on!!
-----