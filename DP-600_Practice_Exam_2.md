# DP-600: Implementing Analytics Solutions Using Microsoft Fabric
## Practice Exam #2 (50 Questions)

*This is an original practice exam designed to reflect the skills measured by the DP-600 certification. It is not sourced from or affiliated with Microsoft's official exam content. This set covers new questions distinct from Practice Exam #1.*

- *Plan, implement, and manage a solution for data analytics (10–15%)*
- *Prepare and serve data (40–45%)*
- *Implement and manage semantic models (20–25%)*
- *Explore and analyze data (20–25%)*

Choose the single best answer unless otherwise noted. An answer key with explanations follows the questions.

---

## Domain 1: Plan, Implement, and Manage a Solution for Data Analytics

**1.** Which Fabric capacity concept determines how much compute is available across all Fabric workloads in workspaces assigned to it?

A) Storage account tier
B) Capacity Units (CUs)
C) Workspace role
D) Tenant region

**2.** A workspace admin notices that a capacity is frequently being throttled during business hours. Which action would most directly help diagnose the cause?

A) Reviewing the Fabric Capacity Metrics app for CU consumption by item and operation
B) Deleting all Viewer role assignments
C) Disabling Git integration
D) Renaming the workspace

**3.** Which statement about Fabric trial capacities is accurate?

A) They never expire
B) They provide a temporary, no-cost way to explore Fabric features before committing to a paid capacity
C) They can only be used for Power BI, not other workloads
D) They require an Azure subscription with pay-as-you-go billing

**4.** You want to prevent accidental deletion of a critical production workspace. Which practice helps mitigate this risk?

A) Restricting Admin role assignment to a small, controlled group and relying on deployment pipeline stage protections
B) Giving every user Admin rights so anyone can restore it
C) Disabling workspace monitoring
D) Removing the workspace from a capacity

**5.** In a deployment pipeline with Dev, Test, and Prod stages, what happens when you use "deployment rules" for a data source connection in the Test stage?

A) Nothing; deployment rules are not supported
B) They let you override specific configuration values (e.g., connection strings) so items behave correctly in that stage without manual reconfiguration each deployment
C) They automatically delete the Dev stage
D) They convert semantic models to DirectQuery

**6.** Which of the following best describes the purpose of sensitivity labels in Fabric?

A) To classify and protect content (e.g., Confidential, Public) and optionally enforce protections like encryption
B) To assign workspace roles
C) To schedule refreshes
D) To configure Git branches

**7.** A team wants a lightweight way to track lineage — which items feed which downstream reports — across a workspace. Which Fabric feature helps visualize this?

A) Lineage view
B) Capacity Metrics app
C) OneLake shortcuts
D) RLS editor

**8.** Which role is required, at minimum, to assign a workspace to a Fabric capacity?

A) Viewer
B) Contributor
C) Capacity Admin (or workspace Admin with appropriate capacity permissions)
D) Member

---

## Domain 2: Prepare and Serve Data

**9.** You need to combine data from a lakehouse table and an on-premises SQL Server table into a single query for ad hoc analysis without building a full pipeline. What is a reasonable low-code approach?

A) Use Dataflow Gen2 to connect to both sources and merge queries in Power Query
B) Manually export both to CSV and merge in Notepad
C) This is not possible in Fabric
D) Use only DAX

**10.** What does the Fabric SQL analytics endpoint of a lakehouse provide?

A) A read-only T-SQL interface for querying lakehouse Delta tables
B) A full read/write T-SQL interface identical to a Warehouse
C) A way to run Spark jobs
D) A way to edit Power Query steps

**11.** You need to write a Spark job that reads a CSV file from the lakehouse Files section, cleans it, and writes it as a managed Delta table. Which Fabric item should you use?

A) KQL Queryset
B) Notebook
C) Power BI report
D) Deployment pipeline

**12.** Which pipeline activity would you use to look up a single configuration value (e.g., last watermark date) from a table before running the rest of the pipeline?

A) Copy activity
B) Lookup activity
C) Wait activity
D) Set variable only

