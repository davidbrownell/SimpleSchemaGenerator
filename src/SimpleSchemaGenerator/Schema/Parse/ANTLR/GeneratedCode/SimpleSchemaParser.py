# Generated from C:/Code/GitHub/davidbrownell/SimpleSchemaGenerator/src/SimpleSchemaGenerator/Schema/Parse/ANTLR/Grammar/SimpleSchema.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,64,480,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,2,46,
        7,46,2,47,7,47,1,0,5,0,98,8,0,10,0,12,0,101,9,0,1,0,5,0,104,8,0,
        10,0,12,0,107,9,0,1,0,5,0,110,8,0,10,0,12,0,113,9,0,1,0,1,0,1,1,
        1,1,1,2,1,2,1,2,3,2,122,8,2,1,2,1,2,1,3,1,3,1,3,1,3,5,3,130,8,3,
        10,3,12,3,133,9,3,1,3,3,3,136,8,3,3,3,138,8,3,1,4,1,4,1,4,4,4,143,
        8,4,11,4,12,4,144,1,4,1,4,3,4,149,8,4,1,4,4,4,152,8,4,11,4,12,4,
        153,4,4,156,8,4,11,4,12,4,157,3,4,160,8,4,1,4,1,4,1,5,1,5,1,5,1,
        5,1,6,1,6,1,6,1,6,1,6,3,6,173,8,6,1,7,1,7,1,8,1,8,1,9,1,9,1,10,1,
        10,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,11,1,12,1,12,1,12,1,12,1,
        12,1,12,1,12,1,12,3,12,199,8,12,1,13,1,13,1,14,1,14,1,15,1,15,1,
        16,1,16,1,17,1,17,1,18,1,18,1,19,1,19,1,19,1,19,5,19,217,8,19,10,
        19,12,19,220,9,19,1,19,3,19,223,8,19,3,19,225,8,19,1,19,1,19,1,20,
        1,20,1,20,3,20,232,8,20,1,20,1,20,1,21,1,21,1,21,1,22,1,22,1,22,
        4,22,242,8,22,11,22,12,22,243,1,22,3,22,247,8,22,1,23,1,23,1,24,
        1,24,1,24,1,24,1,24,4,24,256,8,24,11,24,12,24,257,1,25,3,25,261,
        8,25,1,25,1,25,1,25,3,25,266,8,25,1,25,3,25,269,8,25,4,25,271,8,
        25,11,25,12,25,272,1,26,1,26,1,26,3,26,278,8,26,1,27,1,27,1,28,1,
        28,1,28,1,28,1,29,1,29,1,29,5,29,289,8,29,10,29,12,29,292,9,29,1,
        29,3,29,295,8,29,1,30,1,30,1,30,3,30,300,8,30,1,31,1,31,1,31,1,31,
        3,31,306,8,31,1,32,1,32,1,32,1,32,1,32,1,32,1,32,1,32,3,32,316,8,
        32,1,32,3,32,319,8,32,3,32,321,8,32,1,32,1,32,4,32,325,8,32,11,32,
        12,32,326,1,33,1,33,1,33,5,33,332,8,33,10,33,12,33,335,9,33,1,34,
        1,34,1,34,5,34,340,8,34,10,34,12,34,343,9,34,1,35,1,35,1,35,1,35,
        1,36,1,36,1,36,1,36,4,36,353,8,36,11,36,12,36,354,1,37,1,37,1,37,
        1,37,3,37,361,8,37,3,37,363,8,37,1,37,1,37,1,37,1,37,4,37,369,8,
        37,11,37,12,37,370,1,37,4,37,374,8,37,11,37,12,37,375,3,37,378,8,
        37,1,37,1,37,1,37,5,37,383,8,37,10,37,12,37,386,9,37,1,37,1,37,1,
        37,1,37,3,37,392,8,37,1,37,4,37,395,8,37,11,37,12,37,396,3,37,399,
        8,37,1,38,1,38,1,38,5,38,404,8,38,10,38,12,38,407,9,38,1,38,3,38,
        410,8,38,1,39,1,39,1,39,1,39,1,40,1,40,1,40,4,40,419,8,40,11,40,
        12,40,420,1,41,1,41,1,41,3,41,426,8,41,1,41,3,41,429,8,41,1,41,3,
        41,432,8,41,1,42,3,42,435,8,42,1,42,1,42,1,42,5,42,440,8,42,10,42,
        12,42,443,9,42,1,43,1,43,1,44,1,44,1,44,1,44,5,44,451,8,44,10,44,
        12,44,454,9,44,1,44,1,44,1,44,1,44,1,45,1,45,1,45,3,45,463,8,45,
        1,45,1,45,1,46,1,46,1,46,1,47,1,47,1,47,4,47,473,8,47,11,47,12,47,
        474,1,47,3,47,478,8,47,1,47,0,0,48,0,2,4,6,8,10,12,14,16,18,20,22,
        24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,
        68,70,72,74,76,78,80,82,84,86,88,90,92,94,0,3,1,0,10,20,1,0,21,31,
        4,0,55,55,57,57,59,59,61,61,505,0,99,1,0,0,0,2,116,1,0,0,0,4,118,
        1,0,0,0,6,137,1,0,0,0,8,139,1,0,0,0,10,163,1,0,0,0,12,172,1,0,0,
        0,14,174,1,0,0,0,16,176,1,0,0,0,18,178,1,0,0,0,20,180,1,0,0,0,22,
        184,1,0,0,0,24,198,1,0,0,0,26,200,1,0,0,0,28,202,1,0,0,0,30,204,
        1,0,0,0,32,206,1,0,0,0,34,208,1,0,0,0,36,210,1,0,0,0,38,212,1,0,
        0,0,40,228,1,0,0,0,42,235,1,0,0,0,44,238,1,0,0,0,46,248,1,0,0,0,
        48,250,1,0,0,0,50,260,1,0,0,0,52,277,1,0,0,0,54,279,1,0,0,0,56,281,
        1,0,0,0,58,285,1,0,0,0,60,296,1,0,0,0,62,305,1,0,0,0,64,307,1,0,
        0,0,66,328,1,0,0,0,68,336,1,0,0,0,70,344,1,0,0,0,72,348,1,0,0,0,
        74,356,1,0,0,0,76,400,1,0,0,0,78,411,1,0,0,0,80,415,1,0,0,0,82,425,
        1,0,0,0,84,434,1,0,0,0,86,444,1,0,0,0,88,446,1,0,0,0,90,459,1,0,
        0,0,92,466,1,0,0,0,94,469,1,0,0,0,96,98,5,40,0,0,97,96,1,0,0,0,98,
        101,1,0,0,0,99,97,1,0,0,0,99,100,1,0,0,0,100,105,1,0,0,0,101,99,
        1,0,0,0,102,104,3,46,23,0,103,102,1,0,0,0,104,107,1,0,0,0,105,103,
        1,0,0,0,105,106,1,0,0,0,106,111,1,0,0,0,107,105,1,0,0,0,108,110,
        3,62,31,0,109,108,1,0,0,0,110,113,1,0,0,0,111,109,1,0,0,0,111,112,
        1,0,0,0,112,114,1,0,0,0,113,111,1,0,0,0,114,115,5,0,0,1,115,1,1,
        0,0,0,116,117,5,54,0,0,117,3,1,0,0,0,118,121,5,1,0,0,119,122,3,6,
        3,0,120,122,3,8,4,0,121,119,1,0,0,0,121,120,1,0,0,0,122,123,1,0,
        0,0,123,124,5,2,0,0,124,5,1,0,0,0,125,138,5,3,0,0,126,131,3,10,5,
        0,127,128,5,4,0,0,128,130,3,10,5,0,129,127,1,0,0,0,130,133,1,0,0,
        0,131,129,1,0,0,0,131,132,1,0,0,0,132,135,1,0,0,0,133,131,1,0,0,
        0,134,136,5,4,0,0,135,134,1,0,0,0,135,136,1,0,0,0,136,138,1,0,0,
        0,137,125,1,0,0,0,137,126,1,0,0,0,138,7,1,0,0,0,139,159,5,63,0,0,
        140,142,5,3,0,0,141,143,5,40,0,0,142,141,1,0,0,0,143,144,1,0,0,0,
        144,142,1,0,0,0,144,145,1,0,0,0,145,160,1,0,0,0,146,148,3,10,5,0,
        147,149,5,4,0,0,148,147,1,0,0,0,148,149,1,0,0,0,149,151,1,0,0,0,
        150,152,5,40,0,0,151,150,1,0,0,0,152,153,1,0,0,0,153,151,1,0,0,0,
        153,154,1,0,0,0,154,156,1,0,0,0,155,146,1,0,0,0,156,157,1,0,0,0,
        157,155,1,0,0,0,157,158,1,0,0,0,158,160,1,0,0,0,159,140,1,0,0,0,
        159,155,1,0,0,0,160,161,1,0,0,0,161,162,5,64,0,0,162,9,1,0,0,0,163,
        164,3,2,1,0,164,165,5,5,0,0,165,166,3,24,12,0,166,11,1,0,0,0,167,
        173,3,14,7,0,168,173,3,16,8,0,169,173,3,18,9,0,170,173,3,20,10,0,
        171,173,3,22,11,0,172,167,1,0,0,0,172,168,1,0,0,0,172,169,1,0,0,
        0,172,170,1,0,0,0,172,171,1,0,0,0,173,13,1,0,0,0,174,175,5,6,0,0,
        175,15,1,0,0,0,176,177,5,7,0,0,177,17,1,0,0,0,178,179,5,8,0,0,179,
        19,1,0,0,0,180,181,5,45,0,0,181,182,3,28,14,0,182,183,5,46,0,0,183,
        21,1,0,0,0,184,185,5,45,0,0,185,186,3,28,14,0,186,187,5,9,0,0,187,
        188,3,28,14,0,188,189,5,46,0,0,189,23,1,0,0,0,190,199,3,26,13,0,
        191,199,3,28,14,0,192,199,3,30,15,0,193,199,3,32,16,0,194,199,3,
        34,17,0,195,199,3,36,18,0,196,199,3,38,19,0,197,199,3,40,20,0,198,
        190,1,0,0,0,198,191,1,0,0,0,198,192,1,0,0,0,198,193,1,0,0,0,198,
        194,1,0,0,0,198,195,1,0,0,0,198,196,1,0,0,0,198,197,1,0,0,0,199,
        25,1,0,0,0,200,201,5,52,0,0,201,27,1,0,0,0,202,203,5,53,0,0,203,
        29,1,0,0,0,204,205,7,0,0,0,205,31,1,0,0,0,206,207,7,1,0,0,207,33,
        1,0,0,0,208,209,5,32,0,0,209,35,1,0,0,0,210,211,7,2,0,0,211,37,1,
        0,0,0,212,224,5,45,0,0,213,218,3,24,12,0,214,215,5,4,0,0,215,217,
        3,24,12,0,216,214,1,0,0,0,217,220,1,0,0,0,218,216,1,0,0,0,218,219,
        1,0,0,0,219,222,1,0,0,0,220,218,1,0,0,0,221,223,5,4,0,0,222,221,
        1,0,0,0,222,223,1,0,0,0,223,225,1,0,0,0,224,213,1,0,0,0,224,225,
        1,0,0,0,225,226,1,0,0,0,226,227,5,46,0,0,227,39,1,0,0,0,228,231,
        5,43,0,0,229,232,3,42,21,0,230,232,3,44,22,0,231,229,1,0,0,0,231,
        230,1,0,0,0,232,233,1,0,0,0,233,234,5,44,0,0,234,41,1,0,0,0,235,
        236,3,24,12,0,236,237,5,4,0,0,237,43,1,0,0,0,238,241,3,24,12,0,239,
        240,5,4,0,0,240,242,3,24,12,0,241,239,1,0,0,0,242,243,1,0,0,0,243,
        241,1,0,0,0,243,244,1,0,0,0,244,246,1,0,0,0,245,247,5,4,0,0,246,
        245,1,0,0,0,246,247,1,0,0,0,247,45,1,0,0,0,248,249,3,48,24,0,249,
        47,1,0,0,0,250,251,5,47,0,0,251,252,3,50,25,0,252,253,5,48,0,0,253,
        255,3,52,26,0,254,256,5,40,0,0,255,254,1,0,0,0,256,257,1,0,0,0,257,
        255,1,0,0,0,257,258,1,0,0,0,258,49,1,0,0,0,259,261,5,33,0,0,260,
        259,1,0,0,0,260,261,1,0,0,0,261,270,1,0,0,0,262,266,3,2,1,0,263,
        266,5,9,0,0,264,266,5,34,0,0,265,262,1,0,0,0,265,263,1,0,0,0,265,
        264,1,0,0,0,266,268,1,0,0,0,267,269,5,33,0,0,268,267,1,0,0,0,268,
        269,1,0,0,0,269,271,1,0,0,0,270,265,1,0,0,0,271,272,1,0,0,0,272,
        270,1,0,0,0,272,273,1,0,0,0,273,51,1,0,0,0,274,278,3,54,27,0,275,
        278,3,56,28,0,276,278,3,58,29,0,277,274,1,0,0,0,277,275,1,0,0,0,
        277,276,1,0,0,0,278,53,1,0,0,0,279,280,5,7,0,0,280,55,1,0,0,0,281,
        282,5,43,0,0,282,283,3,58,29,0,283,284,5,44,0,0,284,57,1,0,0,0,285,
        290,3,60,30,0,286,287,5,4,0,0,287,289,3,60,30,0,288,286,1,0,0,0,
        289,292,1,0,0,0,290,288,1,0,0,0,290,291,1,0,0,0,291,294,1,0,0,0,
        292,290,1,0,0,0,293,295,5,4,0,0,294,293,1,0,0,0,294,295,1,0,0,0,
        295,59,1,0,0,0,296,299,3,2,1,0,297,298,5,35,0,0,298,300,3,2,1,0,
        299,297,1,0,0,0,299,300,1,0,0,0,300,61,1,0,0,0,301,306,3,74,37,0,
        302,306,3,80,40,0,303,306,3,72,36,0,304,306,3,64,32,0,305,301,1,
        0,0,0,305,302,1,0,0,0,305,303,1,0,0,0,305,304,1,0,0,0,306,63,1,0,
        0,0,307,308,3,2,1,0,308,320,5,43,0,0,309,310,3,66,33,0,310,311,5,
        4,0,0,311,312,3,68,34,0,312,316,1,0,0,0,313,316,3,66,33,0,314,316,
        3,68,34,0,315,309,1,0,0,0,315,313,1,0,0,0,315,314,1,0,0,0,316,318,
        1,0,0,0,317,319,5,4,0,0,318,317,1,0,0,0,318,319,1,0,0,0,319,321,
        1,0,0,0,320,315,1,0,0,0,320,321,1,0,0,0,321,322,1,0,0,0,322,324,
        5,44,0,0,323,325,5,40,0,0,324,323,1,0,0,0,325,326,1,0,0,0,326,324,
        1,0,0,0,326,327,1,0,0,0,327,65,1,0,0,0,328,333,3,24,12,0,329,330,
        5,4,0,0,330,332,3,24,12,0,331,329,1,0,0,0,332,335,1,0,0,0,333,331,
        1,0,0,0,333,334,1,0,0,0,334,67,1,0,0,0,335,333,1,0,0,0,336,341,3,
        70,35,0,337,338,5,4,0,0,338,340,3,70,35,0,339,337,1,0,0,0,340,343,
        1,0,0,0,341,339,1,0,0,0,341,342,1,0,0,0,342,69,1,0,0,0,343,341,1,
        0,0,0,344,345,3,2,1,0,345,346,5,36,0,0,346,347,3,24,12,0,347,71,
        1,0,0,0,348,349,3,2,1,0,349,350,5,5,0,0,350,352,3,82,41,0,351,353,
        5,40,0,0,352,351,1,0,0,0,353,354,1,0,0,0,354,352,1,0,0,0,354,355,
        1,0,0,0,355,73,1,0,0,0,356,362,3,2,1,0,357,360,5,5,0,0,358,361,3,
        78,39,0,359,361,3,76,38,0,360,358,1,0,0,0,360,359,1,0,0,0,361,363,
        1,0,0,0,362,357,1,0,0,0,362,363,1,0,0,0,363,364,1,0,0,0,364,365,
        5,37,0,0,365,377,5,63,0,0,366,368,5,3,0,0,367,369,5,40,0,0,368,367,
        1,0,0,0,369,370,1,0,0,0,370,368,1,0,0,0,370,371,1,0,0,0,371,378,
        1,0,0,0,372,374,3,62,31,0,373,372,1,0,0,0,374,375,1,0,0,0,375,373,
        1,0,0,0,375,376,1,0,0,0,376,378,1,0,0,0,377,366,1,0,0,0,377,373,
        1,0,0,0,378,379,1,0,0,0,379,398,5,64,0,0,380,384,3,12,6,0,381,383,
        5,40,0,0,382,381,1,0,0,0,383,386,1,0,0,0,384,382,1,0,0,0,384,385,
        1,0,0,0,385,387,1,0,0,0,386,384,1,0,0,0,387,388,3,4,2,0,388,392,
        1,0,0,0,389,392,3,4,2,0,390,392,3,12,6,0,391,380,1,0,0,0,391,389,
        1,0,0,0,391,390,1,0,0,0,392,394,1,0,0,0,393,395,5,40,0,0,394,393,
        1,0,0,0,395,396,1,0,0,0,396,394,1,0,0,0,396,397,1,0,0,0,397,399,
        1,0,0,0,398,391,1,0,0,0,398,399,1,0,0,0,399,75,1,0,0,0,400,405,3,
        82,41,0,401,402,5,4,0,0,402,404,3,82,41,0,403,401,1,0,0,0,404,407,
        1,0,0,0,405,403,1,0,0,0,405,406,1,0,0,0,406,409,1,0,0,0,407,405,
        1,0,0,0,408,410,5,4,0,0,409,408,1,0,0,0,409,410,1,0,0,0,410,77,1,
        0,0,0,411,412,5,43,0,0,412,413,3,76,38,0,413,414,5,44,0,0,414,79,
        1,0,0,0,415,416,3,2,1,0,416,418,3,4,2,0,417,419,5,40,0,0,418,417,
        1,0,0,0,419,420,1,0,0,0,420,418,1,0,0,0,420,421,1,0,0,0,421,81,1,
        0,0,0,422,426,3,90,45,0,423,426,3,88,44,0,424,426,3,84,42,0,425,
        422,1,0,0,0,425,423,1,0,0,0,425,424,1,0,0,0,426,428,1,0,0,0,427,
        429,3,12,6,0,428,427,1,0,0,0,428,429,1,0,0,0,429,431,1,0,0,0,430,
        432,3,4,2,0,431,430,1,0,0,0,431,432,1,0,0,0,432,83,1,0,0,0,433,435,
        3,86,43,0,434,433,1,0,0,0,434,435,1,0,0,0,435,436,1,0,0,0,436,441,
        3,2,1,0,437,438,5,34,0,0,438,440,3,2,1,0,439,437,1,0,0,0,440,443,
        1,0,0,0,441,439,1,0,0,0,441,442,1,0,0,0,442,85,1,0,0,0,443,441,1,
        0,0,0,444,445,5,38,0,0,445,87,1,0,0,0,446,447,5,43,0,0,447,452,3,
        82,41,0,448,449,5,39,0,0,449,451,3,82,41,0,450,448,1,0,0,0,451,454,
        1,0,0,0,452,450,1,0,0,0,452,453,1,0,0,0,453,455,1,0,0,0,454,452,
        1,0,0,0,455,456,5,39,0,0,456,457,3,82,41,0,457,458,5,44,0,0,458,
        89,1,0,0,0,459,462,5,43,0,0,460,463,3,92,46,0,461,463,3,94,47,0,
        462,460,1,0,0,0,462,461,1,0,0,0,463,464,1,0,0,0,464,465,5,44,0,0,
        465,91,1,0,0,0,466,467,3,82,41,0,467,468,5,4,0,0,468,93,1,0,0,0,
        469,472,3,82,41,0,470,471,5,4,0,0,471,473,3,82,41,0,472,470,1,0,
        0,0,473,474,1,0,0,0,474,472,1,0,0,0,474,475,1,0,0,0,475,477,1,0,
        0,0,476,478,5,4,0,0,477,476,1,0,0,0,477,478,1,0,0,0,478,95,1,0,0,
        0,58,99,105,111,121,131,135,137,144,148,153,157,159,172,198,218,
        222,224,231,243,246,257,260,265,268,272,277,290,294,299,305,315,
        318,320,326,333,341,354,360,362,370,375,377,384,391,396,398,405,
        409,420,425,428,431,434,441,452,462,474,477
    ]

