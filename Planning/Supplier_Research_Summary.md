# Titanium Supplier Research Summary

**Prepared for:** AY 25-26 VT Supply Chain Senior Design Project
**Date:** 2026-02-11
**Purpose:** Realistic supplier data for aerospace titanium procurement disruption simulation

---

## 1. Global Titanium Market Overview

### Production by Country (2024 estimates)

| Country | Sponge Production (MT/yr) | Share of Global |
|---------|--------------------------|-----------------|
| China   | 220,000                  | ~57%            |
| Japan   | 55,000                   | ~14%            |
| Russia  | 17,000-34,000            | ~5-9%           |
| Kazakhstan | 19,000                | ~5%             |
| Saudi Arabia | 15,000              | ~4%             |
| United States | ~0 (domestic sponge idled) | ~0%    |
| Others  | ~35,000                  | ~9%             |
| **Total** | **~380,000-400,000**   | **100%**        |

**Sources:**
- USGS Mineral Commodity Summaries 2025, Titanium section [1]
- Argus Media, "Aerospace-approved Ti sponge supply up in 2024" [2]
- World Population Review, "Titanium Production by Country 2026" [3]

### Key Market Facts

- Global titanium material production in 2024: ~260,000 metric tons of mill products [3]
- China accounts for ~66% of global titanium material production (172,000 MT) [3]
- U.S. titanium sponge imports in 2024: ~40,000 MT (near historical high) [1]
- U.S. import sources for sponge: Japan 67%, Saudi Arabia 23%, Kazakhstan 7% [1]
- The U.S. has no active domestic titanium sponge production (TIMET Henderson NV facility idled since 2020) [1]

---

## 2. Aerospace-Grade Ti-6Al-4V Pricing

Ti-6Al-4V (Grade 5) is the most widely used aerospace titanium alloy, accounting for approximately 50% of all titanium usage in aerospace applications.

### Current Price Ranges (2025-2026)

| Form | Price Range | Notes |
|------|-------------|-------|
| Ingot (FOB US producer) | $7.50-10.00/kg | Raw melt form |
| Bar stock (aerospace certified) | $30-88/kg ($15-40/lb) | AMS 4928, annealed |
| Plate/sheet | $44-99/kg ($20-45/lb) | AMS 4911 |
| Forgings | $50-120/kg | Near-net shape, OEM-specific |

**Notes:**
- Pre-war (pre-2022) US market price was ~$10/kg ($4.50/lb) for ingot
- By early 2024, prices reached ~$29/kg ($13/lb) for ingot -- a near tripling [6]
- Aerospace certification documentation adds a premium of 15-30% over commercial grades
- Pricing is highly volume-dependent; long-term contracts with OEMs run 20-40% below spot

**Sources:**
- Pakshal Steel, "Titanium Metal Price Per Kg - Latest 2026 Price List" [4]
- Partsproto, "Cost of Titanium in 2025" [5]
- AeroTime, "The titanium supply chain crisis" [6]
- Argus Metals, "Titanium 6Al 4V ingot FOB US producer prices" [7]

---

## 3. Supplier Profiles

### 3.1 VSMPO-AVISMA (Russia)

- **Headquarters:** Verkhnyaya Salda, Sverdlovsk Oblast, Russia
- **Annual Capacity:** 34,000 MT/yr sponge (nameplate); actual output estimated at ~17,000 MT/yr post-2022 sanctions
- **Capacity (kg/week):** ~327,000 kg/week (at reduced output level)
- **Lead Time to US:** 16+ weeks (effectively unavailable for new Western contracts)
- **Estimated Cost:** ~$18.50/kg (historically the lowest-cost major producer)
- **Aerospace Qualification:** Was qualified by Boeing, Airbus, Rolls-Royce, Safran, Embraer. Boeing suspended purchases March 2022. Airbus continuing via European subsidiaries (VSMPO Tirus UK, Frankfurt, Lausanne) but phasing out.
- **Disruption History:**
  - Feb 2022: Russia-Ukraine war triggers Western supply chain re-evaluation
  - Mar 2022: Boeing and Rolls-Royce suspend VSMPO purchases indefinitely
  - 2022: Airbus imports from VSMPO surged 940% (stockpiling) before beginning phase-out
  - Parent company Rostec and CEO Chemezov under US/EU sanctions; VSMPO itself not directly sanctioned as of 2024
  - Ukraine banned titanium raw material exports to Russia, disrupting VSMPO feedstock supply
  - Output dropped from ~32,000 MT to ~17,000 MT/yr