**13.** What is the main purpose of the "Get Data" experience when creating a new Dataflow Gen2?

A) To connect to and select source data before applying Power Query transformations
B) To assign RLS roles
C) To create a new workspace
D) To publish a Power BI report

**14.** A pipeline needs to run the same set of activities once per file in a folder containing 100 files. Which activity should wrap the logic?

A) If Condition
B) ForEach
C) Lookup
D) Copy data

**15.** Which of the following is a valid reason to use a Warehouse instead of a Lakehouse for a given workload?

A) The team primarily writes T-SQL and needs full read/write DDL/DML support with multi-table transactions
B) The team only needs to store unstructured images
C) The team wants to use PySpark exclusively
D) There is no valid reason; they are identical

**16.** What does "schema-on-read" mean in the context of a lakehouse Files section?

A) The schema is enforced strictly at write time for all files
B) Structure/schema is interpreted only when the data is read/queried, since raw files aren't necessarily structured or validated at ingestion
C) It refers to a feature that does not exist in Fabric
D) It means files cannot be queried at all

**17.** Which command would you use in a Fabric notebook to remove old, unreferenced data files from a Delta table after running OPTIMIZE?

A) VACUUM
B) DELETE FROM
C) TRUNCATE TABLE
D) DROP TABLE

**18.** You need near real-time ingestion of clickstream events from a web application into Fabric for dashboarding within seconds of occurrence. Which combination is most appropriate?

A) Dataflow Gen2 scheduled hourly
B) Eventstream feeding a KQL Database or lakehouse, paired with a real-time dashboard
C) A nightly pipeline with Copy activity
D) Manual CSV upload

**19.** What is the effect of applying a Z-ORDER during an OPTIMIZE operation on a Delta table?

A) It alphabetically sorts column names
B) It co-locates related data in the same files based on specified columns, improving read performance for filters on those columns
C) It deletes duplicate rows
D) It encrypts the table

**20.** Which authentication method is commonly used for a Fabric pipeline's Copy activity connecting to an Azure Data Lake Storage Gen2 source?

A) Only anonymous access
B) Service principal, managed identity, or account key/SAS token, depending on configuration
C) Only Windows NTLM
D) Only email/password

**21.** A data engineer wants to enforce schema consistency (matching column names/types) when writing to a Delta table, rejecting writes that don't match. What Delta feature supports this?

A) Schema enforcement (schema validation on write)
B) VACUUM
C) Shortcuts
D) Sensitivity labels

**22.** Which statement about shortcuts and Delta tables is correct?

A) A shortcut to a folder containing Delta-formatted data can be read as a table without copying the underlying files
B) Shortcuts always copy the full dataset into the destination lakehouse
C) Shortcuts only work within the same workspace
D) Shortcuts cannot reference cloud storage outside of OneLake

**23.** What is the primary benefit of using parameters in a Dataflow Gen2 or pipeline?

A) They make the object read-only
B) They allow reusable, dynamic configuration (e.g., file paths, dates) without hardcoding values
C) They automatically create semantic models
D) They enable Git integration

**24.** You need to merge new incoming records into an existing Delta table, updating matches and inserting new rows. Which SQL/Spark operation is designed for this?

A) INSERT only
B) MERGE (upsert)
C) DROP and CREATE
D) SELECT INTO

**25.** Which Fabric item would be most appropriate for storing and querying large volumes of semi-structured JSON log data with millisecond-level query performance for time-based filtering?

A) KQL Database
B) Power BI dataflow
C) Excel workbook in OneLake
D) SharePoint list

**26.** What does "capacity-aware" scaling mean for Spark jobs in Fabric?

A) Spark jobs ignore capacity limits entirely
B) The compute resources available to Spark jobs are governed by the capacity's allocated Spark VCores/CUs
C) It refers only to Power BI report rendering
D) It applies only to on-premises gateways

**27.** Which of the following best distinguishes a data pipeline's "Copy data" activity from a Dataflow Gen2?

