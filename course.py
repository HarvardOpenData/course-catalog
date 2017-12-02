import re

import utils


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
        'level',
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

        Actually no, keep the department and number together (makes sorting easier).
        But let someone extract the individual pieces.

        Regex for extracting course number:

            [\dA-Z]+$
        """

        # for now, just replace multiple spaces with a single space
        self.number = re.sub(r" +", " ", number.strip())

        # get the actual course number (e.g. "50" in "Computer Science 50")
        # these are formatted strangely; here's a corpus we have to match properly
        #
        # "Computer Science 50",
        # "Anthropology     1010",
        # "Hausa AA",
        # "Astronomy 91R",
        # "Astronomy 202A",
        # "Aramaic 300 Section: 002",
        # "Biological Sci in Public Hlth 389 Section: 01",
        # "Culture & Belief 61 Section: LEC"
        #
        # From those we want to extract 50, 1010, AA, 91R, 202A, 300, 389, 61
        # (all in string format)
        # hence this regex
        number_matcher = re.compile("([\dA-Z]+)(?: *Section: [\dA-Z]+)?$")
        self.actual_number = number_matcher.findall(self.number)[0]

        # from the actual number, guess the level
        # just letters: language course
        # 1-89: undergraduate, non-concentrators
        # 90-99: undergraduate seminars
        # 100-199: undergraduate, concentrators
        # 200-299: undergraduate & graduate
        # 300-399: graduate
        # 900-999: undergraduate seminars
        # 1000-1999: undergraduate, concentrators
        # 2000-2999: undergraduate & graduate
        # 3000-3999: graduate
        #
        # Or, more simply, for "level", just consider
        # Undergraduate/Undergradute+Graduate/Graduate
        self.level = None

        # extract digits and letters
        digit_matcher = re.compile("\d+")
        digit_matches = digit_matcher.findall(self.actual_number)
        if len(digit_matches) > 0:
            # this has digits, like '50' or '91' or '1010'
            digits = int(digit_matches[0])

            # from this, we can determine level (undergrad, mixed, graduate)
            if digits < 200:
                self.level = "Undergraduate"
            elif digits < 300:
                self.level = "Undergraduate + Graduate"
            elif digits < 400:
                self.level = "Graduate"
            elif digits < 2000:
                self.level = "Undergraduate"
            elif digits < 3000:
                self.level = "Undergradute + Graduate"
            else:
                self.level = "Graduate"

        else:
            # this is a language course with only letters
            # languages are all undergraduate!
            self.level = "Undergraduate"

    def set_schedule(self, schedule):
        # take the raw schedule and structure the data better
        self.schedule = schedule

        schedule_matcher = re.compile("([MTWRF]{1,5}) (\d{4}) ([AP]M) - (\d{4}) ([AP]M)")
        matches = schedule_matcher.findall(schedule)

        if len(matches) == 1:
            # we found something!
            # this contains, in order:
            # 0. Days
            # 1. Start time
            # 2. Start AM or PM
            # 3. End time
            # 4. End AM or PM
            # e.g. ('MW', '1100', 'AM', '1159', 'AM')
            schedule_chunks = matches[0]

            # convert start and end time to military time
            # e.g. 0130 PM => 1330
            self.start_time = utils.time_to_military(schedule_chunks[1], schedule_chunks[2])
            self.end_time = utils.time_to_military(schedule_chunks[3], schedule_chunks[4])

            # convert the days into better-readable ones
            # "MW" => ["Monday", "Wednesday]
            # e.g. "MW"
            days_abbreviation_string = schedule_chunks[0]
            # e.g. ["M","W"]
            days_abbreviation_list = list(days_abbreviation_string)

            # convert "M" to "Monday", etc
            abbreviation_dict = {
                "M": "Monday",
                "T": "Tuesday",
                "W": "Wednesday",
                "R": "Thursday",
                "F": "Friday"
            }
            days_full_list = [abbreviation_dict[d] for d in days_abbreviation_list]
            self.days = days_full_list



    def process_strings(self):
        """
        Once all `strings` (i.e. unstructured description text) are loaded,
        pull out useful information like the schedule.
        """
        # try to extract a course schedule
        times = []
        for string in self.strings:
            # TODO factor this out b/c we use it above
            matcher = re.compile("[MTWRF]{1,5} \d{4} [AP]M - \d{4} [AP]M")
            times.append(matcher.findall(string))

        flattened_times = sum(times,[])

        # this array will have max 1 element
        if len(flattened_times) > 0:
            self.set_schedule(flattened_times[0])
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
        # so that means any arrays need to be flattened to scalars
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
            schedule=self.schedule,
            level=self.level
        )