- **Simulation Notes:** This is the primary disruption scenario for the simulation -- loss of the world's largest single-source producer for Western aerospace

**Sources:**
- Wikipedia, "VSMPO-AVISMA" [8]
- Quest Metals, "Western Aerospace's Dependence on Russian Supply" [9]
- Euronews, "Boeing suspends Russian titanium as Airbus keeps buying" [10]
- EU Political Report, "Pressure for Sanctions on Russian Titanium" [11]
- AeroTime, "The titanium supply chain crisis" [6]

### 3.2 TIMET / Titanium Metals Corporation (United States)

- **Headquarters:** Warrensville Heights, Ohio, USA (parent: Precision Castparts Corp / Berkshire Hathaway)
- **Annual Capacity:** ~13,000 MT/yr sponge (Henderson, NV -- idled since 2020); significant mill products capacity across US and Europe
- **Capacity (kg/week):** ~250,000 kg/week mill products
- **Lead Time to US:** 12 weeks (domestic advantage)
- **Estimated Cost:** ~$35/kg (aerospace-grade bar)
- **Aerospace Qualification:** Fully qualified across all major OEMs (Boeing, Airbus, GE, Pratt & Whitney, Rolls-Royce). Supplies approximately 20% of global titanium.
- **Disruption History:**
  - Henderson NV sponge plant idled since 2020 due to market conditions (last domestic US sponge facility)
  - Acquired by PCC in 2012 for $2.9B; PCC acquired by Berkshire Hathaway 2016 for $37.2B
  - New Ravenswood, WV facility under construction for 24/7 titanium melting with 100% renewable energy
- **Simulation Notes:** Premium domestic supplier; capacity-constrained; represents the "reliable but expensive" option

**Sources:**
- Wikipedia, "Titanium Metals Corporation" [12]
- TIMET corporate website [13]
- Jackson County (WV), "PCC Ravenswood" [14]

### 3.3 Toho Titanium (Japan)

- **Headquarters:** Chigasaki, Kanagawa, Japan
- **Annual Capacity:** 25,200 MT/yr sponge (Wakamatsu 15,600 + Chigasaki 9,600); expanding by 3,000 MT/yr by 2026
- **Capacity (kg/week):** ~485,000 kg/week
- **Lead Time to US:** 14 weeks (transpacific shipping + customs)
- **Estimated Cost:** ~$30/kg (aerospace-grade, reflecting quality premium and shipping)
- **Aerospace Qualification:** Fully qualified; Japan supplies 67% of US titanium sponge imports
- **Disruption History:**
  - Generally very reliable; Japan is considered the most stable source for Western aerospace titanium sponge
  - 2011 Tohoku earthquake/tsunami temporarily disrupted Japanese industrial production broadly (not Toho-specific, but scenario-relevant)
  - Capacity expansion underway (construction began Jan 2026)
- **Simulation Notes:** Key alternative supplier post-VSMPO disruption; represents reliability with moderate lead time

**Sources:**
- Toho Titanium corporate announcement, "Expansion of Sponge Titanium Production Capacity" (Oct 2023) [15]
- USGS MCS 2025 [1]
- Argus Media [2]

### 3.4 ATI Inc (United States)

- **Headquarters:** Dallas, Texas, USA
- **Annual Capacity:** ~10,000 MT/yr titanium mill products (pre-expansion); growing to ~18,000 MT/yr by late 2025 (80% increase over FY2022 baseline)
- **Capacity (kg/week):** ~192,000 kg/week (at expanded capacity)
- **Lead Time to US:** 10 weeks (domestic, shortest among major producers)
- **Estimated Cost:** ~$38/kg (premium domestic, aerospace-certified)
- **Aerospace Qualification:** Fully qualified; signed multi-year contract with Airbus (May 2025) for titanium plate, sheet, and billet. Major Boeing and defense supplier.
- **Disruption History:**
  - Restarted Albany, OR melt capacity in FY2023; fourth furnace online H1 FY2024
  - Richland, WA expansion substantially completed late 2024, equipment operating early 2025
  - Legacy Allegheny Technologies name; rebranded to ATI Inc
