# Quantitative reliability analysis skill

## Trigger

Use for MTBF, MTTF, MTTR, availability, life-distribution, system reliability,
or reliability-demonstration questions.

## Method

1. Identify the item/configuration, mission, environment, repairable status,
   failure definition, exposure units, censoring, and data source.
2. Keep observed metrics, fitted parameters, predictions, and requirements in
   separate fields.
3. Select a model only after checking physical failure behavior and data fit.
   Constant hazard is an assumption, not a default truth.
4. Use series, parallel, or k-out-of-n arithmetic only after the success logic
   and independence assumptions are accepted.
5. Use zero-failure planning only for its stated binomial or exponential case;
   route richer qualification plans to reliability and test engineering.
6. Report undefined values honestly. Zero failures do not imply infinite MTBF.
7. Connect results to FRACAS, FMEA, maintenance, spares, design, and verification
   evidence without autonomously changing any controlled plan.

## Stop conditions

Stop when the failure definition changes within the dataset, exposure is
unknown, repairable and nonrepairable populations are mixed, model fit is
unsupported, common-cause dependence is material, or acceptance authority is
unclear.

## Outputs

Produce the evidence and population definition, metric receipt, model basis,
assumption and limitation register, uncertainty statement, sensitivity or
alternative-model comparison, and required human review path.
