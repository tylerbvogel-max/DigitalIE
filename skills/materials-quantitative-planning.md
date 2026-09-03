# Materials quantitative planning

**Use when:** demand history or item-planning data needs a reproducible forecast, accuracy assessment, EOQ, reorder point, safety stock, or time-phased single-item MRP calculation.

**Do:** identify item/configuration/site, units, horizon and bucket, demand source, outlier and zero treatment, service definition, replenishment assumptions, lead-time basis, inventory status, lot policy, and master-data provenance; preserve fitted-period alignment and all exceptions.

**Stop when:** histories mix unlike demand; configuration effectivity is unresolved; lead time or demand is dependent but the independent model is proposed; safety stock is being used to conceal planning defects; BOM/yield/unit conversion is unverified; or the result is being treated as an authorized buy/release.

**Output:** planning context, formula and policy, raw data, receipt, excluded observations, sensitivities, past-due releases, constraint checks, planner disposition, and approval authority. See [the planning calculation playbook](../playbooks/materials-supply-chain/07-forecasting-inventory-and-mrp-calculations.md).
