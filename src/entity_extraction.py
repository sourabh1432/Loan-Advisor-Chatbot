"""Entity extraction functions for the Loan Advisor Chatbot.

Extracts income, loan amount/type, tenure, interest rate, credit score,
dependents, existing-loan details, and a combined entity dictionary.
"""

import re

def find_income_expression(text):

    text = text.lower().strip()

    income_patterns = [
        r"\b(?:my\s+)?(?:monthly\s+)?income\s+(?:is|of|around|about)?\s*",
        r"\b(?:my\s+)?(?:monthly\s+)?salary\s+(?:is|of|around|about)?\s*",
        r"\bi\s+(?:earn|make|receive|get|take home)\s*",
        r"\bi\s+am\s+earning\s*",
        r"\bearning\s+(?:an?\s+)?income\s+of\s*"
    ]

    money_pattern = r"""
        (?P<currency>₹|rs\.?|inr|\$|usd)?
        \s*
        (?P<number>\d+(?:,\d+)*(?:\.\d+)?)
        \s*
        (?P<unit>lakhs?|lacs?|crores?|k|thousand|million)?
    """

    for income_pattern in income_patterns:

        for phrase_match in re.finditer(income_pattern, text):

            remaining_text = text[phrase_match.end():]

            money_match = re.match(
                r"\s*" + money_pattern,
                remaining_text,
                re.VERBOSE
            )

            if money_match:

                return {
                    "currency": money_match.group("currency"),
                    "number": money_match.group("number"),
                    "unit": money_match.group("unit")
                }

    return None

def normalize_money_value(result):

    if result is None:
        return None

    number = float(result['number'].replace(",",""))
    unit = result['unit']

    multipliers = {
        "k":1_000,
        "thousand":1_000,
        "lakh":1_00_000,
        "lakhs":1_00_000,
        "lac":1_00_000,
        "lacs":1_00_000,
        "crore":1_00_00_000,
        "crores":1_00_00_000,
        "million":10_00_000
    }

    if unit:
        number = number * multipliers.get(unit,1)
    return number

frequency_patterns={
    "monthly":[
        'per month',
        'monthly',
        'a month',
        'every month',
        'each month'
    ],
    "yearly":[
        'per year',
        'yearly',
        'annual',
        'annually',
        'every year',
        'each year',

    ],
    "weekly":[
        'per week',
        'weekly',
        'a week',
        'each week',
        'every week'
    ],
    "daily":[
        'per day',
        'each day',
        'every day',
        'daily'
    ]

}

def detect_income_frequency(text):

    if not isinstance(text, str) or not text.strip():
        return None

    text = re.sub(r"\s+", " ", text.lower().strip())

    for frequency, patterns in frequency_patterns.items():
        for pattern in patterns:
            if pattern in text:
                return frequency

    return None

def extract_income(text):
    result = find_income_expression(text)
    income = normalize_money_value(result)
    frequency = detect_income_frequency(text)

    return {
        "income":income,
        "frequency":frequency
    }

