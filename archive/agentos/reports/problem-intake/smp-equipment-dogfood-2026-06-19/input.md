# SMP Equipment Dogfood Input

## Problem Statement

The ambulance station has poor control over medical equipment movement, frequent loss of inventory, and fragmented documentation that does not reflect factual equipment availability.

## Target User

- Ambulance crew doctors.
- Ambulance crew feldshers.
- Ambulance crew nurses.
- Duty room feldsher.
- Senior feldsher.
- Station manager.
- Material support department staff.
- Deputy chief physician.
- Chief physician.

## Current Workflow

Equipment arrives through the health department, acceptance paperwork is created, documentation is started, and equipment is distributed to substations and then to crews. Each shift formally receives and hands over the ambulance with paper checklists, but factual verification is often partial. The duty room keeps a journal that is not filled consistently, and the material support department maintains Excel that reflects the expected rather than factual distribution state.

## Desired Outcome

Create a reviewable technical assignment draft for an equipment control system that shows factual availability, condition, location, and accountable chain for each equipment unit over time.

## Constraints

- Every significant equipment interaction must leave an electronic trace.
- Crew work must not be blocked if replacement equipment is unavailable.
- Recording actions must stay practical for field use and should fit within about 5 minutes.
- Primary working devices are personal phones and tablets.
- Connectivity usually exists, but operating flow must account for non-ideal network conditions.

## Known Risks

- Formal transfer records may not match factual equipment condition.
- Shift-to-shift handover is the main source of drift and disputes.
- Replacement equipment creates secondary traceability loss when issued under time pressure.
- Repair and calibration visibility is concentrated in the material support department.
- Broad "record every interaction" scope may overload users if significant interactions are not bounded carefully.

## Open Questions

- Exact access matrix by role remains to be defined.
- The boundary between significant interaction and ordinary use still needs formal definition.
- MVP coverage by equipment category is not finalized.
- Required management reports are not finalized.
- Escalation rules for each violation type are not finalized.
- Exceptions for inter-substation transfer need a dedicated pass.

## Data Discovery

Each equipment unit may have an inventory number, assigned substation, assigned crew context, repair state, calibration state, loss state, write-off state, donor-for-parts state, and transfer history. Inventory numbers exist today but are often hard to verify because they are long or partially erased.

## Information Flow

Health department intake -> station documentation -> substation distribution -> crew assignment -> shift handover / replacement / transfer / repair / calibration / write-off events -> factual state and accountability recovery.

## Access / Permissions

Only humans may approve execution, commit, push, release, production use, or protected lifecycle changes. Operationally, the duty room, senior feldsher, station manager, and material support department have different visibility and escalation responsibilities.

## Requirements

- Preserve factual history of significant equipment interactions.
- Separate expected assigned equipment from factual current state.
- Support shift handover, replacement issue/return, inter-substation transfer, repair, calibration, write-off, and donor-for-parts lifecycle.
- Keep accountability visible without blocking brigade continuity.
- Surface mismatches, defects, incomplete sets, and overdue service states.

## Acceptance Criteria

- Draft artifacts preserve the current process pain and target model without claiming approval.
- Core transfer event data is explicit.
- UNKNOWN remains visible.
- No artifact claims execution, implementation, or production authorization.

## MVP

Prioritize shift-to-shift handover, replacement issue/return, and factual state visibility for expensive equipment first, while keeping the long-term model open to all equipment units.

## Implementation Hints

Personal mobile devices are the realistic operational entry point. The model should optimize around quick event capture rather than retrospective reconciliation only.

## Contradictions

- Formal handover exists, but factual verification is often weak.
- Equipment may continue to be used with defects or expired calibration if no replacement exists.
