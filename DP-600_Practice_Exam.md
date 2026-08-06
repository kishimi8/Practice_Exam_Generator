# DP-600: Implementing Analytics Solutions Using Microsoft Fabric
## Practice Exam (50 Questions)

*This is an original practice exam designed to reflect the skills measured by the DP-600 certification. It is not sourced from or affiliated with Microsoft's official exam content. Domain weightings roughly mirror the published exam objectives:*

- *Plan, implement, and manage a solution for data analytics (10–15%)*
- *Prepare and serve data (40–45%)*
- *Implement and manage semantic models (20–25%)*
- *Explore and analyze data (20–25%)*

Choose the single best answer unless otherwise noted. An answer key with explanations follows the questions.

---

## Domain 1: Plan, Implement, and Manage a Solution for Data Analytics

**1.** You need to create a Fabric workspace that will be billed against your organization's Fabric capacity. Which workspace setting must you configure to link the workspace to that capacity?

A) Workspace access control
B) Workspace license mode / capacity assignment
C) OneLake data access roles
D) Git integration settings

**2.** Your organization wants developers to work on Fabric items using a branching workflow with pull requests, syncing changes back to workspaces. Which Fabric feature should you configure?

A) Deployment pipelines
B) Git integration
C) OneLake shortcuts
D) Workspace monitoring

**3.** You are promoting a set of Fabric items (a lakehouse, notebooks, and a semantic model) from a Development workspace to a Test workspace, then to Production. Which feature is purpose-built for this?

A) OneLake shortcuts
B) Deployment pipelines
C) Fabric domains
D) Workspace roles

**4.** A workspace admin needs to grant a business analyst the ability to view and edit reports but NOT manage workspace settings or add members. Which workspace role should be assigned?

A) Admin
B) Member
C) Contributor
D) Viewer

**5.** You want to organize workspaces across the organization by business unit (e.g., Finance, Sales) for governance and discoverability purposes. Which Fabric feature should you use?

A) Domains
B) Capacities
C) Deployment pipelines
D) Endorsements

**6.** Which Fabric item type would you use to grant read access to a lakehouse's data to users who should not be able to modify pipelines or notebooks in the workspace?

A) Assign them the Admin role
B) Assign them the Viewer role
C) Assign them the Contributor role
D) Grant them capacity administrator rights

**7.** You need to monitor capacity utilization across Fabric workloads (Power BI, Data Engineering, Data Warehouse) to identify throttling risk. Which tool should you use?

A) Fabric Capacity Metrics app
B) OneLake file explorer
C) Purview Data Map
D) Deployment pipeline history

**8.** An item in a workspace has been marked "Certified." What does this endorsement primarily signal to consumers?

A) The item is protected by sensitivity labels
B) The item has passed organizational quality/governance review
C) The item is automatically refreshed hourly
D) The item cannot be modified by anyone

---

## Domain 2: Prepare and Serve Data

**9.** You need to store both structured (Delta tables) and unstructured (files) data in a single Fabric item that data engineers and data scientists can access through Spark. Which item should you create?

A) Data warehouse
B) Lakehouse
C) Dataflow Gen2
D) KQL database

**10.** You are building a data warehouse in Fabric and want to write T-SQL to create tables and load data. Which experience should you use?

A) Lakehouse SQL analytics endpoint (read-only)
B) Warehouse item with the SQL editor
C) KQL Queryset
D) Power Query Editor in Dataflow Gen2

**11.** Which Fabric item allows low-code, Power Query-based transformation with the output automatically landing as Delta tables in OneLake?

A) Data pipeline
B) Dataflow Gen2
C) Notebook
D) Eventstream

**12.** You need to orchestrate a sequence of activities: copy data from an on-premises SQL Server, then run a notebook, then refresh a semantic model. Which Fabric item is best suited?

A) Dataflow Gen2
B) Data pipeline
C) Eventstream
D) KQL Database

