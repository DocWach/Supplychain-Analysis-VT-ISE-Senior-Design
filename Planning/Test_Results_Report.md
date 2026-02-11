# Titanium Supply Chain Analyzer - Test Results Report

**Generated:** 2026-02-11 13:30:19

**Solver Backend:** `scipy`

**Python:** `3.12.10`


## Summary

| Metric | Count |
|--------|-------|
| Total checks | 155 |
| Passed | 155 |
| Failed | 0 |
| Warnings | 0 |

### Anomalies

None detected.

---

## Test 1: Baseline (No Disruption)

#### Order: 1000 kg, qualified_only=True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $26,999.60 | 8 | Yes | Titan-US: 173.9; Titan-JP: 260.9; Titan-RU: 434.8; Titan-AU: 130.4 |
| cheapest_first | $22,000.00 | 8 | Yes | Titan-RU: 1,000.0 |
| fastest_first | $32,000.00 | 4 | Yes | Titan-US: 1,000.0 |
| optimal_cost | $22,000.00 | 8 | Yes | Titan-RU: 1,000.0 |
| optimal_time | $32,000.00 | 4 | Yes | Titan-US: 1,000.0 |
| optimal_balanced | $22,000.00 | 8 | Yes | Titan-RU: 1,000.0 |


#### Order: 1000 kg, qualified_only=False

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $26,262.20 | 8 | Yes | Titan-US: 131.1; Titan-JP: 196.7; Titan-RU: 327.9; Titan-CN: 245.9; Titan-AU: 98.4 |
| cheapest_first | $22,000.00 | 8 | Yes | Titan-RU: 1,000.0 |
| fastest_first | $32,000.00 | 4 | Yes | Titan-US: 1,000.0 |
| optimal_cost | $22,000.00 | 8 | Yes | Titan-RU: 1,000.0 |
| optimal_time | $32,000.00 | 4 | Yes | Titan-US: 1,000.0 |
| optimal_balanced | $24,000.00 | 7 | Yes | Titan-CN: 1,000.0 |


#### Order: 5000 kg, qualified_only=True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $135,000.40 | 8 | Yes | Titan-US: 869.6; Titan-JP: 1,304.3; Titan-RU: 2,173.9; Titan-AU: 652.2 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |


#### Order: 5000 kg, qualified_only=False

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $131,308.80 | 8 | Yes | Titan-US: 655.7; Titan-JP: 983.6; Titan-RU: 1,639.3; Titan-CN: 1,229.5; Titan-AU: 491.8 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $120,000.00 | 7 | Yes | Titan-CN: 5,000.0 |


#### Order: 10000 kg, qualified_only=True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $269,996.90 | 8 | Yes | Titan-US: 1,739.1; Titan-JP: 2,608.7; Titan-RU: 4,347.8; Titan-AU: 1,304.3 |
| cheapest_first | $220,000.00 | 8 | Yes | Titan-RU: 10,000.0 |
| fastest_first | $321,200.00 | 12.0 | Yes | Titan-US: 9,600.0; Titan-AU: 400.0 |
| optimal_cost | $220,000.00 | 8 | Yes | Titan-RU: 10,000.0 |
| optimal_time | $321,200.00 | 12.0 | Yes | Titan-US: 9,600.0; Titan-AU: 400.0 |
| optimal_balanced | $220,000.00 | 8 | Yes | Titan-RU: 10,000.0 |


#### Order: 10000 kg, qualified_only=False

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $262,623.00 | 8 | Yes | Titan-US: 1,311.5; Titan-JP: 1,967.2; Titan-RU: 3,278.7; Titan-CN: 2,459.0; Titan-AU: 983.6 |
| cheapest_first | $220,000.00 | 8 | Yes | Titan-RU: 10,000.0 |
| fastest_first | $321,200.00 | 12.0 | Yes | Titan-US: 9,600.0; Titan-AU: 400.0 |
| optimal_cost | $220,000.00 | 8 | Yes | Titan-RU: 10,000.0 |
| optimal_time | $321,200.00 | 12.0 | Yes | Titan-US: 9,600.0; Titan-AU: 400.0 |
| optimal_balanced | $240,000.00 | 7 | Yes | Titan-CN: 10,000.0 |


#### Order: 20000 kg, qualified_only=True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $540,002.70 | 8 | Yes | Titan-US: 3,478.3; Titan-JP: 5,217.4; Titan-RU: 8,695.7; Titan-AU: 2,608.7 |
| cheapest_first | $440,000.00 | 10.0 | Yes | Titan-RU: 20,000.0 |
| fastest_first | $648,800.00 | 12.0 | Yes | Titan-US: 9,600.0; Titan-AU: 7,200.0; Titan-JP: 3,200.0 |
| optimal_cost | $440,000.00 | 10.0 | Yes | Titan-RU: 20,000.0 |
| optimal_time | $648,800.00 | 12.0 | Yes | Titan-US: 9,600.0; Titan-JP: 3,200.0; Titan-AU: 7,200.0 |
| optimal_balanced | $440,000.00 | 10.0 | Yes | Titan-RU: 20,000.0 |


