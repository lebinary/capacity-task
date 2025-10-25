# **Understanding Capacity**

Capacity is a measure of how much shipping capacity is available on a particular tradelane. So for example we might say, “on Far East Main to North Europe Main, there was 293k twenty-foot equivalent unit (TEU) of offered capacity on the week of 2025-08-18”. That 293k TEU is an indication of the number of TEUs offered on this particular corridors based on the vessels that are expected to go from 'Far East Main' to 'North Europe Main' on the week of `2025-08-18`. Capacity can be calculated from sailing-level raw data.

# **Dataset**

- You are given a sample dataset which contains sailing-level raw data China-Main ↔︎ North Europe Main trading routes.
- You will need to be aware of the following:
    - To define the week within which the capacity of a given vessel should be assigned, you will need to find the latest point of departure from the origin region (`china_main`) for that particular vessel and service.
    - One vessel and service combination can be identified based on the following unique identifiers:
        - `service_version_and_roundtrip_identfiers`
        - `origin_service_version_and_master`
        - `destination_service_version_and_master`
    - By filtering on the above columns, you should be able to see an individual service and vessel travelling within one specific journey.
    - You will need to ensure that each of the unique identifiers above only appears once within your final calculations.
    - `Origin_at_utc` defines the time at the origin port.`origin_port_code` and `destination_port_code` define the ports that the vessel passed through.

# **Task**

- You are asked to evaluate offered_capacity data per TEU as a 4-week rolling average for the corridor `china_main - north_europe_main`. This should be done for the period between January 1st to March 31st, 2024.
- Implement an API endpoint that takes the following parameters:
  - date_from
  - date_to

and returns a list with capacity for each week within the given date range.

```
curl "http://127.0.0.1/capacity?date_from=2025-08-11&date_to=2025-08-25
[
    {
        "week_start_date": "2025-08-11",
        "week_no": 33,
        "offered_capacity_teu": 123000
    },
    {
        "week_start_date": "2025-08-18",
        "week_no": 34,
        "offered_capacity_teu": 123000
    },
    {
        "week_start_date": "2025-08-25",
        "week_no": 35,
        "offered_capacity_teu": 86000
    },
    ...
]
```

# **Requirements**

- Upload the provided dataset to a database of your choice.
- Solve the task to calculate offered capacity 4-week rolling average in SQL.
- Implement an API endpoint in Python.
- Use dates in YYYY-MM-DD format for the API.
- Keep your solution in a Version Control System of your choice. *Provide the solution as a public repository that can be easily cloned by our development team.*
- Provide instructions needed to set up and run your solution in `README.md`.

# **Extra details**

- Our key evaluation criteria:
    - Correctness of calculations
    - Ease of setup and testing
    - Code clarity and simplicity
    - Code organisation
    - Tests
- If you have any questions, please don't hesitate to contact us
- Please let us know how much time you spent on the task, and of any difficulties that you ran into.
