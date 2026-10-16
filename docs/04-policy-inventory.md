# 04 · Disclaimer and policy inventory (stage 1 — inventory only)

**Status:** no wording has been redrafted. The existing text stays in the build until replacement wording is approved. Nothing here is legal advice, and nothing is described as compliant. Authoritative sources (ICO, FCA Handbook/register, legislation.gov.uk) have **not yet been consulted**; that happens in stage 2 once the facts in §3 are confirmed, and each source will be recorded with its access date.

## 1. Inventory

| Item | Where | Existing text (verbatim copies in `audit/baseline/text/`) | Last-updated marker |
|---|---|---|---|
| Regulatory statement | Footer, every page | "GLOBAL WEALTH MANAGEMENT SOLUTIONS LLP IS AUTHORISED AND REGULATED BY THE FINANCIAL CONDUCT AUTHORITY REF:678746." | none |
| Credentials | `/about-gwms` | "Global Wealth Management Solutions LLP is authorised and regulated by the Financial Conduct Authority (ref 678746)." | none |
| Entry notice (modal, Accept/Decline) | Markup on every page | "Global Wealth Management Solutions deals exclusively with Intermediaries … none of its content should be construed as explicit or implicit advice of any kind." + "Cookie Statement" paragraph | none |
| Cookie bar (plugin) | Every page | "We use cookies to improve your experience … By browsing this website, you agree to our use of cookies." | none |
| Cookie Information | `/cookie-information` | 4 cookie descriptions (disclaimer pop-up, analytics, CMS session) | none |
| Disclaimer / site terms | `/disclaimer` | "General Site Terms and Conditions": Advice, Variation of content, Disclaimer | none |
| Privacy Notice | `/privacy-notice` | ~1,190 words | "Last updated: 25 May 2018" |
| Product qualifications on fund/platform pages | various | e.g. footnote "[1] as of 31 July 2023" (ASK); Morningstar rating; performance statements | see §2 |

## 2. Potential issues found (observations, not conclusions)

**Inconsistencies between policy text and the live site**
1. Cookie Information says the site uses cookies "for the essential running of the website" (entry notice) and that analytics cookies "do NOT identify any person" — yet Google Analytics loads on first page view before any choice is made (measured), and the cookie bar's *Decline* does not stop it. *Dependency: is analytics intended to stay? Is consent being obtained?*
2. Cookie Information says "…agree to the Disclaimer of using **darwinpim.com**" — a different organisation's domain, apparently carried over from another site.
3. Privacy Notice says the **Contact page** lets people submit a name, e-mail and message. The Contact page has no form; it lists names, phone numbers and e-mail links.
4. Privacy Notice links to `https://globalwms.com/about` (404) and `https://globalwms.com/cookie-information.` (trailing full stop → 404).
5. Privacy Notice calls it a "Cookie Policy"; the page is titled "Cookie Information".
6. Privacy Notice list of recipients is numbered (i), (ii), (iv), (v) — (iii) missing.
7. Privacy Notice says servers are "located in the EU and the US" and relies on Standard Contractual Clauses; hosting location/provider is unconfirmed. It also states the data controller as "Global Wealth Management Solutions, a limited liability partnership" at *Wrest Park, Silsoe*, whereas the regulatory line says "…Solutions **LLP**" and the PDF form shows *Sunnyhill House, Great Horwood*. Registered name, address and ICO registration need confirming.
8. Privacy Notice contact route is a Privacy@ address only; no ICO registration number, no DPO statement, no named retention periods.
9. Privacy Notice dated 25 May 2018 (GDPR commencement date) and refers to "EU privacy rules"; it does not mention UK GDPR / Data Protection Act 2018 or post-2021 UK/EU transfer mechanisms (UK IDTA / Addendum).
10. Disclaimer says "buy any … product **from this site**" — the site sells nothing (see decision D8).
11. Disclaimer reserves the right to vary terms "without notice" and treats continued use as acceptance; no date or version.
12. The entry notice's **Decline** sends the visitor to google.com.

**Regulatory-claim wording that compliance should review before anything is republished** (content is preserved unchanged; I am not changing or judging it):
- Levendi: "SONIA + 6.00%", "top decile of Absolute Return Funds in the UK", "Proven, award-winning strategy", "Since inception … more years of positive performance than any of the markets…" — no dates, sources or past-performance warnings on the page.
- Pecora Manning & Napier: "Morningstar 5 Star Rating … (MNHAX)" — undated.
- ASK: "AUM of ~USD 10.1 billion[1]" is footnoted "as of 31 July 2023" but "USD 2.4 billion in AUM" and "13 years" are undated.
- 1OAK: "Up to 4% initial commission and 0.75% pa trail fee" — commission terms stated on a public page.
- Platforms: "100% Client Asset Protection", "at least 90% of client assets" (GFSC), "$20 billion in assets under administration".
- The site states the audience is intermediaries only, but it carries no wording identifying who counts as an eligible intermediary.

## 3. Facts needed before any redrafting (please confirm)

1. Is analytics (Google Analytics/GTM) to be kept? If yes: consent mechanism, account owner, IP-anonymisation/retention settings. If no: remove, and cookie wording simplifies.
2. Will the new site use **any** cookie or storage at all? (My default: none — static, no analytics, no session cookie, no fonts from Google. The entry-notice choice can be remembered with no cookie at all, or not remembered.)
3. Is there any form, mailing list, enquiry route or third-party widget on the new site? (My default: none; only `mailto:` links.)
4. Hosting provider and country for the new static site (needed for "International data transfers").
5. Correct legal entity name, registered office, FCA firm reference verification, ICO registration number, data-protection contact.
6. Is the entry notice (Accept/Decline) a compliance requirement or a legacy feature? What is the intended consequence of Decline?
7. Who is the approving person (compliance adviser: the About page names *FM Consult*; legal: *BDB Pitmans LLP*) for stage 2 review?

## 4. Stage 2 plan (after you answer §3)

For each document I will deliver one review table: **existing wording · proposed wording · reason · supporting source or factual dependency · questions for qualified legal/compliance review**, marked "DRAFT — not approved". Sources to consult and date-stamp: ICO guidance on cookies/storage and access technologies and on privacy notices; PECR 2003 and the Data (Use and Access) Act 2025 as amended; UK GDPR Art. 13/14; the FCA Handbook on financial promotions and the FCA register entry for ref 678746; Companies House/LLP registration for entity details. Until each is approved, the build keeps the existing text.