#### Order: 20000 kg, qualified_only=False

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $525,246.00 | 8 | Yes | Titan-US: 2,623.0; Titan-JP: 3,934.4; Titan-RU: 6,557.4; Titan-CN: 4,918.0; Titan-AU: 1,967.2 |
| cheapest_first | $440,000.00 | 10.0 | Yes | Titan-RU: 20,000.0 |
| fastest_first | $648,800.00 | 12.0 | Yes | Titan-US: 9,600.0; Titan-AU: 7,200.0; Titan-JP: 3,200.0 |
| optimal_cost | $440,000.00 | 10.0 | Yes | Titan-RU: 20,000.0 |
| optimal_time | $648,800.00 | 12.0 | Yes | Titan-US: 9,600.0; Titan-JP: 3,200.0; Titan-AU: 7,200.0 |
| optimal_balanced | $476,000.00 | 12.0 | Yes | Titan-RU: 2,000.0; Titan-CN: 18,000.0 |


---

## Test 2: Individual Supplier Disruptions

#### Disrupted: Titan-US (12 weeks)

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $129,736.90 | 8 | Yes | Titan-JP: 1,578.9; Titan-RU: 2,631.6; Titan-AU: 789.5 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $175,000.00 | 8.3 | Yes | Titan-AU: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $175,000.00 | 8.3 | Yes | Titan-AU: 5,000.0 |
| optimal_balanced | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |


#### Disrupted: Titan-JP (12 weeks)

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $133,238.40 | 8 | Yes | Titan-US: 1,176.5; Titan-RU: 2,941.2; Titan-AU: 882.4 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |


#### Disrupted: Titan-RU (12 weeks)

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $154,230.60 | 6 | Yes | Titan-US: 1,538.5; Titan-JP: 2,307.7; Titan-AU: 1,153.8 |
| cheapest_first | $140,000.00 | 6 | Yes | Titan-JP: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $140,000.00 | 6 | Yes | Titan-JP: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |


#### Disrupted: Titan-CN (12 weeks)

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $135,000.40 | 8 | Yes | Titan-US: 869.6; Titan-JP: 1,304.3; Titan-RU: 2,173.9; Titan-AU: 652.2 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |


#### Disrupted: Titan-AU (12 weeks)

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $129,000.00 | 8 | Yes | Titan-US: 1,000.0; Titan-JP: 1,500.0; Titan-RU: 2,500.0 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |


---

## Test 3: Edge Cases

#### 3a: Very Large Order (50,000 kg), Titan-RU Disrupted, qualified_only=True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $1,542,307.90 | 19.2 | Yes | Titan-US: 15,384.6; Titan-JP: 23,076.9; Titan-AU: 11,538.5 |
| cheapest_first | $962,400.00 | 12.0 | NO | Titan-JP: 14,400.0; Titan-US: 9,600.0; Titan-AU: 7,200.0 |
| fastest_first | $962,400.00 | 12.0 | NO | Titan-US: 9,600.0; Titan-AU: 7,200.0; Titan-JP: 14,400.0 |
| optimal_cost | $962,400.00 | 12.0 | NO | Titan-US: 9,600.0; Titan-JP: 14,400.0; Titan-AU: 7,200.0 |
| optimal_time | $962,400.00 | 12.0 | NO | Titan-US: 9,600.0; Titan-JP: 14,400.0; Titan-AU: 7,200.0 |
| optimal_balanced | $962,400.00 | 12.0 | NO | Titan-US: 9,600.0; Titan-JP: 14,400.0; Titan-AU: 7,200.0 |


#### 3b: Very Small Order (100 kg), No Disruption

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $2,699.60 | 8 | Yes | Titan-US: 17.4; Titan-JP: 26.1; Titan-RU: 43.5; Titan-AU: 13.0 |
| cheapest_first | $2,200.00 | 8 | Yes | Titan-RU: 100.0 |
| fastest_first | $3,200.00 | 4 | Yes | Titan-US: 100.0 |
| optimal_cost | $2,200.00 | 8 | Yes | Titan-RU: 100.0 |
| optimal_time | $3,200.00 | 4 | Yes | Titan-US: 100.0 |
| optimal_balanced | $2,200.00 | 8 | Yes | Titan-RU: 100.0 |


