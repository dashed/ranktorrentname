import streamlit as st
from RTN import RTN
from RTN.fetch import check_required, check_exclude
from RTN.parser import parse
from RTN.ranker import calculate_preferred
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

Test settings for `riven`.

- https://github.com/dreulavelle/rank-torrent-name
- https://github.com/rivenmedia/riven

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
            "require": [],
            "exclude": [],
            "preferred": [],
            "custom_ranks": {
                "uhd": {"fetch": False, "rank": 120, "enable": False},
                "fhd": {"fetch": True, "rank": 100, "enable": False},
                "hd": {"fetch": True, "rank": 80, "enable": False},
                "sd": {"fetch": False, "rank": -120, "enable": False},
                "bluray": {"fetch": True, "rank": 80, "enable": False},
                "hdr": {"fetch": False, "rank": 80, "enable": False},
                "hdr10": {"fetch": False, "rank": 90, "enable": False},
                "dolby_video": {"fetch": False, "rank": -100, "enable": False},
                "dts_x": {"fetch": False, "rank": 0, "enable": False},
                "dts_hd": {"fetch": False, "rank": 0, "enable": False},
                "dts_hd_ma": {"fetch": False, "rank": 0, "enable": False},
                "atmos": {"fetch": False, "rank": 0, "enable": False},
                "truehd": {"fetch": False, "rank": 0, "enable": False},
                "ddplus": {"fetch": False, "rank": 0, "enable": False},
                "aac": {"fetch": True, "rank": 70, "enable": False},
                "ac3": {"fetch": True, "rank": 50, "enable": False},
                "remux": {"fetch": False, "rank": -1000, "enable": False},
                "webdl": {"fetch": True, "rank": 90, "enable": False},
                "repack": {"fetch": True, "rank": 5, "enable": False},
                "proper": {"fetch": True, "rank": 4, "enable": False},
                "dubbed": {"fetch": True, "rank": 3, "enable": False},
                "subbed": {"fetch": True, "rank": 3, "enable": False},
                "av1": {"fetch": False, "rank": 0, "enable": False},
                "h264": {"fetch": True, "rank": 0, "enable": False},
                "h265": {"fetch": True, "rank": 0, "enable": False},
                "hevc": {"fetch": True, "rank": 0, "enable": False},
                "avc": {"fetch": True, "rank": 0, "enable": False},
                "dvdrip": {"fetch": True, "rank": -100, "enable": False},
                "bdrip": {"fetch": True, "rank": 5, "enable": False},
                "brrip": {"fetch": True, "rank": 0, "enable": False},
                "hdtv": {"fetch": True, "rank": -100, "enable": False},
            }
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


def get_settings_model(settings_model):

    custom_ranks = dict()
    for type, custom_rank in settings_model['custom_ranks'].items():
        custom_ranks[type] = CustomRank(
            fetch=bool(custom_rank['fetch']), rank=custom_rank['rank'])

    return SettingsModel(
        profile=settings_model['profile'],
        require=settings_model['require'],
        exclude=settings_model['exclude'],
        preferred=settings_model['preferred'],
        custom_ranks=custom_ranks,
    )


def remove_falsey(original_list):
    return list(filter(lambda x: x, original_list))


def emoji_bool(value):
    if bool(value):
        return ":white_check_mark:"
    return ":x:"


