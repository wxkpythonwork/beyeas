from configparser import ConfigParser
from sys import argv
import numpy as np
import pandas as pd
from scipy import special


class BayesianSmoothing(object):
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    def update(self, imps, clks, iter_num, epsilon):
        for i in range(iter_num):
            new_alpha, new_beta = self.__fixed_point_iteration(imps, clks, self.alpha, self.beta)
            if abs(new_alpha - self.alpha) < epsilon and abs(new_beta - self.beta) < epsilon:
                break
            self.alpha = new_alpha
            self.beta = new_beta

    def __fixed_point_iteration(self, imps, clks, alpha, beta):
        numerator_alpha = 0.0
        numerator_beta = 0.0
        denominator = 0.0

        for i in range(len(imps)):
            numerator_alpha += (special.digamma(clks[i] + alpha) - special.digamma(alpha))
            numerator_beta += (special.digamma(imps[i] - clks[i] + beta) - special.digamma(beta))
            denominator += (special.digamma(imps[i] + alpha + beta) - special.digamma(alpha + beta))

        return alpha * (numerator_alpha / denominator), beta * (numerator_beta / denominator)


def gen_parmeter(inupt_file, numerator, denominator):
    df = pd.read_csv(inupt_file)
    sample = df.sample(n=10000, replace=True)
    bs = BayesianSmoothing(1, 1)
    sample[numerator] = np.where(sample[denominator] >= sample[numerator], sample[numerator], sample[denominator])
    denominators, numerators = sample[denominator].values.tolist(), sample[numerator].values.tolist()
    bs.update(denominators, numerators, 100, 0.000001)
    a, b = round(bs.alpha, 6), round(bs.beta, 6)
    return a, b


def main():
    input_file, numerator, denominator, cfg_file = argv[1], argv[2], argv[3], argv[4]
    config = ConfigParser()
    a, b = gen_parmeter(input_file, numerator, denominator)
    config['COMMON'] = {'a': a, 'b': b}
    with open(cfg_file, 'w') as f:
        config.write(f)


if __name__ == '__main__':
    main()