#### 3c: Only Titan-AU Available (5000 kg)

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $175,000.00 | 8.3 | Yes | Titan-AU: 5,000.0 |
| cheapest_first | $175,000.00 | 8.3 | Yes | Titan-AU: 5,000.0 |
| fastest_first | $175,000.00 | 8.3 | Yes | Titan-AU: 5,000.0 |
| optimal_cost | $175,000.00 | 8.3 | Yes | Titan-AU: 5,000.0 |
| optimal_time | $175,000.00 | 8.3 | Yes | Titan-AU: 5,000.0 |
| optimal_balanced | $175,000.00 | 8.3 | Yes | Titan-AU: 5,000.0 |


#### 3d: Non-Qualified Supplier (Titan-CN) Disrupted, qualified_only=True

Expected: Results identical to baseline (Titan-CN already excluded by qualification filter).

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $135,000.40 | 8 | Yes | Titan-US: 869.6; Titan-JP: 1,304.3; Titan-RU: 2,173.9; Titan-AU: 652.2 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |


---

## Test 4: Optimizer-Specific Tests

**Solver backend detected:** `scipy`

#### Objective: min_cost

- **Feasible:** Yes
- **Total Cost:** $110,000.00
- **Weighted Lead Time:** 8.0 weeks
- **Objective Value:** 110000.00
- **Allocation:** Titan-RU: 5,000.0
- **Notes:** Titan-CN excluded (not aerospace-qualified).

#### Objective: min_time

- **Feasible:** Yes
- **Total Cost:** $160,000.00
- **Weighted Lead Time:** 4.0 weeks
- **Objective Value:** 20000.00
- **Allocation:** Titan-US: 5,000.0
- **Notes:** Titan-CN excluded (not aerospace-qualified).

#### Objective: balanced

- **Feasible:** Yes
- **Total Cost:** $110,000.00
- **Weighted Lead Time:** 8.0 weeks
- **Objective Value:** 2000.00
- **Allocation:** Titan-RU: 5,000.0
- **Notes:** Titan-CN excluded (not aerospace-qualified).

#### 4b: min_cost Optimizer vs cheapest_first Heuristic

- Heuristic (cheapest_first) cost: $110,000.00
- Optimizer (min_cost) cost: $110,000.00
- **Result: PASS** - Optimizer cost <= heuristic cost

#### 4c: min_time Optimizer vs fastest_first Heuristic

- Heuristic (fastest_first) weighted lead time: 4.00 weeks
- Optimizer (min_time) weighted lead time: 4.0 weeks
- **Result: PASS** - Optimizer time <= heuristic time

#### 4d: Titan-RU Disrupted, Objective=min_cost

- **Feasible:** Yes
- **Total Cost:** $140,000.00
- **Weighted Lead Time:** 6.0 weeks
- **Allocation:** Titan-JP: 5,000.0

#### 4d: Titan-RU Disrupted, Objective=min_time

- **Feasible:** Yes
- **Total Cost:** $160,000.00
- **Weighted Lead Time:** 4.0 weeks
- **Allocation:** Titan-US: 5,000.0

#### 4d: Titan-RU Disrupted, Objective=balanced

- **Feasible:** Yes
- **Total Cost:** $160,000.00
- **Weighted Lead Time:** 4.0 weeks
- **Allocation:** Titan-US: 5,000.0


---

## Test 5: Scenario Sweep (S01-S10)

#### S01: Russian Sanctions

- **Disrupted:** Titan-RU
- **Duration:** 52 weeks
- **Order Qty:** 5,000 kg
- **Qualified Only:** True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $154,230.60 | 6 | Yes | Titan-US: 1,538.5; Titan-JP: 2,307.7; Titan-AU: 1,153.8 |
| cheapest_first | $140,000.00 | 6 | Yes | Titan-JP: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $140,000.00 | 6 | Yes | Titan-JP: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |


#### S02: Japan Earthquake

- **Disrupted:** Titan-JP
- **Duration:** 12 weeks
- **Order Qty:** 5,000 kg
- **Qualified Only:** True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $133,238.40 | 8 | Yes | Titan-US: 1,176.5; Titan-RU: 2,941.2; Titan-AU: 882.4 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |


#### S03: COVID Shipping Delays (baseline proxy)

- **Disrupted:** None
- **Duration:** 0 weeks
- **Order Qty:** 5,000 kg
- **Qualified Only:** True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $135,000.40 | 8 | Yes | Titan-US: 869.6; Titan-JP: 1,304.3; Titan-RU: 2,173.9; Titan-AU: 652.2 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |


#### S04: China Export Controls