**13.** To connect to an on-premises SQL Server from Fabric, what must you install and configure?

A) A OneLake shortcut
B) An on-premises data gateway
C) A Fabric domain
D) A deployment pipeline

**14.** What is a OneLake shortcut primarily used for?

A) Compressing Delta tables to reduce storage costs
B) Referencing data stored in another location (e.g., another lakehouse, ADLS Gen2, S3) without copying it
C) Creating a scheduled refresh for a dataflow
D) Assigning row-level security to a table

**15.** You want to ingest a continuous stream of IoT telemetry data and analyze it with near real-time queries. Which Fabric item is designed for this scenario?

A) Dataflow Gen2
B) Eventstream + KQL Database
C) Data warehouse
D) Lakehouse with a scheduled pipeline

**16.** In a medallion architecture implemented in a Fabric lakehouse, which layer typically contains raw, unaltered source data?

A) Gold
B) Silver
C) Bronze
D) Platinum

**17.** Which Spark language(s) can you use in a Fabric notebook to transform data in a lakehouse? (Select all that apply)

A) PySpark
B) Spark SQL
C) Scala
D) Spark R
E) All of the above

**18.** You need to enforce that only rows where `Region = 'West'` are visible to a specific group of warehouse users. Which feature should you implement?

A) Sensitivity labels
B) Row-level security (RLS)
C) OneLake shortcuts
D) Deployment pipeline rules

**19.** What is the primary difference between a Fabric Lakehouse and a Fabric Warehouse in terms of write access?

A) Lakehouses support only read access; warehouses support only write access
B) Lakehouses support both Spark and T-SQL reads (via SQL analytics endpoint, read-only) with Spark writes; warehouses support full T-SQL read/write
C) Warehouses cannot store Delta tables
D) There is no meaningful difference

**20.** You need to schedule a Dataflow Gen2 to refresh every night at 2 AM. Where do you configure this?

A) In the notebook's Spark session settings
B) In the dataflow's own scheduled refresh settings
C) In the workspace's Git integration settings
D) In the Fabric Capacity Metrics app

**21.** Which file format is the native storage format for tables in a Fabric Lakehouse?

A) Parquet only
B) Delta (Parquet + transaction log)
C) CSV
D) Avro

**22.** You need to incrementally load only new or changed rows from a source table into your lakehouse rather than reloading all data each time. Which technique is most appropriate?

A) Full load with TRUNCATE and reload every run
B) Incremental refresh / watermark-based incremental load in the pipeline or dataflow
C) Manual file upload
D) OneLake shortcut

**23.** A data engineer wants to optimize a large Delta table by compacting small files and improving read performance. Which command should they run in a notebook?

A) VACUUM only
B) OPTIMIZE (with optional Z-ORDER)
C) DROP TABLE and recreate
D) MERGE

**24.** Which Fabric item would you use to write real-time queries against streaming telemetry using a SQL-like syntax optimized for time-series and log data?

A) T-SQL in a Warehouse
B) KQL (Kusto Query Language) in a KQL Queryset
C) DAX in a semantic model
D) Power Query in a Dataflow

**25.** You are designing a pipeline that must call a notebook conditionally based on the outcome of a prior activity. Which pipeline construct enables this?

A) ForEach activity only
B) If Condition / Switch activity
C) Lookup activity only
D) Wait activity only

**26.** What is the purpose of the "Copy data" activity in a Fabric data pipeline?

A) To duplicate an entire workspace
B) To move/copy data from a source to a destination, optionally with schema mapping
C) To copy a Power BI report between workspaces
D) To back up a semantic model

**27.** Which of the following is true about OneLake?

A) It is a separate storage account per workspace that must be manually provisioned
B) It is a single, unified, tenant-wide data lake built on ADLS Gen2 that all Fabric items store data in
C) It only stores Power BI datasets
D) It requires a separate Azure subscription

