import re


#
# Extremely small initial policy.
# Later this will become configurable.
#

BLOCKED_PATTERNS = {

    #
    # Prompt Injection
    #

    "PROMPT_INJECTION": [

        r"ignore\s+previous\s+instructions",

        r"ignore\s+all\s+instructions",

        r"system\s+prompt",

        r"developer\s+prompt",

        r"reveal\s+your\s+prompt",

        r"show\s+your\s+prompt",

        r"print\s+your\s+prompt",

        r"bypass",

        r"jailbreak"

    ],

    #
    # Violence
    #

    "VIOLENCE": [

        r"\bkill\b",

        r"\bmurder\b",

        r"\bterror\b",

        r"\bbomb\b"

    ],

    #
    # Hate
    #

    "HATE": [

        r"\brace\b",

        r"\bnazi\b"

    ],

    #
    # Sexual
    #

    "SEXUAL": [

        r"\bsex\b",

        r"\bporn\b",

        r"\bnude\b"

    ]

}