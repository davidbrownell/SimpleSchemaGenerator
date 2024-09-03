# ----------------------------------------------------------------------
# |
# |  Common.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-08-23 10:10:27
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Common functionality shared by multiple stages of the parsing process."""

# ----------------------------------------------------------------------
# Include a couple of characters within the name that can'be be replicated
# when files are parsed (as they aren't supported). This should eliminate
# the chance that someone will accidentally name an element this themselves.
PSEUDO_TYPE_NAME_PREFIX = "_PseudoType#^"
