# Data Quality Report

## Summary
- Rows loaded: 45
- Rows excluded (known customer): 1
- Rows quarantined (status not verified): 18
- Rows eligible for scoring (before dedup): 26
- Duplicates removed: 0
- Rows eligible for scoring (after dedup): 26

## What was excluded and why
      company_name            status
Pfanner Holding AG excluded_customer

## What was quarantined and why
                                company_name           status
                         ROTOP Pharmaka GmbH      verify_date
                                    Mindcurv verify_ownership
                                 FACT-Finder verify_ownership
                          Robert Bürkle GmbH verify_ownership
                           häussermann group verify_ownership
                    Rossmanith GmbH & Co. KG       verify_url
Energiekonzepte Mitteldeutschland GmbH (EKM) verify_ownership
                            Oxalis Logistics  verify_location
                          mindful collection  verify_location
                               Contus-Gruppe   verify_article
                    A. Schmidt GmbH & Co. KG   verify_article
                  Schlau Elektrotechnik GmbH   verify_article
                                  WWB Gruppe   verify_article
                             Bäckerei Sommer   verify_article
                        Topinstallateur GmbH   verify_details
                        StrikoWestofen Group verify_ownership
                            Cornelsen Verlag   verify_icp_fit
                                    BayWa AG   verify_icp_fit

## ICP size flags
icp_size_flag
in_range    26

## Decisions documented
- "unknown" is treated as "no data", not "no". A row with
  pe_backed=unknown is not scored as if it were pe_backed=no.
- Rows with status verify_* are quarantined, not deleted.
  They remain in the dataset for audit; they are simply not
  scored until a human verifies them.
- Excluded rows (customers) are kept in a separate file, not
  deleted. The record of *why* a company was excluded is
  itself useful data.
- Company names were normalized (lowercase, legal suffixes
  stripped, whitespace collapsed) before deduplication.
- ICP size flags are derived from notes, not from a dedicated
  employees column (which we don't have). The flag is honest:
  it reflects facts we recorded, not assumptions.
