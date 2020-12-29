from code import output
import argparse

__author__ = 'Duy Cao'
__copyright__ = 'Duy Cao, 2020'
__license__ = 'MIT'
__status__ = 'release'
__url__ = 'https://github.com/caominhduy/bitcoin-indicated'
__version__ = '1.0'

def main(args):
    if args.all:
        output.indicator('all')
    if args.bollinger:
        output.indicator('bollinger')
    if args.MACD:
        output.indicator('macd')
    if args.RSI:
        output.indicator('rsi')
    if args.ichimoku:
        output.indicator('ichimoku')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bitcoin All-in-one Indicator\n',\
                                    usage='use "-h" or "--help" for more instructions')
    parser.add_argument('-a', '--all', action='store_true', help='Use all indicators')
    parser.add_argument('--bollinger', action='store_true', help='Use Bollinger Band only')
    parser.add_argument('--ichimoku', action='store_true', help='Use Ichimoku Cloud only')
    parser.add_argument('--MACD', action='store_true', help='Use Moving Average Convergent/Divergence only')
    parser.add_argument('--RSI', action='store_true', help='Use Relative Strength Index')
    args = parser.parse_args()
    main(args)