def find_loan_amount_expression(text):

    if not isinstance(text, str) or not text.strip():
        return None

    text = re.sub(r"\s+", " ", text.lower().strip())

    money_pattern = re.compile(
        r"(?P<currency>₹|rs\.?|inr|\$|usd)?\s*"
        r"(?P<number>-?\d+(?:,\d{3})*(?:\.\d+)?)\s*"
        r"(?P<unit>lakhs?|lacs?|crores?|k|thousand|millions?)?",
        re.IGNORECASE
    )

    request_patterns = [
        r"\bloan amount\s*(?:is|about|around|of)?\s*",
        r"\b(?:student|education|personal|business|car|vehicle|home|house|auto)\s+loans?\s+of\s*",
        r"\bloans?\s+of\s*",
        r"\b(?:need|want|require)\s+(?:a\s+)?loans?\s+(?:of\s*)?",
        r"\b(?:need|want|require)\s+(?:to\s+)?borrow\s*",
        r"\b(?:need|want|require)\s+",
        r"\b(?:car|vehicle|house|home|property|flat)\s+worth\s*",
        r"\b(?:finance|financing)\b[^.!?]{0,60}?\bfor\s*",
    ]

    for pattern in request_patterns:
        for phrase_match in re.finditer(pattern, text):

            remaining_text = text[phrase_match.end():]
            money_match = money_pattern.match(remaining_text)

            if money_match:
                return {
                    "currency": money_match.group("currency"),
                    "number": money_match.group("number"),
                    "unit": money_match.group("unit")
                }

    money_with_currency = re.compile(
        r"(?P<currency>₹|rs\.?|inr|\$|usd)\s*"
        r"(?P<number>-?\d+(?:,\d{3})*(?:\.\d+)?)\s*"
        r"(?P<unit>lakhs?|lacs?|crores?|k|thousand|millions?)?",
        re.IGNORECASE
    )

    request_cue = re.compile(
        r"\b(?:need|want|require|borrow|loan|finance|financing)\b",
        re.IGNORECASE
    )

    for money_match in money_with_currency.finditer(text):

        prefix = text[:money_match.start()]
        cues = list(request_cue.finditer(prefix))

        if not cues:
            continue

        context = prefix[cues[-1].end():]

        if re.search(
            r"\b(?:salary|income|earn|earning)\b",
            context
        ):
            continue

        return {
            "currency": money_match.group("currency"),
            "number": money_match.group("number"),
            "unit": money_match.group("unit")
        }

    return None

def extract_loan_amount(text):
    money_data = find_loan_amount_expression(text)
    loan_amount = normalize_money_value(money_data)

    return loan_amount

loan_patterns = {
    "personal_loan": [
        "want a personal loan"
        "need a personal loan",
        "apply for a personal loan",
        "want to get a personal loan",
        "looking for a personal loan",
        "I want personal loan",
        "I need money for personal expenses",
        "can I get a personal loan",
        "I require a personal loan",
        "I want to borrow money",
        "how to apply for a personal loan",
        "I need funds for an emergency",
        "personal loan for medical expenses",
        "I want a loan for my wedding",
        "tell me about personal loans",
        "what are the personal loan options",
        "I need an unsecured loan",
        "I want to take a personal loan",
        "help me get a personal loan",
        "am I eligible for a personal loan",
        "what documents are needed for a personal loan",
        "want a personal loan",
        "need a personal loan",
        "personal loan",
        "want personal loan",
        "need personal loan",
        "for personal expenses",
    ],
    "business_loan":[
        "need a business loan",
        "apply for a business loan",
        "want to get a business loan",
        "looking for a business loan",
        "I want a business loan",
        "I need money for business expenses",
        "can I get a business loan",
        "I require a business loan",
        "how to apply for a business loan",
        "I want a business loan for my company",
        "tell me about business loan",
        "I want to take a business loan",
        "help me get a business loan",
        "am I eligible for a business loan",
        "what documents are needed for a business loan",
        "loan for my business",
        "loan for my company",
        "I need funds to start a business",
        "I need capital for my business",
        "loan for business expansion",
        "funding for my startup",
        "I want to expand my business",
        "I need working capital",
        "loan to purchase business equipment",
        "loan to open a new shop",
        "small business loan",
        "startup business loan",
        "business loan interest rate",
        "business loan eligibility",
        "business loan repayment options",
        "how can I finance my business",
        "I need money to grow my company",
        "loan for business development",
        "I want funding for my new venture",
        "what is the minimum business loan amount"
    ],

    "car_loan": [
        "need a car loan",
        "apply for a car loan",
        "I want to get a car loan",
        "looking for a car loan",
        "can I get a car loan",
        "I want to buy a new car",
        "I need a loan to purchase a car",
        "loan for buying a used car",
        "I want to finance my car",
        "I need car financing",
        "what are the car loan interest rates",
        "am I eligible for a car loan",
        "what documents are needed for a car loan",
        "I want to take a car loan",
        "help me get a car loan",
        "car loan repayment options",
        "I need a vehicle loan for my car",
        "how can I apply for car finance",
        "I want to buy a second hand car",
        "tell me about car loans"
    ],

    "home_loan": [
        "need a home loan",
        "apply for a home loan",
        "I want to get a home loan",
        "looking for a home loan",
        "can I get a home loan",
        "I want to buy a house",
        "I need a loan to purchase a house",
        "loan for buying a flat",
        "I want to purchase a new apartment",
        "I need financing for a property",
        "what are the home loan interest rates",
        "am I eligible for a home loan",
        "what documents are needed for a home loan",
        "I want to take a home loan",
        "help me get a home loan",
        "home loan repayment options",
        "I need a mortgage loan",
        "loan for construction of a house",
        "I want a loan to renovate my home",
        "tell me about home loans",
        "want home loan",
        "need home loan",
        "home loan",
        "need a loan to buy a house",
        "need money to buy a house",
        "need funds to buy a house",
        "need a loan to purchase a house",
        "need ₹25 lakh to buy a house",
        "loan to buy a house",
        "loan to purchase a house",
        "want to buy a house with a loan",
        "need financing to buy a house",
        "loan to construct my house",
        "loan to construct a house",
        "need a loan to construct my house",
        "want a loan to construct my house",
        "finance to construct a house",
        "loan for house construction",
        "home construction loan",

    ],

    "education_loan": [
        "need an education loan",
        "apply for an education loan",
        "I want to get an education loan",
        "looking for an education loan",
        "can I get an education loan",
        "I need a loan for my college fees",
        "loan for higher studies",
        "I want to study abroad and need a loan",
        "I need financial assistance for my studies",
        "loan for university tuition fees",
        "what are the education loan interest rates",
        "am I eligible for an education loan",
        "what documents are needed for an education loan",
        "I want to take an education loan",
        "help me get an education loan",
        "education loan repayment options",
        "I need funding for my master's degree",
        "loan for engineering studies",
        "loan for medical college admission",
        "tell me about student loans"
    ]

}

