import streamlit as st
from RTN import RTN
from RTN.fetch import check_required, check_exclude
from RTN.parser import parse
from RTN.ranker import calculate_preferred
from RTN.models import (
    BaseRankingModel, DefaultRanking, SettingsModel, CustomRank,
    ResolutionConfig, OptionsConfig, LanguagesConfig, CustomRanksConfig,
    QualityRankModel, RipsRankModel, HdrRankModel, AudioRankModel, ExtrasRankModel, TrashRankModel
)
import json
from pydantic import BaseModel
from typing import List, Dict
from importlib.metadata import version
import lzstring
import regex

# Get RTN version
try:
    rtn_version = version('rank-torrent-name')
except:
    rtn_version = "Unknown"

# Set the page configuration with a modern layout
st.set_page_config(
    page_title="Rank Torrent Name (RTN)",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/dreulavelle/rank-torrent-name',
        'Report a bug': 'https://github.com/dreulavelle/rank-torrent-name/issues',
        'About': '''
        # Rank Torrent Name (RTN)
        
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
    .st-emotion-cache-1y4p8pa {
        max-width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize LZString compressor
lz = lzstring.LZString()

def compress_string(string: str) -> str:
    """Compress a string using LZString and make it URL safe."""
    try:
        # Use compressToEncodedURIComponent instead of compressToBase64
        compressed = lz.compressToEncodedURIComponent(string)
        if compressed:
            return compressed
        return string
    except Exception:
        return string

def decompress_string(string: str, default_value: str = '') -> str:
    """Decompress a URL-safe LZString compressed string."""
    try:
        decompressed = lz.decompressFromEncodedURIComponent(string)
        return decompressed if decompressed else default_value
    except Exception:
        return default_value

# -----------------------------------------------------------------------------
# Sidebar navigation and info
with st.sidebar:
    st.title("🎬 rank-torrent-name")
    st.title("Navigation")
    
    # Display version
    st.caption(f"RTN Version: {rtn_version}")
    
    page = st.radio(
        "Go to",
        ["Settings", "Test Titles", "Preset Profiles", "Import/Export"],
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

# Default ranking models from RTN
class DefaultRanking(BaseRankingModel):
    """Default ranking model preset that covers the most common use cases."""
    # quality
    av1: int = 0
    avc: int = 500
    bluray: int = 100
    dvd: int = -1000
    hdtv: int = -1000
    hevc: int = 500
    mpeg: int = -100
    remux: int = -10000
    vhs: int = -10000
    web: int = 150
    webdl: int = 5000
    webmux: int = -10000
    xvid: int = -10000
    pdtv: int = -10000

    # rips
    bdrip: int = -1000
    brrip: int = -1000
    dvdrip: int = -1000
    hdrip: int = -1000
    ppvrip: int = -1000
    tvrip: int = -10000
    uhdrip: int = -1000
    vhsrip: int = -10000
    webdlrip: int = -10000
    webrip: int = 30

    # hdr
    bit_10: int = 5
    dolby_vision: int = 50
    hdr: int = 50
    hdr10plus: int = 0
    sdr: int = 0

    # audio
    aac: int = 250
    ac3: int = 30
    atmos: int = 400
    dolby_digital: int = 0
    dolby_digital_plus: int = 0
    dts_lossy: int = 600
    dts_lossless: int = 0
    eac3: int = 250
    flac: int = 0
    mono: int = -10000
    mp3: int = -10000
    stereo: int = 0
    surround: int = 0
    truehd: int = -100

    # extras
    three_d: int = -10000
    converted: int = -1250
    documentary: int = -250
    dubbed: int = 0
    edition: int = 100
    hardcoded: int = 0
    network: int = 300
    proper: int = 1000
    repack: int = 1000
    retail: int = 0
    site: int = -10000
    subbed: int = 0
    upscaled: int = -10000
    scene: int = 2000

    # trash
    cam: int = -10000
    clean_audio: int = -10000
    r5: int = -10000
    satrip: int = -10000
    screener: int = -10000
    size: int = -10000
    telecine: int = -10000
    telesync: int = -10000
    adult: int = -10000


class BestRanking(BaseRankingModel):
    """Ranking model preset that prioritizes the highest quality and most desirable attributes."""
    # quality
    av1: int = 500
    avc: int = 500
    bluray: int = 100
    dvd: int = -5000
    hdtv: int = -5000
    hevc: int = 500
    mpeg: int = -1000
    remux: int = 10000
    vhs: int = -10000
    web: int = 100
    webdl: int = 200
    webmux: int = -10000
    xvid: int = -10000
    pdtv: int = -10000

    # rips
    bdrip: int = -5000
    brrip: int = -10000
    dvdrip: int = -5000
    hdrip: int = -10000
    ppvrip: int = -10000
    tvrip: int = -10000
    uhdrip: int = -5000
    vhsrip: int = -10000
    webdlrip: int = -10000
    webrip: int = -1000

    # hdr
    bit_10: int = 100
    dolby_vision: int = 3000
    hdr: int = 2000
    hdr10plus: int = 2100
    sdr: int = 0

    # audio
    aac: int = 100
    ac3: int = 50
    atmos: int = 1000
    dolby_digital: int = 0
    dolby_digital_plus: int = 0
    dts_lossy: int = 100
    dts_lossless: int = 2000
    eac3: int = 150
    flac: int = 0
    mono: int = -1000
    mp3: int = -1000
    stereo: int = 0
    surround: int = 0
    truehd: int = 2000

    # extras
    three_d: int = -10000
    converted: int = -1000
    documentary: int = -250
    dubbed: int = -1000
    edition: int = 100
    hardcoded: int = 0
    network: int = 0
    proper: int = 20
    repack: int = 20
    retail: int = 0
    site: int = -10000
    subbed: int = 0
    upscaled: int = -10000
    scene: int = 0

    # trash
    cam: int = -10000
    clean_audio: int = -10000
    r5: int = -10000
    satrip: int = -10000
    screener: int = -10000
    size: int = -10000
    telecine: int = -10000
    telesync: int = -10000
    adult: int = -10000


# Available ranking models
rtn_rank_models = {
    "default": DefaultRanking(),
    "best": BestRanking(),
    "custom": BaseRankingModel(),
}


def generate_initial_conf():
    # Initialize with default settings
    default_settings = SettingsModel(
        profile="default",
        require=[],
        exclude=[],
        preferred=[],
        resolutions=ResolutionConfig(
            # Enable common resolutions by default
            r2160p=True,  # 4K
            r1080p=True,  # 1080p
            r720p=True,   # 720p
            r480p=False,  # 480p
            r360p=False,  # 360p
            unknown=True  # Allow unknown resolutions
        ),
        options=OptionsConfig(),
        languages=LanguagesConfig(),
        custom_ranks=CustomRanksConfig()
    ).model_dump()

    return {
        "titles": [{
            "raw_title": "Example.Movie.2020.1080p.BluRay.x264-Example",
            "correct_title": ""
        }],
        "remove_trash": True,
        "settings_model": default_settings
    }


def save_conf_to_query_params():
    """Save the current configuration to URL query parameters with compression."""
    if 'conf' not in st.session_state:
        return
    
    try:
        # Convert configuration to JSON string with compact encoding
        conf_json = json.dumps(st.session_state.conf, separators=(',', ':'))
        
        # Compress the JSON string and save to query params
        st.query_params['conf'] = compress_string(conf_json)
        
    except Exception as e:
        st.error(f"Failed to save configuration to URL: {str(e)}")


def validate_conf(conf):
    """Validate the configuration structure and return a valid conf."""
    default_conf = generate_initial_conf()
    
    if not isinstance(conf, dict):
        return default_conf
        
    # Ensure required top-level keys exist
    required_keys = {'titles', 'remove_trash', 'settings_model'}
    if not all(key in conf for key in required_keys):
        return default_conf
        
    # Validate titles array
    if not isinstance(conf.get('titles'), list):
        conf['titles'] = default_conf['titles']
    
    # Ensure each title has required structure
    for i, title in enumerate(conf['titles']):
        if not isinstance(title, dict) or 'raw_title' not in title or 'correct_title' not in title:
            conf['titles'][i] = {"raw_title": "", "correct_title": ""}
            
    # Ensure remove_trash is boolean
    conf['remove_trash'] = bool(conf.get('remove_trash', True))
    
    # Validate settings_model structure
    if not isinstance(conf.get('settings_model'), dict):
        conf['settings_model'] = default_conf['settings_model']
        
    return conf


def load_conf_from_query_params():
    """Load configuration from URL query parameters with decompression and validation."""
    try:
        # Get configuration from query parameters
        compressed_conf = st.query_params.get("conf")
        
        if not compressed_conf:
            # No configuration in URL, use default
            conf = generate_initial_conf()
            initial_bootstrap = True
        else:
            try:
                # Decompress and parse JSON configuration
                conf_json = decompress_string(compressed_conf)
                if not conf_json:
                    raise ValueError("Failed to decompress configuration")
                    
                conf = json.loads(conf_json)
                initial_bootstrap = False
            except (json.JSONDecodeError, ValueError) as e:
                # Invalid JSON or decompression failed, use default
                st.error(f"Invalid configuration in URL: {str(e)}. Using default settings.")
                conf = generate_initial_conf()
                initial_bootstrap = True
                
        # Validate configuration structure
        conf = validate_conf(conf)
        
        # Update session state
        st.session_state['conf'] = conf
        
        # Save validated configuration back to URL if this is initial bootstrap
        if initial_bootstrap:
            save_conf_to_query_params()
            
    except Exception as e:
        st.error(f"Error loading configuration: {str(e)}")
        # Fallback to default configuration
        st.session_state['conf'] = generate_initial_conf()


load_conf_from_query_params()


def get_settings_model(settings_model):
    # Convert the custom ranks configuration
    custom_ranks_config = CustomRanksConfig(
        quality=QualityRankModel(**settings_model.get('custom_ranks', {}).get('quality', {})),
        rips=RipsRankModel(**settings_model.get('custom_ranks', {}).get('rips', {})),
        hdr=HdrRankModel(**settings_model.get('custom_ranks', {}).get('hdr', {})),
        audio=AudioRankModel(**settings_model.get('custom_ranks', {}).get('audio', {})),
        extras=ExtrasRankModel(**settings_model.get('custom_ranks', {}).get('extras', {})),
        trash=TrashRankModel(**settings_model.get('custom_ranks', {}).get('trash', {}))
    )

    # Get resolution configuration
    resolution_config = ResolutionConfig(**settings_model.get('resolutions', {}))

    # Get options configuration
    options_config = OptionsConfig(**settings_model.get('options', {}))

    # Get languages configuration
    languages_config = LanguagesConfig(**settings_model.get('languages', {}))

    return SettingsModel(
        profile=settings_model['profile'],
        require=settings_model['require'],
        exclude=settings_model['exclude'],
        preferred=settings_model['preferred'],
        resolutions=resolution_config,
        options=options_config,
        languages=languages_config,
        custom_ranks=custom_ranks_config
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
    For more information, check out the [RTN documentation](https://github.com/dreulavelle/rank-torrent-name#readme).
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
                "🗑️ Remove trash titles",
                value=bool(st.session_state.conf['remove_trash']),
                help="Automatically remove titles containing trash patterns like CAM, TS, etc.")

            choices = ["default", "best", "custom"]
            profile = settings_model.get('profile', 'default')
            rank_model_profile = st.selectbox(
                "📊 Rank Model Profile",
                options=choices, 
                index=choices.index(profile),
                help="""Select a predefined ranking profile:

- **default**: Optimized for streaming without transcoding
  - Excludes remuxes
  - Limits resolutions to 1080p and 720p
  - Ideal for users who want high-quality content that doesn't require transcoding on most devices

- **best**: Aimed at obtaining the highest quality content available
  - Includes all resolutions, including 4K/2160p
  - Prioritizes remuxes and high-bitrate encodes
  - Perfect for users with powerful hardware who prioritize quality over compatibility

- **custom**: Start with a blank profile and customize everything
  - All ranks start at 0
  - Perfect for creating your own custom ranking system
  
Note: Profiles are meant to be a starting point. You should fine-tune the settings to your specific needs.""")

            submit = st.form_submit_button('💾 Save Core Settings')
            if submit:
                st.session_state.conf['remove_trash'] = bool(remove_trash)
                settings_model['profile'] = rank_model_profile
                save_conf_to_query_params()
                st.success("✅ Core settings saved!")

    with settings_tabs[1]:
        with st.form("filters_form"):
            st.markdown(r"""
            ### Pattern Matching Filters
            Configure regex patterns for filtering torrents. You can use:
            - Regular expressions (case-insensitive by default)
            - Case-sensitive patterns (enclosed in /pattern/)
            - Add patterns one at a time with the form below
            
            Examples:
            - `BluRay|WEB-DL` - Match BluRay or WEB-DL (case-insensitive)
            - `/SPARKS|DIMENSION/` - Match specific release groups (case-sensitive)
            - `1080p|2160p` - Match common resolutions
            - `/^(?!.*\bCAM\b).*/` - Exclude titles containing "CAM"
            """)

            # Pattern testing section
            st.markdown("### 🧪 Test Your Pattern")
            col1, col2 = st.columns([3, 1])
            with col1:
                test_pattern = st.text_input(
                    "Enter a pattern to test",
                    help="Enter a regex pattern. Enclose in /pattern/ for case-sensitive matching."
                )
            with col2:
                # Remove manual case-sensitive checkbox since it's determined by pattern format
                st.markdown("ℹ️ Use /pattern/ for case-sensitive")
            
            test_string = st.text_input(
                "Test string",
                help="Enter a string to test your pattern against"
            )
            
            if test_pattern and test_string:
                try:
                    # Check if pattern is enclosed in slashes for case-sensitivity
                    is_case_sensitive = test_pattern.startswith('/') and test_pattern.endswith('/') and len(test_pattern) > 2
                    if is_case_sensitive:
                        # Remove the enclosing slashes and compile without IGNORECASE flag
                        pattern = regex.compile(test_pattern[1:-1])
                    else:
                        # Non-case-sensitive pattern
                        pattern = regex.compile(test_pattern, regex.IGNORECASE)
                    
                    match = pattern.search(test_string)
                    if match:
                        st.success(f"✅ Pattern matches! Found: {match.group(0)}")
                        if is_case_sensitive:
                            st.info("Note: This is a case-sensitive match")
                    else:
                        st.error("❌ Pattern does not match")
                except Exception as e:
                    st.error(f"❌ Invalid regex pattern: {str(e)}")
            
            st.markdown("---")
            
            # Required Patterns
            st.markdown("#### Required Patterns")
            st.markdown("Patterns that must be present in the torrent name")
            current_required = settings_model.get('require', [])
            
            # Single text area for all required patterns
            current_required_text = st.text_area(
                "Current patterns (one per line)",
                value="\n".join(current_required),
                key="current_required",
                height=100,
                help="Edit or remove existing patterns. One pattern per line."
            )
            
            # Required patterns testing
            with st.expander("🧪 Test Required Patterns"):
                test_string_required = st.text_input(
                    "Enter a string to test against required patterns",
                    key="test_string_required",
                    help="Enter a string to test against all your required patterns"
                )
                
                if test_string_required:
                    st.markdown("#### Test Results:")
                    any_patterns = False
                    for pattern in [p.strip() for p in current_required_text.split('\n') if p.strip()]:
                        any_patterns = True
                        try:
                            # Check if pattern is enclosed in slashes for case-sensitivity
                            is_case_sensitive = pattern.startswith('/') and pattern.endswith('/') and len(pattern) > 2
                            if is_case_sensitive:
                                # Remove the enclosing slashes and compile without IGNORECASE flag
                                regex_pattern = regex.compile(pattern[1:-1])
                            else:
                                # Non-case-sensitive pattern
                                regex_pattern = regex.compile(pattern, regex.IGNORECASE)
                            
                            match = regex_pattern.search(test_string_required)
                            if match:
                                st.success(f"✅ Pattern `{pattern}` matches! Found: `{match.group(0)}`")
                                if is_case_sensitive:
                                    st.info("Note: This was a case-sensitive match")
                            else:
                                st.error(f"❌ Pattern `{pattern}` does not match")
                        except Exception as e:
                            st.error(f"❌ Invalid regex pattern `{pattern}`: {str(e)}")
                    
                    if not any_patterns:
                        st.info("No patterns to test. Add some patterns above.")
            
            st.markdown("---")
            
            # Excluded Patterns
            st.markdown("#### Excluded Patterns")
            st.markdown("Patterns that will cause a torrent to be excluded if matched")
            current_excluded = settings_model.get('exclude', [])
            
            # Single text area for all excluded patterns
            current_excluded_text = st.text_area(
                "Current patterns (one per line)",
                value="\n".join(current_excluded),
                key="current_excluded",
                height=100,
                help="Edit or remove existing patterns. One pattern per line."
            )
            
            # Excluded patterns testing
            with st.expander("🧪 Test Excluded Patterns"):
                test_string_excluded = st.text_input(
                    "Enter a string to test against excluded patterns",
                    key="test_string_excluded",
                    help="Enter a string to test against all your excluded patterns"
                )
                
                if test_string_excluded:
                    st.markdown("#### Test Results:")
                    any_patterns = False
                    for pattern in [p.strip() for p in current_excluded_text.split('\n') if p.strip()]:
                        any_patterns = True
                        try:
                            # Check if pattern is enclosed in slashes for case-sensitivity
                            is_case_sensitive = pattern.startswith('/') and pattern.endswith('/') and len(pattern) > 2
                            if is_case_sensitive:
                                # Remove the enclosing slashes and compile without IGNORECASE flag
                                regex_pattern = regex.compile(pattern[1:-1])
                            else:
                                # Non-case-sensitive pattern
                                regex_pattern = regex.compile(pattern, regex.IGNORECASE)
                            
                            match = regex_pattern.search(test_string_excluded)
                            if match:
                                st.error(f"❌ Pattern `{pattern}` matches (would exclude)! Found: `{match.group(0)}`")
                                if is_case_sensitive:
                                    st.info("Note: This was a case-sensitive match")
                            else:
                                st.success(f"✅ Pattern `{pattern}` does not match (would not exclude)")
                        except Exception as e:
                            st.error(f"❌ Invalid regex pattern `{pattern}`: {str(e)}")
                    
                    if not any_patterns:
                        st.info("No patterns to test. Add some patterns above.")
            
            st.markdown("---")
            
            # Preferred Patterns
            st.markdown("#### Preferred Patterns")
            st.markdown("Patterns that will give a rank boost to matching torrents")
            current_preferred = settings_model.get('preferred', [])
            
            # Single text area for all preferred patterns
            current_preferred_text = st.text_area(
                "Current patterns (one per line)",
                value="\n".join(current_preferred),
                key="current_preferred",
                height=100,
                help="Edit or remove existing patterns. One pattern per line."
            )
            
            # Preferred patterns testing
            with st.expander("🧪 Test Preferred Patterns"):
                test_string_preferred = st.text_input(
                    "Enter a string to test against preferred patterns",
                    key="test_string_preferred",
                    help="Enter a string to test against all your preferred patterns"
                )
                
                if test_string_preferred:
                    st.markdown("#### Test Results:")
                    any_patterns = False
                    for pattern in [p.strip() for p in current_preferred_text.split('\n') if p.strip()]:
                        any_patterns = True
                        try:
                            # Check if pattern is enclosed in slashes for case-sensitivity
                            is_case_sensitive = pattern.startswith('/') and pattern.endswith('/') and len(pattern) > 2
                            if is_case_sensitive:
                                # Remove the enclosing slashes and compile without IGNORECASE flag
                                regex_pattern = regex.compile(pattern[1:-1])
                            else:
                                # Non-case-sensitive pattern
                                regex_pattern = regex.compile(pattern, regex.IGNORECASE)
                            
                            match = regex_pattern.search(test_string_preferred)
                            if match:
                                st.success(f"✅ Pattern `{pattern}` matches (would boost)! Found: `{match.group(0)}`")
                                if is_case_sensitive:
                                    st.info("Note: This was a case-sensitive match")
                            else:
                                st.warning(f"⚠️ Pattern `{pattern}` does not match (no boost)")
                        except Exception as e:
                            st.error(f"❌ Invalid regex pattern `{pattern}`: {str(e)}")
                    
                    if not any_patterns:
                        st.info("No patterns to test. Add some patterns above.")

            # Common patterns suggestions
            with st.expander("📚 Common Pattern Examples"):
                st.markdown("""
                ### Required Patterns
                - `1080p|2160p` - Match common HD resolutions
                - `BluRay|WEB-DL` - Match common source types
                - `/SPARKS|DIMENSION/` - Match specific release groups (case-sensitive)
                
                ### Excluded Patterns
                - `CAM|TS|HDTS` - Exclude low quality releases
                - `/\\[TGx\\]/` - Exclude specific release group (case-sensitive)
                - `LQ|LOW.?QUALITY` - Exclude low quality indicators
                
                ### Preferred Patterns
                - `BluRay|REMUX` - Prefer high quality sources
                - `HDR|DV` - Prefer HDR content
                - `/\\bS\\d+/` - Prefer season numbering format
                """)

            submit = st.form_submit_button('💾 Save Changes')
            if submit:
                # Update patterns from text areas
                settings_model['require'] = [p.strip() for p in current_required_text.split('\n') if p.strip()]
                settings_model['exclude'] = [p.strip() for p in current_excluded_text.split('\n') if p.strip()]
                settings_model['preferred'] = [p.strip() for p in current_preferred_text.split('\n') if p.strip()]
                
                save_conf_to_query_params()
                st.success("✅ Changes saved!")
                st.rerun()

    with settings_tabs[2]:
        with st.form("languages_form"):
            st.markdown("""
            ### Language Settings
            Configure language preferences using ISO 639-1 two-letter language codes. RTN supports a wide range of languages and allows you to:
            - Require specific languages
            - Exclude unwanted languages
            - Give preference to certain languages
            
            Common language codes:
            | Code | Language   | Code | Language   | Code | Language   |
            |------|------------|------|------------|------|------------|
            | `en`   | English    | `es`   | Spanish    | `fr`   | French     |
            | `de`   | German     | `it`   | Italian    | `ja`   | Japanese   |
            | `ko`   | Korean     | `zh`   | Chinese    | `ru`   | Russian    |
            | `pt`   | Portuguese | `hi`   | Hindi      | `ar`   | Arabic     |
            
            [View full language list](https://github.com/dreulavelle/rank-torrent-name/blob/main/docs/users/languages.md)
            """)
            
            languages_config = settings_model.get('languages', {})
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### Required Languages")
                st.markdown("Languages that must be present")
                required_langs = st.text_area(
                    "One language code per line",
                    value="\n".join(languages_config.get('required', [])),
                    height=200,
                    help="""Example:
- en
- ja
- ko"""
                )

            with col2:
                st.markdown("#### Excluded Languages")
                st.markdown("Languages that must not be present")
                default_excludes = ["ar", "hi", "fr", "es", "de", "ru", "pt", "it"]
                excluded_langs = st.text_area(
                    "One language code per line",
                    value="\n".join(languages_config.get('exclude', default_excludes)),
                    height=200,
                    help=f"""Default exclusions: {', '.join(default_excludes)}

Example:
- ar
- hi
- fr"""
                )

            with col3:
                st.markdown("#### Preferred Languages")
                st.markdown("Languages that get a rank boost")
                preferred_langs = st.text_area(
                    "One language code per line",
                    value="\n".join(languages_config.get('preferred', [])),
                    height=200,
                    help="""Example:
- en
- ja"""
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
            st.markdown("""
            ### Resolution Settings
            Enable or disable specific resolutions that RTN should consider when ranking torrents.
            
            Default configuration:
            - 4K/2160p: Disabled by default (for compatibility)
            - 1080p: Enabled by default (recommended)
            - 720p: Enabled by default (acceptable quality)
            - 480p: Disabled by default (low quality)
            - 360p: Disabled by default (very low quality)
            - Unknown: Enabled by default (for unspecified resolutions)
            
            Note: These settings only affect which resolutions are considered during ranking.
            The actual ranking values are determined by the profile and custom ranks.
            """)
            
            resolutions_config = settings_model.get('resolutions', {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### High Definition")
                r2160p = st.checkbox("4K/2160p", value=resolutions_config.get('r2160p', False),
                                   help="Ultra HD / 4K resolution (3840×2160)")
                r1080p = st.checkbox("1080p", value=resolutions_config.get('r1080p', True),
                                   help="Full HD resolution (1920×1080)")
                r720p = st.checkbox("720p", value=resolutions_config.get('r720p', True),
                                   help="HD resolution (1280×720)")
                
            with col2:
                st.markdown("#### Standard Definition & Other")
                r480p = st.checkbox("480p", value=resolutions_config.get('r480p', False),
                                   help="SD resolution (854×480)")
                r360p = st.checkbox("360p", value=resolutions_config.get('r360p', False),
                                   help="Low resolution (640×360)")
                unknown = st.checkbox("Unknown", value=resolutions_config.get('unknown', True),
                                   help="Allow torrents with unspecified resolution")

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
        st.markdown("""
        ### Custom Rank Settings
        Fine-tune ranking values for specific attributes. Each attribute can be configured with:
        
        - **Fetch**: Whether to look for this attribute (affects filtering)
        - **Rank**: The ranking score for this attribute (-10000 to 10000)
        - **Override**: Enable to use custom rank instead of profile default
        
        Notes:
        - Disabled attributes (Fetch = False) will cause torrents with that attribute to be filtered out
        - The Override option lets you use your custom rank value instead of the profile's value
        - Rank values: Positive = preferred, Negative = undesired, 0 = neutral
        """)
        
        rank_categories = [
            ("Quality", "quality", {
                "av1": False, "avc": True, "bluray": True, "dvd": False,
                "hdtv": True, "hevc": True, "mpeg": False, "remux": False,
                "vhs": False, "web": True, "webdl": True, "webmux": False,
                "xvid": False
            }),
            ("Rips", "rips", {
                "bdrip": False, "brrip": False, "dvdrip": False,
                "hdrip": False, "ppvrip": False, "tvrip": False,
                "uhdrip": False, "vhsrip": False, "webdlrip": False,
                "webrip": True
            }),
            ("HDR", "hdr", {
                "bit10": True, "dolby_vision": False, "hdr": True,
                "hdr10plus": True, "sdr": True
            }),
            ("Audio", "audio", {
                "aac": True, "ac3": True, "atmos": True,
                "dolby_digital": True, "dolby_digital_plus": True,
                "dts_lossy": True, "dts_lossless": True,
                "eac3": True, "flac": True, "mono": False,
                "mp3": False, "stereo": True, "surround": True,
                "truehd": True
            }),
            ("Extras", "extras", {
                "three_d": False, "converted": False, "documentary": False,
                "dubbed": True, "edition": True, "hardcoded": True,
                "network": True, "proper": True, "repack": True,
                "retail": True, "site": False, "subbed": True,
                "upscaled": False
            }),
            ("Trash", "trash", {
                "cam": False, "clean_audio": False, "pdtv": False,
                "r5": False, "screener": False, "size": False,
                "telecine": False, "telesync": False
            })
        ]
        
        category_tabs = st.tabs([cat[0] for cat in rank_categories])
        
        for tab, (category_name, category_key, default_fetch) in zip(category_tabs, rank_categories):
            with tab:
                with st.form(f"custom_ranks_{category_key}_form"):
                    custom_ranks = settings_model.get('custom_ranks', {}).get(category_key, {})
                    
                    # Get the appropriate rank model class based on category
                    rank_model_class = {
                        'quality': QualityRankModel,
                        'rips': RipsRankModel,
                        'hdr': HdrRankModel,
                        'audio': AudioRankModel,
                        'extras': ExtrasRankModel,
                        'trash': TrashRankModel
                    }[category_key]
                    
                    # Create or get the rank model instance
                    rank_model = rank_model_class(**custom_ranks) if custom_ranks else rank_model_class()
                    
                    # Convert the model to a list for the data editor
                    ranks_list = []
                    for field_name, field_value in rank_model.model_dump().items():
                        if isinstance(field_value, CustomRank):
                            ranks_list.append({
                                "type": field_name,
                                "fetch": field_value.fetch,
                                "rank": field_value.rank,
                                "enable": field_value.use_custom_rank,
                                "default_fetch": default_fetch.get(field_name, True)
                            })
                    
                    # Sort the list by type for consistency
                    ranks_list.sort(key=lambda x: x['type'])
                    
                    st.markdown(f"""
                    #### {category_name} Attributes
                    Configure how {category_name.lower()} attributes affect torrent ranking.
                    Default fetch values are shown in the help text for each attribute.
                    """)
                    
                    edited_ranks = st.data_editor(
                        ranks_list,
                        num_rows="fixed",
                        use_container_width=True,
                        disabled=["type", "default_fetch"],
                        column_config={
                            "type": st.column_config.TextColumn(
                                "Attribute",
                                help="The media attribute to rank"
                            ),
                            "fetch": st.column_config.CheckboxColumn(
                                "Fetch",
                                help="Whether to consider this attribute (affects filtering)"
                            ),
                            "rank": st.column_config.NumberColumn(
                                "Rank Value",
                                help="The ranking score (-10000 to 10000)",
                                min_value=-10000,
                                max_value=10000
                            ),
                            "enable": st.column_config.CheckboxColumn(
                                "Override",
                                help="Enable to use custom rank instead of profile default"
                            ),
                            "default_fetch": st.column_config.CheckboxColumn(
                                "Default Fetch",
                                help="The default fetch value for this attribute"
                            ),
                        },
                        hide_index=True
                    )
                    
                    submit = st.form_submit_button(f'💾 Save {category_name} Ranks')
                    if submit:
                        # Convert the edited ranks back to the model format
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
            torrent = None
            error_occurred = False
            
            try:
                ranking_model = rtn_rank_models.get(
                    st.session_state.conf['settings_model']['profile'],
                    DefaultRanking()  # Default to DefaultRanking if profile not found
                )

                settings_model = get_settings_model(
                    st.session_state.conf['settings_model'])
                rtn = RTN(settings=settings_model,
                          ranking_model=ranking_model)
                info_hash = "BE417768B5C3C5C1D9BCB2E7C119196DD76B5570"

                # Use speed_mode from options config
                speed_mode = settings_model.options.get("enable_fetch_speed_mode", True)
                
                torrent = rtn.rank(raw_title=raw_title_text_input,
                                   correct_title=correct_title_text_input, 
                                   infohash=info_hash, 
                                   remove_trash=conf['remove_trash'],
                                   speed_mode=speed_mode)

            except Exception as err:
                error_occurred = True
                st.error(f"❌ Error during ranking: {str(err)}")

            # Show metrics if we have torrent data
            if torrent:
                try:
                    # Main metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Rank Score", f"{torrent.rank:,}")
                    
                    with col2:
                        st.metric("Fetch Status", "✅ Yes" if torrent.fetch else "❌ No")
                    
                    with col3:
                        matches_preferred = calculate_preferred(torrent.data, settings_model) > 0
                        st.metric("Preferred Boost", "✅ Yes" if matches_preferred else "❌ No")
                    
                    with col4:
                        st.metric("Title Similarity", f"{torrent.lev_ratio:.2%}")
                except Exception as err:
                    st.error(f"❌ Error displaying metrics: {str(err)}")

                # Detailed analysis in tabs
                analysis_tabs = st.tabs([
                    "📊 Overview",
                    "🔍 Parsed Data",
                    "⚡ Quality Analysis",
                    "🎯 Pattern Matches",
                    "📈 Additional Info"
                ])

                with analysis_tabs[0]:
                    try:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("### 📝 Basic Information")
                            st.markdown(f"**Parsed Title:** {torrent.data.parsed_title}")
                            st.markdown(f"**Year:** {torrent.data.year or 'N/A'}")
                            st.markdown(f"**Type:** {torrent.data.type.title()}")
                            if torrent.data.seasons:
                                st.markdown(f"**Seasons:** {', '.join(map(str, torrent.data.seasons))}")
                            if torrent.data.episodes:
                                st.markdown(f"**Episodes:** {', '.join(map(str, torrent.data.episodes))}")
                            if torrent.data.group:
                                st.markdown(f"**Release Group:** {torrent.data.group}")
                        
                        with col2:
                            st.markdown("### 🎥 Media Information")
                            st.markdown(f"**Resolution:** {torrent.data.resolution}")
                            if torrent.data.quality:
                                st.markdown(f"**Quality:** {torrent.data.quality}")
                            if torrent.data.codec:
                                st.markdown(f"**Codec:** {torrent.data.codec}")
                            if torrent.data.audio:
                                st.markdown(f"**Audio:** {', '.join(torrent.data.audio)}")
                            if torrent.data.hdr:
                                st.markdown(f"**HDR:** {', '.join(torrent.data.hdr)}")
                    except Exception as err:
                        st.error(f"❌ Error displaying overview: {str(err)}")

                with analysis_tabs[1]:
                    try:
                        st.json(torrent.data.model_dump())
                    except Exception as err:
                        st.error(f"❌ Error displaying parsed data: {str(err)}")

                with analysis_tabs[2]:
                    try:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("### 🎬 Video Quality")
                            quality_attrs = {
                                "Resolution": torrent.data.resolution,
                                "Quality": torrent.data.quality,
                                "Codec": torrent.data.codec,
                                "Bit Depth": torrent.data.bit_depth,
                                "HDR": ", ".join(torrent.data.hdr) if torrent.data.hdr else None
                            }
                            for attr, value in quality_attrs.items():
                                if value:
                                    st.markdown(f"**{attr}:** {value}")
                        
                        with col2:
                            st.markdown("### 🔊 Audio Quality")
                            audio_attrs = {
                                "Audio Codecs": ", ".join(torrent.data.audio) if torrent.data.audio else None,
                                "Channels": ", ".join(torrent.data.channels) if torrent.data.channels else None
                            }
                            for attr, value in audio_attrs.items():
                                if value:
                                    st.markdown(f"**{attr}:** {value}")
                            
                            if torrent.data.dubbed:
                                st.markdown("**Dubbed:** ✅")
                            if torrent.data.subbed:
                                st.markdown("**Subbed:** ✅")
                    except Exception as err:
                        st.error(f"❌ Error displaying quality analysis: {str(err)}")

                with analysis_tabs[3]:
                    try:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            matches_required = check_required(torrent.data, settings_model)
                            st.markdown(
                                f"**Required Patterns:** {emoji_bool(matches_required)}",
                                help="Check if the title meets the required patterns"
                            )

                            failed_keys = []
                            matches_exclude = check_exclude(torrent.data, settings_model, failed_keys)
                            st.markdown(
                                f"**Excluded Patterns:** {emoji_bool(not matches_exclude)}",
                                help="Check if the title contains excluded patterns"
                            )
                            if failed_keys:
                                st.markdown("**Failed Exclude Patterns:**")
                                for key in failed_keys:
                                    st.markdown(f"- `{key}`")
                        
                        with col2:
                            st.markdown("### 🚩 Special Flags")
                            flags = {
                                "Extended": torrent.data.extended,
                                "Converted": torrent.data.converted,
                                "Hardcoded": torrent.data.hardcoded,
                                "Proper": torrent.data.proper,
                                "Repack": torrent.data.repack,
                                "Retail": torrent.data.retail,
                                "Remastered": torrent.data.remastered,
                                "Unrated": torrent.data.unrated,
                                "Documentary": torrent.data.documentary,
                                "Scene Release": torrent.data.scene
                            }
                            for flag, value in flags.items():
                                if value:
                                    st.markdown(f"- {flag}")
                    except Exception as err:
                        st.error(f"❌ Error displaying pattern matches: {str(err)}")

                with analysis_tabs[4]:
                    try:
                        st.markdown("### 📊 Additional Information")
                        additional_info = {
                            "Seeders": torrent.seeders or "N/A",
                            "Leechers": torrent.leechers or "N/A",
                            "Infohash": torrent.infohash,
                        }
                        
                        for label, value in additional_info.items():
                            st.markdown(f"**{label}:** {value}")
                            
                        if torrent.trackers:
                            st.markdown("### 🌐 Trackers")
                            for tracker in torrent.trackers:
                                st.markdown(f"- {tracker}")
                    except Exception as err:
                        st.error(f"❌ Error displaying additional info: {str(err)}")


def render_preset_profiles():
    st.header("📚 Preset Ranking Profiles")
    st.markdown("""
    These are the built-in ranking profiles that you can use as a starting point.
    Each profile has different ranking weights optimized for specific use cases.
    
    - **default**: Optimized for streaming without transcoding
    - **best**: Aimed at obtaining the highest quality content available
    - **custom**: Start with a blank profile and customize everything
    
    The tables below show the exact ranking values for each attribute in each profile.
    These values determine how torrents are scored during ranking.
    """)
    
    # Display raw JSON data for each profile
    st.subheader("🔍 Raw Profile Data")
    profile_tabs = st.tabs(["Default Profile", "Best Profile", "Custom Profile"])
    
    with profile_tabs[0]:
        st.markdown("### Default Profile JSON")
        st.json(dict(DefaultRanking()))
        
    with profile_tabs[1]:
        st.markdown("### Best Profile JSON")
        st.json(dict(BestRanking()))
        
    with profile_tabs[2]:
        st.markdown("### Custom Profile JSON")
        st.json(dict(BaseRankingModel()))
    
    st.markdown("---")
    
    # Quality Rankings
    st.subheader("🎥 Quality Rankings")
    quality_data = {
        "Attribute": ["av1", "avc", "bluray", "dvd", "hdtv", "hevc", "mpeg", "remux", "vhs", "web", "webdl", "webmux", "xvid", "pdtv"],
        "Default": [0, 500, 100, -1000, -1000, 500, -100, -10000, -10000, 150, 5000, -10000, -10000, -10000],
        "Best": [0, 500, 100, -5000, -5000, 500, -1000, 10000, -10000, 100, 200, -10000, -10000, -10000],
        "Custom": [0] * 14
    }
    st.dataframe(quality_data, use_container_width=True)
    
    # Rips Rankings
    st.subheader("📼 Rips Rankings")
    rips_data = {
        "Attribute": ["bdrip", "brrip", "dvdrip", "hdrip", "ppvrip", "tvrip", "uhdrip", "vhsrip", "webdlrip", "webrip"],
        "Default": [-1000, -1000, -1000, -1000, -1000, -10000, -1000, -10000, -10000, 30],
        "Best": [-5000, -10000, -5000, -10000, -10000, -10000, -5000, -10000, -10000, -1000],
        "Custom": [0] * 10
    }
    st.dataframe(rips_data, use_container_width=True)
    
    # HDR Rankings
    st.subheader("🌈 HDR Rankings")
    hdr_data = {
        "Attribute": ["bit_10", "dolby_vision", "hdr", "hdr10plus", "sdr"],
        "Default": [5, 50, 50, 0, 0],
        "Best": [100, 1000, 500, 1000, 0],
        "Custom": [0] * 5
    }
    st.dataframe(hdr_data, use_container_width=True)
    
    # Audio Rankings
    st.subheader("🔊 Audio Rankings")
    audio_data = {
        "Attribute": ["aac", "ac3", "atmos", "dolby_digital", "dolby_digital_plus", "dts_lossy", "dts_lossless", 
                     "eac3", "flac", "mono", "mp3", "stereo", "surround", "truehd"],
        "Default": [250, 30, 400, 0, 0, 600, 0, 250, 0, -10000, -10000, 0, 0, -100],
        "Best": [100, 50, 1000, 0, 0, 100, 1000, 150, 0, -1000, -1000, 0, 0, 1000],
        "Custom": [0] * 14
    }
    st.dataframe(audio_data, use_container_width=True)
    
    # Extras Rankings
    st.subheader("✨ Extras Rankings")
    extras_data = {
        "Attribute": ["three_d", "converted", "documentary", "dubbed", "edition", "hardcoded", "network", 
                     "proper", "repack", "retail", "site", "subbed", "upscaled"],
        "Default": [-10000, -1250, -250, 0, 100, 0, 300, 1000, 1000, 0, -10000, 0, -10000],
        "Best": [-10000, -1000, -250, -1000, 100, 0, 0, 20, 20, 0, -10000, 0, -10000],
        "Custom": [0] * 13
    }
    st.dataframe(extras_data, use_container_width=True)
    
    # Trash Rankings
    st.subheader("🗑️ Trash Rankings")
    trash_data = {
        "Attribute": ["cam", "clean_audio", "r5", "satrip", "screener", "size", "telecine", "telesync"],
        "Default": [-10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000],
        "Best": [-10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000],
        "Custom": [0] * 8
    }
    st.dataframe(trash_data, use_container_width=True)
    
    st.markdown("""
    ### 📝 Notes
    - Positive values indicate preferred attributes
    - Negative values indicate undesired attributes
    - The `custom` profile starts with all values at 0, allowing you to build your own ranking system
    - These values can be overridden using custom ranks in the settings
    """)


def render_import_export():
    st.header("📤 Import/Export Settings")
    st.markdown("""
    Import or export your RTN settings. You can:
    - Export your current settings to a JSON file
    - Import settings from a JSON file
    - View and edit your current settings in JSON format
    """)

    tab1, tab2 = st.tabs(["📂 Import/Export File", "📝 View/Edit JSON"])

    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Export button and functionality
            if st.button("📤 Export Settings"):
                settings_model = get_settings_model(st.session_state.conf['settings_model'])
                settings_json = settings_model.model_dump_json(indent=2)
                
                # Create a download button for the JSON file
                st.download_button(
                    label="💾 Download Settings JSON",
                    data=settings_json,
                    file_name="rtn_settings.json",
                    mime="application/json"
                )

        with col2:
            # Import button and functionality
            uploaded_file = st.file_uploader("📥 Import Settings", type=['json'])
            if uploaded_file is not None:
                try:
                    # Read and parse the uploaded JSON
                    settings_json = uploaded_file.read()
                    settings_model = SettingsModel.model_validate_json(settings_json)
                    
                    # Update the session state with the new settings
                    st.session_state.conf['settings_model'] = settings_model.model_dump()
                    save_conf_to_query_params()
                    st.success("✅ Settings imported successfully!")
                    st.rerun()  # Refresh the page to show the new settings
                except Exception as e:
                    st.error(f"❌ Error importing settings: {str(e)}")

    with tab2:
        st.markdown("""
        ### Current Settings JSON
        View your current settings in JSON format. You can also edit the JSON directly.
        
        !!! warning
            Be careful when editing JSON directly. Invalid JSON or incorrect settings structure will cause errors.
        """)
        
        # Get current settings as formatted JSON
        settings_model = get_settings_model(st.session_state.conf['settings_model'])
        current_settings_json = settings_model.model_dump_json(indent=2)
        
        # Create an editable JSON area
        edited_json = st.text_area(
            "Edit JSON",
            value=current_settings_json,
            height=400
        )
        
        # Add apply button for JSON changes
        if st.button("Apply JSON Changes"):
            try:
                # Validate and update settings
                new_settings = SettingsModel.model_validate_json(edited_json)
                st.session_state.conf['settings_model'] = new_settings.model_dump()
                save_conf_to_query_params()
                st.success("✅ Settings updated successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error updating settings: {str(e)}")
        
        # Show current settings in a read-only format
        with st.expander("View Parsed Settings"):
            st.json(settings_model.model_dump())


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
        
elif page == "Preset Profiles":
    render_preset_profiles()
elif page == "Import/Export":
    render_import_export()
