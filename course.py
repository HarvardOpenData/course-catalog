class Course(object):

    # static
    # this is the list of fields that are exported to CSV
    # see to_dict_for_csv()
    CSV_FIELDS = [
        'number',
        'semester',
        'name',
        'instructors',
        'schedule',
        'id',
    ]

    def __init__(self):
        self.number = None
        self.name = None
        self.instructors = []
        self.semester = None
        self.schedule = None
        self.strings = []
        self.id = None

    def set_id(self, raw_id_string):
        """
        Raw course ID strings are formatted in the catalog PDF as `(123456)  `
        or something similar. Here we clean it up for you.
        """
        # trim whitespace
        trimmed = raw_id_string.strip()

        if len(course_id) > 0:
            # as long as the course id isn't empty
            # (sometimes it is)

            # then remove parentheses
            course_id_without_parens = course_id[1:-1]

            current_course.id = course_id_without_parens

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        # for nicer ipython debugging
        return str(self.__dict__)

    def to_dict(self):
        # ALIAS
        return self.__dict__

    def to_dict_for_csv(self):
        # returns a nicer-formatted dict ready for insertion into a csv
        # also everything needs to be converted to ascii

        def to_ascii(unicode_str):
            if unicode_str is None:
                return None
            return unicode_str.encode("ascii","replace")

        return dict(
            id=self.id,
            name=to_ascii(self.name),
            number=self.number,
            instructors=to_ascii((" & ".join(self.instructors))),
            semester=self.semester,
            schedule=self.schedule
        )