class SimpleSchemaParser ( Parser ):

    grammarFileName = "SimpleSchema.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "'}'", "'pass'", "','", "':'", 
                     "'?'", "'*'", "'+'", "'..'", "'y'", "'Y'", "'yes'", 
                     "'Yes'", "'YES'", "'true'", "'True'", "'TRUE'", "'on'", 
                     "'On'", "'ON'", "'n'", "'N'", "'no'", "'No'", "'NO'", 
                     "'false'", "'False'", "'FALSE'", "'off'", "'Off'", 
                     "'OFF'", "'None'", "'/'", "'.'", "'as'", "'='", "'->'", 
                     "'::'", "'|'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'('", "')'", "'['", "']'", "'from'", "'import'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "NEWLINE", "NESTED_NEWLINE", "LINE_CONTINUATION", 
                      "LPAREN", "RPAREN", "LBRACK", "RBRACK", "INCLUDE_FROM", 
                      "INCLUDE_IMPORT", "MULTI_LINE_COMMENT", "SINGLE_LINE_COMMENT", 
                      "HORIZONTAL_WHITESPACE", "NUMBER", "INTEGER", "IDENTIFIER", 
                      "DOUBLE_QUOTE_STRING", "UNTERMINATED_DOUBLE_QUOTE_STRING", 
                      "SINGLE_QUOTE_STRING", "UNTERMINATED_SINGLE_QUOTE_STRING", 
                      "TRIPLE_DOUBLE_QUOTE_STRING", "UNTERMINATED_TRIPLE_DOUBLE_QUOTE_STRING", 
                      "TRIPLE_SINGLE_QUOTE_STRING", "UNTERMINATED_TRIPLE_SINGLE_QUOTE_STRING", 
                      "INDENT", "DEDENT" ]

    RULE_entry_point__ = 0
    RULE_identifier = 1
    RULE_metadata_clause = 2
    RULE_metadata_clause_single_line__ = 3
    RULE_metadata_clause_multi_line__ = 4
    RULE_metadata_clause_item = 5
    RULE_cardinality_clause = 6
    RULE_cardinality_clause_optional = 7
    RULE_cardinality_clause_zero_or_more = 8
    RULE_cardinality_clause_one_or_more = 9
    RULE_cardinality_clause_fixed = 10
    RULE_cardinality_clause_range__ = 11
    RULE_expression__ = 12
    RULE_number_expression = 13
    RULE_integer_expression = 14
    RULE_true_expression = 15
    RULE_false_expression = 16
    RULE_none_expression = 17
    RULE_string_expression = 18
    RULE_list_expression = 19
    RULE_tuple_expression = 20
    RULE_tuple_expression_single_item__ = 21
    RULE_tuple_expression_multi_item__ = 22
    RULE_header_statement__ = 23
    RULE_include_statement = 24
    RULE_include_statement_from = 25
    RULE_include_statement_import__ = 26
    RULE_include_statement_import_star = 27
    RULE_include_statement_import_grouped_items__ = 28
    RULE_include_statement_import_items__ = 29
    RULE_include_statement_import_element = 30
    RULE_body_statement__ = 31
    RULE_extension_statement = 32
    RULE_extension_statement_positional_args = 33
    RULE_extension_statement_keyword_args = 34
    RULE_extension_statement_keyword_arg = 35
    RULE_parse_item_statement = 36
    RULE_parse_structure_statement = 37
    RULE_parse_structure_statement_base_items__ = 38
    RULE_parse_structure_statement_base_grouped_items__ = 39
    RULE_parse_structure_simplified_statement = 40
    RULE_parse_type = 41
    RULE_parse_identifier_type = 42
    RULE_parse_identifier_type_global = 43
    RULE_parse_variant_type = 44
    RULE_parse_tuple_type = 45
    RULE_parse_tuple_type_single_item__ = 46
    RULE_parse_tuple_type_multi_item__ = 47

    ruleNames =  [ "entry_point__", "identifier", "metadata_clause", "metadata_clause_single_line__", 
                   "metadata_clause_multi_line__", "metadata_clause_item", 
                   "cardinality_clause", "cardinality_clause_optional", 
                   "cardinality_clause_zero_or_more", "cardinality_clause_one_or_more", 
                   "cardinality_clause_fixed", "cardinality_clause_range__", 
                   "expression__", "number_expression", "integer_expression", 
                   "true_expression", "false_expression", "none_expression", 
                   "string_expression", "list_expression", "tuple_expression", 
                   "tuple_expression_single_item__", "tuple_expression_multi_item__", 
                   "header_statement__", "include_statement", "include_statement_from", 
                   "include_statement_import__", "include_statement_import_star", 
                   "include_statement_import_grouped_items__", "include_statement_import_items__", 
                   "include_statement_import_element", "body_statement__", 
                   "extension_statement", "extension_statement_positional_args", 
                   "extension_statement_keyword_args", "extension_statement_keyword_arg", 
                   "parse_item_statement", "parse_structure_statement", 
                   "parse_structure_statement_base_items__", "parse_structure_statement_base_grouped_items__", 
                   "parse_structure_simplified_statement", "parse_type", 
                   "parse_identifier_type", "parse_identifier_type_global", 
                   "parse_variant_type", "parse_tuple_type", "parse_tuple_type_single_item__", 
                   "parse_tuple_type_multi_item__" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    T__32=33
    T__33=34
    T__34=35
    T__35=36
    T__36=37
    T__37=38
    T__38=39
    NEWLINE=40
    NESTED_NEWLINE=41
    LINE_CONTINUATION=42
    LPAREN=43
    RPAREN=44
    LBRACK=45
    RBRACK=46
    INCLUDE_FROM=47
    INCLUDE_IMPORT=48
    MULTI_LINE_COMMENT=49
    SINGLE_LINE_COMMENT=50
    HORIZONTAL_WHITESPACE=51
    NUMBER=52
    INTEGER=53
    IDENTIFIER=54
    DOUBLE_QUOTE_STRING=55
    UNTERMINATED_DOUBLE_QUOTE_STRING=56
    SINGLE_QUOTE_STRING=57
    UNTERMINATED_SINGLE_QUOTE_STRING=58
    TRIPLE_DOUBLE_QUOTE_STRING=59
    UNTERMINATED_TRIPLE_DOUBLE_QUOTE_STRING=60
    TRIPLE_SINGLE_QUOTE_STRING=61
    UNTERMINATED_TRIPLE_SINGLE_QUOTE_STRING=62
    INDENT=63
    DEDENT=64

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Entry_point__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(SimpleSchemaParser.EOF, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSchemaParser.NEWLINE)
            else:
                return self.getToken(SimpleSchemaParser.NEWLINE, i)

        def header_statement__(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Header_statement__Context)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Header_statement__Context,i)


        def body_statement__(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Body_statement__Context)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Body_statement__Context,i)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_entry_point__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEntry_point__" ):
                return visitor.visitEntry_point__(self)
            else:
                return visitor.visitChildren(self)




    def entry_point__(self):

        localctx = SimpleSchemaParser.Entry_point__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_entry_point__)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 96
                self.match(SimpleSchemaParser.NEWLINE)
                self.state = 101
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 105
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==47:
                self.state = 102
                self.header_statement__()
                self.state = 107
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 111
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==54:
                self.state = 108
                self.body_statement__()
                self.state = 113
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 114
            self.match(SimpleSchemaParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdentifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(SimpleSchemaParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_identifier

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentifier" ):
                return visitor.visitIdentifier(self)
            else:
                return visitor.visitChildren(self)




    def identifier(self):

        localctx = SimpleSchemaParser.IdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_identifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            self.match(SimpleSchemaParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Metadata_clauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def metadata_clause_single_line__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Metadata_clause_single_line__Context,0)


        def metadata_clause_multi_line__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Metadata_clause_multi_line__Context,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_metadata_clause

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMetadata_clause" ):
                return visitor.visitMetadata_clause(self)
            else:
                return visitor.visitChildren(self)




    def metadata_clause(self):

        localctx = SimpleSchemaParser.Metadata_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_metadata_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.match(SimpleSchemaParser.T__0)
            self.state = 121
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3, 54]:
                self.state = 119
                self.metadata_clause_single_line__()
                pass
            elif token in [63]:
                self.state = 120
                self.metadata_clause_multi_line__()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 123
            self.match(SimpleSchemaParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Metadata_clause_single_line__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def metadata_clause_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Metadata_clause_itemContext)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Metadata_clause_itemContext,i)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_metadata_clause_single_line__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMetadata_clause_single_line__" ):
                return visitor.visitMetadata_clause_single_line__(self)
            else:
                return visitor.visitChildren(self)




    def metadata_clause_single_line__(self):

        localctx = SimpleSchemaParser.Metadata_clause_single_line__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_metadata_clause_single_line__)
        self._la = 0 # Token type
        try:
            self.state = 137
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.enterOuterAlt(localctx, 1)
                self.state = 125
                self.match(SimpleSchemaParser.T__2)
                pass
            elif token in [54]:
                self.enterOuterAlt(localctx, 2)
                self.state = 126
                self.metadata_clause_item()
                self.state = 131
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 127
                        self.match(SimpleSchemaParser.T__3)
                        self.state = 128
                        self.metadata_clause_item() 
                    self.state = 133
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

                self.state = 135
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==4:
                    self.state = 134
                    self.match(SimpleSchemaParser.T__3)


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Metadata_clause_multi_line__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INDENT(self):
            return self.getToken(SimpleSchemaParser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(SimpleSchemaParser.DEDENT, 0)

        def metadata_clause_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Metadata_clause_itemContext)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Metadata_clause_itemContext,i)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSchemaParser.NEWLINE)
            else:
                return self.getToken(SimpleSchemaParser.NEWLINE, i)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_metadata_clause_multi_line__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMetadata_clause_multi_line__" ):
                return visitor.visitMetadata_clause_multi_line__(self)
            else:
                return visitor.visitChildren(self)




    def metadata_clause_multi_line__(self):

        localctx = SimpleSchemaParser.Metadata_clause_multi_line__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_metadata_clause_multi_line__)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            self.match(SimpleSchemaParser.INDENT)
            self.state = 159
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.state = 140
                self.match(SimpleSchemaParser.T__2)
                self.state = 142 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 141
                    self.match(SimpleSchemaParser.NEWLINE)
                    self.state = 144 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==40):
                        break

                pass
            elif token in [54]:
                self.state = 155 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 146
                    self.metadata_clause_item()
                    self.state = 148
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==4:
                        self.state = 147
                        self.match(SimpleSchemaParser.T__3)


                    self.state = 151 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while True:
                        self.state = 150
                        self.match(SimpleSchemaParser.NEWLINE)
                        self.state = 153 
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if not (_la==40):
                            break

                    self.state = 157 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==54):
                        break

                pass
            else:
                raise NoViableAltException(self)

            self.state = 161
            self.match(SimpleSchemaParser.DEDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Metadata_clause_itemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(SimpleSchemaParser.IdentifierContext,0)


        def expression__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Expression__Context,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_metadata_clause_item

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMetadata_clause_item" ):
                return visitor.visitMetadata_clause_item(self)
            else:
                return visitor.visitChildren(self)




    def metadata_clause_item(self):

        localctx = SimpleSchemaParser.Metadata_clause_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_metadata_clause_item)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 163
            self.identifier()
            self.state = 164
            self.match(SimpleSchemaParser.T__4)
            self.state = 165
            self.expression__()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Cardinality_clauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def cardinality_clause_optional(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Cardinality_clause_optionalContext,0)


        def cardinality_clause_zero_or_more(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Cardinality_clause_zero_or_moreContext,0)


        def cardinality_clause_one_or_more(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Cardinality_clause_one_or_moreContext,0)


        def cardinality_clause_fixed(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Cardinality_clause_fixedContext,0)


        def cardinality_clause_range__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Cardinality_clause_range__Context,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_cardinality_clause

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCardinality_clause" ):
                return visitor.visitCardinality_clause(self)
            else:
                return visitor.visitChildren(self)




    def cardinality_clause(self):

        localctx = SimpleSchemaParser.Cardinality_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_cardinality_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 172
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                self.state = 167
                self.cardinality_clause_optional()
                pass

            elif la_ == 2:
                self.state = 168
                self.cardinality_clause_zero_or_more()
                pass

            elif la_ == 3:
                self.state = 169
                self.cardinality_clause_one_or_more()
                pass

            elif la_ == 4:
                self.state = 170
                self.cardinality_clause_fixed()
                pass

            elif la_ == 5:
                self.state = 171
                self.cardinality_clause_range__()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Cardinality_clause_optionalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_cardinality_clause_optional

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCardinality_clause_optional" ):
                return visitor.visitCardinality_clause_optional(self)
            else:
                return visitor.visitChildren(self)




    def cardinality_clause_optional(self):

        localctx = SimpleSchemaParser.Cardinality_clause_optionalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_cardinality_clause_optional)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 174
            self.match(SimpleSchemaParser.T__5)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Cardinality_clause_zero_or_moreContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_cardinality_clause_zero_or_more

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCardinality_clause_zero_or_more" ):
                return visitor.visitCardinality_clause_zero_or_more(self)
            else:
                return visitor.visitChildren(self)




    def cardinality_clause_zero_or_more(self):

        localctx = SimpleSchemaParser.Cardinality_clause_zero_or_moreContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_cardinality_clause_zero_or_more)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 176
            self.match(SimpleSchemaParser.T__6)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Cardinality_clause_one_or_moreContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_cardinality_clause_one_or_more

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCardinality_clause_one_or_more" ):
                return visitor.visitCardinality_clause_one_or_more(self)
            else:
                return visitor.visitChildren(self)




    def cardinality_clause_one_or_more(self):

        localctx = SimpleSchemaParser.Cardinality_clause_one_or_moreContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_cardinality_clause_one_or_more)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            self.match(SimpleSchemaParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Cardinality_clause_fixedContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACK(self):
            return self.getToken(SimpleSchemaParser.LBRACK, 0)

        def integer_expression(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Integer_expressionContext,0)


        def RBRACK(self):
            return self.getToken(SimpleSchemaParser.RBRACK, 0)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_cardinality_clause_fixed

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCardinality_clause_fixed" ):
                return visitor.visitCardinality_clause_fixed(self)
            else:
                return visitor.visitChildren(self)




    def cardinality_clause_fixed(self):

        localctx = SimpleSchemaParser.Cardinality_clause_fixedContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_cardinality_clause_fixed)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 180
            self.match(SimpleSchemaParser.LBRACK)
            self.state = 181
            self.integer_expression()
            self.state = 182
            self.match(SimpleSchemaParser.RBRACK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Cardinality_clause_range__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACK(self):
            return self.getToken(SimpleSchemaParser.LBRACK, 0)

        def integer_expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Integer_expressionContext)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Integer_expressionContext,i)


        def RBRACK(self):
            return self.getToken(SimpleSchemaParser.RBRACK, 0)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_cardinality_clause_range__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCardinality_clause_range__" ):
                return visitor.visitCardinality_clause_range__(self)
            else:
                return visitor.visitChildren(self)




    def cardinality_clause_range__(self):

        localctx = SimpleSchemaParser.Cardinality_clause_range__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_cardinality_clause_range__)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 184
            self.match(SimpleSchemaParser.LBRACK)
            self.state = 185
            self.integer_expression()
            self.state = 186
            self.match(SimpleSchemaParser.T__8)
            self.state = 187
            self.integer_expression()
            self.state = 188
            self.match(SimpleSchemaParser.RBRACK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expression__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def number_expression(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Number_expressionContext,0)


        def integer_expression(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Integer_expressionContext,0)


        def true_expression(self):
            return self.getTypedRuleContext(SimpleSchemaParser.True_expressionContext,0)


        def false_expression(self):
            return self.getTypedRuleContext(SimpleSchemaParser.False_expressionContext,0)


        def none_expression(self):
            return self.getTypedRuleContext(SimpleSchemaParser.None_expressionContext,0)


        def string_expression(self):
            return self.getTypedRuleContext(SimpleSchemaParser.String_expressionContext,0)


        def list_expression(self):
            return self.getTypedRuleContext(SimpleSchemaParser.List_expressionContext,0)


        def tuple_expression(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Tuple_expressionContext,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_expression__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression__" ):
                return visitor.visitExpression__(self)
            else:
                return visitor.visitChildren(self)




    def expression__(self):

        localctx = SimpleSchemaParser.Expression__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_expression__)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 198
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [52]:
                self.state = 190
                self.number_expression()
                pass
            elif token in [53]:
                self.state = 191
                self.integer_expression()
                pass
            elif token in [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
                self.state = 192
                self.true_expression()
                pass
            elif token in [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]:
                self.state = 193
                self.false_expression()
                pass
            elif token in [32]:
                self.state = 194
                self.none_expression()
                pass
            elif token in [55, 57, 59, 61]:
                self.state = 195
                self.string_expression()
                pass
            elif token in [45]:
                self.state = 196
                self.list_expression()
                pass
            elif token in [43]:
                self.state = 197
                self.tuple_expression()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Number_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(SimpleSchemaParser.NUMBER, 0)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_number_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber_expression" ):
                return visitor.visitNumber_expression(self)
            else:
                return visitor.visitChildren(self)




    def number_expression(self):

        localctx = SimpleSchemaParser.Number_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_number_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
            self.match(SimpleSchemaParser.NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Integer_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(SimpleSchemaParser.INTEGER, 0)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_integer_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInteger_expression" ):
                return visitor.visitInteger_expression(self)
            else:
                return visitor.visitChildren(self)




    def integer_expression(self):

        localctx = SimpleSchemaParser.Integer_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_integer_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 202
            self.match(SimpleSchemaParser.INTEGER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class True_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_true_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTrue_expression" ):
                return visitor.visitTrue_expression(self)
            else:
                return visitor.visitChildren(self)




    def true_expression(self):

        localctx = SimpleSchemaParser.True_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_true_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 204
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2096128) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class False_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_false_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFalse_expression" ):
                return visitor.visitFalse_expression(self)
            else:
                return visitor.visitChildren(self)




    def false_expression(self):

        localctx = SimpleSchemaParser.False_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_false_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 206
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4292870144) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class None_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_none_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNone_expression" ):
                return visitor.visitNone_expression(self)
            else:
                return visitor.visitChildren(self)




    def none_expression(self):

        localctx = SimpleSchemaParser.None_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_none_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 208
            self.match(SimpleSchemaParser.T__31)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class String_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOUBLE_QUOTE_STRING(self):
            return self.getToken(SimpleSchemaParser.DOUBLE_QUOTE_STRING, 0)

        def SINGLE_QUOTE_STRING(self):
            return self.getToken(SimpleSchemaParser.SINGLE_QUOTE_STRING, 0)

        def TRIPLE_DOUBLE_QUOTE_STRING(self):
            return self.getToken(SimpleSchemaParser.TRIPLE_DOUBLE_QUOTE_STRING, 0)

        def TRIPLE_SINGLE_QUOTE_STRING(self):
            return self.getToken(SimpleSchemaParser.TRIPLE_SINGLE_QUOTE_STRING, 0)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_string_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString_expression" ):
                return visitor.visitString_expression(self)
            else:
                return visitor.visitChildren(self)




    def string_expression(self):

        localctx = SimpleSchemaParser.String_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_string_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 210
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3062447746611937280) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class List_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACK(self):
            return self.getToken(SimpleSchemaParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(SimpleSchemaParser.RBRACK, 0)

        def expression__(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Expression__Context)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Expression__Context,i)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_list_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitList_expression" ):
                return visitor.visitList_expression(self)
            else:
                return visitor.visitChildren(self)




    def list_expression(self):

        localctx = SimpleSchemaParser.List_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_list_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 212
            self.match(SimpleSchemaParser.LBRACK)
            self.state = 224
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3076002534549093376) != 0):
                self.state = 213
                self.expression__()
                self.state = 218
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 214
                        self.match(SimpleSchemaParser.T__3)
                        self.state = 215
                        self.expression__() 
                    self.state = 220
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

                self.state = 222
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==4:
                    self.state = 221
                    self.match(SimpleSchemaParser.T__3)




            self.state = 226
            self.match(SimpleSchemaParser.RBRACK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Tuple_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(SimpleSchemaParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(SimpleSchemaParser.RPAREN, 0)

        def tuple_expression_single_item__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Tuple_expression_single_item__Context,0)


        def tuple_expression_multi_item__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Tuple_expression_multi_item__Context,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_tuple_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTuple_expression" ):
                return visitor.visitTuple_expression(self)
            else:
                return visitor.visitChildren(self)




    def tuple_expression(self):

        localctx = SimpleSchemaParser.Tuple_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_tuple_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 228
            self.match(SimpleSchemaParser.LPAREN)
            self.state = 231
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.state = 229
                self.tuple_expression_single_item__()
                pass

            elif la_ == 2:
                self.state = 230
                self.tuple_expression_multi_item__()
                pass


            self.state = 233
            self.match(SimpleSchemaParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Tuple_expression_single_item__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Expression__Context,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_tuple_expression_single_item__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTuple_expression_single_item__" ):
                return visitor.visitTuple_expression_single_item__(self)
            else:
                return visitor.visitChildren(self)




    def tuple_expression_single_item__(self):

        localctx = SimpleSchemaParser.Tuple_expression_single_item__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_tuple_expression_single_item__)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 235
            self.expression__()
            self.state = 236
            self.match(SimpleSchemaParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Tuple_expression_multi_item__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression__(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Expression__Context)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Expression__Context,i)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_tuple_expression_multi_item__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTuple_expression_multi_item__" ):
                return visitor.visitTuple_expression_multi_item__(self)
            else:
                return visitor.visitChildren(self)




    def tuple_expression_multi_item__(self):

        localctx = SimpleSchemaParser.Tuple_expression_multi_item__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_tuple_expression_multi_item__)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 238
            self.expression__()
            self.state = 241 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 239
                    self.match(SimpleSchemaParser.T__3)
                    self.state = 240
                    self.expression__()

                else:
                    raise NoViableAltException(self)
                self.state = 243 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,18,self._ctx)

            self.state = 246
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 245
                self.match(SimpleSchemaParser.T__3)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Header_statement__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def include_statement(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Include_statementContext,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_header_statement__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHeader_statement__" ):
                return visitor.visitHeader_statement__(self)
            else:
                return visitor.visitChildren(self)




    def header_statement__(self):

        localctx = SimpleSchemaParser.Header_statement__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_header_statement__)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 248
            self.include_statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Include_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INCLUDE_FROM(self):
            return self.getToken(SimpleSchemaParser.INCLUDE_FROM, 0)

        def include_statement_from(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Include_statement_fromContext,0)


        def INCLUDE_IMPORT(self):
            return self.getToken(SimpleSchemaParser.INCLUDE_IMPORT, 0)

        def include_statement_import__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Include_statement_import__Context,0)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSchemaParser.NEWLINE)
            else:
                return self.getToken(SimpleSchemaParser.NEWLINE, i)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_include_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInclude_statement" ):
                return visitor.visitInclude_statement(self)
            else:
                return visitor.visitChildren(self)




    def include_statement(self):

        localctx = SimpleSchemaParser.Include_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_include_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 250
            self.match(SimpleSchemaParser.INCLUDE_FROM)
            self.state = 251
            self.include_statement_from()
            self.state = 252
            self.match(SimpleSchemaParser.INCLUDE_IMPORT)
            self.state = 253
            self.include_statement_import__()
            self.state = 255 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 254
                self.match(SimpleSchemaParser.NEWLINE)
                self.state = 257 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==40):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Include_statement_fromContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.IdentifierContext,i)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_include_statement_from

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInclude_statement_from" ):
                return visitor.visitInclude_statement_from(self)
            else:
                return visitor.visitChildren(self)




    def include_statement_from(self):

        localctx = SimpleSchemaParser.Include_statement_fromContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_include_statement_from)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 260
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==33:
                self.state = 259
                self.match(SimpleSchemaParser.T__32)


            self.state = 270 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 265
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [54]:
                    self.state = 262
                    self.identifier()
                    pass
                elif token in [9]:
                    self.state = 263
                    self.match(SimpleSchemaParser.T__8)
                    pass
                elif token in [34]:
                    self.state = 264
                    self.match(SimpleSchemaParser.T__33)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 268
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==33:
                    self.state = 267
                    self.match(SimpleSchemaParser.T__32)


                self.state = 272 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 18014415689351680) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Include_statement_import__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def include_statement_import_star(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Include_statement_import_starContext,0)


        def include_statement_import_grouped_items__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Include_statement_import_grouped_items__Context,0)


        def include_statement_import_items__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Include_statement_import_items__Context,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_include_statement_import__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInclude_statement_import__" ):
                return visitor.visitInclude_statement_import__(self)
            else:
                return visitor.visitChildren(self)




    def include_statement_import__(self):

        localctx = SimpleSchemaParser.Include_statement_import__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_include_statement_import__)
        try:
            self.state = 277
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7]:
                self.enterOuterAlt(localctx, 1)
                self.state = 274
                self.include_statement_import_star()
                pass
            elif token in [43]:
                self.enterOuterAlt(localctx, 2)
                self.state = 275
                self.include_statement_import_grouped_items__()
                pass
            elif token in [54]:
                self.enterOuterAlt(localctx, 3)
                self.state = 276
                self.include_statement_import_items__()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Include_statement_import_starContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_include_statement_import_star

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInclude_statement_import_star" ):
                return visitor.visitInclude_statement_import_star(self)
            else:
                return visitor.visitChildren(self)




    def include_statement_import_star(self):

        localctx = SimpleSchemaParser.Include_statement_import_starContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_include_statement_import_star)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 279
            self.match(SimpleSchemaParser.T__6)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Include_statement_import_grouped_items__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(SimpleSchemaParser.LPAREN, 0)

        def include_statement_import_items__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Include_statement_import_items__Context,0)


        def RPAREN(self):
            return self.getToken(SimpleSchemaParser.RPAREN, 0)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_include_statement_import_grouped_items__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInclude_statement_import_grouped_items__" ):
                return visitor.visitInclude_statement_import_grouped_items__(self)
            else:
                return visitor.visitChildren(self)




    def include_statement_import_grouped_items__(self):

        localctx = SimpleSchemaParser.Include_statement_import_grouped_items__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_include_statement_import_grouped_items__)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 281
            self.match(SimpleSchemaParser.LPAREN)
            self.state = 282
            self.include_statement_import_items__()
            self.state = 283
            self.match(SimpleSchemaParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Include_statement_import_items__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def include_statement_import_element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Include_statement_import_elementContext)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Include_statement_import_elementContext,i)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_include_statement_import_items__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInclude_statement_import_items__" ):
                return visitor.visitInclude_statement_import_items__(self)
            else:
                return visitor.visitChildren(self)




    def include_statement_import_items__(self):

        localctx = SimpleSchemaParser.Include_statement_import_items__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_include_statement_import_items__)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 285
            self.include_statement_import_element()
            self.state = 290
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,26,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 286
                    self.match(SimpleSchemaParser.T__3)
                    self.state = 287
                    self.include_statement_import_element() 
                self.state = 292
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,26,self._ctx)

            self.state = 294
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 293
                self.match(SimpleSchemaParser.T__3)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Include_statement_import_elementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.IdentifierContext,i)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_include_statement_import_element

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInclude_statement_import_element" ):
                return visitor.visitInclude_statement_import_element(self)
            else:
                return visitor.visitChildren(self)




    def include_statement_import_element(self):

        localctx = SimpleSchemaParser.Include_statement_import_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_include_statement_import_element)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 296
            self.identifier()
            self.state = 299
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==35:
                self.state = 297
                self.match(SimpleSchemaParser.T__34)
                self.state = 298
                self.identifier()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Body_statement__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parse_structure_statement(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_structure_statementContext,0)


        def parse_structure_simplified_statement(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_structure_simplified_statementContext,0)


        def parse_item_statement(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_item_statementContext,0)


        def extension_statement(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Extension_statementContext,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_body_statement__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBody_statement__" ):
                return visitor.visitBody_statement__(self)
            else:
                return visitor.visitChildren(self)




    def body_statement__(self):

        localctx = SimpleSchemaParser.Body_statement__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_body_statement__)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 305
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,29,self._ctx)
            if la_ == 1:
                self.state = 301
                self.parse_structure_statement()
                pass

            elif la_ == 2:
                self.state = 302
                self.parse_structure_simplified_statement()
                pass

            elif la_ == 3:
                self.state = 303
                self.parse_item_statement()
                pass

            elif la_ == 4:
                self.state = 304
                self.extension_statement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Extension_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(SimpleSchemaParser.IdentifierContext,0)


        def LPAREN(self):
            return self.getToken(SimpleSchemaParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(SimpleSchemaParser.RPAREN, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSchemaParser.NEWLINE)
            else:
                return self.getToken(SimpleSchemaParser.NEWLINE, i)

        def extension_statement_positional_args(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Extension_statement_positional_argsContext,0)


        def extension_statement_keyword_args(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Extension_statement_keyword_argsContext,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_extension_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExtension_statement" ):
                return visitor.visitExtension_statement(self)
            else:
                return visitor.visitChildren(self)




    def extension_statement(self):

        localctx = SimpleSchemaParser.Extension_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_extension_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 307
            self.identifier()
            self.state = 308
            self.match(SimpleSchemaParser.LPAREN)

            self.state = 320
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3094016933058575360) != 0):
                self.state = 315
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
                if la_ == 1:
                    self.state = 309
                    self.extension_statement_positional_args()
                    self.state = 310
                    self.match(SimpleSchemaParser.T__3)
                    self.state = 311
                    self.extension_statement_keyword_args()
                    pass

                elif la_ == 2:
                    self.state = 313
                    self.extension_statement_positional_args()
                    pass

                elif la_ == 3:
                    self.state = 314
                    self.extension_statement_keyword_args()
                    pass


                self.state = 318
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==4:
                    self.state = 317
                    self.match(SimpleSchemaParser.T__3)




            self.state = 322
            self.match(SimpleSchemaParser.RPAREN)
            self.state = 324 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 323
                self.match(SimpleSchemaParser.NEWLINE)
                self.state = 326 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==40):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Extension_statement_positional_argsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression__(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Expression__Context)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Expression__Context,i)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_extension_statement_positional_args

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExtension_statement_positional_args" ):
                return visitor.visitExtension_statement_positional_args(self)
            else:
                return visitor.visitChildren(self)




    def extension_statement_positional_args(self):

        localctx = SimpleSchemaParser.Extension_statement_positional_argsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_extension_statement_positional_args)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 328
            self.expression__()
            self.state = 333
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,34,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 329
                    self.match(SimpleSchemaParser.T__3)
                    self.state = 330
                    self.expression__() 
                self.state = 335
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,34,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Extension_statement_keyword_argsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def extension_statement_keyword_arg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Extension_statement_keyword_argContext)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Extension_statement_keyword_argContext,i)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_extension_statement_keyword_args

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExtension_statement_keyword_args" ):
                return visitor.visitExtension_statement_keyword_args(self)
            else:
                return visitor.visitChildren(self)




    def extension_statement_keyword_args(self):

        localctx = SimpleSchemaParser.Extension_statement_keyword_argsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_extension_statement_keyword_args)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 336
            self.extension_statement_keyword_arg()
            self.state = 341
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,35,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 337
                    self.match(SimpleSchemaParser.T__3)
                    self.state = 338
                    self.extension_statement_keyword_arg() 
                self.state = 343
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,35,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Extension_statement_keyword_argContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(SimpleSchemaParser.IdentifierContext,0)


        def expression__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Expression__Context,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_extension_statement_keyword_arg

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExtension_statement_keyword_arg" ):
                return visitor.visitExtension_statement_keyword_arg(self)
            else:
                return visitor.visitChildren(self)




    def extension_statement_keyword_arg(self):

        localctx = SimpleSchemaParser.Extension_statement_keyword_argContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_extension_statement_keyword_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 344
            self.identifier()
            self.state = 345
            self.match(SimpleSchemaParser.T__35)
            self.state = 346
            self.expression__()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parse_item_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(SimpleSchemaParser.IdentifierContext,0)


        def parse_type(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_typeContext,0)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSchemaParser.NEWLINE)
            else:
                return self.getToken(SimpleSchemaParser.NEWLINE, i)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_parse_item_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse_item_statement" ):
                return visitor.visitParse_item_statement(self)
            else:
                return visitor.visitChildren(self)




    def parse_item_statement(self):

        localctx = SimpleSchemaParser.Parse_item_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_parse_item_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 348
            self.identifier()
            self.state = 349
            self.match(SimpleSchemaParser.T__4)
            self.state = 350
            self.parse_type()
            self.state = 352 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 351
                self.match(SimpleSchemaParser.NEWLINE)
                self.state = 354 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==40):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parse_structure_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(SimpleSchemaParser.IdentifierContext,0)


        def INDENT(self):
            return self.getToken(SimpleSchemaParser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(SimpleSchemaParser.DEDENT, 0)

        def parse_structure_statement_base_grouped_items__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_structure_statement_base_grouped_items__Context,0)


        def parse_structure_statement_base_items__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_structure_statement_base_items__Context,0)


        def body_statement__(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Body_statement__Context)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Body_statement__Context,i)


        def metadata_clause(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Metadata_clauseContext,0)


        def cardinality_clause(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Cardinality_clauseContext,0)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSchemaParser.NEWLINE)
            else:
                return self.getToken(SimpleSchemaParser.NEWLINE, i)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_parse_structure_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse_structure_statement" ):
                return visitor.visitParse_structure_statement(self)
            else:
                return visitor.visitChildren(self)




    def parse_structure_statement(self):

        localctx = SimpleSchemaParser.Parse_structure_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_parse_structure_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 356
            self.identifier()
            self.state = 362
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 357
                self.match(SimpleSchemaParser.T__4)
                self.state = 360
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,37,self._ctx)
                if la_ == 1:
                    self.state = 358
                    self.parse_structure_statement_base_grouped_items__()
                    pass

                elif la_ == 2:
                    self.state = 359
                    self.parse_structure_statement_base_items__()
                    pass




            self.state = 364
            self.match(SimpleSchemaParser.T__36)
            self.state = 365
            self.match(SimpleSchemaParser.INDENT)
            self.state = 377
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.state = 366
                self.match(SimpleSchemaParser.T__2)
                self.state = 368 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 367
                    self.match(SimpleSchemaParser.NEWLINE)
                    self.state = 370 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==40):
                        break

                pass
            elif token in [54]:
                self.state = 373 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 372
                    self.body_statement__()
                    self.state = 375 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==54):
                        break

                pass
            else:
                raise NoViableAltException(self)

            self.state = 379
            self.match(SimpleSchemaParser.DEDENT)
            self.state = 398
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 35184372089282) != 0):
                self.state = 391
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,43,self._ctx)
                if la_ == 1:
                    self.state = 380
                    self.cardinality_clause()
                    self.state = 384
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==40:
                        self.state = 381
                        self.match(SimpleSchemaParser.NEWLINE)
                        self.state = 386
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 387
                    self.metadata_clause()
                    pass

                elif la_ == 2:
                    self.state = 389
                    self.metadata_clause()
                    pass

                elif la_ == 3:
                    self.state = 390
                    self.cardinality_clause()
                    pass


                self.state = 394 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 393
                    self.match(SimpleSchemaParser.NEWLINE)
                    self.state = 396 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==40):
                        break



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parse_structure_statement_base_items__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parse_type(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Parse_typeContext)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Parse_typeContext,i)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_parse_structure_statement_base_items__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse_structure_statement_base_items__" ):
                return visitor.visitParse_structure_statement_base_items__(self)
            else:
                return visitor.visitChildren(self)




    def parse_structure_statement_base_items__(self):

        localctx = SimpleSchemaParser.Parse_structure_statement_base_items__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_parse_structure_statement_base_items__)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 400
            self.parse_type()
            self.state = 405
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,46,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 401
                    self.match(SimpleSchemaParser.T__3)
                    self.state = 402
                    self.parse_type() 
                self.state = 407
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,46,self._ctx)

            self.state = 409
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 408
                self.match(SimpleSchemaParser.T__3)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parse_structure_statement_base_grouped_items__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(SimpleSchemaParser.LPAREN, 0)

        def parse_structure_statement_base_items__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_structure_statement_base_items__Context,0)


        def RPAREN(self):
            return self.getToken(SimpleSchemaParser.RPAREN, 0)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_parse_structure_statement_base_grouped_items__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse_structure_statement_base_grouped_items__" ):
                return visitor.visitParse_structure_statement_base_grouped_items__(self)
            else:
                return visitor.visitChildren(self)




    def parse_structure_statement_base_grouped_items__(self):

        localctx = SimpleSchemaParser.Parse_structure_statement_base_grouped_items__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_parse_structure_statement_base_grouped_items__)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 411
            self.match(SimpleSchemaParser.LPAREN)
            self.state = 412
            self.parse_structure_statement_base_items__()
            self.state = 413
            self.match(SimpleSchemaParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parse_structure_simplified_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(SimpleSchemaParser.IdentifierContext,0)


        def metadata_clause(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Metadata_clauseContext,0)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSchemaParser.NEWLINE)
            else:
                return self.getToken(SimpleSchemaParser.NEWLINE, i)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_parse_structure_simplified_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse_structure_simplified_statement" ):
                return visitor.visitParse_structure_simplified_statement(self)
            else:
                return visitor.visitChildren(self)




    def parse_structure_simplified_statement(self):

        localctx = SimpleSchemaParser.Parse_structure_simplified_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_parse_structure_simplified_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 415
            self.identifier()
            self.state = 416
            self.metadata_clause()
            self.state = 418 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 417
                self.match(SimpleSchemaParser.NEWLINE)
                self.state = 420 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==40):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parse_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parse_tuple_type(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_tuple_typeContext,0)


        def parse_variant_type(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_variant_typeContext,0)


        def parse_identifier_type(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_identifier_typeContext,0)


        def cardinality_clause(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Cardinality_clauseContext,0)


        def metadata_clause(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Metadata_clauseContext,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_parse_type

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse_type" ):
                return visitor.visitParse_type(self)
            else:
                return visitor.visitChildren(self)




    def parse_type(self):

        localctx = SimpleSchemaParser.Parse_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_parse_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 425
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,49,self._ctx)
            if la_ == 1:
                self.state = 422
                self.parse_tuple_type()
                pass

            elif la_ == 2:
                self.state = 423
                self.parse_variant_type()
                pass

            elif la_ == 3:
                self.state = 424
                self.parse_identifier_type()
                pass


            self.state = 428
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 35184372089280) != 0):
                self.state = 427
                self.cardinality_clause()


            self.state = 431
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 430
                self.metadata_clause()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parse_identifier_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.IdentifierContext,i)


        def parse_identifier_type_global(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_identifier_type_globalContext,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_parse_identifier_type

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse_identifier_type" ):
                return visitor.visitParse_identifier_type(self)
            else:
                return visitor.visitChildren(self)




    def parse_identifier_type(self):

        localctx = SimpleSchemaParser.Parse_identifier_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_parse_identifier_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 434
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==38:
                self.state = 433
                self.parse_identifier_type_global()


            self.state = 436
            self.identifier()
            self.state = 441
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 437
                self.match(SimpleSchemaParser.T__33)
                self.state = 438
                self.identifier()
                self.state = 443
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parse_identifier_type_globalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_parse_identifier_type_global

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse_identifier_type_global" ):
                return visitor.visitParse_identifier_type_global(self)
            else:
                return visitor.visitChildren(self)




    def parse_identifier_type_global(self):

        localctx = SimpleSchemaParser.Parse_identifier_type_globalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_parse_identifier_type_global)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 444
            self.match(SimpleSchemaParser.T__37)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parse_variant_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(SimpleSchemaParser.LPAREN, 0)

        def parse_type(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Parse_typeContext)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Parse_typeContext,i)


        def RPAREN(self):
            return self.getToken(SimpleSchemaParser.RPAREN, 0)

        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_parse_variant_type

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse_variant_type" ):
                return visitor.visitParse_variant_type(self)
            else:
                return visitor.visitChildren(self)




    def parse_variant_type(self):

        localctx = SimpleSchemaParser.Parse_variant_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_parse_variant_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 446
            self.match(SimpleSchemaParser.LPAREN)
            self.state = 447
            self.parse_type()
            self.state = 452
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,54,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 448
                    self.match(SimpleSchemaParser.T__38)
                    self.state = 449
                    self.parse_type() 
                self.state = 454
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,54,self._ctx)

            self.state = 455
            self.match(SimpleSchemaParser.T__38)
            self.state = 456
            self.parse_type()
            self.state = 457
            self.match(SimpleSchemaParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parse_tuple_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(SimpleSchemaParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(SimpleSchemaParser.RPAREN, 0)

        def parse_tuple_type_single_item__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_tuple_type_single_item__Context,0)


        def parse_tuple_type_multi_item__(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_tuple_type_multi_item__Context,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_parse_tuple_type

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse_tuple_type" ):
                return visitor.visitParse_tuple_type(self)
            else:
                return visitor.visitChildren(self)




    def parse_tuple_type(self):

        localctx = SimpleSchemaParser.Parse_tuple_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_parse_tuple_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 459
            self.match(SimpleSchemaParser.LPAREN)
            self.state = 462
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,55,self._ctx)
            if la_ == 1:
                self.state = 460
                self.parse_tuple_type_single_item__()
                pass

            elif la_ == 2:
                self.state = 461
                self.parse_tuple_type_multi_item__()
                pass


            self.state = 464
            self.match(SimpleSchemaParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parse_tuple_type_single_item__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parse_type(self):
            return self.getTypedRuleContext(SimpleSchemaParser.Parse_typeContext,0)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_parse_tuple_type_single_item__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse_tuple_type_single_item__" ):
                return visitor.visitParse_tuple_type_single_item__(self)
            else:
                return visitor.visitChildren(self)




    def parse_tuple_type_single_item__(self):

        localctx = SimpleSchemaParser.Parse_tuple_type_single_item__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_parse_tuple_type_single_item__)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 466
            self.parse_type()
            self.state = 467
            self.match(SimpleSchemaParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Parse_tuple_type_multi_item__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parse_type(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSchemaParser.Parse_typeContext)
            else:
                return self.getTypedRuleContext(SimpleSchemaParser.Parse_typeContext,i)


        def getRuleIndex(self):
            return SimpleSchemaParser.RULE_parse_tuple_type_multi_item__

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse_tuple_type_multi_item__" ):
                return visitor.visitParse_tuple_type_multi_item__(self)
            else:
                return visitor.visitChildren(self)




    def parse_tuple_type_multi_item__(self):

        localctx = SimpleSchemaParser.Parse_tuple_type_multi_item__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_parse_tuple_type_multi_item__)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 469
            self.parse_type()
            self.state = 472 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 470
                    self.match(SimpleSchemaParser.T__3)
                    self.state = 471
                    self.parse_type()

                else:
                    raise NoViableAltException(self)
                self.state = 474 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,56,self._ctx)

            self.state = 477
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 476
                self.match(SimpleSchemaParser.T__3)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