- **Simulation Notes:** Fastest lead time; actively expanding; most responsive to surge demand

**Sources:**
- ATI 2024 Annual Report [16]
- ATI press release, "Richland Washington titanium melt expansion" (2023) [17]
- Tri-Cities Area Journal of Business, "ATI plant expansion" [18]

### 3.5 Baoji Titanium Industry / BAOTI (China)

- **Headquarters:** Baoji, Shaanxi Province, China (the "Titanium Valley" of China)
- **Annual Capacity:** 30,000 MT/yr ingot capacity; 20,000 MT/yr finished mill products
- **Capacity (kg/week):** ~385,000 kg/week (mill products)
- **Lead Time to US:** 18 weeks (transpacific shipping + extended customs/certification delays)
- **Estimated Cost:** ~$22/kg (significantly lower than Western producers)
- **Aerospace Qualification:** Qualified by Boeing, Airbus, Rolls-Royce, Bombardier, Snecma, and others for specific non-critical applications. Chinese titanium sponge is generally NOT qualified for critical aerospace structures in Western programs.
- **Disruption History:**
  - US-China trade tensions and tariffs create procurement uncertainty
  - Chinese titanium increasingly redirected to domestic COMAC C919 and military programs (J-36)
  - Quality consistency concerns for highest-specification aerospace applications
  - Geopolitical risk of export restrictions or tariff escalation
- **Simulation Notes:** Lowest cost but highest qualification risk; represents the cost-vs-qualification tradeoff

**Sources:**
- BAOTI corporate website, "About" section [19]
- Airframer, company profiles [20]
- Major-Ti.com, "After The World's Largest Production Capacity, China's Titanium Advantages" [21]

### 3.6 Kobe Steel / KOBELCO Titanium (Japan)

- **Headquarters:** Kobe, Hyogo, Japan
- **Annual Capacity:** ~6,000 MT/yr titanium products (forgings, bar, plate)
- **Capacity (kg/week):** ~115,000 kg/week
- **Lead Time to US:** 14 weeks
- **Estimated Cost:** ~$33/kg
- **Aerospace Qualification:** Qualified by Rolls-Royce (first Japanese supplier, 2001), Airbus (A350 XWB landing gear forgings), GE (via IHI for large jet engine shafts). Expanding ring rolling capacity at Takasago Works.
- **Disruption History:**
  - **2017 Data Falsification Scandal:** Kobe Steel admitted to deliberately falsifying strength and quality data on aluminum, copper, and steel products shipped to over 600 companies. The practice dated back to the 1970s, involved 40+ employees across 23 plants, and affected 20,000+ tons of product. Customers included Boeing, Airbus, GM, Ford. Kobe Steel was fined 100 million yen. The scandal severely damaged the "Made in Japan" quality reputation.
  - Company has since implemented remediation and strengthened quality controls
  - May 2025: Collaborating on ultra-lightweight Ti alloys for next-gen aircraft
- **Simulation Notes:** Represents the "quality scandal" disruption scenario; good for modeling trust/reputation recovery dynamics

**Sources:**
- Kobe Steel corporate, "Top Titanium Manufacturer Kobelco Titanium" [22]
- Kobe Steel press release, "Titanium alloy forged material for large jet engine" [23]
- Bloomberg, "Kobe Steel Faked Data for Metal Used in Planes and Cars" (2017) [24]
- Supply Chain Dive, "Kobe Steel's quality scandal" [25]

### 3.7 Western Superconducting Technologies / WST (China)

- **Headquarters:** Xi'an, Shaanxi Province, China
- **Annual Capacity:** ~15,000 MT/yr high-performance titanium alloy products
- **Capacity (kg/week):** ~288,000 kg/week
- **Lead Time to US:** 20 weeks (longest; limited trade channels for aerospace)
- **Estimated Cost:** ~$20/kg
- **Aerospace Qualification:** Primarily serves Chinese domestic aerospace market (COMAC, AVIC, Chinese military). Limited Western aerospace qualification. World-leading production line for high-end Ti alloy bars.
- **Disruption History:**
  - Subject to potential US export control scrutiny as a Chinese defense-adjacent company
  - CITIC Metal is a major investor
  - Capacity expanding with new SMS group 63/80-MN forging press
