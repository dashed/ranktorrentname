import streamlit as st
from RTN import RTN
from RTN.models import BaseRankingModel
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

# From https://github.com/rivenmedia/riven/blob/0dbc9f70161dc6cd5f219e81a4424b15aa6fbf14/backend/program/settings/versions.py


class DefaultRanking(BaseRankingModel):
    uhd: int = -1000
    fhd: int = 100
    hd: int = 50
    sd: int = -100
    dolby_video: int = -100
    aac: int = 70
    ac3: int = 50
    remux: int = -1000
    webdl: int = 90
    bluray: int = 80
    dvdrip: int = -100
    hdtv: int = -100


class BestRemuxRanking(BaseRankingModel):
    uhd: int = 100
    fhd: int = 60
    hd: int = 40
    sd: int = 20
    dolby_video: int = 100
    hdr: int = 80
    hdr10: int = 90
    dts_x: int = 100
    dts_hd: int = 80
    dts_hd_ma: int = 90
    atmos: int = 90
    truehd: int = 60
    aac: int = 30
    ac3: int = 20
    remux: int = 150
    webdl: int = -1000


class BestWebRanking(BaseRankingModel):
    uhd: int = 100
    fhd: int = 90
    hd: int = 80
    sd: int = 20
    dolby_video: int = 100
    hdr: int = 80
    hdr10: int = 90
    aac: int = 50
    ac3: int = 40
    remux: int = -1000
    webdl: int = 100


class BestResolutionRanking(BaseRankingModel):
    uhd: int = 100
    fhd: int = 90
    hd: int = 80
    sd: int = 70
    dolby_video: int = 100
    hdr: int = 80
    hdr10: int = 90
    dts_x: int = 100
    dts_hd: int = 80
    dts_hd_ma: int = 90
    atmos: int = 90
    truehd: int = 60
    ddplus: int = 90
    aac: int = 30
    ac3: int = 20
    remux: int = 150
    bluray: int = 120
    webdl: int = -1000


class BestOverallRanking(BaseRankingModel):
    uhd: int = 100
    fhd: int = 90
    hd: int = 80
    sd: int = 70
    dolby_video: int = 100
    hdr: int = 80
    hdr10: int = 90
    dts_x: int = 100
    dts_hd: int = 80
    dts_hd_ma: int = 90
    atmos: int = 90
    truehd: int = 60
    ddplus: int = 40
    aac: int = 30
    ac3: int = 20
    remux: int = 150
    bluray: int = 120
    webdl: int = 90


class AnimeRanking(BaseRankingModel):
    uhd: int = -1000
    fhd: int = 90
    hd: int = 80
    sd: int = 20
    aac: int = 70
    ac3: int = 50
    remux: int = -1000
    webdl: int = 90
    bluray: int = 50
    dubbed: int = 100
    subbed: int = 100


class AllRanking(BaseRankingModel):
    uhd: int = 2
    fhd: int = 3
    hd: int = 1
    sd: int = 1
    dolby_video: int = 1
    hdr: int = 1
    dts_x: int = 1
    dts_hd: int = 1
    dts_hd_ma: int = 1
    atmos: int = 1
    truehd: int = 1
    ddplus: int = 1
    aac: int = 2
    ac3: int = 1
    remux: int = 1
    webdl: int = 1
    bluray: int = 1


riven_rank_models = {
    "default":  DefaultRanking(),
    "custom": BaseRankingModel(),
    "remux":   BestRemuxRanking(),
    "web":   BestWebRanking(),
    "resolution":   BestResolutionRanking(),
    "overall":   BestOverallRanking(),
    "anime":   AnimeRanking(),
    "all":   AllRanking(),
}


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

        "remove_trash": True,

        # settings model
        "settings_model": {
            "profile": "default",
            "require": ["4K", "1080p"],
            "exclude": ["/CAM/i", "TS"],
            "preferred": ["HDR", "/BluRay/"],
        }
    }


def save_conf_to_query_params():
    if 'conf' not in st.session_state:
        return
    st.query_params['conf'] = json.dumps(st.session_state.conf)
    # st.rerun()