A) Copy data is optimized for moving data at scale with minimal transformation; Dataflow Gen2 is designed for richer Power Query–based transformation
B) They are functionally identical in every respect
C) Copy data can only move data within the same lakehouse
D) Dataflow Gen2 cannot connect to cloud sources

**28.** A table in your lakehouse needs to be queried by both Spark notebooks and Power BI reports via DirectQuery. Which endpoint enables the Power BI DirectQuery connection?

A) The lakehouse's SQL analytics endpoint
B) The Spark job definition
C) The KQL Queryset
D) The Git integration endpoint

---

## Domain 3: Implement and Manage Semantic Models

**29.** What is the purpose of a role-playing dimension in a semantic model (e.g., a single Date table used for both OrderDate and ShipDate)?

A) It is not supported in Power BI
B) Using inactive relationships (activated via USERELATIONSHIP in DAX) lets one dimension table serve multiple roles without duplicating it
C) It requires duplicating the Date table for each role
D) It only works with DirectQuery

**30.** Which DAX function would you use to explicitly change the filter context of a calculation, such as removing filters on the Product table?

A) SUM
B) CALCULATE with ALL(Product)
C) CONCATENATE
D) IF

**31.** You need to create a table of distinct years for a Date table without importing it from a source. Which DAX approach is appropriate?

A) A calculated table using DAX (e.g., using CALENDAR or CALENDARAUTO)
B) A Power Query custom function only
C) It is not possible to create tables via DAX
D) SUMX

**32.** What does "Mark as Date Table" do in a semantic model?

A) Deletes the table
B) Tells Power BI to treat the table as a proper date dimension, enabling accurate time intelligence functions
C) Converts the table to DirectQuery
D) Hides the table from the field list

**33.** Which of the following is a best practice for measure organization in large semantic models?

A) Placing all measures in a single random table with no naming convention
B) Using display folders and a dedicated "Measures" table to group and organize related DAX measures
C) Avoiding measures entirely in favor of calculated columns
D) Renaming all tables to "Table1", "Table2", etc.

**34.** A semantic model uses Import mode. Which factor most directly affects how "fresh" the data appears to report viewers?

A) The report's color theme
B) The refresh schedule/frequency configured for the semantic model
C) The number of visuals on the report page
D) The workspace's Git integration status

**35.** What is the effect of setting a relationship's cross-filter direction to "Both" in a semantic model?

A) Filters propagate in a single direction only
B) Filters can propagate in both directions across the relationship, which can introduce ambiguity in some models and should be used carefully
C) It disables the relationship
D) It converts the relationship to many-to-many automatically

**36.** Which feature lets you validate that RLS is correctly restricting data before publishing, by simulating a specific user's view?

A) "View as" role/user feature in Power BI Desktop
B) Deployment pipelines
C) OneLake shortcuts
D) Capacity Metrics app

**37.** What is a key consideration when deciding between a calculated column and a measure for a given calculation?

A) Calculated columns are computed row-by-row at refresh/processing time and stored in the model (consuming memory); measures are computed dynamically at query time based on filter context
B) There is no difference; they behave identically
C) Measures always use more memory than calculated columns
D) Calculated columns can only reference other calculated columns

**38.** Which of the following would most likely cause a Direct Lake model to fall back to DirectQuery for a given query?

A) The report uses a Card visual
B) A query requires a feature or transformation not supported by Direct Lake for that specific table/version, triggering fallback behavior
C) The user has Viewer permissions
D) The model uses a star schema

**39.** You want to prevent business users from seeing a sensitive "Cost" column and its associated measures entirely, not just filtering rows. Which feature should you apply?

A) Row-level security (RLS)
B) Object-level security (OLS)
C) Sensitivity labels only
D) Workspace roles

**40.** Which of the following is true about composite models that combine Import tables with DirectQuery tables from different sources?

A) This configuration is not supported in Power BI
B) It enables blending cached and live data in a single model, though it requires attention to relationship and performance implications
C) It automatically converts all tables to Import
D) It requires disabling all relationships

**41.** What is the recommended approach for handling many-to-many relationships between two dimension tables in a semantic model?

