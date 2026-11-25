import streamlit as st
from triage import CASES, Case, assess

st.set_page_config(page_title='Indexability Triage Lab', page_icon='🔎', layout='wide')
st.title('Indexability Triage Lab')
st.caption('Interactive learning tool for interpreting hypothetical crawl and indexability evidence.')
st.info('All cases are fictional. This app does not crawl, inspect or submit any live URLs. It does not predict indexing or rankings.')
left, right = st.columns([1, 1], gap='large')
with left:
    st.subheader('1. Choose a starting case')
    selected = st.selectbox('Fictional scenario', [c.name for c in CASES])
    original = next(c for c in CASES if c.name == selected)
    # Separate widget state by case so changing the scenario restores its own defaults.
    key = selected
    st.subheader('2. Change the observed signals')
    statuses = [None, 200, 204, 301, 302, 401, 403, 404, 410, 429, 500, 503]
    status = st.selectbox('HTTP response', statuses, index=statuses.index(original.status), format_func=lambda s: 'Unknown' if s is None else str(s), key=f'{key}:status')
    def pick(label, options, value):
        return st.selectbox(label, options, index=options.index(value), key=f'{key}:{label}')
    crawl = pick('Crawler access', ['Allowed', 'Blocked', 'Unknown'], original.crawl)
    directive = pick('Observed indexing directive', ['Absent', 'Noindex', 'Unknown'], original.directive)
    canonical = pick('Declared canonical', ['Self', 'Other', 'Unknown'], original.canonical)
    content = pick('Observed content', ['Substantive', 'Thin or error-like', 'Unknown'], original.content)
    changed = Case(selected, status, crawl, directive, canonical, content)
with right:
    st.subheader('3. Compare findings')
    before, after = assess(original), assess(changed)
    st.caption('Starting case')
    st.write(before.state)
    st.caption('Current hypothetical case')
    st.subheader(after.state)
    st.write(after.explanation)
    st.markdown('**Next verification step**')
    st.write(after.next_step)
    st.caption('Decision order: crawl access → HTTP response → noindex → evidence completeness → content → canonical. This is a teaching simplification, not Google\'s ranking or indexing algorithm.')
st.divider()
st.subheader('Reference cases')
st.dataframe([{'Scenario': c.name, 'HTTP': str(c.status) if c.status else 'Unknown', 'Crawler access': c.crawl, 'Directive': c.directive, 'Triage': assess(c).state} for c in CASES], hide_index=True, use_container_width=True)
st.markdown('### Further reading\n- [Google Search technical requirements](https://developers.google.com/search/docs/essentials/technical)\n- [Noindex and crawler access](https://developers.google.com/search/docs/crawling-indexing/block-indexing)\n- [Canonicalization guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)\n- [HTTP response codes](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes)')
st.caption('Original AI-assisted educational example from the DigestSEO project. No Google affiliation.')
st.markdown('[DigestSEO](https://digestseo.com/) | [Engineering portfolio](https://tomiseregi.si/)')
