# ASL Platform

ASL means Active Sustainment Loop. These documents describe a package-level control and resilience architecture for AI chiplet systems.

## Documents

- **ASL Dual-Scale Macro Ring Memo v0.1**: full Z-matrix verification of the outer macro ring. It records provisional operating windows and notes that the Monte Carlo robustness gate has not reached the 90% target.
- **ASL Platform Spec v0.1**: architecture and interface specification for an ASL-enabled AI chiplet platform. ASL is a parallel control fabric for reset, health sensing, emergency control, and field sustainment; it does not replace UCIe, SerDes, NVLink, or other high-speed data fabrics.
- **ASL Formal Closure v0.1**: formal boundary and evidence summary. The model supports full sustainment up to 30% outer-ring current degradation under stated limits; higher degradation is mitigation only.

## Evidence status

The documents are model-supported and based on FastHenry extraction, coupled-circuit models, and control simulations. They are not silicon-validated. Open engineering work includes square-ring re-extraction, driver-circuit verification, power-integrity and return-path analysis, electromigration checks, receiver/BER validation, and full-wave electromagnetic validation.

## Publication note

These are provisional working documents and were previously marked confidential. They are published here at the repository owner's direction. Technical and commercial claims should be treated as research-stage claims until independent hardware validation is completed.
