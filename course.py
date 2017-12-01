import re
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

        if len(trimmed) > 2:
            # remove parens
            without_parens = trimmed[1:-1]
            self.id = without_parens

    def set_course_number(self, number):
        """
        e.g. "Computer Science 50"

        TODO
        From the course number (e.g. Computer Science 50), extract the dept
        (e.g. Computer Science). Ideally we'd split up the course number into
        [Computer Science, 50] but I'm not sure how to name that without
        being confusing. Maybe department and number? idk.

        Regex for extracting course number:

            [\dA-Z]+$
        """
        self.number = number.strip()

        """
        OTHER TODOS
        Many course numbers have tons of spaces such as

            Haitian     BB

        We should replace everything with more than one space, with just one space.
        """

        # TODO extract the department name, and isolate the number itself
        # e.g. [Computer Science, 50]

    def process_strings(self):
        """
        Once all `strings` (i.e. unstructured description text) are loaded,
        pull out useful information like the schedule.
        """
        # try to extract a course schedule
        times = []
        for string in self.strings:
            matcher = re.compile("[MTWRF]{1,5} \d{4} [AP]M - \d{4} [AP]M")
            times.append(matcher.findall(string))

        flattened_times = sum(times,[])

        # this array will have max 1 element
        if len(flattened_times) > 0:
            self.schedule = flattened_times[0]
        else:
            self.schedule = None

        # try to extract a semester
        for string in self.strings:
            semester = re.search("20\d\d ((Fall)|(Spring))", string)
            if semester is not None:
                # just find the first one then quit
                self.semester = semester.group()
                break


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