- **Simulation Notes:** Represents the "emerging competitor" with low cost but highest geopolitical and qualification barriers

**Sources:**
- WST corporate website [26]
- CITIC Metal, "WST Investments" [27]
- Thermprocess Online, "More capacity at Chinese titanium manufacturer WST" [28]

### 3.8 Howmet Aerospace / formerly RTI International Metals (United States)

- **Headquarters:** Pittsburgh, Pennsylvania, USA
- **Annual Capacity:** ~9,000 MT/yr titanium mill products and forgings
- **Capacity (kg/week):** ~173,000 kg/week
- **Lead Time to US:** 12 weeks (domestic)
- **Estimated Cost:** ~$36/kg
- **Aerospace Qualification:** Fully qualified across all major OEMs. Key supplier for Boeing 787 Dreamliner and Airbus A350. Vertically integrated titanium processing.
- **Disruption History:**
  - RTI acquired by Alcoa in 2015; Alcoa split into Arconic + Alcoa Corp in 2016; Arconic split into Howmet Aerospace + Arconic Corp in 2020
  - Corporate restructuring created some supply chain complexity during transitions
  - Now stable under Howmet Aerospace brand
- **Simulation Notes:** Reliable domestic alternative; strong in forgings; premium pricing

**Sources:**
- Wikipedia, "RTI International Metals" [29]
- Kings Research, "Top 10 Aerospace Titanium Vendors Worldwide in 2024" [30]

---

## 4. Lead Time Analysis

Specific published lead-time data for aerospace titanium bar stock is not widely available in public sources due to confidential nature of OEM supply agreements. The following estimates are synthesized from industry reports, trade publications, and procurement discussions.

| Supplier | Est. Lead Time (weeks) | Basis |
|----------|----------------------|-------|
| ATI Inc | 10 | Domestic US, large inventory, expanding capacity |
| TIMET | 12 | Domestic US, established distribution |
| Howmet Aerospace | 12 | Domestic US, vertically integrated |
| Toho Titanium | 14 | Transpacific shipping (~4 wks) + production |
| Kobe Steel | 14 | Transpacific shipping (~4 wks) + production |
| VSMPO-AVISMA | 16 | Effectively unavailable for new Western contracts |
| BAOTI | 18 | Transpacific + extended certification/customs |
| WST | 20 | Limited Western trade channels |

**Key factors affecting lead times (2024-2025):**
- Aerospace Ti supply chain recovery from post-COVID and post-Ukraine-war disruptions is ongoing [31]
- Certification bottlenecks (NADCAP, OEM-specific) add 4-12 weeks beyond raw material availability [32]
- Port congestion and elevated shipping costs extend international lead times [31]
- Increased demand from Boeing 737 MAX ramp-up and Airbus A320neo production rate increases

**Sources:**
- Roland Berger, "Aerospace supply chain report 2025" [31]
- NAMF, "NADCAP Approved Suppliers" [32]
- Thomas Net, "Why Is There a Titanium Shortage?" [33]

---

## 5. Aerospace Supplier Qualification Timeline

Qualifying a new titanium supplier for aerospace applications is a multi-year process:

| Phase | Duration | Description |
|-------|----------|-------------|
| NADCAP accreditation | 3-6 months | Special process certification (melting, forging, heat treatment) |
| OEM supplier audit | 6-12 months | Boeing D1-4426, Airbus AQPL, etc. |
| First article / validation batch | 6-12 months | Production qualification with full traceability |
| Probationary supply period | 6-12 months | Minimum 3 consecutive accepted shipments |
| **Total (structural grades)** | **1-3 years** | Non-rotating structural applications |
| **Total (engine/rotating)** | **3-5+ years** | Prime-quality rotating-grade titanium |

This long qualification cycle is a critical factor in the supply chain simulation: when a disruption occurs, new suppliers cannot be rapidly substituted.

