import os
from pathlib import Path
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components
from typing import Iterable
from typing import List
from typing import Text

from src.utils import EntityNotFoundError
from src.utils import get_report_name
from src.utils import period_dir_to_dates_range



def display_sidebar_header() -> None:

    # Logo
    logo = Image.open("static/logo.png")
    with st.sidebar:
        st.image(logo, use_column_width=True)
        col1, col2 ,col3= st.columns(3)
        streamlit_docs: Text = (
            "https://docs.streamlit.io/"
        )
        evidently_docs: Text = "https://docs.evidentlyai.com/"
        pycaret_docs: Text="https://pycaret.gitbook.io/docs/"
        col3.markdown(
            f"<a style='display: block; text-align: center;' href={streamlit_docs}>Streamlit docs</a>",
            unsafe_allow_html=True,
        )
        col1.markdown(
            f"<a style='display: block; text-align: center;' href={evidently_docs}>Evidently docs</a>",
            unsafe_allow_html=True,
        )
        col2.markdown(
            f"<a style='display: block; text-align: center;' href={pycaret_docs}>Pycaret docs</a>",
            unsafe_allow_html=True,
        )
        
        st.header("")  # add space between logo and selectors
        


def select_project(projects: List[Text]) -> Path:
    """Select a project name form selectbox
    and return path to the project directory.

    Args:
        projects (List[Text]): List of available projects.

    Raises:
        EntityNotFoundError: If projects list is empty.

    Returns:
        Path: Path to the project.
    """

    if not projects:
        raise EntityNotFoundError("🔍 Projects not found")

    selected_project: Text = st.sidebar.selectbox(
        label="💼 Select project", options=projects
    )

    return Path(selected_project)


def select_period(periods: List[Text]) -> Text:
    """

    Args:
        periods (List[Text]): List of period strings.

    Raises:
        EntityNotFoundError: If periods list is empty.

    Returns:
        Text: Dates period in format '%Y-%m-%d - %Y-%m-%d'.
    """
    

    selected_period: Text = st.sidebar.selectbox(
        label="📆 Select period", options=periods, 
    )

    return selected_period


def select_report(report_names: List[Text]) -> Text:
    """Select a report name from a selectbox.

    Args:
        report_names (List[Text]): Available report names.

    Raises:
        EntityNotFoundError: If report name list is empty.

    Returns:
        Text: Report name.
    """

    if not report_names:
        raise EntityNotFoundError("🔍 Reports not found")

    selected_report_name: Text = st.sidebar.selectbox(
        label="📈 Select report", options=report_names
    )
    
    return selected_report_name
    


def display_header(project_name: Text, period: Text, report_name: Text) -> None:
    """Display report header.

    Args:
        project_name (Text): Project name.
        period (Text): Period.
        report_name (Text): Report name.
    """
    glowing_text_style = '''
    <style>
        .glowing-text {
            font-family: 'Arial Black', sans-serif;
            font-size: 45px;
            text-align: center;
            animation: glowing 2s infinite;
        }
        
        @keyframes glowing {
            0% { color: #FF9933; } /* Saffron color */
            25% { color: #FFFFFF; } /* White color */
            50% { color: #128807; } /* Green color */
            75% { color: #0000FF; } /* Blue color */
            100% { color: #FF9933; } /* Saffron color */
        }
    </style>
'''


    dates_range: Text = period_dir_to_dates_range(period)
    # Display the glowing text using st.markdown
    st.markdown(glowing_text_style, unsafe_allow_html=True)
    st.markdown(f'<p class="glowing-text">📊 Real-Time Model Monitoring 💹</p>', unsafe_allow_html=True)
    st.info(f"Project: {project_name.title()}")
    #st.markdown(f"<div align='center'><h1>💼 Project: {project_name}<h1></div>",unsafe_allow_html=True)
    st.info(f"Report: {report_name}")
    st.info(f"Period: {dates_range}")




@st.cache_data
def display_report(report_path: Path) -> List[Text]:
    """Display report.

    Args:
        report (Path): Report path.

    Returns:
        List[Text]: Report parts content - list report part contents.
    """

    # If a report is file then read and display the report
    if report_path.is_file():
        with open(report_path, encoding="utf8") as report_f:
            report: Text = report_f.read()
            components.html(report, width=1000, height=1200, scrolling=True)
        return [report]

    # If a report is complex report (= directory) then
    elif report_path.is_dir():
        # list report parts
        report_parts: List[Path] = sorted(
            list(map(
                lambda report_part: report_path / report_part, 
                os.listdir(report_path))
                )
            )
        tab_names: List[Text] = map(get_report_name, report_parts)
        tab_names_formatted = [f"📈 {name}" for name in tab_names]
        
        # create tabs
        tabs: Iterable[object] = st.tabs(tab_names_formatted)
        report_contents: List[Text] = []

        # read each report part and display in separate tab
        for tab, report_part_path in zip(tabs, report_parts):
            with tab:
                with open(report_part_path) as report_part_f:
                    report_part_content: Text = report_part_f.read()
                    report_contents.append(report_part_content)
                    components.html(
                        report_part_content, width=1000, height=1200, scrolling=True
                    )

        return report_contents
    
    else: 
        return EntityNotFoundError("🔍 No reports found")
   