- **Disrupted:** Titan-CN
- **Duration:** 26 weeks
- **Order Qty:** 5,000 kg
- **Qualified Only:** True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $135,000.40 | 8 | Yes | Titan-US: 869.6; Titan-JP: 1,304.3; Titan-RU: 2,173.9; Titan-AU: 652.2 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |


#### S05: US Factory Fire

- **Disrupted:** Titan-US
- **Duration:** 8 weeks
- **Order Qty:** 5,000 kg
- **Qualified Only:** True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $129,736.90 | 8 | Yes | Titan-JP: 1,578.9; Titan-RU: 2,631.6; Titan-AU: 789.5 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $175,000.00 | 8.3 | Yes | Titan-AU: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $175,000.00 | 8.3 | Yes | Titan-AU: 5,000.0 |
| optimal_balanced | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |


#### S06: Demand Spike (7500 kg)

- **Disrupted:** None
- **Duration:** 0 weeks
- **Order Qty:** 7,500 kg
- **Qualified Only:** True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $202,499.90 | 8 | Yes | Titan-US: 1,304.3; Titan-JP: 1,956.5; Titan-RU: 3,260.9; Titan-AU: 978.3 |
| cheapest_first | $165,000.00 | 8 | Yes | Titan-RU: 7,500.0 |
| fastest_first | $240,000.00 | 9.4 | Yes | Titan-US: 7,500.0 |
| optimal_cost | $165,000.00 | 8 | Yes | Titan-RU: 7,500.0 |
| optimal_time | $240,000.00 | 9.4 | Yes | Titan-US: 7,500.0 |
| optimal_balanced | $165,000.00 | 8 | Yes | Titan-RU: 7,500.0 |


#### S07: Quality Defect Australia

- **Disrupted:** Titan-AU
- **Duration:** 6 weeks
- **Order Qty:** 5,000 kg
- **Qualified Only:** True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $129,000.00 | 8 | Yes | Titan-US: 1,000.0; Titan-JP: 1,500.0; Titan-RU: 2,500.0 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |


#### S08: Partial Russia Disruption (full proxy)

- **Disrupted:** Titan-RU
- **Duration:** 12 weeks
- **Order Qty:** 5,000 kg
- **Qualified Only:** True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $154,230.60 | 6 | Yes | Titan-US: 1,538.5; Titan-JP: 2,307.7; Titan-AU: 1,153.8 |
| cheapest_first | $140,000.00 | 6 | Yes | Titan-JP: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $140,000.00 | 6 | Yes | Titan-JP: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |


#### S10: Baseline

- **Disrupted:** None
- **Duration:** 0 weeks
- **Order Qty:** 5,000 kg
- **Qualified Only:** True

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $135,000.40 | 8 | Yes | Titan-US: 869.6; Titan-JP: 1,304.3; Titan-RU: 2,173.9; Titan-AU: 652.2 |
| cheapest_first | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $110,000.00 | 8 | Yes | Titan-RU: 5,000.0 |


#### S09: Dual Disruption (Titan-RU + Titan-JP)

- **Disrupted:** Titan-RU + Titan-JP (both removed from supplier list)
- **Order Qty:** 5,000 kg
- **Qualified Only:** True

Remaining qualified suppliers: Titan-US (800 kg/wk), Titan-AU (600 kg/wk).
Combined 12-week capacity: 16,800 kg.

| Strategy | Cost (USD) | Delivery (wk) | Feasible | Allocation |
|----------|------------|---------------|----------|------------|
| proportional | $166,428.70 | 5 | Yes | Titan-US: 2,857.1; Titan-AU: 2,142.9 |
| cheapest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| fastest_first | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_cost | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_time | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |
| optimal_balanced | $160,000.00 | 6.2 | Yes | Titan-US: 5,000.0 |

**Comparison - Single disruptions:**

- Titan-RU disrupted alone: Cost=$154,230.60, Delivery=6wk, Feasible=Yes
- Titan-JP disrupted alone: Cost=$133,238.40, Delivery=8wk, Feasible=Yes


---

## Supplier Reference Data

| Name | Region | Lead Time (wk) | Capacity (kg/wk) | Cost ($/kg) | Quality | Qualified |

|------|--------|----------------|-------------------|-------------|---------|----------|

| Titan-US | United States | 4 | 800 | $32.00 | 0.95 | Yes |

| Titan-JP | Japan | 6 | 1,200 | $28.00 | 0.92 | Yes |

| Titan-RU | Russia | 8 | 2,000 | $22.00 | 0.88 | Yes |

| Titan-CN | China | 7 | 1,500 | $24.00 | 0.85 | No |

| Titan-AU | Australia | 5 | 600 | $35.00 | 0.90 | Yes |


---

*End of report.*