def extract_requested_loan_type(text):

    if not isinstance(text, str) or not text.strip():
        return None

    text = re.sub(r"\s+", " ", text.lower().strip())

    loan_patterns = {
        "personal_loan": [
            r"\bpersonal loans?\b",
            r"\bunsecured loans?\b",
            r"\bpersonal expenses\b"
        ],

        "business_loan": [
            r"\bbusiness loans?\b",
            r"\bworking capital\b",
            r"\bcapital for my business\b",
            r"\bexpand my company\b",
            r"\bexpand my business\b",
            r"\bcompany expansion\b",
            r"\bbusiness expansion\b",
            r"\bfunds? to expand\b",
            r"\bcapital for expansion\b",
            r"\bstart a business\b",
            r"\bstartup funding\b"
        ],

        "car_loan": [
            r"\bcar loans?\b",
            r"\bvehicle loans?\b",
            r"\bauto loans?\b",
            r"\bcar financing\b",
            r"\bcar finance\b",
            r"\bbuy (?:a |my )?(?:new |used )?car\b",
            r"\bfinance (?:a |my )?(?:new |used )?car\b",
            r"\bused car financing\b"
        ],

        "home_loan": [
            r"\bhome loans?\b",
            r"\bmortgage loans?\b",
            r"\bhouse loans?\b",
            r"\b(?:construct|build|buy|purchase|renovate)"
            r"\s+(?:a|my|our|the)\s+"
            r"(?:house|home|flat|property)\b",
            r"\b(?:construction|renovation) of "
            r"(?:a|my|our|the)\s+"
            r"(?:house|home|flat|property)\b",
            r"\b(?:buying|building|constructing|renovating)"
            r"\s+(?:a|my|our|the)\s+"
            r"(?:house|home|flat|property)\b",
            r"\bhouse construction\b",
            r"\bhome construction\b",
            r"\bproperty purchase\b"
        ],

        "education_loan": [
            r"\beducation loans?\b",
            r"\bstudent loans?\b",
            r"\bloan for (?:my )?"
            r"(?:college fees|studies|tuition fees)\b",
            r"\bmedical college fees\b",
            r"\bloan for medical college\b",
            r"\bcollege fees\b",
            r"\bengineering college fees\b",
            r"\bmedical studies\b",
            r"\bstudy abroad\b",
            r"\bhigher studies\b"
        ]
    }

    clauses = re.split(
        r"\bbut\b|\bhowever\b|[.!?;]",
        text
    )

    request_pattern = re.compile(
        r"\b(?:want|need|require|"
        r"apply for|looking for|would like|"
        r"prefer|choose|wish to|get|take)\b"
    )

    negation_pattern = re.compile(
        r"\b(?:don't|do not|doesn't|does not|"
        r"didn't|did not|cannot|can't|"
        r"never|no longer|not)\b"
    )

    if re.search(
        r"\b(?:either|or|undecided|not sure|"
        r"cannot decide|can't decide)\b",
        text
    ):
        mentioned_types = {
            loan_type
            for loan_type, patterns in loan_patterns.items()
            if any(re.search(p, text) for p in patterns)
        }

        if len(mentioned_types) > 1:
            return None

    for clause in clauses:

        clause = clause.strip()

        if not clause:
            continue

        for request in request_pattern.finditer(clause):

            prefix = clause[:request.start()]
            requested_part = clause[request.start():]

            if negation_pattern.search(prefix):
                continue

            matches = {
                loan_type
                for loan_type, patterns in loan_patterns.items()
                if any(re.search(p, requested_part) for p in patterns)
            }

            if len(matches) == 1:
                return next(iter(matches))

            if len(matches) > 1:
                return None

        matches = {
            loan_type
            for loan_type, patterns in loan_patterns.items()
            if any(re.search(p, clause) for p in patterns)
        }

        if len(matches) == 1:
            return next(iter(matches))

        if len(matches) > 1:
            return None

    return None

