1. Group edges into voyages (by 3-column composite key)
2. Assign each voyage to a week using MAX(origin_at_utc) where origin is in China
3. Sum capacity across all voyages per week
4. Calculate 4-week rolling average
5. Filter output by date range (date_from, date_to parameters)

Step 1: Deduplicate edges → voyages
  Voyage A: edges [(CNSGH→NLRTM, 2024-03-27), (CNYTN→NLRTM, 2024-03-28)]
           → latest China departure: 2024-03-28
           → capacity: 23992 TEU
           → assigned to week of 2024-03-25

Step 2: Aggregate by week
  Week 2024-03-25: [Voyage A: 23992, Voyage B: 19273, ...]
                 → total: 43265 TEU

Step 3: Rolling average (4-week window)
  Week 2024-03-25: AVG(weeks [2024-03-04, 2024-03-11, 2024-03-18, 2024-03-25])

Step 4: Filter by parameters
  Return only weeks where week_start_date BETWEEN date_from AND date_to
