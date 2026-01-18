
## Introduction
<img width="714" height="712" alt="image" src="https://github.com/user-attachments/assets/8371c1fb-bc44-4eb9-8767-1bc83256ead0" />


While working on real production pipelines and designing solution architectures, I’ve repeatedly come across challenges like these. 
So I decided to compile them into a guide — not theory, but practical, hands-on scenarios that help you strengthen your skills with GCP, Python, and modern data engineering best practices.
**How to use this guide:**
- Start with challenges that match your current skill level
- Try to solve each challenge independently before seeking solutions
- Focus on understanding the "why" behind architectural decisions
- Consider scalability, cost, and maintainability in your solutions

---

## Level 1: Foundation Challenges

### Challenge 1.1: Raw Data Ingestion from Multiple Sources
**Scenario:** You're working for an e-commerce company that needs to consolidate data from multiple sources.

**Your Task:**
Design and implement a data ingestion pipeline that:
- Pulls daily sales data from a PostgreSQL database (transactional data)
- Ingests user behavior logs from Cloud Storage (JSON files, ~50GB/day)
- Fetches product catalog updates from a REST API (updates every 4 hours)
- Stores all raw data in Google Cloud Storage with proper partitioning

**Considerations:**
- How will you handle data that arrives late?
- What happens if the API is temporarily unavailable?
- How will you organize your GCS bucket structure?
- What metadata should you capture during ingestion?

---

### Challenge 1.2: Schema Evolution Handling
**Scenario:** Your upstream systems frequently add new fields to their data without warning.

**Your Task:**
Build a resilient ingestion system that:
- Automatically detects schema changes in incoming CSV/JSON files
- Logs all schema changes with timestamps
- Continues processing data even when new columns appear
- Alerts the data team when breaking changes occur (removed columns, data type changes)

**Considerations:**
- How will you differentiate between additive and breaking schema changes?
- Where will you store historical schema versions?
- Should your pipeline stop or continue when schemas change?

---

### Challenge 1.3: Incremental Data Loading
**Scenario:** You need to sync 100 million rows from a production database daily, but full loads are too slow.

**Your Task:**
Implement an incremental loading strategy that:
- Identifies only new or updated records since the last load
- Handles records that don't have updated_at timestamps
- Manages the watermark/checkpoint state reliably
- Validates that no records were missed

**Considerations:**
- What if records can be deleted in the source system?
- How will you handle the initial full load vs. incremental loads?
- Where will you store your high-water marks?
- What happens if your pipeline fails mid-processing?

---

## Level 2: Transformation & Processing Challenges

### Challenge 2.1: Complex Data Transformation with BigQuery
**Scenario:** Raw data needs significant transformation before it's useful for analytics.

**Your Task:**
Design SQL transformations in BigQuery that:
- Join 5+ tables with billions of rows efficiently
- Create slowly changing dimension (SCD Type 2) tables for customer data
- Calculate rolling 30-day metrics for each customer
- Handle NULL values and data quality issues gracefully
- Complete within a 2-hour processing window

**Considerations:**
- How will you optimize query costs in BigQuery?
- What partitioning and clustering strategies will you use?
- How will you handle historical corrections in SCD Type 2?
- Should you use materialized views, scheduled queries, or external orchestration?

---

### Challenge 2.2: Real-time Stream Processing
**Scenario:** Your company needs to detect fraudulent transactions within seconds of occurrence.

**Your Task:**
Build a streaming pipeline using Pub/Sub and Dataflow that:
- Processes 10,000+ transactions per second
- Enriches transaction data with user profile information
- Applies machine learning model predictions in real-time
- Calculates moving averages and aggregations over sliding windows
- Writes flagged transactions to BigQuery and normal transactions to Cloud Storage

**Considerations:**
- How will you handle late-arriving data?
- What windowing strategy is appropriate for your use case?
- How will you deal with lookup/enrichment data that changes?
- What happens during ML model retraining and deployment?

---

### Challenge 2.3: Data Quality Framework
**Scenario:** Bad data keeps breaking downstream reports and ML models.

**Your Task:**
Create a comprehensive data quality framework that:
- Validates data completeness (row counts, NULL checks)
- Checks data accuracy (range checks, pattern matching)
- Ensures consistency (referential integrity, cross-table validation)
- Monitors data freshness and staleness
- Quarantines bad data instead of failing the entire pipeline
- Sends alerts when quality thresholds are breached