A) Avoid them entirely; they are never supported
B) Use a bridge table or set the relationship cardinality to many-to-many with careful validation of filter behavior
C) Always use bidirectional filtering with no bridge table
D) Convert both tables to measures

---

## Domain 4: Explore and Analyze Data

**42.** Which Power BI feature allows end users to create ad hoc "what-if" scenarios by adjusting a slider that feeds into a DAX calculation?

A) What-if parameter
B) Row-level security
C) Deployment pipeline
D) OneLake shortcut

**43.** You want to highlight related data points across multiple visuals on a report page when a user clicks one visual. What behavior is this called?

A) Bookmarking
B) Cross-highlighting/cross-filtering
C) Drillthrough
D) Tooltips

**44.** Which feature allows a user to click a data point in a summary report and navigate to a detailed report page filtered to that context?

A) Drillthrough
B) Bookmarks
C) Field parameters
D) Sync slicers

**45.** A stakeholder wants to compare actual sales against a fixed target line on the same chart. Which technique is most appropriate?

A) Adding a constant/target line via an analytics pane reference line or a measure representing the target
B) Removing the axis entirely
C) Using only a table visual with no chart
D) Applying RLS to hide the target

**46.** Which visual is best suited to show the relationship/correlation between two numeric variables (e.g., marketing spend vs. revenue) across many data points?

A) Scatter chart
B) Card
C) Gauge
D) Slicer

**47.** What is the purpose of "Sync slicers" in Power BI?

A) To apply the same slicer selection across multiple report pages
B) To hide slicers from viewers
C) To convert slicers into bookmarks
D) To disable filtering entirely

**48.** You want end users of a published report to export the underlying data of a visual to Excel for further analysis. Which capability enables this (subject to permissions)?

A) Export data feature on the visual
B) Deployment pipelines
C) Git integration
D) OneLake shortcuts

**49.** Which DAX time intelligence function returns sales from the same date one year earlier, useful for year-over-year comparisons?

A) TOTALYTD
B) SAMEPERIODLASTYEAR
C) CALENDAR
D) ALLSELECTED

**50.** A report author wants to let users pick which measure (e.g., Sales, Profit, or Quantity) is plotted on a chart, entirely from a dropdown in the report — without creating separate visuals for each. Which feature enables this?

A) Field parameters
B) Row-level security
C) Bookmarks
D) Data alerts

---

## Answer Key with Explanations

**1. B** — Capacity Units (CUs) represent the compute resources available across Fabric workloads in a capacity.

**2. A** — The Capacity Metrics app breaks down CU consumption by item/operation, helping pinpoint what's driving throttling.

**3. B** — Fabric trial capacities offer a temporary, free way to try Fabric features before purchasing a capacity.

**4. A** — Limiting Admin access and using deployment pipeline governance reduces accidental deletion/modification risk.

**5. B** — Deployment rules let you customize stage-specific values (like data source connections) so promoted content works correctly without manual fixes each time.

**6. A** — Sensitivity labels classify and can enforce protection (e.g., encryption) on content based on data sensitivity.

**7. A** — Lineage view visually maps upstream/downstream dependencies between items in a workspace.

**8. C** — Assigning a workspace to a capacity requires capacity administrator permissions (or equivalent elevated permission).

**9. A** — Dataflow Gen2 can connect to multiple sources (lakehouse, on-prem SQL via gateway) and merge them using Power Query.

**10. A** — The SQL analytics endpoint provides read-only T-SQL querying of lakehouse Delta tables; writes must go through Spark.

**11. B** — Notebooks (using PySpark/Spark SQL) are used for custom data engineering logic like reading, cleaning, and writing Delta tables.

**12. B** — Lookup activity retrieves a single value or small result set, commonly used for configuration/watermark values.

**13. A** — "Get Data" is where you connect to and select the source before transforming it with Power Query.

**14. B** — ForEach iterates the same activity logic across a collection, such as one file per loop iteration.

**15. A** — Warehouses are ideal when teams need full T-SQL DDL/DML and multi-table transactional support.