**28.** You need to give a partner organization read access to specific Delta tables in your lakehouse without exporting or duplicating the data. What should you use?

A) External sharing / OneLake shortcuts to their tenant (where supported) or workspace sharing with appropriate permissions
B) Export to CSV and email the file
C) Publish to web
D) Screen sharing during a meeting

---

## Domain 3: Implement and Manage Semantic Models

**29.** What is the primary difference between Import mode and DirectQuery mode in a Power BI semantic model?

A) Import mode always queries the source live; DirectQuery caches data in memory
B) Import mode loads a compressed copy of the data into the model's memory; DirectQuery sends queries to the source at report run-time
C) There is no meaningful difference
D) DirectQuery only works with Excel files

**30.** Which storage mode combines Import and DirectQuery within a single semantic model, allowing some tables to be cached and others queried live?

A) Dual mode / Composite model
B) Live Connect
C) Direct Lake
D) Push mode

**31.** What is Direct Lake mode designed to do?

A) Cache data in a separate Azure SQL Database
B) Load data directly from Delta tables in OneLake into the semantic model's memory representation without a traditional import/refresh ETL step
C) Replace the need for a lakehouse entirely
D) Only work with on-premises data sources

**32.** You need to create a calculated column that concatenates FirstName and LastName in a semantic model. Which language should you use?

A) T-SQL
B) KQL
C) DAX
D) Python

**33.** Which DAX function would you use to calculate a running total of Sales by date within the current filter context?

A) SUM
B) CALCULATE combined with a date filter (e.g., using FILTER and ALL/ALLSELECTED)
C) CONCATENATE
D) LOOKUPVALUE

**34.** You want to define a relationship between a Sales table and a Date table where one date row can relate to many sales rows. What cardinality should this relationship have?

A) Many-to-many
B) One-to-many (one side on Date, many side on Sales)
C) Many-to-one (Sales to Date)
D) One-to-one

**35.** What is the purpose of a star schema in semantic modeling?

A) To normalize all tables to reduce redundancy as much as possible
B) To organize data into fact tables (measures/events) and dimension tables (descriptive attributes) for optimized analytical querying
C) To store unstructured JSON data efficiently
D) To eliminate the need for relationships

**36.** You need to hide the technical key columns used only for relationships from report authors browsing the field list. What should you do?

A) Delete the columns
B) Set the column's "Is Hidden" property to true
C) Rename the columns to start with an underscore
D) Move them to a different table

**37.** Which feature allows you to define reusable, named business calculations (like "Total Revenue" or "YoY Growth") directly in the semantic model for consistent use across reports?

A) Calculated columns
B) Measures (DAX)
C) Power Query steps
D) Row-level security roles

**38.** You need to restrict report viewers so that a regional manager only sees data for their own region when viewing the same report as other managers. Which feature should you configure?

A) Object-level security only
B) Row-level security (RLS) with DAX filter expressions tied to user identity
C) Workspace roles
D) Sensitivity labels

**39.** What is the benefit of enabling "Large semantic model storage format" for a model approaching or exceeding 1 GB?

A) It disables compression
B) It removes the model size limitations associated with the default small dataset storage format, allowing larger models within capacity limits
C) It converts the model automatically to DirectQuery
D) It disables refresh scheduling

**40.** Which tool would you use to analyze and optimize the performance of DAX queries and identify expensive visuals or measures in a semantic model?

A) Performance Analyzer in Power BI Desktop
B) OneLake file explorer
C) Deployment pipelines
D) Git integration

**41.** You need to schedule automatic refresh of an Import-mode semantic model that pulls from a lakehouse. What must be true for scheduled refresh to succeed if the source requires credentials?

A) Nothing; scheduled refresh never requires credentials
B) Valid, configured data source credentials (and gateway, if needed) must be set for the semantic model
C) The model must be converted to Direct Lake
D) The workspace must be in Development mode

