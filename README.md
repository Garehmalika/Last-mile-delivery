# Last-mile-delivery
# ETA-Modelling-and-Optimizing-Last-Mile-Logistics
The company aims to optimize the allocation of delivery partners based on delivery volumes, regional demands, partner performance, and dynamic traffic conditions. The goal is to minimize delivery costs while ensuring on-time delivery.

## Overview
This repository contains a project focused on optimizing last-mile logistics operations using **Business Intelligence (BI)** and **Machine Learning (ML)** techniques. It leverages the **last Miles Dataset** to improve delivery efficiency, reduce costs, and enhance customer satisfaction.

---

## Problem Statement
GoLogistics faces inefficiencies in last-mile delivery operations due to suboptimal allocation of delivery partners. This project addresses the challenges of:
1. Increasing delivery costs.
2. Delays caused by traffic and poor route planning.
3. Underutilization of delivery partner resources.

---

## Objectives
- **BI Analysis**: Create dashboards to monitor delivery performance, costs, and regional trends.
- **Machine Learning Models**: Predict delivery times and optimize partner allocation dynamically.

---

## Dataset
The **LaDe Dataset** is a real-world dataset containing:
- **10 million+ package records**.
- Information about delivery times, locations, traffic density, and courier performance.
- Six months of data from diverse regions, including Shanghai and Hangzhou.
- 
---

## Project Workflow

1. **Data Preprocessing**:
   - Clean raw data.
   - Engineer features like `delivery_distance` and `traffic_impact`.

2. **BI Dashboards**:
   - Visualize KPIs: delivery cost trends, partner performance, and delay analysis.
   - Tools: Power BI and Tableau.

3. **ML Models**:
   - Regression model to predict delivery times.
   - Optimization algorithm for efficient delivery partner allocation.

4. **Evaluation**:
   - **BI Dashboards**: Insight clarity and actionable metrics.
   - **ML Models**: Metrics like RMSE, cost savings, and customer satisfaction rate.

Description
Below is the detailed field of each sub-dataset.
## Last Miles-P [Pickup Download](https://drive.google.com/file/d/1BWZ1Z-Vg0HoKWIuTyrLKzVTuN38fPB3K/view?usp=sharing)
| Data field                 | Description                                  | Unit/format  |
|----------------------------|----------------------------------------------|--------------|
| **Package information**    |                                              |              |
| package_id                 | Unique identifier of each package             | Id           |
| time_window_start          | Start of the required time window             | Time         |
| time_window_end            | End of the required time window               | Time         |
| **Stop information**       |                                              |              |
| lng/lat                    | Coordinates of each stop                      | Float        |
| city                       | City                                         | String       |
| region_id                  | Id of the Region                              | String       |
| aoi_id                     | Id of the AOI (Area of Interest)              | Id           |
| aoi_type                   | Type of the AOI                               | Categorical  |
| **Courier Information**    |                                              |              |
| courier_id                 | Id of the courier                             | Id           |
| **Task-event Information** |                                              |              |
| accept_time                | The time when the courier accepts the task    | Time         |
| accept_gps_time            | The time of the GPS point closest to accept time | Time       |
| accept_gps_lng/lat         | Coordinates when the courier accepts the task | Float        |
| pickup_time                | The time when the courier picks up the task   | Time         |
| pickup_gps_time            | The time of the GPS point closest to pickup_time | Time       |
| pickup_gps_lng/lat         | Coordinates when the courier picks up the task | Float        |
| **Context information**    |                                              |              |
| ds                         | The date of the package pickup                | Date         |


## Last Miles-D [Delivery Download](https://drive.google.com/file/d/1rTe8l68zin2e0QX1sn4HMGjx2bz1e1qz/view?usp=sharing)
| Data field            | Description                          | Unit/format   |
|-----------------------|--------------------------------------|---------------|
| **Package information**   |                                      |               |
| package_id            | Unique identifier of each package     | Id            |
| **Stop information**      |                                      |               |
| lng/lat               | Coordinates of each stop              | Float         |
| city                  | City                                 | String        |
| region_id             | Id of the region                      | Id            |
| aoi_id                | Id of the AOI                         | Id            |
| aoi_type              | Type of the AOI                       | Categorical   |
| **Courier Information**   |                                      |               |
| courier_id     

https://github.com/user-attachments/assets/32345a4c-dab6-4f08-be3c-6a9cb38c03df

       | Id of the courier                     | Id            |
| **Task-event Information**|                                      |               |
| accept_time           | The time when the courier accepts the task | Time      |
| accept_gps_time       | The time of the GPS point whose time is the closest to accept time | Time |
| accept_gps_lng/accept_gps_lat | Coordinates when the courier accepts the task | Float |
| delivery_time         | The time when the courier finishes delivering the task | Time |
| delivery_gps_time     | The time of the GPS point whose time is the closest to the delivery time | Time |
| delivery_gps_lng/delivery_gps_lat | Coordinates when the courier finishes the task | Float |
| **Context information**  |                                      |               |
| ds                    | The date of the package delivery      | Date          |
