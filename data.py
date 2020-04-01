class Form:
    def __init__(self, author_id):
        self.author_id = author_id
        self.completed = False
        self.story_details = {
            'Link to the story': "",
            'author': "",
            'cover url': "", # There wasn't a cover image url
            'title': "",
            'genre': "",
            'warnings': "", # No warnings
            'description': "",
            'length': "", # Unknown
        }