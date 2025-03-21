"""The API for accessing LeetCode's front end."""

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from http.client import HTTPResponse

from click import ClickException

URL_TITLE_SLUG_PATTERN = re.compile(
    r"^https://leetcode\.com/problems/(?P<slug>[-\w]+)/"
)
TITLE_SLUG_PATTERN = re.compile(r"\w+(?:-\w+)+")

LEETCODE_API_URL = "https://leetcode.com/graphql/"
GRAPHQL_QUERY_TEMPLATE = """
query questionEditorData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    # questionId
    # questionFrontendId
    codeSnippets {
      lang
      langSlug
      code
    }
    # envInfo
    # enableRunCode
  }
}
"""
FAKE_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 "
    "(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
)


def is_title_slug(title_slug: str) -> bool:
    """Checks if the value matches the title slug pattern."""
    match = TITLE_SLUG_PATTERN.fullmatch(title_slug)
    return match is not None
    # if match is None:
    #     raise ClickException(f"Invalid title slug '{title_slug}'.")


def _get_title_slug(problem_url: str) -> str:
    match = URL_TITLE_SLUG_PATTERN.match(problem_url)
    if match is None:
        raise ClickException(f"Invalid LeetCode problem URL '{problem_url}'.")
    title_slug = match.group("slug")
    return title_slug


def _create_graphql_request(title_slug: str):
    """Creates a GraphQL query to fetch the problem code using the title slug."""
    body = {"query": GRAPHQL_QUERY_TEMPLATE, "variables": {"titleSlug": title_slug}}
    body_bytes = bytes(json.dumps(body), encoding="utf-8")
    headers = {"User-Agent": FAKE_USER_AGENT, "Content-Type": "application/json"}
    request = urllib.request.Request(
        LEETCODE_API_URL, body_bytes, method="POST", headers=headers
    )
    return request


def _get_body_from_request(request: urllib.request.Request) -> dict:
    try:
        with urllib.request.urlopen(request) as res:
            response: HTTPResponse = res
            text = response.read()
    except urllib.error.URLError as error:
        print(str(error))
        raise ClickException("Could not get data from API.") from error
    body: str = text.decode("utf-8")
    data = json.loads(body)
    return data


def get_code_snippets(title_slug: str) -> list[dict[str, str]]:
    """Fetches all code snippets for the given LeetCode problem."""
    request = _create_graphql_request(title_slug)
    body = _get_body_from_request(request)
    question = body["data"]["question"]
    try:
        code_snippets = question["codeSnippets"]
    except TypeError as type_error:
        raise ClickException("Invalid title slug.") from type_error
    return code_snippets


def _get_template_data(title_slug, language: str):
    code_snippets = get_code_snippets(title_slug)

    for lang_data in code_snippets:
        if lang_data["langSlug"] != language:
            continue
        return lang_data
    raise ClickException(f"Invalid programming language '{language}'.")


def get_leetcode_template(
    language: str, title_slug: str | None = None, url: str | None = None
):
    """Fetches the LeetCode problem code template for the given language."""
    if url is None:
        if title_slug is None:
            raise ClickException("Either url or title slug must be specified.")
    else:
        title_slug = _get_title_slug(url)
    template_data = _get_template_data(title_slug, language)
    return title_slug, template_data