def render_settings():
    st.header('Settings')
    with st.container(border=True):
        with st.form("render_settings_form", border=False):
            settings_model = st.session_state.conf['settings_model']

            remove_trash = st.checkbox(
                "Indicate trash titles", value=bool(st.session_state.conf['remove_trash']))

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

            filters = {"require": settings_model.get('require', []) or [''],
                       "exclude": settings_model.get('exclude', []) or [''],
                       "preferred": settings_model.get('preferred', []) or ['']}

            st.write('#### Filters')
            next_filters = st.data_editor(
                filters, num_rows="dynamic", use_container_width=True,
                column_config={
                    "require": st.column_config.TextColumn(),
                    "exclude": st.column_config.TextColumn(),
                    "preferred": st.column_config.TextColumn(),
                }
            )

            st.write('#### Custom Ranks')
            st.write("**NOTE:** When `enable` is `True` then we use the custom `rank` instead of the rank model profile's preset `rank`. Otherwise, we use the rank model profile's preset `rank`.")
            custom_ranks = settings_model['custom_ranks']

            serialized_custom_ranks = []
            for name, custom_rank in custom_ranks.items():
                serialized_custom_ranks.append({
                    "type": name,
                    "fetch": bool(custom_rank['fetch']),
                    "rank": custom_rank['rank'],
                    "enable": bool(custom_rank['enable']),
                })

            next_custom_ranks = st.data_editor(
                serialized_custom_ranks, num_rows="fixed", use_container_width=True,
                disabled=["type"],
                column_config={
                    "fetch": st.column_config.CheckboxColumn(),
                    "rank": st.column_config.NumberColumn(),
                    "enable": st.column_config.CheckboxColumn(),
                }
            )

            submit = st.form_submit_button('Update Settings')

            if submit:
                custom_ranks = {}
                for custom_rank in next_custom_ranks:
                    type = custom_rank['type']
                    custom_ranks[type] = {
                        "fetch": bool(custom_rank['fetch']),
                        "rank": int(custom_rank['rank']),
                        "enable": bool(custom_rank['enable']),
                    }

                st.session_state.conf['remove_trash'] = bool(remove_trash)
                st.session_state.conf['settings_model'] = {
                    "profile": rank_model_profile or 'default',
                    "require": remove_falsey(next_filters.get('require', [])),
                    "exclude": remove_falsey(next_filters.get('exclude', [])),
                    "preferred": remove_falsey(next_filters.get('preferred', [])),
                    "custom_ranks": custom_ranks, }
                save_conf_to_query_params()


render_settings()


def render_title(*, conf, index, initial_raw_title, initial_correct_title):
    with st.container(border=True):
        unique_key = f"{index}_{initial_raw_title}_{initial_correct_title}"
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
                conf['titles'][index] = {
                    "raw_title": raw_title_text_input,
                    "correct_title": correct_title_text_input
                }
                save_conf_to_query_params()

        try:
            ranking_model = riven_rank_models.get(
                st.session_state.conf['settings_model']['profile'])

            settings_model = get_settings_model(
                st.session_state.conf['settings_model'])
            rtn = RTN(settings=settings_model,
                      ranking_model=ranking_model)
            info_hash = "BE417768B5C3C5C1D9BCB2E7C119196DD76B5570"

            torrent = rtn.rank(raw_title=raw_title_text_input,
                               correct_title=correct_title_text_input, infohash=info_hash, remove_trash=conf['remove_trash'])

            st.write(f"**Rank:** {torrent.rank}")
            st.write(f"**Fetch:** {torrent.fetch} {emoji_bool(torrent.fetch)}")

            parsed_data = parse(
                raw_title=raw_title_text_input, remove_trash=False)

            matches_required = check_required(parsed_data, settings_model)
            st.write(
                f"**Matches `required`:** {matches_required} {emoji_bool(matches_required)}")

            matches_exclude = check_exclude(parsed_data, settings_model)
            st.write(
                f"**Matches `exclude`:** {matches_exclude} {emoji_bool(matches_exclude)}")

            matches_preferred = calculate_preferred(
                parsed_data, settings_model) > 0
            st.write(
                f"**Matches `preferred`:** {matches_preferred} {emoji_bool(matches_preferred)}")

            with st.expander("Debug"):
                parsed_data = dict(parsed_data)
                st.subheader('ParsedData')
                st.write(parsed_data)
        except Exception as err:
            st.write(str(err))
            raise err


st.header('Test Your Titles')
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

with st.expander("Export Settings"):
    st.write("Copy to your riven settings.")
    st.write(st.session_state.conf['settings_model'])
