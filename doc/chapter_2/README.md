# Chapter 2 - Practical Case : The Retailer's KPIs

## Objective

Through this practical case, you will use important aspects of the building of modern data pipelines.

You will focus on the business logic of converting raw data into data assets that are valuable to your company,
and leave the technical details of traditional data pipelining to Dagster.

In particular, you will

- Define your business logic as a graph of data assets
- Materialize and refresh your assets responding to business needs
- Attach visual meaning and context to the materialization of your assets
- Configure orchestration and persistence details in a decoupled way from your business logic

## Context

You are hired by a fashion retailer who would like to get insights into their business performance.

The kind of metrics they need are Key Performance Indicators (KPIs), and they are calculated by refining and aggregating basic operational data.

Their data team is able to provide a daily batch of operational data from their transactional system.

From this stream of operational data, they want to generate a stream of KPI data, which needs to be consumable by their BI tool for monitoring and analysis.

You will help the retailer integrate the materialization of KPI data into their system.

Good luck!

## Project

### General guidance

- To create an asset, annotate the method implementing the materialization logic with the `@asset`
- All assets defined the `chapter_2.assets` package are automatically imported by dagster
- To attach metadata to an asset, use the `add_output_metadata` method on the asset execution context within the materialization code.
- After modifying your assets, reload chapter 2 definitions from the dagster UI.
- All the scaffolding around your asset is pre-written outside of the `chapter_2.assets` package

### Assignments

1. Integration validation

   **Context**

   Your client's IT department gets in touch to validate that you can properly read the files from their system. They left a file in their environment, at `https://raw.githubusercontent.com/dfernandezcalle/stock-data/main/data/csv/2023-08-02/stock.csv`

   ---
   **Assignment**

   Create an `operational_data` asset (formatted as a pandas dataframe) attaching its number of records in the `num_records` metadata field.

    <details>
    <summary>TIPS</summary>

    - To easily convert a csv from an url to a dataframe, you can use `pd.read_csv(csv_url)`
    </details>

   ---

2. Functional validation

   **Context**

   The client wants to validate the calculation logic of their KPIs on the example operational data.

   ---
   **Assignment**

   Materialize the the following KPIs, each in its own asset, without re-materializing the example operational data

   - `revenue`, as the sum of the 'Sales' field
   - `units_sold`, as the sum of the 'Quantity' field
   - `average_sales_price`, as the division of `revenue` by `units_sold`


    <details>
    <summary>TIPS</summary>

    - A [simple sum on the dataframe's columns](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sum.html) should do the trick!
    </details>

   ---

3. Configurable integration

   **Context**

   Your client wants to test your pipeline with other files, but they did not tell you which ones yet.

   ---
   **Assignment**

   - Make your `operational_data` asset configurable at run time, through a `source_data_path` parameter
   - Try out materialization with a few different paths
     - `https://raw.githubusercontent.com/dfernandezcalle/stock-data/main/data/csv/2023-08-03/stock.csv`
     - `https://raw.githubusercontent.com/dfernandezcalle/stock-data/main/data/csv/2023-08-04/stock.csv`

   ---

4. Production Integration with Partitioning

   **Context**

   Your client is now comfortable with your ability to get the job done, and is ready to share their whole set of historical data with you. That's a lot of data, and obviously you won't want to refresh all of it on every run of the materialization.

   This is a great opportunity for you to partition your data set!

   ---
   **Assignment**

   Introduce daily paritioning in your pipeline

   > Test: Materialize a few partitions manually on upstream and downstream assets

   <details>
   <summary>TIPS</summary>

    - Partitioning needs to be introduced in all the assets of your pipeline
   </details>

    ---

5. Deliver Value - Send KPIs to File Storage

   Enough playing, your client now wants you to get value from your work, and wants to retrieve their KPIs in a S3 bucket, in JSON format.
   They also want to keep a snapshot of the operational data used to calculate the KPIs for auditability, or in case some more KPIs need to be calculated on the same operational data in the future.

   ---
   **Assignment**

   Materialize all your assets in JSON format in S3 (S3 is represented as localstack in the project)

   > Test: visualize the data in S3 using your web browser, under localstack_host/dagster/
   >
   > (if you are executing dagster in your local machine, local stack host is 127.0.0.1:4566, if you are executing it through codespaces, the host is exposed publicly, check out your codespace ports)


   <details>
   <summary>TIPS</summary>

   - There is an IO manager ready to take care of persistence for you under resources

   </details>

   ---


6. Deliver Value - Write KPIs to the client's data warehouse

   **Context**

   Your client fully trusts you now, and figures that you probably could take care of the integration of the data directly into their data warehouse.
   Your cousin is a database expert, she decided to give you a hand and made a contribution to your project under `cousins_assets`.
   Her solution does not look bad, but you feel that it has a lot of boilerplate. Let's take a look and try to make it better.


   ---
   **Assignment**

   - Try out your cousin's solution by incorporating it into your own assets. Make sure it persists value to the database (check the SQL Tools connection configured in your Dev Container) on a few partitions
   - Remove the data manipulation boilerplate from your cousin's solution using `PartitionedNumericTimeSeriesPostgresIOManager`

   ---


## Wrap-up

Congratulations! Through these assignments, you learned to
- Iteratively define as software a collection of inter-related assets
- Manipulate and visualize your software-defined assets through a web interface
- Flexibly change the persistence mechanisms of your assets