def extract_tenure(text):

    if not isinstance(text, str) or not text.strip():
        return None

    text = re.sub(r"\s+", " ", text.lower().strip())

    patterns = [
        r"\b(?:over|for|within|in|of)\s+(\d+)\s*[- ]?\s*(years?|yrs?|months?|mos?)\b",
        r"\b(\d+)\s*[- ]?\s*(years?|yrs?|months?|mos?)\s+(?:tenure|period)\b",
        r"\btenure\s+(?:of\s+)?(\d+)\s*[- ]?\s*(years?|yrs?|months?|mos?)\b",
        r"\b(\d+)\s*[- ]?\s*(years?|yrs?|months?|mos?)\b"
    ]

    match = None

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            break

    if not match:
        return None

    value = int(match.group(1))
    raw_unit = match.group(2)

    if value <= 0:
        return None

    if raw_unit.startswith(("year", "yr")):
        unit = "years"
        tenure_months = value * 12
    else:
        unit = "months"
        tenure_months = value

    if tenure_months > 480:
        return None

    return {
        "value": value,
        "unit": unit,
        "tenure_months": tenure_months
    }

def extract_interest_rate(text):

    if not isinstance(text, str) or not text.strip():
        return None

    text = text.lower().strip()

    rate_number_pattern = (
        r"(?<![\d.-])"
        r"(?P<rate>\d+(?:\.\d+)?)"
        r"\s*(?:%|percent(?:age)?\b)"
    )

    patterns = [
        re.compile(
            r"\b(?:interest\s+rate|rate\s+of\s+interest|"
            r"loan\s+(?:interest\s+)?rate|"
            r"annual\s+interest(?:\s+rate)?|interest)\b"
            r"[^.!?]{0,40}?"
            + rate_number_pattern
        ),

        re.compile(
            rate_number_pattern
            + r"\s*(?:(?:per\s+annum|p\.?\s*a\.?|"
              r"annual(?:ly)?|yearly)\s*)?"
              r"(?:loan\s+)?interest\b"
        ),

        re.compile(
            r"\brate\b[^.!?]{0,30}?"
            + rate_number_pattern
            + r"[^.!?]{0,15}"
              r"\b(?:per\s+annum|p\.?\s*a\.?|"
              r"annually|annual|yearly|per\s+year)\b"
        )
    ]

    for pattern in patterns:

        match = pattern.search(text)

        if not match:
            continue

        rate = float(match.group("rate"))

        preceding_text = text[:match.start("rate")]

        if re.search(r"-\s*$", preceding_text):
            continue

        context = text[
            max(0, match.start() - 35):
            min(len(text), match.end() + 35)
        ]

        annual_pattern = (
            r"\b(?:per\s+annum|p\.?\s*a\.?|"
            r"annually|annual|yearly|per\s+year)(?!\w)"
        )

        if re.search(annual_pattern, context):
            period = "annual"
        else:
            period = None

        return {
            "value": rate,
            "unit": "%",
            "period": period
        }

    return None

