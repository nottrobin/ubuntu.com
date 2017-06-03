from copy import deepcopy
from django.conf import settings


def _find_page_by_path(path, pages):
    """
    Locate a page from within a tree pages and children
    of any depth.
    """

    current_page = None

    for page in pages:
        if path == page['url_path']:
            current_page = page
            break
        elif 'children' in page:
            current_page = _find_page_by_path(path, page['children'])

    return current_page


def _find_page_section(path, sections):
    """
    Given a tree of sections with child pages,
    Return the page and its section.

    If the path matches the section itself,
    return a page with the title of "Overview"
    """

    matching_page = None
    matching_section = None

    for section_id, section in sections.items():
        if path == section['url_path']:
            matching_section = section
            matching_page = deepcopy(section)
            matching_page['title'] = 'Overview'
            break
        elif 'children' in section:
            page = _find_page_by_path(path, section['children'])

            if page:
                matching_section = section
                matching_page = page
                break

    return matching_section, matching_page


def navigation(request):
    """
    Set any context that we want to pass to all pages
    """

    nav_context = {}

    # Get breadcrumb information and pass to template
    section, page = _find_page_section(request.path, settings.NAV_ITEMS)
    if section and page:
        nav_context['section_path'] = section.get('url_path')
        nav_context['section_title'] = section.get('title')
        nav_context['page_path'] = page.get('url_path')
        nav_context['page_title'] = page.get('title')
        nav_context['page_children'] = page.get('children')

    nav_context['menu_sections'] = settings.MENU_SECTIONS

    return nav_context
