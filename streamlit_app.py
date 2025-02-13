import streamlit as st
from RTN import RTN
from RTN.fetch import check_required, check_exclude
from RTN.parser import parse
from RTN.ranker import calculate_preferred
from RTN.models import BaseRankingModel
from RTN.models import DefaultRanking
from RTN.models import SettingsModel, CustomRank
import json
from pydantic import BaseModel
from typing import List, Dict
import pkg_resources

# Get RTN version
try:
    rtn_version = pkg_resources.get_distribution('rank-torrent-name').version
except:
    rtn_version = "Unknown"

# Set the page configuration with a modern layout
st.set_page_config(
    page_title="Riven Torrent Name Ranker",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/dreulavelle/rank-torrent-name',
        'Report a bug': 'https://github.com/dreulavelle/rank-torrent-name/issues',
        'About': '''
        # Riven Torrent Name Ranker
        
        A tool to test and configure ranking settings for the Riven media manager.
        
        - [rank-torrent-name](https://github.com/dreulavelle/rank-torrent-name)
        - [riven](https://github.com/rivenmedia/riven)
        '''
    }
)

# Add custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main > div {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .custom-container {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sidebar navigation and info
with st.sidebar:
    st.image("https://raw.githubusercontent.com/rivenmedia/riven/main/docs/logo.png", width=200)
    st.title("Navigation")
    
    # Display version
    st.caption(f"RTN Version: {rtn_version}")
    
    page = st.radio(
        "Go to",
        ["Settings", "Test Titles", "Preset Profiles"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("""
    ### Quick Links
    - [Documentation](https://github.com/dreulavelle/rank-torrent-name#readme)
    - [Report Issues](https://github.com/dreulavelle/rank-torrent-name/issues)
    - [Riven Media](https://github.com/rivenmedia/riven)
    """)
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This tool helps you test and configure ranking settings for the Riven media manager.
    Configure your preferences and test different torrent names to see how they rank.
    """)

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
    initial_bootstrap = False
    conf = st.query_params.get("conf")
    if not conf:
        conf = generate_initial_conf()
        initial_bootstrap = True
    else:
        try:
            conf = json.loads(conf)
        except Exception:
            pass

    st.session_state['conf'] = conf
    if initial_bootstrap:
        save_conf_to_query_params()


load_conf_from_query_params()


def get_settings_model(settings_model):

    custom_ranks = dict()
    for type, custom_rank in settings_model['custom_ranks'].items():
        custom_ranks[type] = CustomRank(
            fetch=bool(custom_rank['fetch']),
            rank=int(custom_rank['rank']),
            enable=bool(custom_rank['enable']))

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


class RivenRankingSettings(BaseModel):
    profile: str
    require: List[str]
    exclude: List[str]
    preferred: List[str]
    custom_ranks: Dict[str, CustomRank]


def render_settings():
    st.header('🛠️ Settings Configuration')
    st.markdown("""
    Configure your ranking preferences and filters. These settings will be used to evaluate and rank torrent names.
    """)

    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.expander("⚙️ Core Settings", expanded=True):
            with st.form("render_settings_form", border=False):
                settings_model = st.session_state.conf['settings_model']

                remove_trash = st.checkbox(
                    "🗑️ Indicate trash titles",
                    value=bool(st.session_state.conf['remove_trash']),
                    help="Checks if the title contains any unwanted patterns.")

                choices = list(riven_rank_models.keys())
                choices.sort()
                index = 0
                profile = settings_model['profile']
                if profile in choices:
                    index = choices.index(profile)
                rank_model_profile = st.selectbox(
                    "📊 Rank Model Profile",
                    options=choices, 
                    index=index,
                    help="Select a predefined ranking profile that best matches your preferences.")

                st.markdown("### 🎯 Filters")
                st.markdown("""
                Configure pattern matching filters:
                - **Require**: Patterns that must be present
                - **Exclude**: Patterns that must not be present
                - **Preferred**: Patterns that give a rank boost if present
                """)

                filters = {"require": settings_model.get('require', []) or [''],
                           "exclude": settings_model.get('exclude', []) or [''],
                           "preferred": settings_model.get('preferred', []) or ['']}

                def transform_filters_dict(input_dict):
                    result = []
                    max_length = max(len(input_dict.get('require', [])),
                                     len(input_dict.get('exclude', [])),
                                     len(input_dict.get('preferred', [])))

                    for i in range(max_length):
                        new_dict = {
                            "require": input_dict.get('require', [])[i] if i < len(input_dict.get('require', [])) else None,
                            "exclude": input_dict.get('exclude', [])[i] if i < len(input_dict.get('exclude', [])) else None,
                            "preferred": input_dict.get('preferred', [])[i] if i < len(input_dict.get('preferred', [])) else None
                        }
                        result.append(new_dict)

                    return result

                next_filters = st.data_editor(
                    transform_filters_dict(filters), 
                    num_rows="dynamic", 
                    use_container_width=True,
                    column_config={
                        "require": st.column_config.TextColumn(
                            "Required Patterns",
                            help="Patterns that must be present",
                            width="medium"
                        ),
                        "exclude": st.column_config.TextColumn(
                            "Excluded Patterns",
                            help="Patterns that must not be present",
                            width="medium"
                        ),
                        "preferred": st.column_config.TextColumn(
                            "Preferred Patterns",
                            help="Patterns that give a rank boost",
                            width="medium"
                        ),
                    }
                )

                st.markdown("### ⚖️ Custom Ranks")
                st.markdown("""
                Fine-tune ranking values for specific attributes. Enable custom ranks to override the profile's default values.
                """)
                
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
                    serialized_custom_ranks,
                    num_rows="fixed",
                    use_container_width=True,
                    disabled=["type"],
                    column_config={
                        "type": st.column_config.TextColumn(
                            "Attribute",
                            help="The media attribute to rank"
                        ),
                        "fetch": st.column_config.CheckboxColumn(
                            "Fetch",
                            help="Whether to look for this attribute"
                        ),
                        "rank": st.column_config.NumberColumn(
                            "Rank Value",
                            help="The ranking score for this attribute"
                        ),
                        "enable": st.column_config.CheckboxColumn(
                            "Override",
                            help="Enable to use custom rank instead of profile default"
                        ),
                    }
                )

                submit = st.form_submit_button('💾 Save Settings')

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

                    def reverse_filters_transform(input_list):
                        result = {"require": [], "exclude": [], "preferred": []}

                        for item in input_list:
                            for key in ["require", "exclude", "preferred"]:
                                if item[key] is not None:
                                    result[key].append(item[key])

                        # Remove empty lists
                        result = {k: v for k, v in result.items() if v}

                        return result

                    next_filters = reverse_filters_transform(next_filters)

                    st.session_state.conf['settings_model'] = {
                        "profile": rank_model_profile or 'default',
                        "require": remove_falsey(next_filters.get('require', [])),
                        "exclude": remove_falsey(next_filters.get('exclude', [])),
                        "preferred": remove_falsey(next_filters.get('preferred', [])),
                        "custom_ranks": custom_ranks,
                    }
                    save_conf_to_query_params()
                    st.success("✅ Settings saved successfully!")

    with col2:
        with st.expander("📤 Export Settings", expanded=True):
            st.markdown("Copy these settings to your Riven configuration under the `ranking` section:")
            st.json(st.session_state.conf['settings_model'])
            
        with st.expander("📥 Import Settings"):
            st.markdown("Paste your Riven ranking settings here:")
            with st.form("settings_import", border=False):
                json_string = st.text_area("JSON Configuration")
                submit = st.form_submit_button('📥 Import')
                if submit:
                    json_import = None
                    try:
                        json_import = json.loads(json_string)
                        if 'ranking' in json_import:
                            json_import = json_import['ranking']
                        RivenRankingSettings(**json_import)
                    except Exception as e:
                        st.error(f"❌ Invalid configuration: {str(e)}")
                    else:
                        if json_import is not None:
                            st.session_state.conf['settings_model'] = json_import
                            save_conf_to_query_params()
                            st.success("✅ Settings imported successfully!")


def render_title(*, conf, index, initial_raw_title, initial_correct_title):
    with st.container(border=True):
        unique_key = f"{index}_{initial_raw_title}_{initial_correct_title}"
        
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"### 🎬 Test Case #{index + 1}")
        with col2:
            if index > 0:
                def delete_current_title():
                    del st.session_state.conf['titles'][index]
                    save_conf_to_query_params()
                st.button("🗑️ Remove", on_click=delete_current_title,
                          key=f"render_title_form_{unique_key}_delete")

        with st.form(f"render_title_form_{unique_key}", border=False):
            col1, col2 = st.columns(2)
            
            with col1:
                raw_title_text_input = st.text_input(
                    "📝 Raw title (required)", 
                    value=initial_raw_title,
                    help="Enter the original torrent name to test",
                    placeholder="Example.Movie.2020.1080p.BluRay.x264-Example"
                )

            with col2:
                correct_title_text_input = st.text_input(
                    "✨ Correct title",
                    value=initial_correct_title,
                    help="Enter the expected clean title (optional)",
                    placeholder="Example Movie"
                )

            submit = st.form_submit_button('🔍 Analyze')

            if submit:
                conf['titles'][index] = {
                    "raw_title": raw_title_text_input,
                    "correct_title": correct_title_text_input
                }
                save_conf_to_query_params()

        if raw_title_text_input:
            try:
                ranking_model = riven_rank_models.get(
                    st.session_state.conf['settings_model']['profile'])

                settings_model = get_settings_model(
                    st.session_state.conf['settings_model'])
                rtn = RTN(settings=settings_model,
                          ranking_model=ranking_model)
                info_hash = "BE417768B5C3C5C1D9BCB2E7C119196DD76B5570"

                torrent = rtn.rank(raw_title=raw_title_text_input,
                                   correct_title=correct_title_text_input, 
                                   infohash=info_hash, 
                                   remove_trash=conf['remove_trash'])

                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Rank Score", f"{torrent.rank:,}")
                
                with col2:
                    st.metric("Fetch Status", "✅ Yes" if torrent.fetch else "❌ No")
                
                parsed_data = parse(raw_title=raw_title_text_input, remove_trash=False)
                
                with col3:
                    matches_preferred = calculate_preferred(parsed_data, settings_model) > 0
                    st.metric("Preferred Boost", "✅ Yes" if matches_preferred else "❌ No")

                with st.expander("🔍 Detailed Analysis"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        matches_required = check_required(parsed_data, settings_model)
                        st.markdown(
                            f"**Required Patterns:** {emoji_bool(matches_required)}",
                            help="Check if the title meets the required patterns"
                        )

                        matches_exclude = check_exclude(parsed_data, settings_model)
                        st.markdown(
                            f"**Excluded Patterns:** {emoji_bool(not matches_exclude)}",
                            help="Check if the title contains excluded patterns"
                        )
                    
                    with col2:
                        st.markdown("**Parsed Attributes:**")
                        parsed_dict = dict(parsed_data)
                        for key, value in parsed_dict.items():
                            if value:
                                st.markdown(f"- `{key}`: {value}")

            except Exception as err:
                st.error(f"❌ Error: {str(err)}")


def render_preset_profiles():
    st.header("📚 Preset Ranking Profiles")
    st.markdown("""
    These are the built-in ranking profiles that you can use as a starting point.
    Each profile has different ranking weights optimized for specific use cases.
    """)
    
    for name, rank_model in riven_rank_models.items():
        with st.expander(f"📋 {name.title()} Profile"):
            st.json(dict(rank_model))


# Main content based on navigation
if page == "Settings":
    render_settings()
elif page == "Test Titles":
    st.header("🧪 Test Your Titles")
    st.markdown("""
    Test how your titles rank with the current settings. Add multiple test cases to compare results.
    """)
    
    for index, section in enumerate(st.session_state.conf['titles']):
        initial_raw_title = section['raw_title']
        initial_correct_title = section['correct_title']

        render_title(
            conf=st.session_state.conf,
            index=index,
            initial_raw_title=initial_raw_title,
            initial_correct_title=initial_correct_title
        )

    if st.button("➕ Add Test Case"):
        st.session_state.conf['titles'].append({
            "raw_title": "",
            "correct_title": ""
        })
        save_conf_to_query_params()
        
else:  # Preset Profiles
    render_preset_profiles()