def load_conf_from_query_params():
    conf = st.query_params.get("conf")
    if not conf:
        conf = generate_initial_conf()
    else:
        try:
            conf = json.loads(conf)
        except Exception:
            pass

    st.session_state['conf'] = conf


load_conf_from_query_params()


def get_settings_model():
    settings_model = st.session_state.conf['settings_model']
    return SettingsModel(
        profile=settings_model['profile'],
        require=settings_model['require'],
        exclude=settings_model['exclude'],
        preferred=settings_model['preferred'],
        custom_ranks=default_custom_ranks()
    )


def remove_none(original_list):
    return list(filter(lambda x: x, original_list))


def render_settings():
    with st.container(border=True):
        st.subheader('Settings')
        with st.form("render_settings_form", border=False):
            remove_trash = st.checkbox("Indicate trash titles")

            settings_model = st.session_state.conf['settings_model']

            choices = list(riven_rank_models.keys())
            choices.sort()
            index = 0
            profile = settings_model['profile']
            if profile in choices:
                index = choices.index(profile)
            rank_model_profile = st.selectbox(
                "Rank Model Profile",
                options=choices, index=index)

            # "require": ["4K", "1080p"],
            # "exclude": ["/CAM/i", "TS"],
            # "preferred": ["HDR", "/BluRay/"],

            data = {"require": settings_model['require'],
                    "exclude": settings_model['exclude'],
                    "preferred": settings_model['preferred']}

            st.write('Filters')
            next_data = st.data_editor(
                data, num_rows="dynamic", use_container_width=True)

            submit = st.form_submit_button('Update Settings')

        if submit:
            st.write('submitted')
            st.session_state.conf['remove_trash'] = bool(remove_trash)
            st.session_state.conf['settings_model'] = {
                "profile": rank_model_profile or 'default',
                "require": remove_none(next_data['require']),
                "exclude": remove_none(next_data['exclude']),
                "preferred": remove_none(next_data['preferred'])}

            st.code(json.dumps(st.session_state.conf['settings_model']))
            save_conf_to_query_params()


render_settings()


def render_title(*, conf, index, initial_raw_title, initial_correct_title):
    with st.container(border=True):
        unique_key = f"{index}_{initial_raw_title}_{initial_correct_title}"
        st.write(unique_key)
        if index > 0:
            def delete_current_title():
                del st.session_state.conf['titles'][index]
                save_conf_to_query_params()
            st.button("Remove", on_click=delete_current_title,
                      key=f"render_title_form_{unique_key}_delete")

        with st.form(f"render_title_form_{unique_key}", border=False):
            raw_title_text_input = st.text_input("Raw title (required)", value=initial_raw_title, type="default",
                                                 placeholder="Example.Movie.2020.1080p.BluRay.x264-Example")

            correct_title_text_input = st.text_input("Correct title", value=initial_correct_title, type="default",
                                                     placeholder="Example Movie")

            submit = st.form_submit_button('Rank')

        if submit:
            st.write('submitted')
            conf['titles'][index] = {
                "raw_title": raw_title_text_input,
                "correct_title": correct_title_text_input
            }
            save_conf_to_query_params()

        try:
            ranking_model = riven_rank_models.get(
                st.session_state.conf['settings_model']['profile'])

            rtn = RTN(settings=get_settings_model(),
                      ranking_model=ranking_model)
            info_hash = "BE417768B5C3C5C1D9BCB2E7C119196DD76B5570"

            torrent = rtn.rank(raw_title=raw_title_text_input,
                               correct_title=correct_title_text_input, infohash=info_hash, remove_trash=conf['remove_trash'])

            st.markdown(f"**Rank:** {torrent.rank}")
        except Exception as err:
            st.write(str(err))


for index, section in enumerate(st.session_state.conf['titles']):
    initial_raw_title = section['raw_title']
    initial_correct_title = section['correct_title']

    render_title(conf=st.session_state.conf, index=index, initial_raw_title=initial_raw_title,
                 initial_correct_title=initial_correct_title)


def add_new_title():
    st.session_state.conf['titles'].append({
        "raw_title": "",
        "correct_title": ""
    })
    save_conf_to_query_params()


st.button("Add", on_click=add_new_title)
