from mongoengine import (
    Document,
    StringField,
    DateField,
)

class Report(Document):
    """
    A lost/found report.
    """
    kind = StringField(
        required=True,
        choices=("lost", "found")
    )
    name = StringField(
        required=True,
        max_length=200
    )
    description = StringField()
    date = DateField()            # stores a Python date
    location = StringField()
    contact = StringField()
    image = StringField()         # filename in UPLOAD_FOLDER

    meta = {
        "collection": "reports",
        "ordering": ["-date"]
    }