**Considerations:**
- How will you define and store data quality rules?
- Should validation happen before or after transformation?
- How will you track data quality metrics over time?
- What's your strategy for handling failed validation?

---

### Challenge 2.4: Deduplication Strategy
**Scenario:** Duplicate records are appearing in your dataset from multiple sources and retries.

**Your Task:**
Implement a deduplication system that:
- Identifies duplicates across multiple ingestion batches
- Handles exact duplicates and fuzzy duplicates
- Preserves the most recent/accurate version
- Works efficiently on billion-row datasets
- Maintains deduplication history for audit purposes

**Considerations:**
- What defines a duplicate in your context (composite keys, similarity scores)?
- How will you handle deduplication in streaming vs. batch pipelines?
- Should you deduplicate during ingestion or during transformation?
- How will you validate your deduplication logic?

---

## Level 3: Orchestration & Pipeline Management

### Challenge 3.1: Complex DAG Design with Cloud Composer (Airflow)
**Scenario:** You need to orchestrate a complex data pipeline with 50+ interdependent tasks.

**Your Task:**
Build an Airflow DAG that:
- Orchestrates ingestion from 10 different sources in parallel
- Runs transformations in the correct dependency order
- Handles dynamic task generation based on configuration
- Implements proper error handling and retries
- Sends notifications on success/failure
- Supports backfilling historical data

**Considerations:**
- How will you structure your DAG for maintainability?
- What's your strategy for handling task failures and partial reruns?
- How will you pass data and metadata between tasks?
- Should you use SubDAGs, TaskGroups, or dynamic task mapping?

---

### Challenge 3.2: Cross-Project Data Pipeline
**Scenario:** Data needs to flow between development, staging, and production projects with proper governance.

**Your Task:**
Design a multi-environment pipeline strategy that:
- Promotes data through dev → staging → production
- Maintains separate datasets and resources per environment
- Uses service accounts with least-privilege access
- Implements environment-specific configurations
- Allows for testing in non-production without affecting production data

**Considerations:**
- How will you handle secrets and credentials across environments?
- What's your deployment strategy for pipeline code?
- How will you ensure data lineage across projects?
- Should you use shared or separate GCP projects?

---

### Challenge 3.3: Pipeline Monitoring and Alerting
**Scenario:** Pipelines are failing silently, and teams learn about issues from business users.

**Your Task:**
Implement comprehensive monitoring that tracks:
- Pipeline execution duration and success/failure rates
- Data volume processed (row counts, GB processed)
- Data quality metrics and anomaly detection
- Resource utilization (CPU, memory, slot hours)
- Cost per pipeline run
- Custom business KPIs
- Sends alerts through multiple channels (email, Slack, PagerDuty)

**Considerations:**
- What metrics matter most for different stakeholders?
- How will you distinguish between expected and unexpected failures?
- What's your alerting threshold strategy to avoid alert fatigue?
- How will you track and visualize pipeline health over time?

---

### Challenge 3.4: Idempotent Pipeline Design
**Scenario:** Pipelines need to be rerun without creating duplicate data or corrupting state.

**Your Task:**
Design pipelines that are truly idempotent:
- Can be safely rerun for any date range
- Produce identical results regardless of run count
- Handle partial failures and reruns gracefully
- Don't create duplicate records
- Maintain audit trail of all runs

**Considerations:**
- How will you implement upsert logic in your pipelines?
- What's your strategy for handling time-sensitive transformations?
- Should you delete and reload data or merge updates?
- How will you test idempotency?

---

## Level 4: Performance & Cost Optimization

### Challenge 4.1: BigQuery Cost Optimization
**Scenario:** Your monthly BigQuery bill is $50,000 and stakeholders want it reduced by 60%.

**Your Task:**
Audit and optimize your BigQuery usage:
- Identify the most expensive queries and optimize them
- Implement proper partitioning and clustering
- Reduce data scanned through strategic materialized views
- Remove or archive unused tables and datasets
- Implement query cost guardrails and budgets
- Educate users on cost-effective query patterns

**Considerations:**
- How will you measure and track cost savings?
- What are the trade-offs between performance and cost?
- Should you use BI Engine, materialized views, or query results caching?
- How will you prevent cost regression?

