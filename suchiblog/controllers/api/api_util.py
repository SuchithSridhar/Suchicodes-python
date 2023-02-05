import os
from ...config import Config
from ..resources.res_util import ResUtil
from ...util import Util


class ApiUtil:

    BLOG_BRIEF = 'brief'
    BLOG_TITLE = 'title'
    BLOG_CATEGORY = 'category'
    BLOG_ID = 'id'

    @staticmethod
    def verify_blog_config(config) -> tuple:
        '''
        Checks all the required fields for a blog upload.
        If a required field is not present it will return:
        (False, <the missing field>).
        If all fields are present, returns: (True, '').
        '''
        required = (
            ApiUtil.BLOG_BRIEF,
            ApiUtil.BLOG_TITLE,
            ApiUtil.BLOG_CATEGORY
        )
        for element in required:
            if element not in config:
                return (False, element)

        return (True, '')

    @staticmethod
    def categorize_files(uploaded_files) -> dict:
        files = {
                'other': [],
                'pictures': [],
                'config': None,
                'markdown': None
        }

        for file in uploaded_files:
            if file.filename is None:
                continue

            file.filename = os.path.basename(file.filename)

            if (file.filename.endswith('.png') or
                    file.filename.endswith('.jpg')):

                files['pictures'].append(file)

            if file.filename == Config.NOTES_CONFIG_FILENAME:
                files['config'] = file

            if file.filename.endswith('.md'):
                files['markdown'] = file

        return files

    @staticmethod
    def substitute_picute_paths(markdown: str, picture_map: dict) -> str:
        for picture, path in picture_map.items():
            start = markdown.find(picture)
            open_brace = ResUtil.find_open_parenthesis(markdown, start)
            close_brace = markdown.find(")", start)
            path = os.path.join(Config.UPLOAD_DIR_URL, path)
            markdown = (
                markdown[:open_brace + 1] +
                path + markdown[close_brace:]
            )

        return markdown

    @staticmethod
    def save_required_files(files: list, picture_map: dict = {}) -> dict:
        if len(picture_map) == 0:
            picture_map = {}

        for file in files:
            if file.filename in picture_map:
                continue

            uuid = Util.create_uuid()
            new_file_name = uuid + f"{os.path.splitext(file.filename)[1]}"
            file.save(
                os.path.join(Config.PROJECTS_UPLOAD_FOLDER, new_file_name)
            )
            picture_map[file.filename] = new_file_name

        return picture_map