**Sources:**
- QStrat, "Best Practices for Supplier Qualification in Aerospace" [34]
- Sensata/Kavlico, "Aerospace Procedure for Supplier Quality" [35]
- Lockheed Martin, "Supplier Quality Requirements" [36]

---

## 6. Notable Disruption Scenarios for Simulation

### Scenario 1: Russian Titanium Embargo (Based on Real Events, 2022-present)
- VSMPO-AVISMA supplies cut off due to sanctions expansion
- Impact: Loss of ~15-20% of Western aerospace titanium supply
- Response: Shift to Japanese (Toho, Kobe Steel) and US (ATI, TIMET, Howmet) producers
- Price impact: Near-tripling of ingot prices observed in 2022-2024

### Scenario 2: Quality Scandal (Based on Kobe Steel 2017)
- Major supplier caught falsifying quality data
- Impact: Immediate grounding/quarantine of all material from that supplier
- Response: Emergency qualification of alternative sources; 6-18 month disruption
- Cascading effects on all customers sharing that supplier

### Scenario 3: Natural Disaster (Based on 2011 Tohoku Earthquake)
- Japanese production facilities damaged or disrupted
- Impact: Loss of 67% of US sponge import source
- Response: Draw on Saudi Arabia, Kazakhstan; attempt Henderson NV sponge restart
- Lead time extension: 4-8 additional weeks across supply chain

### Scenario 4: Chinese Export Restrictions
- China restricts titanium exports (as done with gallium/germanium in 2023)
- Impact: Loss of lowest-cost supply; 57% of global sponge production affected
- Response: Non-Chinese sources already capacity-constrained; severe shortage
- Price impact: Potential 2-3x price increase for non-Chinese supply

---

## 7. Data Quality Notes

- Production capacity figures are compiled from corporate disclosures, USGS data, and industry estimates. Exact figures are commercially sensitive and may vary.
- Pricing is approximate and reflects 2025-2026 market conditions for aerospace-grade Ti-6Al-4V bar stock. Actual contract pricing varies with volume, specification, and relationship.
- Lead times are estimated based on geographic distance, known production schedules, and industry reports. They do not reflect specific contractual commitments.
- Quality ratings in the CSV (0.0-1.0 scale) are the author's synthesis based on aerospace qualification status, disruption history, and industry reputation -- not a standardized metric.
- The `is_qualified` column refers specifically to current qualification status for critical aerospace structural applications by major Western OEMs (Boeing, Airbus).

---

## References

[1] USGS, "Mineral Commodity Summaries 2025 - Titanium and Titanium Dioxide," https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-titanium.pdf

[2] Argus Media, "Aerospace-approved Ti sponge supply up in 2024," https://www.argusmedia.com/en/news-and-insights/latest-market-news/2659047-aerospace-approved-ti-sponge-supply-up-in-2024

[3] World Population Review, "Titanium Production by Country 2026," https://worldpopulationreview.com/country-rankings/titanium-production-by-country

[4] Pakshal Steel, "Titanium Metal Price Per Kg - Latest 2026 Price List," https://www.pakshalsteel.com/titanium-metal-price.html

[5] Partsproto, "Cost of Titanium in 2025: Prices, Factors, and Market Insights," https://partsproto.com/cost-of-titanium

[6] AeroTime, "The titanium supply chain crisis: how it began and what it means for aerospace," https://www.aerotime.aero/articles/32464-titanium-supply-crisis-what-does-this-mean-for-aerospace

[7] Argus Metals, "Titanium 6Al 4V ingot FOB US producer prices," https://www.argusmedia.com/metals-platform/price/assessment/titanium-6al-4v-ingot-fob-us-producer-prices-PA00191280000

[8] Wikipedia, "VSMPO-AVISMA," https://en.wikipedia.org/wiki/VSMPO-AVISMA

[9] Quest Metals, "Western Aerospace's Dependence on Russian Supply," https://www.questmetals.com/blog/western-aerospace-s-dependence-on-russian-supply

[10] Euronews, "Boeing suspends Russian titanium as Airbus keeps buying," https://www.euronews.com/next/2022/03/07/ukraine-crisis-boeing-russia

[11] EU Political Report, "Pressure for Sanctions on Russian Titanium," https://eupoliticalreport.com/pressure-for-sanctions-on-russian-titanium/