---

### Challenge 4.2: Large-Scale Data Migration
**Scenario:** You need to migrate 500TB of data from on-premises Hadoop to Google Cloud.

**Your Task:**
Plan and execute a migration strategy that:
- Minimizes downtime for business operations
- Validates data completeness and accuracy
- Handles different data formats (Parquet, Avro, ORC, CSV)
- Manages network bandwidth constraints
- Provides rollback capability if issues occur
- Documents the entire migration process

**Considerations:**
- Should you use Transfer Service, gsutil, or Storage Transfer Service?
- How will you handle the cutover from old to new system?
- What's your data validation strategy?
- How will you manage metadata and permissions migration?

---

### Challenge 4.3: Pipeline Performance Tuning
**Scenario:** Your nightly batch pipeline takes 8 hours but needs to complete in 2 hours.

**Your Task:**
Optimize pipeline performance by:
- Profiling to identify bottlenecks
- Parallelizing independent tasks
- Optimizing SQL queries and BigQuery jobs
- Tuning Dataflow worker configuration
- Implementing caching where appropriate
- Using appropriate file formats (Parquet vs. CSV)

**Considerations:**
- What's causing the slowdown (I/O, CPU, network, or inefficient code)?
- How will you balance performance gains vs. increased costs?
- Should you refactor the pipeline architecture?
- What metrics will you track to measure improvements?

---

### Challenge 4.4: Dynamic Resource Allocation
**Scenario:** Pipeline resource needs vary dramatically by day (10x difference between weekdays and weekends).

**Your Task:**
Implement smart resource management that:
- Scales resources based on data volume
- Uses appropriate machine types for different workloads
- Leverages preemptible VMs where possible
- Automatically adjusts BigQuery slot reservations
- Monitors and alerts on resource utilization
- Maximizes cost efficiency without sacrificing SLAs

**Considerations:**
- How will you predict resource needs before pipeline execution?
- What's your fallback strategy if preemptible VMs are terminated?
- Should you use autoscaling or fixed resource allocation?
- How will you balance cost vs. reliability?

---

## Level 5: Advanced Challenges

### Challenge 5.1: Multi-Region Data Replication
**Scenario:** Your company operates globally and needs data available in US, EU, and Asia with <100ms latency.

**Your Task:**
Design a multi-region architecture that:
- Replicates data across 3 regions
- Ensures data consistency and compliance (GDPR)
- Minimizes cross-region data transfer costs
- Provides disaster recovery capabilities
- Handles region-specific data privacy requirements
- Optimizes query routing to nearest region

**Considerations:**
- What's your data residency strategy for regulated data?
- How will you handle schema changes across regions?
- Should you use active-active or active-passive replication?
- What's your failover strategy if a region goes down?

---

### Challenge 5.2: Change Data Capture (CDC) Implementation
**Scenario:** You need near-real-time replication from 20 production databases without impacting application performance.

**Your Task:**
Implement CDC that:
- Captures INSERT, UPDATE, DELETE operations
- Minimizes load on source databases
- Handles high-volume databases (1M+ transactions/hour)
- Maintains transaction order and consistency
- Recovers from failures without data loss
- Works with various database types (PostgreSQL, MySQL, Oracle)

**Considerations:**
- Should you use log-based or query-based CDC?
- How will you handle initial snapshot + ongoing changes?
- What's your strategy for DDL changes in source systems?
- How will you monitor replication lag?

---

### Challenge 5.3: Data Lineage and Metadata Management
**Scenario:** Teams can't trace where data came from or how it was transformed, causing compliance issues.

**Your Task:**
Build a metadata management system that:
- Captures end-to-end data lineage automatically
- Documents all transformations and business logic
- Tracks data quality issues to their source
- Provides impact analysis (upstream/downstream dependencies)
- Integrates with existing tools (Composer, BigQuery, Dataflow)
- Offers searchable documentation for all datasets

**Considerations:**
- Should you build or buy a metadata solution?
- How will you capture lineage without modifying every pipeline?
- What granularity of lineage is useful (table, column, row)?
- How will you keep metadata synchronized with actual pipelines?

---

### Challenge 5.4: ML Feature Store Integration
**Scenario:** Data scientists need consistent features for training and serving ML models.