credit_keywords = [
    "cibil score",
    "credit score"
]

def extract_credit_score(text):

    if not isinstance(text, str) or not text.strip():
        return None

    text = text.lower().strip()

    pattern_after = (
        r"\b(?:cibil|credit)\s+score\b"
        r"\s*(?:is|of|:)?\s*"
        r"(?P<score>\d{3})\b"
    )

    pattern_before = (
        r"\b(?P<score>\d{3})\s+"
        r"(?:cibil|credit)\s+score\b"
    )

    match = re.search(pattern_after, text)

    if not match:
        match = re.search(pattern_before, text)

    if not match:
        return None

    score = int(match.group("score"))

    if 300 <= score <= 900:
        return score

    return None

def extract_dependents(text):

    if not isinstance(text, str) or not text.strip():
        return None

    text = text.lower().strip()

    number_words = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20
    }

    count_token = (
        r"\d+|"
        r"zero|one|two|three|four|five|six|seven|eight|nine|"
        r"ten|eleven|twelve|thirteen|fourteen|fifteen|"
        r"sixteen|seventeen|eighteen|nineteen|twenty"
    )

    zero_patterns = [
        r"\b(?:i\s+)?(?:do\s+not|don't|dont)\s+"
        r"have\s+(?:any\s+)?(?:financial\s+)?dependents?\b",

        r"\b(?:i\s+)?have\s+"
        r"(?:no|zero)\s+(?:financial\s+)?dependents?\b",

        r"\b(?:no|zero)\s+(?:financial\s+)?dependents?\b",

        r"\bno\s+one\s+(?:is\s+)?"
        r"(?:financially\s+)?dependent\s+on\s+"
        r"(?:me|my\s+income|my\s+salary)\b"
    ]

    for pattern in zero_patterns:
        if re.search(pattern, text):
            return 0

    patterns = [
        r"\b(?P<count>" + count_token + r")\s+"
        r"(?:(?:financial|family)\s+)?dependents?\b",

        r"\b(?:number\s+of\s+)?dependents?\s*"
        r"(?:is|are|:|=)?\s*"
        r"(?P<count>" + count_token + r")\b",

        r"\b(?P<count>" + count_token + r")\s+"
        r"(?:people|persons|family\s+members)\s+"
        r"(?:are\s+)?(?:financially\s+)?dependent\s+on\s+"
        r"(?:me|my\s+income|my\s+salary)\b",

        r"\b(?:financially\s+)?support\s+"
        r"(?P<count>" + count_token + r")\s+"
        r"(?:people|persons|family\s+members)\b",

        r"\b(?P<count>" + count_token + r")\s+"
        r"children\s+(?:are\s+)?dependent\s+on\s+"
        r"(?:me|my\s+income|my\s+salary)\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if not match:
            continue

        raw_count = match.group("count")

        if raw_count.isdigit():
            count = int(raw_count)
        else:
            count = number_words[raw_count]

        if count < 0:
            return None

        return count

    return None

def extract_existing_loan(text):

    unknown_result = {
        "status": "unknown",
        "active_loan_mentioned": None,
        "closed_loan_mentioned": None,
        "outstanding_amount": None,
        "emi_amount": None
    }

    if not isinstance(text, str) or not text.strip():
        return unknown_result

    text = re.sub(r"\s+", " ", text.lower().strip())

    no_loan_patterns = [
        r"\bno existing loans?\b",
        r"\bno active loans?\b",
        r"\bno current loans?\b",
        r"\bno outstanding loans?\b",
        r"\b(?:i|we) don't have (?:any |an? )?"
        r"(?:existing |active |current )?loans?\b",
        r"\b(?:i|we) do not have (?:any |an? )?"
        r"(?:existing |active |current )?loans?\b",
        r"\bno loans? at all\b"
    ]

    explicitly_none = any(
        re.search(p, text) for p in no_loan_patterns
    )

    closed_patterns = [
        r"\b(?:loan|loans)\b.{0,50}"
        r"\b(?:paid off|fully repaid|closed|settled)\b",
        r"\b(?:paid off|fully repaid|closed|settled)\b.{0,50}"
        r"\b(?:loan|loans)\b"
    ]

    active_patterns = [
        r"\b(?:active|ongoing|outstanding|unpaid)\b.{0,30}\bloan\b",
        r"\b(?:currently paying|paying emi|repaying)\b.{0,50}"
        r"\b(?:loan|emi)\b",
        r"\b(?:have|hold|owe)\b.{0,40}"
        r"\b(?:existing|current|active)\b.{0,20}\bloan\b",
        r"\b(?:have|hold|owe)\b.{0,30}"
        r"\b(?:personal|home|car|education|business)\s+loan\b",
        r"\bmy\s+(?:personal|home|car|education|business)\s+"
        r"loan\s+is\s+active\b"
    ]

    clauses = re.split(r"\bbut\b|[.!?;]", text)
    active = False
    closed = False

    for clause in clauses:
        clause = clause.strip()

        if not clause:
            continue

        denies_loan = bool(re.search(
            r"\b(?:no|don't have|do not have|"
            r"don't owe|do not owe)\b.{0,35}\b"
            r"(?:existing |active |current |outstanding |"
            r"personal |home |car |education |business )?loans?\b",
            clause
        ))

        if not denies_loan and any(
            re.search(p, clause) for p in active_patterns
        ):
            active = True

        if any(re.search(p, clause) for p in closed_patterns):
            closed = True

    if active and closed:
        status = "mixed"
    elif active:
        status = "active"
    elif closed:
        status = "closed"
    elif explicitly_none:
        status = "none"
    else:
        status = "unknown"

    money_pattern = (
        r"(?P<currency>₹|rs\.?|inr|\$|usd)?\s*"
        r"(?P<number>-?\d+(?:,\d{3})*(?:\.\d+)?)\s*"
        r"(?P<unit>lakhs?|lacs?|crores?|k|thousands?|millions?)?"
    )

    outstanding_patterns = [
        r"\b(?:outstanding balance|outstanding amount|"
        r"remaining loan amount|remaining balance|"
        r"loan balance|balance remaining|"
        r"outstanding loan)\b"
        r"\s*(?:is|of|:|=|about|around)?\s*"
        + money_pattern
    ]

    emi_patterns = [
        r"\b(?:monthly emi|emi amount|loan emi|"
        r"emi|monthly instalment|monthly installment)\b"
        r"\s*(?:is|of|:|=|about|around)?\s*"
        + money_pattern
    ]

    def find_amount(patterns):
        for pattern in patterns:
            match = re.search(pattern, text)

            if match:
                amount = normalize_money_value(
                    match.groupdict()
                )

                if amount is not None and amount > 0:
                    return amount

        return None

    outstanding_amount = find_amount(outstanding_patterns)
    emi_amount = find_amount(emi_patterns)

    return {
        "status": status,
        "active_loan_mentioned": (
            True if active else False if explicitly_none else None
        ),
        "closed_loan_mentioned": True if closed else None,
        "outstanding_amount": outstanding_amount,
        "emi_amount": emi_amount
    }

def extract_entities(text):

    if not isinstance(text, str) or not text.strip():
        return {
            "income": None,
            "income_frequency": None,
            "loan_amount": None,
            "loan_type": None,
            "tenure": None,
            "interest_rate": None,
            "credit_score": None,
            "dependents": None,
            "existing_loan": {
                "status": "unknown",
                "active_loan_mentioned": None,
                "closed_loan_mentioned": None
            }
        }

    income_result = extract_income(text)

    if isinstance(income_result, dict):
        income = income_result.get("income")
        income_frequency = income_result.get("frequency")
    else:
        income = income_result
        income_frequency = detect_income_frequency(text)

    applicant_data = {
        "income": income,
        "income_frequency": income_frequency,
        "loan_amount": extract_loan_amount(text),
        "loan_type": extract_requested_loan_type(text),
        "tenure": extract_tenure(text),
        "interest_rate": extract_interest_rate(text),
        "credit_score": extract_credit_score(text),
        "dependents": extract_dependents(text),
        "existing_loan": extract_existing_loan(text)
    }

    return applicant_data
