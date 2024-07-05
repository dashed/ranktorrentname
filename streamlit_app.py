import streamlit as st
from RTN import RTN
from RTN.models import DefaultRanking
from RTN.models import SettingsModel, CustomRank
import json


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="riven ranktorrentname",
    page_icon=':popcorn:',  # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :popcorn: riven ranktorrentname

https://github.com/dreulavelle/rank-torrent-name
'''

# Add some spacing
''
''


def default_custom_ranks():
    return {
        "uhd": CustomRank(fetch=False, rank=120),
        "fhd": CustomRank(fetch=True, rank=100),
        "hd": CustomRank(fetch=True, rank=80),
        "sd": CustomRank(fetch=False, rank=-120),
        "bluray": CustomRank(fetch=True, rank=80),
        "hdr": CustomRank(fetch=False, rank=80),
        "hdr10": CustomRank(fetch=False, rank=90),
        "dolby_video": CustomRank(fetch=False, rank=-100),
        "dts_x": CustomRank(fetch=False, rank=0),
        "dts_hd": CustomRank(fetch=False, rank=0),
        "dts_hd_ma": CustomRank(fetch=False, rank=0),
        "atmos": CustomRank(fetch=False, rank=0),
        "truehd": CustomRank(fetch=False, rank=0),
        "ddplus": CustomRank(fetch=False, rank=0),
        "aac": CustomRank(fetch=True, rank=70),
        "ac3": CustomRank(fetch=True, rank=50),
        "remux": CustomRank(fetch=False, rank=-1000),
        "webdl": CustomRank(fetch=True, rank=90),
        "repack": CustomRank(fetch=True, rank=5),
        "proper": CustomRank(fetch=True, rank=4),
        "dubbed": CustomRank(fetch=True, rank=3),
        "subbed": CustomRank(fetch=True, rank=3),
        "av1": CustomRank(fetch=False, rank=0),
        "h264": CustomRank(fetch=True, rank=0),
        "h265": CustomRank(fetch=True, rank=0),
        "hevc": CustomRank(fetch=True, rank=0),
        "avc": CustomRank(fetch=True, rank=0),
        "dvdrip": CustomRank(fetch=True, rank=-100),
        "bdrip": CustomRank(fetch=True, rank=5),
        "brrip": CustomRank(fetch=True, rank=0),
        "hdtv": CustomRank(fetch=True, rank=-100),
    }


def generate_initial_conf():
    return {
        "titles": [{
            "raw_title": "Example.Movie.2020.1080p.BluRay.x264-Example",
            "correct_title": ""
        }],

        # settings model
        "settings_model": {
            "profile": "default",
            "require": ["4K", "1080p"],
            "exclude": ["/CAM/i", "TS"],
            "preferred": ["HDR", "/BluRay/"],
        }
    }


if 'conf' not in st.session_state:
    st.session_state['conf'] = generate_initial_conf()

settings = SettingsModel(
    profile="default",
    require=["4K", "1080p"],
    exclude=["/CAM/i", "TS"],
    preferred=["HDR", "/BluRay/"],
    custom_ranks=default_custom_ranks()
)

if 'raw_title' not in st.session_state or not st.session_state['raw_title']:
    st.session_state.raw_title = "Example.Movie.2020.1080p.BluRay.x264-Example"

if 'correct_title' not in st.session_state:
    st.session_state.correct_title = ""

raw_title_query = st.query_params.get("raw_title")
if raw_title_query:
    st.session_state.raw_title = raw_title_query

correct_title_query = st.query_params.get("correct_title")
if correct_title_query:
    st.session_state.correct_title = correct_title_query


def render_title(*, conf, index, initial_raw_title, initial_correct_title):
    with st.container(border=True):
        with st.form("my_form"):
            raw_title_text_input = st.text_input("Raw title (required)", value=initial_raw_title, type="default",
                                                 placeholder="Example.Movie.2020.1080p.BluRay.x264-Example")

            correct_title = st.text_input("Correct title", value=initial_correct_title, type="default",
                                          placeholder="Example Movie")
            submit = st.form_submit_button('Rank')

        # if submit:
        #     st.query_params['raw_title'] = raw_title
        #     st.query_params['correct_title'] = correct_title

        try:
            rtn = RTN(settings=settings, ranking_model=DefaultRanking())
            info_hash = "BE417768B5C3C5C1D9BCB2E7C119196DD76B5570"
            torrent = rtn.rank(raw_title=raw_title_text_input,
                               correct_title=correct_title, infohash=info_hash, remove_trash=True)
            st.markdown(f"**Rank:** {torrent.rank}")
        except Exception as err:
            st.write(str(err))


for index, section in enumerate(st.session_state.conf['titles']):
    initial_raw_title = section['raw_title']
    initial_correct_title = section['correct_title']

    render_title(conf=st.session_state.conf, index=index, initial_raw_title=initial_raw_title,
                 initial_correct_title=initial_correct_title)