**42.** What is a key advantage of Direct Lake mode over traditional Import mode for very large fact tables?

A) It requires no data at all
B) It avoids the need to fully import/refresh large volumes of data while still providing near-import-level query performance
C) It only works with CSV files
D) It eliminates the need for measures

---

## Domain 4: Explore and Analyze Data

**43.** You want to quickly explore a lakehouse table's data distribution without writing code. Which Fabric feature allows this directly from the lakehouse UI?

A) Data pipeline monitoring
B) Lakehouse "Load to Tables" preview / SQL analytics endpoint query
C) Deployment pipeline comparison
D) Capacity Metrics app

**44.** A business user wants to ask natural-language questions like "What were total sales last quarter?" against a semantic model without writing DAX. Which Power BI feature supports this?

A) Q&A visual / Copilot for Power BI
B) Row-level security
C) Deployment pipelines
D) OneLake shortcuts

**45.** Which visual would be most appropriate to show the trend of monthly revenue over the past two years?

A) Pie chart
B) Line chart
C) Card visual
D) Matrix with no axis

**46.** You need to allow report consumers to dynamically switch between viewing Sales by Region vs. Sales by Product on the same visual. Which feature enables this?

A) Bookmarks only
B) Field parameters
C) Row-level security
D) Deployment pipelines

**47.** What is the purpose of a Power BI dashboard versus a report?

A) A dashboard is a single-page, pinned-tile summary view often aggregating visuals from multiple reports; a report is a multi-page, interactive analytical document
B) They are functionally identical
C) A dashboard can only show one visual
D) A report cannot be shared

**48.** You want business analysts to explore a semantic model's data in Excel using PivotTables connected live to the model. Which feature supports this?

A) Analyze in Excel
B) Export to PDF
C) Deployment pipelines
D) OneLake shortcuts

**49.** Which DAX time intelligence function would you use to calculate year-to-date sales?

A) SAMEPERIODLASTYEAR
B) TOTALYTD
C) DATEADD
D) PARALLELPERIOD

**50.** A stakeholder wants a single number showing current total sales, prominently displayed, with no axes or categories. Which visual type is most appropriate?

A) Card
B) Stacked bar chart
C) Scatter chart
D) Ribbon chart

---

## Answer Key with Explanations

**1. B** — Workspaces must be assigned to a Fabric (or Premium) capacity to be billed against it and unlock Fabric workloads.

**2. B** — Git integration connects a workspace to a Git repository (Azure DevOps/GitHub) enabling branching, commits, and pull requests.

**3. B** — Deployment pipelines manage promotion of content across Development, Test, and Production stages.

**4. C** — Contributor can edit content but cannot manage workspace access or settings like Admin/Member can.

**5. A** — Domains group workspaces by business area for governance, ownership, and discoverability.

**6. B** — Viewer role grants read-only access to content without edit or management rights.

**7. A** — The Fabric Capacity Metrics app provides visibility into capacity unit (CU) consumption and throttling.

**8. B** — Certification indicates the item has been reviewed and approved by a governance authority in the organization.

**9. B** — A Lakehouse stores structured (Delta tables) and unstructured (files) data, accessible via Spark and a SQL analytics endpoint.

**10. B** — The Warehouse item provides a full read/write T-SQL experience.

**11. B** — Dataflow Gen2 uses Power Query and outputs data as Delta tables in OneLake.

**12. B** — Data pipelines orchestrate multi-step workflows across diverse activities including copy, notebook, and refresh operations.

**13. B** — An on-premises data gateway is required to securely connect cloud services to on-premises data sources.

**14. B** — Shortcuts are pointers to data in another location, avoiding data duplication.

**15. B** — Eventstream ingests streaming data and can route it to a KQL Database for real-time analytical queries.

**16. C** — Bronze is the raw ingestion layer; Silver is cleansed/conformed; Gold is business-level aggregated data.

