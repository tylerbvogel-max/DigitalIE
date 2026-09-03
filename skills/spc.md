# Statistical process control

Before charting, confirm operational definition, measurement-system suitability, rational subgrouping, sample window, and data completeness. Declare chart choice, constants, rules, and inputs.

For I–MR use \(MR_i=|x_i-x_{i-1}|\), \(\hat\sigma=\bar{MR}/1.128\), and individual limits \(\bar x\pm3\hat\sigma\). For X-bar/R use \(\bar{\bar x}\pm A_2\bar R\) and \([D_3\bar R,D_4\bar R]\) with verified subgroup constants. For a p chart use \(\bar p\pm3\sqrt{\bar p(1-\bar p)/n_i}\), truncating the lower probability limit at zero.

Analyze dispersion first. Distinguish control limits from specifications. A signal identifies a special-cause period, not its cause. Capability requires stability and declared within/overall variation. See [the full calculation playbook](../playbooks/industrial-engineering/05-spc.md).
