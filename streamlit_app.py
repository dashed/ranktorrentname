import streamlit as st
from RTN import RTN
from RTN.fetch import check_required, check_exclude
from RTN.parser import parse
from RTN.ranker import calculate_preferred
from RTN.models import (
    BaseRankingModel, DefaultRanking, SettingsModel, CustomRank,
    ResolutionConfig, OptionsConfig, LanguagesConfig, CustomRanksConfig
)
import json
from pydantic import BaseModel
from typing import List, Dict
from importlib.metadata import version

# Get RTN version
try:
    rtn_version = version('rank-torrent-name')
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sidebar navigation and info
with st.sidebar:
    st.title("🎬 rank-torrent-name")
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
        "settings_model": SettingsModel().model_dump()
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

    settings_tabs = st.tabs([
        "⚙️ Core Settings",
        "🎯 Filters & Patterns",
        "🌍 Languages",
        "📺 Resolutions",
        "⚡ Options",
        "⚖️ Custom Ranks"
    ])

    with settings_tabs[0]:
        with st.form("core_settings_form"):
            settings_model = st.session_state.conf['settings_model']

            remove_trash = st.checkbox(
                "🗑️ Indicate trash titles",
                value=bool(st.session_state.conf['remove_trash']),
                help="Checks if the title contains any unwanted patterns.")

            choices = ["default", "best", "custom"]
            profile = settings_model.get('profile', 'default')
            rank_model_profile = st.selectbox(
                "📊 Rank Model Profile",
                options=choices, 
                index=choices.index(profile),
                help="Select a predefined ranking profile that best matches your preferences.")

            submit = st.form_submit_button('💾 Save Core Settings')
            if submit:
                st.session_state.conf['remove_trash'] = bool(remove_trash)
                settings_model['profile'] = rank_model_profile
                save_conf_to_query_params()
                st.success("✅ Core settings saved!")

    with settings_tabs[1]:
        with st.form("filters_form"):
            st.markdown("""
            ### Pattern Matching Filters
            Configure regex patterns for filtering torrents. Patterns can be:
            - Regular expressions (case-insensitive by default)
            - Case-sensitive patterns (enclosed in /pattern/)
            """)

            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### Required Patterns")
                st.markdown("Patterns that must be present")
                required_patterns = st.text_area(
                    "One pattern per line",
                    value="\n".join(settings_model.get('require', [])),
                    height=200,
                    key="required_patterns"
                )

            with col2:
                st.markdown("#### Excluded Patterns")
                st.markdown("Patterns that must not be present")
                excluded_patterns = st.text_area(
                    "One pattern per line",
                    value="\n".join(settings_model.get('exclude', [])),
                    height=200,
                    key="excluded_patterns"
                )

            with col3:
                st.markdown("#### Preferred Patterns")
                st.markdown("Patterns that give a rank boost")
                preferred_patterns = st.text_area(
                    "One pattern per line",
                    value="\n".join(settings_model.get('preferred', [])),
                    height=200,
                    key="preferred_patterns"
                )

            submit = st.form_submit_button('💾 Save Filters')
            if submit:
                settings_model['require'] = [p for p in required_patterns.split('\n') if p.strip()]
                settings_model['exclude'] = [p for p in excluded_patterns.split('\n') if p.strip()]
                settings_model['preferred'] = [p for p in preferred_patterns.split('\n') if p.strip()]
                save_conf_to_query_params()
                st.success("✅ Filters saved!")

    with settings_tabs[2]:
        with st.form("languages_form"):
            st.markdown("### Language Settings")
            languages_config = settings_model.get('languages', {})
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### Required Languages")
                required_langs = st.text_area(
                    "One language code per line",
                    value="\n".join(languages_config.get('required', [])),
                    height=200,
                    help="Language codes that must be present (e.g., en, es, fr)"
                )

            with col2:
                st.markdown("#### Excluded Languages")
                excluded_langs = st.text_area(
                    "One language code per line",
                    value="\n".join(languages_config.get('exclude', [])),
                    height=200,
                    help="Language codes to exclude"
                )

            with col3:
                st.markdown("#### Preferred Languages")
                preferred_langs = st.text_area(
                    "One language code per line",
                    value="\n".join(languages_config.get('preferred', [])),
                    height=200,
                    help="Language codes that get a rank boost"
                )

            submit = st.form_submit_button('💾 Save Language Settings')
            if submit:
                settings_model['languages'] = {
                    'required': [l for l in required_langs.split('\n') if l.strip()],
                    'exclude': [l for l in excluded_langs.split('\n') if l.strip()],
                    'preferred': [l for l in preferred_langs.split('\n') if l.strip()]
                }
                save_conf_to_query_params()
                st.success("✅ Language settings saved!")

    with settings_tabs[3]:
        with st.form("resolutions_form"):
            st.markdown("### Resolution Settings")
            resolutions_config = settings_model.get('resolutions', {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Enable/Disable Resolutions")
                r2160p = st.checkbox("4K/2160p", value=resolutions_config.get('r2160p', False))
                r1080p = st.checkbox("1080p", value=resolutions_config.get('r1080p', True))
                r720p = st.checkbox("720p", value=resolutions_config.get('r720p', True))
                
            with col2:
                r480p = st.checkbox("480p", value=resolutions_config.get('r480p', False))
                r360p = st.checkbox("360p", value=resolutions_config.get('r360p', False))
                unknown = st.checkbox("Unknown", value=resolutions_config.get('unknown', True))

            submit = st.form_submit_button('💾 Save Resolution Settings')
            if submit:
                settings_model['resolutions'] = {
                    'r2160p': r2160p,
                    'r1080p': r1080p,
                    'r720p': r720p,
                    'r480p': r480p,
                    'r360p': r360p,
                    'unknown': unknown
                }
                save_conf_to_query_params()
                st.success("✅ Resolution settings saved!")

    with settings_tabs[4]:
        with st.form("options_form"):
            st.markdown("### General Options")
            options_config = settings_model.get('options', {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                title_similarity = st.slider(
                    "Title Similarity Threshold",
                    min_value=0.0,
                    max_value=1.0,
                    value=float(options_config.get('title_similarity', 0.85)),
                    help="Minimum similarity ratio required between parsed and correct titles"
                )
                
                remove_ranks_under = st.number_input(
                    "Remove Ranks Under",
                    value=int(options_config.get('remove_ranks_under', -10000)),
                    help="Remove torrents with ranks below this value"
                )

            with col2:
                remove_all_trash = st.checkbox(
                    "Remove All Trash",
                    value=bool(options_config.get('remove_all_trash', True)),
                    help="Remove torrents marked as trash"
                )
                
                remove_unknown_languages = st.checkbox(
                    "Remove Unknown Languages",
                    value=bool(options_config.get('remove_unknown_languages', False)),
                    help="Remove torrents with unknown languages"
                )
                
                allow_english_in_languages = st.checkbox(
                    "Allow English in Languages",
                    value=bool(options_config.get('allow_english_in_languages', False)),
                    help="Always allow English language regardless of language settings"
                )
                
                enable_fetch_speed_mode = st.checkbox(
                    "Enable Fetch Speed Mode",
                    value=bool(options_config.get('enable_fetch_speed_mode', True)),
                    help="Optimize fetch operations for speed"
                )
                
                remove_adult_content = st.checkbox(
                    "Remove Adult Content",
                    value=bool(options_config.get('remove_adult_content', True)),
                    help="Remove adult content from results"
                )

            submit = st.form_submit_button('💾 Save Options')
            if submit:
                settings_model['options'] = {
                    'title_similarity': title_similarity,
                    'remove_ranks_under': remove_ranks_under,
                    'remove_all_trash': remove_all_trash,
                    'remove_unknown_languages': remove_unknown_languages,
                    'allow_english_in_languages': allow_english_in_languages,
                    'enable_fetch_speed_mode': enable_fetch_speed_mode,
                    'remove_adult_content': remove_adult_content
                }
                save_conf_to_query_params()
                st.success("✅ Options saved!")

    with settings_tabs[5]:
        st.markdown("### Custom Rank Settings")
        st.markdown("""
        Fine-tune ranking values for specific attributes. Enable custom ranks to override the profile's default values.
        Each attribute can be configured with:
        - **Fetch**: Whether to look for this attribute
        - **Rank**: The ranking score for this attribute
        - **Override**: Enable to use custom rank instead of profile default
        """)
        
        rank_categories = [
            ("Quality", "quality"),
            ("Rips", "rips"),
            ("HDR", "hdr"),
            ("Audio", "audio"),
            ("Extras", "extras"),
            ("Trash", "trash")
        ]
        
        category_tabs = st.tabs([cat[0] for cat in rank_categories])
        
        for tab, (category_name, category_key) in zip(category_tabs, rank_categories):
            with tab:
                with st.form(f"custom_ranks_{category_key}_form"):
                    custom_ranks = settings_model.get('custom_ranks', {}).get(category_key, {})
                    
                    # Convert the custom ranks to a list for the data editor
                    ranks_list = []
                    for name, rank_data in custom_ranks.items():
                        ranks_list.append({
                            "type": name,
                            "fetch": bool(rank_data.get('fetch', True)),
                            "rank": int(rank_data.get('rank', 0)),
                            "enable": bool(rank_data.get('use_custom_rank', False))
                        })
                    
                    # Sort the list by type for consistency
                    ranks_list.sort(key=lambda x: x['type'])
                    
                    edited_ranks = st.data_editor(
                        ranks_list,
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
                    
                    submit = st.form_submit_button(f'💾 Save {category_name} Ranks')
                    if submit:
                        # Convert the edited ranks back to a dictionary
                        new_ranks = {}
                        for rank in edited_ranks:
                            new_ranks[rank['type']] = {
                                'fetch': rank['fetch'],
                                'rank': rank['rank'],
                                'use_custom_rank': rank['enable']
                            }
                        
                        # Update the settings model
                        if 'custom_ranks' not in settings_model:
                            settings_model['custom_ranks'] = {}
                        settings_model['custom_ranks'][category_key] = new_ranks
                        save_conf_to_query_params()
                        st.success(f"✅ {category_name} ranks saved!")


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
