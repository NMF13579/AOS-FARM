# Simple Control Fixtures

This directory is reserved for AOS-FARM.681 Simple Control Surface contract, menu, planning, validation, and derived-status fixtures.

The targeted tests generate temporary negative fixtures from the canonical contract files so each mutation stays local to the test process.

AOS-FARM.681.5 tests construct validation bundles in memory. They do not persist decision records, Evidence, operation ledgers, status caches, or task files.

AOS-FARM.681.6 tests construct execution requests, execution authorization witnesses, previews, and execution packages in memory. They do not apply planned actions, create operation journals, mark witnesses consumed, or write product files.

AOS-FARM.681.7 tests validate controlled local writes only in temporary sandbox directories. They may create sandbox operation records under that sandbox's `.aos-tmp/simple-control/` path, but they do not apply the backend to the active AOS-FARM repository, do not touch accepted candidate artifacts through the backend, and do not perform commit, push, integration, lifecycle mutation, or platform enforcement.

AOS-FARM.681.8 tests validate commit and Build-branch push controls only in temporary Git repositories and local bare remotes. They do not stage, commit, or push the active AOS-FARM repository; do not contact GitHub; and do not grant integration, release, lifecycle mutation, or approval.