**Your Task:**
Design a feature engineering pipeline that:
- Computes features from raw data consistently
- Serves features for both batch training and real-time inference
- Handles feature versioning and experimentation
- Ensures point-in-time correctness (no data leakage)
- Supports feature reuse across multiple models
- Monitors feature drift and data quality

**Considerations:**
- Should you use Vertex AI Feature Store or build custom?
- How will you handle features with different freshness requirements?
- What's your strategy for feature backfilling?
- How will you ensure training/serving consistency?

---

### Challenge 5.5: Event-Driven Architecture
**Scenario:** Your pipeline needs to react to events rather than running on schedules.

**Your Task:**
Build an event-driven data platform that:
- Triggers processing when new data arrives
- Handles event ordering and exactly-once processing
- Scales automatically based on event volume
- Maintains state across event processing
- Provides replay capability for events
- Integrates with existing scheduled pipelines

**Considerations:**
- What events should trigger which pipelines?
- How will you handle event storms (sudden spike in events)?
- Should you use Pub/Sub, Eventarc, or Cloud Functions?
- How will you debug and troubleshoot event flows?

---

## Level 6: Enterprise-Scale Challenges

### Challenge 6.1: Data Mesh Implementation
**Scenario:** Your centralized data team has become a bottleneck. You need to decentralize data ownership.

**Your Task:**
Design a data mesh architecture where:
- Domain teams own their data products end-to-end
- Central platform team provides self-service infrastructure
- Data discovery and governance are standardized
- Data quality ownership is distributed
- Cross-domain data sharing is seamless
- Costs are tracked and allocated per domain

**Considerations:**
- How will you define domain boundaries?
- What platform capabilities need to be standardized?
- How will you enforce governance without centralization?
- What's your strategy for shared/reference data?

---

### Challenge 6.2: Disaster Recovery and Business Continuity
**Scenario:** You need to guarantee <4 hour RTO and <15 minute RPO for critical data pipelines.

**Your Task:**
Design and test a DR strategy that:
- Maintains backups across regions
- Allows rapid failover to backup infrastructure
- Tests DR procedures regularly (chaos engineering)
- Automates recovery processes
- Maintains audit logs of all DR activities
- Documents recovery procedures clearly

**Considerations:**
- What pipelines are truly critical vs. nice-to-have?
- How will you keep backup infrastructure in sync?
- What's your strategy for testing without disrupting production?
- How will you handle stateful vs. stateless components?

---

### Challenge 6.3: Data Privacy and Compliance
**Scenario:** Your company must comply with GDPR, CCPA, and HIPAA while maintaining useful analytics.

**Your Task:**
Implement data governance that:
- Classifies all data by sensitivity level
- Implements encryption at rest and in transit
- Provides data masking/tokenization for PII
- Enables right-to-be-forgotten requests
- Maintains audit logs of all data access
- Restricts data access based on user roles
- Generates compliance reports automatically

**Considerations:**
- How will you balance data utility with privacy requirements?
- What's your strategy for data anonymization vs. pseudonymization?
- How will you handle cross-border data transfers?
- Should you use column-level security, dynamic data masking, or both?

---

### Challenge 6.4: Platform Cost Attribution
**Scenario:** Leadership wants to understand data platform costs by team, project, and business unit.

**Your Task:**
Build a cost tracking and attribution system that:
- Tags all resources with cost centers
- Tracks BigQuery costs by team/project/query
- Monitors Dataflow and Composer costs per pipeline
- Allocates shared infrastructure costs fairly
- Provides cost forecasting and budgets
- Generates chargeback reports automatically

**Considerations:**
- How will you handle shared resources (networking, monitoring)?
- What granularity of cost tracking is useful vs. burdensome?
- Should you use GCP labels, custom tagging, or both?
- How will you enforce cost accountability?

---

### Challenge 6.5: Zero-Downtime Schema Migration
**Scenario:** You need to completely restructure your data warehouse schema without any downtime.

**Your Task:**
Execute a schema migration that:
- Maintains backward compatibility during transition
- Runs old and new schemas in parallel
- Gradually migrates users to new schema
- Validates data consistency between versions
- Provides rollback capability at any point
- Completes migration within 3 months

**Considerations:**
- How will you handle applications that depend on the old schema?
- What's your strategy for data backfilling in the new schema?
- Should you use views as an abstraction layer?
- How will you communicate changes to stakeholders?

