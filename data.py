class Form:
    def __init__(self, author_id):
        self.author_id = author_id
        self.completed = False
        self.story_details = {
            'link': "",
            'author': "",
            'cover_url': "", # There wasn't a cover image url
            'title': "",
            'genre': "",
            'warning': "", # No warnings
            'description': "",
            'length': "", # Unknown
        }