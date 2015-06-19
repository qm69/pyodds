"""
Odds portal scraper

Usage:
    scrap.py full <mhsh> <seas> [<fpage> <lpage>]
    scrap.py last <mhsh> <days>
    scrap.py each
    scraper.py -d | --debug
    scraper.py -v | --version
    scraper.py -h | --help

Options:
    -d --debug          Show debug messages.
    -h --help           Show this screen.
    -v --version        Show version.
"""
"""
    scraper.py full bsusml 2012-2013 1 36 {
        "full": true,
        "<mhsh>": "bsusml",
        "<seas>": "2012-2013",
        "<fpage>": "1",
        "<lpage>": "36",
        "--help": false,
        "--version": false }

    scraper.py  last bsusml 3 {
        "full": false,
        "last": true,
        "<mhsh>": "bsusml",
        "<seas>": null,
        "<fpage>": null,
        "<lpage>": null,
        "<days>": "3" }
"""

from docopt import docopt
from libs.tabler import table, rows
from libs.logger import log_main
from libs.db import get_xeid
# from libs.db import save_to_db
# from libs.odds import get_odds
# from libs.builder import builder

# пока мало модулей, то их не выгодно тянуть из базы,
# разве что потом попробовать 'pickel'
shts = ['2015', '2014', '2013', '2012', '2011',
        '2010', '2009', '2008', '2007', '2006']
lngs = ['2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011',
        '2009-2010', '2008-2009', '2007-2008', '2006-2007', '2005-2006']
mhsh_dict = {
    'bsusml': ('baseball', 'usa', 'mlb', shts),
    'bbitla': ('basketball', 'italy', 'lega-a', lngs),
    'bbusnb': ('basketball', 'usa', 'nba', lngs)
}

args = docopt(__doc__, version='0.3.109')
season, mhsh = args['<seas>'], args['<mhsh>']
module = mhsh_dict[mhsh]

if args['full'] is True:
    # if first and last page was not defined
    #  create it like 1 and 50
    first = 1 if args['<fpage>'] is None else int(args['<fpage>'])
    first = 50 if args['<lpage>'] is None else int(args['<lpage>'])

    #  check if page numb arguments is correct
    if first < first:
        raise Exception('First page is bigger than last!')

    """   SCRAP RESULTS PAGE   """
    diapazon = range(first, first)
    text = 'Start season {} from {} to {} page'
    log_main.info(text.format(season, first, first))

    """  DO SMTH  """
    tags_list = table(module, season, diapazon)

    if tags_list is not None:
        ###################
        #   row by rows   #
        ###################

        for y, tag_arr in enumerate(tags_list):
            seas_type, xeid, bs4_tag = tag_arr
            ###################
            #   check xeid    #
            ###################
            if get_xeid(xeid) is True:
                print('Xeid: %s exist' % xeid)

            #######################
            #   match from tags   #
            #######################
            else:
                match = rows(bs4_tag)
                """" УБРАТЬ ОТСБДА И ПОМЕСТИТЬ В TABLER.PY
                if match is not None:
                    match['season'] = season
                    match['type'] = seas_type
                    match['xeid'] = xeid
                    bet_odd = get_odds(match['xeid'], match['xhash'])

                    if bet_odd is not None:
                        match['line'], match['hcap'], match['totl'] = bet_odd
                        #   build the Match
                        m = builder(match)

                        if m is not None:
                            res = save_to_db(m)
                            if res is not None:
                                txt = "%s %s %s %s SAVED" % (season, x, y + 1, m['xeid'])
                                log_main.info(txt)
                """
elif args['last'] is True:
    pass

elif args['each'] is True:
    # last resalts for all modules
    pass

else:
    print('ERROR! Chose statement')