**16. B** — Schema-on-read means structure is applied when data is queried/read, not necessarily enforced at ingestion.

**17. A** — VACUUM removes old, unreferenced data files no longer needed after operations like OPTIMIZE, based on a retention threshold.

**18. B** — Eventstream feeding a KQL Database (or lakehouse) with a real-time dashboard supports low-latency ingestion and near-instant visibility.

**19. B** — Z-ORDER clusters related data together on disk to speed up filtering on the specified columns.

**20. B** — Fabric supports multiple auth methods for ADLS Gen2 connections, including service principal, managed identity, and keys/SAS tokens.

**21. A** — Delta's schema enforcement rejects writes that don't conform to the table's defined schema, protecting data quality.

**22. A** — A shortcut can point to Delta-formatted data and be queried as a table without physically copying files.

**23. B** — Parameters enable reusable, dynamic pipelines/dataflows by avoiding hardcoded values.

**24. B** — MERGE performs an upsert: updating matched rows and inserting unmatched ones in a single operation.

**25. A** — KQL Database is optimized for fast ingestion and querying of semi-structured, time-series data like logs.

**26. B** — Spark compute for jobs draws from the capacity's allocated resources (e.g., Spark VCores), governed by capacity limits.

**27. A** — Copy data activity focuses on efficient bulk data movement; Dataflow Gen2 focuses on Power Query–based transformation.

**28. A** — Power BI DirectQuery against a lakehouse connects through its SQL analytics endpoint.

**29. B** — Role-playing dimensions use one physical table with multiple relationships (most inactive) activated via USERELATIONSHIP as needed.

**30. B** — CALCULATE with ALL() modifies filter context, here removing filters applied to the Product table.

**31. A** — DAX calculated tables (e.g., via CALENDAR/CALENDARAUTO) can generate a date table without a data source.

**32. B** — Marking a table as a date table enables correct behavior for DAX time intelligence functions.

**33. B** — Display folders and a dedicated measures table improve organization and discoverability in large models.

**34. B** — Data freshness in Import mode depends directly on how often/when scheduled refresh runs.

**35. B** — Bidirectional cross-filtering allows filters to flow both ways but can create ambiguous filter paths if overused.

**36. A** — "View as" lets you preview the model as a specific role or user to validate RLS behavior before publishing.

**37. A** — Calculated columns are precomputed and stored (using memory); measures compute dynamically based on the current filter context at query time.

**38. B** — Direct Lake falls back to DirectQuery when a query needs something not supported directly by Direct Lake for that data.

**39. B** — Object-level security (OLS) hides entire columns/tables and their associated measures from specified users/roles.

**40. B** — Composite models blend Import and DirectQuery sources but require careful design due to potential performance/relationship complexities.

**41. B** — Many-to-many relationships are supported but are best handled with a bridge table or careful validation of many-to-many cardinality settings.

**42. A** — What-if parameters create a slicer-driven variable that feeds into DAX calculations for scenario analysis.

**43. B** — Clicking a data point cross-highlights/cross-filters related visuals on the same page by default.

**44. A** — Drillthrough navigates from a summary context to a detail page filtered on the selected data point.

**45. A** — A reference/target line (via the analytics pane or a target measure) overlays a constant comparison point on a chart.

**46. A** — Scatter charts are designed to reveal correlation/relationships between two numeric variables across data points.

**47. A** — Sync slicers apply a slicer's selection consistently across multiple pages in a report.

**48. A** — The Export data option on a visual (when enabled and permitted) lets users export the underlying data.

**49. B** — SAMEPERIODLASTYEAR shifts the current date context back one year for prior-year comparisons.

**50. A** — Field parameters let users dynamically choose which field/measure populates a visual from a dropdown, without duplicating visuals.

---

### Scoring Guide
- 45–50 correct: Excellent — you're likely exam-ready.
- 38–44 correct: Good — review the domain(s) where you missed the most questions.
- Below 38: Spend more time with hands-on practice in Fabric (lakehouses, warehouses, pipelines, semantic models) before scheduling the exam.
