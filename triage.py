"""Small, deterministic educational rules for hypothetical Google Search cases."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Case:
    name: str
    status: int | None
    crawl: str
    directive: str
    canonical: str
    content: str

@dataclass(frozen=True)
class Finding:
    state: str
    explanation: str
    next_step: str

CASES = (
    Case('Healthy article', 200, 'Allowed', 'Absent', 'Self', 'Substantive'),
    Case('Robots blocked + reported noindex', 200, 'Blocked', 'Noindex', 'Self', 'Substantive'),
    Case('Accessible noindex page', 200, 'Allowed', 'Noindex', 'Self', 'Substantive'),
    Case('Duplicate URL', 200, 'Allowed', 'Absent', 'Other', 'Substantive'),
    Case('Permanent redirect', 301, 'Allowed', 'Unknown', 'Unknown', 'Unknown'),
    Case('Removed URL', 404, 'Allowed', 'Unknown', 'Unknown', 'Unknown'),
    Case('Temporary server error', 503, 'Allowed', 'Unknown', 'Unknown', 'Unknown'),
    Case('Rate limited', 429, 'Allowed', 'Unknown', 'Unknown', 'Unknown'),
    Case('Empty success page', 200, 'Allowed', 'Absent', 'Self', 'Thin or error-like'),
    Case('Incomplete evidence', None, 'Unknown', 'Unknown', 'Unknown', 'Unknown'),
)

def assess(c: Case) -> Finding:
    """Triage known signals, never infer Google-selected canonical or indexed state."""
    if c.crawl == 'Blocked':
        return Finding('Crawl blocked', 'A crawler may not see the page content or its noindex directive. A blocked URL may still be known to Search.', 'Check whether blocking is intentional. If noindex is required, permit crawling so the directive can be seen.')
    if c.crawl != 'Allowed' or c.status is None:
        return Finding('Evidence missing', 'Crawler access or response status is unknown.', 'Verify crawler access and the response with URL Inspection before drawing a conclusion.')
    if c.status == 429 or 500 <= c.status <= 599:
        return Finding('Temporary availability issue', 'Throttling or a server error can interrupt crawling and processing; persistent errors can affect indexing.', 'Investigate availability and rate limits, then retest after recovery.')
    if 300 <= c.status <= 399:
        return Finding('Redirect: inspect destination', 'A redirect is not an ordinary indexable content response. The destination must be checked separately.', 'Check the redirect target, chain and intended canonical destination.')
    if 400 <= c.status <= 499:
        return Finding('Client error', 'The observed response is a client error rather than working indexable content.', 'Confirm whether removal or restricted access is intentional; repair unexpected errors.')
    if c.status != 200:
        return Finding('Other HTTP response', 'This simplified lab does not classify this status as a working 200 page.', 'Consult the HTTP-status documentation and gather more evidence.')
    if c.directive == 'Noindex':
        return Finding('Noindex observed', 'When Google can crawl and read a supported noindex directive, the page is excluded from indexing.', 'If the page should be indexed, remove the unintended directive and request a fresh inspection.')
    if c.directive != 'Absent' or c.canonical == 'Unknown' or c.content == 'Unknown':
        return Finding('Evidence missing', 'One or more necessary checks have not been observed.', 'Inspect the rendered content, indexing directives and canonical signals.')
    if c.content == 'Thin or error-like':
        return Finding('Content review needed', 'A success status alone does not prove useful indexable content; an error-like page can be treated as a soft 404.', 'Inspect the rendered page and intended content; confirm the response matches its purpose.')
    if c.canonical == 'Other':
        return Finding('Canonical review needed', 'The declared canonical points elsewhere. Canonical declarations are signals, not proof of Google\'s selected URL.', 'Check whether consolidation is intended and inspect the target and Google-selected canonical.')
    return Finding('Technical candidate', 'The modeled access, response, directive and content signals have no obvious blocker. This is not proof of indexing.', 'Verify actual indexing and Google-selected canonical in Search Console.')