[12] Wikipedia, "Titanium Metals Corporation," https://en.wikipedia.org/wiki/Titanium_Metals_Corporation

[13] TIMET, corporate website, https://www.timet.com/

[14] Jackson County, WV, "PCC Ravenswood," https://www.jacksoncountygrows.com/pcc.html

[15] Toho Titanium, "Expansion of Sponge Titanium Production Capacity," Oct 2023, https://www.toho-titanium.co.jp/2023/10/expansion-of-sponge-titanium-production-capacity/

[16] ATI Inc, "2024 Annual Report," https://s27.q4cdn.com/226628310/files/doc_financials/2024/ar/ATI-2024-Annual-Report-March-2025.pdf

[17] ATI Inc, "ATI announces Richland, Washington as site of titanium melt expansion," 2023, https://ir.atimaterials.com/news-events/news-details/2023/ATI-announces-Richland-Washington-as-site-of-titanium-melt-expansion/

[18] Tri-Cities Area Journal of Business, "ATI plant expansion is ready to meet soaring demand for titanium," https://www.tricitiesbusinessnews.com/articles/ati-plant-expansion

[19] BAOTI, "About," http://www.baoti.com/en/about.php?cat_id=1975

[20] Airframer, "Western Superconducting Technologies Co. Ltd. (WST)," https://www.airframer.com/direct_detail.html?company=167151

[21] Major-Ti.com, "After The World's Largest Production Capacity, China's Titanium Advantages," https://www.major-ti.com/news/after-the-world-s-largest-production-capacity-85321961.html

[22] Kobe Steel, "Top Titanium Manufacturer Kobelco Titanium," https://www.kobelco.co.jp/english/titan/kobelco/index.html

[23] Kobe Steel, "Begins mass production of titanium alloy forged material for large jet engine made by GE," https://www.kobelco.co.jp/english/releases/1196209_15581.html

[24] Bloomberg, "Kobe Steel Faked Data for Metal Used in Planes and Cars," Oct 2017, https://www.bloomberg.com/news/articles/2017-10-10/kobe-steel-untraded-amid-deluge-of-sell-orders-on-data-scandal

[25] Supply Chain Dive, "Kobe Steel's quality scandal is an age-old supply chain tale," https://www.supplychaindive.com/news/Kobe-Steel-scandal-data-supplier-fraud/507729/

[26] Western Superconducting Technologies, corporate website, https://en.c-wst.com/

[27] CITIC Metal, "WST Investments," https://www.metal.citic/en/business/details_18_43.html

[28] Thermprocess Online, "More capacity at Chinese titanium manufacturer WST," https://www.thermprocess-online.com/en/News/Business_News/More_capacity_at_Chinese_titanium_manufacturer_WST

[29] Wikipedia, "RTI International Metals," https://en.wikipedia.org/wiki/RTI_International_Metals

[30] Kings Research, "Top 10 Aerospace Titanium Vendors Worldwide in 2024," https://www.kingsresearch.com/blog/top-10-aerospace-titanium-vendors-worldwide-2024

[31] Roland Berger, "Aerospace supply chain report 2025: Is the crisis over?" https://www.rolandberger.com/en/Insights/Publications/Aerospace-supply-chain-report-2025-Is-the-crisis-over.html

[32] NAMF, "NADCAP Approved Suppliers: Why Companies Choose Them," https://www.namf.com/what-it-means-to-be-nadcap-approved/

[33] Thomas Net, "Why Is There a Titanium Shortage? What It Means for Aerospace," https://www.thomasnet.com/insights/titanium-shortage/

[34] QStrat, "Best Practices for Supplier Qualification in Aerospace," https://qstrat.com/supplier-qualification-best-practices-aerospace/

[35] Sensata/Kavlico, "Aerospace Procedure for Supplier Quality," https://www.sensata.com/sites/default/files/a/kavlico-supplier-quality-requirements-manual-ap0425.pdf

[36] Lockheed Martin, "Supplier Quality Requirements," https://www.lockheedmartin.com/content/dam/lockheed-martin/eo/documents/suppliers/rms/rms-quality-procure-2-011-052023.pdf