**17. E** — Fabric notebooks support PySpark, Spark SQL, Scala, and SparkR.

**18. B** — Row-level security restricts which rows a user can query based on their identity or role.

**19. B** — Lakehouses expose a read-only SQL analytics endpoint alongside Spark read/write; Warehouses support full T-SQL read/write natively.

**20. B** — Scheduled refresh is configured on the dataflow item itself.

**21. B** — Delta format (Parquet files plus a transaction log) is the native lakehouse table format.

**22. B** — Incremental/watermark-based loading avoids reprocessing unchanged data.

**23. B** — OPTIMIZE (optionally with Z-ORDER) compacts files and improves query performance; VACUUM removes old files but doesn't compact.

**24. B** — KQL is purpose-built for querying time-series/log/telemetry data efficiently.

**25. B** — If Condition (or Switch) enables conditional branching logic in a pipeline.

**26. B** — Copy data activity moves data between a source and sink, with optional schema/column mapping.

**27. B** — OneLake is a single, tenant-wide lake (built on ADLS Gen2) shared across all Fabric workloads.

**28. A** — External sharing capabilities (where enabled) or shortcuts let partners access specific data without duplication; exporting files is not the intended governed approach.

**29. B** — Import caches a compressed copy in memory for fast queries; DirectQuery executes queries against the source at run-time.

**30. A** — Composite/dual mode models combine Import and DirectQuery tables in one model.

**31. B** — Direct Lake reads Delta tables directly from OneLake into memory for query, skipping a traditional import/refresh pipeline.

**32. C** — DAX is the formula language used for calculated columns, measures, and calculated tables in semantic models.

**33. B** — A running total typically uses CALCULATE with a filter expression (e.g., dates ≤ current date) rather than SUM alone.

**34. B** — The "one" side is Date, "many" side is Sales — a standard one-to-many relationship in a star schema.

**35. B** — Star schema separates facts (measures) from dimensions (descriptive attributes) for efficient, intuitive analytical queries.

**36. B** — Setting "Is Hidden" hides a field from the report field list while keeping it usable for relationships/calculations.

**37. B** — Measures are reusable DAX calculations defined once in the model and reused across reports.

**38. B** — RLS with DAX filter expressions (often tied to USERPRINCIPALNAME()) restricts visible rows per user.

**39. B** — Large semantic model storage format removes the default size cap tied to small-model storage, subject to capacity limits.

**40. A** — Performance Analyzer in Power BI Desktop captures visual/DAX query durations to identify bottlenecks.

**41. B** — Scheduled refresh requires valid configured credentials (and a gateway if the source is on-premises or requires one).

**42. B** — Direct Lake avoids a full import/refresh cycle for large data volumes while approaching Import-mode query speed.

**43. B** — You can preview/query lakehouse table data directly via the UI or SQL analytics endpoint without external tools.

**44. A** — The Q&A visual (and Copilot capabilities) let users ask natural-language questions against a semantic model.

**45. B** — A line chart is best suited to show trends over a continuous time period.

**46. B** — Field parameters let users dynamically swap the field(s) used in a visual, such as switching between Region and Product.

**47. A** — Dashboards are single-page pinned-tile summaries (often cross-report); reports are multi-page interactive documents built on a single dataset.

**48. A** — Analyze in Excel connects Excel PivotTables live to a published semantic model.

**49. B** — TOTALYTD calculates a year-to-date aggregation directly; SAMEPERIODLASTYEAR and DATEADD shift periods rather than accumulate YTD.

**50. A** — The Card visual displays a single prominent value with no axes or categories.

---

### Scoring Guide
- 45–50 correct: Excellent — you're likely exam-ready.
- 38–44 correct: Good — review the domain(s) where you missed the most questions.
- Below 38: Spend more time with hands-on practice in Fabric (lakehouses, warehouses, pipelines, semantic models) before scheduling the exam.
