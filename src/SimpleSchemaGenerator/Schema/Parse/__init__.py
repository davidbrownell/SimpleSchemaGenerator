# ----------------------------------------------------------------------
# |
# |  __init__.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-05-28 06:58:37
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Functionality common to Parse modules"""

# ----------------------------------------------------------------------
# Include a couple of characters within the name that can'be be replicated
# when files are parsed (as they aren't supported by the grammar). Doing this
# should eliminate the chance that someone will accidentally name an element
# this themselves.
PSEUDO_TYPE_NAME_PREFIX = "_PseudoType#^"
