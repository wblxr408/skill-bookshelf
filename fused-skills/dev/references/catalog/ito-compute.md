# ito-compute

Read only relevant technical detail. The local contract governs source mandates, test style, tool/agent usage and user authorization.

| Capability | Existing owner / integration | Use when |
|---|---|---|
| [ito-compute](../../modules/ecc/library/ito-compute/GUIDE.md) | dev / engineering-toolbox; technical-reference | Query live GPU inventory, submit an authenticated Itô fixed-rate RFQ, inspect RFQ or procurement status, revoke device credentials, and run explicitly gated node qualification through the separately installed canonical C |
| [ito-inference](../../modules/ecc/library/ito-inference/GUIDE.md) | dev / engineering-toolbox; technical-reference | Inspect the availability of model serving on a completed Itô compute booking and, when the canonical backend becomes available, hand off an explicitly confirmed serving manifest. Use after ito-compute has booked GPU node |
| [ito-training](../../modules/ecc/library/ito-training/GUIDE.md) | dev / engineering-toolbox; technical-reference | Inspect the availability of ML training on a completed Itô compute booking and, when the canonical backend becomes available, hand off an explicitly confirmed training manifest. Use after ito-compute has booked GPU nodes |
