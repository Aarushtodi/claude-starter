---
type: dashboard
---
# Home

**Goal:** (Claude fills this in during setup)

If the boxes below show raw code instead of tables, Dataview is not on yet. Open [[Start Here]] and follow "Turn on Dataview".

## Classes
(Claude adds a link to each class hub here, like [[Classes/AP Lang]])

## Active projects
```dataview
TABLE status AS Status, updated AS Updated
FROM "Projects"
WHERE type = "project" AND status = "active"
SORT updated DESC
```

## Everything I marked weak
```dataview
TABLE class AS Class, unit AS Unit
FROM "Notes"
WHERE status = "weak"
SORT class ASC, unit ASC
```

## Open tasks by class
```dataview
TASK
FROM "Notes" OR "Daily" OR "Projects"
WHERE !completed
GROUP BY class
```

## Upcoming tests and assignments
```dataview
TABLE class AS Class, date AS Date, weight AS Weight
FROM "Notes"
WHERE type = "assessment" AND status = "upcoming"
SORT date ASC
```

## Recently touched
```dataview
TABLE file.mtime AS "Last edited"
FROM "Notes" OR "Projects"
SORT file.mtime DESC
LIMIT 10
```

---
New here? [[Start Here]]
