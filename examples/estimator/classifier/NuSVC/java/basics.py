# -*- coding: utf-8 -*-

from sklearn import svm
from sklearn.datasets import load_iris
from sklearn_porter import Porter


iris_data = load_iris()
X = iris_data.data
y = iris_data.target

clf = svm.NuSVC(gamma=0.001, kernel='rbf', random_state=0)
clf.fit(X, y)

porter = Porter(clf)
output = porter.export()
print(output)

"""
class NuSVC {

    private enum Kernel { LINEAR, POLY, RBF, SIGMOID }

    private int nClasses;
    private int nRows;
    private int[] classes;
    private double[][] vectors;
    private double[][] coefficients;
    private double[] intercepts;
    private int[] weights;
    private Kernel kernel;
    private double gamma;
    private double coef0;
    private double degree;

    public NuSVC (int nClasses, int nRows, double[][] vectors, double[][] coefficients, double[] intercepts, int[] weights, String kernel, double gamma, double coef0, double degree) {
        this.nClasses = nClasses;
        this.classes = new int[nClasses];
        for (int i = 0; i < nClasses; i++) {
            this.classes[i] = i;
        }
        this.nRows = nRows;

        this.vectors = vectors;
        this.coefficients = coefficients;
        this.intercepts = intercepts;
        this.weights = weights;

        this.kernel = Kernel.valueOf(kernel.toUpperCase());
        this.gamma = gamma;
        this.coef0 = coef0;
        this.degree = degree;
    }

    public int predict(double[] features) {
    
        double[] kernels = new double[vectors.length];
        double kernel;
        switch (this.kernel) {
            case LINEAR:
                // <x,x'>
                for (int i = 0; i < this.vectors.length; i++) {
                    kernel = 0.;
                    for (int j = 0; j < this.vectors[i].length; j++) {
                        kernel += this.vectors[i][j] * features[j];
                    }
                    kernels[i] = kernel;
                }
                break;
            case POLY:
                // (y<x,x'>+r)^d
                for (int i = 0; i < this.vectors.length; i++) {
                    kernel = 0.;
                    for (int j = 0; j < this.vectors[i].length; j++) {
                        kernel += this.vectors[i][j] * features[j];
                    }
                    kernels[i] = Math.pow((this.gamma * kernel) + this.coef0, this.degree);
                }
                break;
            case RBF:
                // exp(-y|x-x'|^2)
                for (int i = 0; i < this.vectors.length; i++) {
                    kernel = 0.;
                    for (int j = 0; j < this.vectors[i].length; j++) {
                        kernel += Math.pow(this.vectors[i][j] - features[j], 2);
                    }
                    kernels[i] = Math.exp(-this.gamma * kernel);
                }
                break;
            case SIGMOID:
                // tanh(y<x,x'>+r)
                for (int i = 0; i < this.vectors.length; i++) {
                    kernel = 0.;
                    for (int j = 0; j < this.vectors[i].length; j++) {
                        kernel += this.vectors[i][j] * features[j];
                    }
                    kernels[i] = Math.tanh((this.gamma * kernel) + this.coef0);
                }
                break;
        }
    
        int[] starts = new int[this.nRows];
        for (int i = 0; i < this.nRows; i++) {
            if (i != 0) {
                int start = 0;
                for (int j = 0; j < i; j++) {
                    start += this.weights[j];
                }
                starts[i] = start;
            } else {
                starts[0] = 0;
            }
        }
    
        int[] ends = new int[this.nRows];
        for (int i = 0; i < this.nRows; i++) {
            ends[i] = this.weights[i] + starts[i];
        }
    
        if (this.nClasses == 2) {
    
            for (int i = 0; i < kernels.length; i++) {
                kernels[i] = -kernels[i];
            }
    
            double decision = 0.;
            for (int k = starts[1]; k < ends[1]; k++) {
                decision += kernels[k] * this.coefficients[0][k];
            }
            for (int k = starts[0]; k < ends[0]; k++) {
                decision += kernels[k] * this.coefficients[0][k];
            }
            decision += this.intercepts[0];
    
            if (decision > 0) {
                return 0;
            }
            return 1;
    
        }
    
        double[] decisions = new double[this.intercepts.length];
        for (int i = 0, d = 0, l = this.nRows; i < l; i++) {
            for (int j = i + 1; j < l; j++) {
                double tmp = 0.;
                for (int k = starts[j]; k < ends[j]; k++) {
                    tmp += this.coefficients[i][k] * kernels[k];
                }
                for (int k = starts[i]; k < ends[i]; k++) {
                    tmp += this.coefficients[j - 1][k] * kernels[k];
                }
                decisions[d] = tmp + this.intercepts[d];
                d++;
            }
        }
    
        int[] votes = new int[this.intercepts.length];
        for (int i = 0, d = 0, l = this.nRows; i < l; i++) {
            for (int j = i + 1; j < l; j++) {
                votes[d] = decisions[d] > 0 ? i : j;
                d++;
            }
        }
    
        int[] amounts = new int[this.nClasses];
        for (int i = 0, l = votes.length; i < l; i++) {
            amounts[votes[i]] += 1;
        }
    
        int classVal = -1, classIdx = -1;
        for (int i = 0, l = amounts.length; i < l; i++) {
            if (amounts[i] > classVal) {
                classVal = amounts[i];
                classIdx= i;
            }
        }
        return this.classes[classIdx];
    
    }

    public static void main(String[] args) {
        if (args.length == 4) {

            // Features:
            double[] features = new double[args.length];
            for (int i = 0, l = args.length; i < l; i++) {
                features[i] = Double.parseDouble(args[i]);
            }

            // Parameters:
            double[][] vectors = {{4.9000000000000004, 3.0, 1.3999999999999999, 0.20000000000000001}, {4.5999999999999996, 3.1000000000000001, 1.5, 0.20000000000000001}, {5.4000000000000004, 3.8999999999999999, 1.7, 0.40000000000000002}, {5.0, 3.3999999999999999, 1.5, 0.20000000000000001}, {4.9000000000000004, 3.1000000000000001, 1.5, 0.10000000000000001}, {5.4000000000000004, 3.7000000000000002, 1.5, 0.20000000000000001}, {4.7999999999999998, 3.3999999999999999, 1.6000000000000001, 0.20000000000000001}, {5.7000000000000002, 4.4000000000000004, 1.5, 0.40000000000000002}, {5.7000000000000002, 3.7999999999999998, 1.7, 0.29999999999999999}, {5.0999999999999996, 3.7999999999999998, 1.5, 0.29999999999999999}, {5.4000000000000004, 3.3999999999999999, 1.7, 0.20000000000000001}, {5.0999999999999996, 3.7000000000000002, 1.5, 0.40000000000000002}, {5.0999999999999996, 3.2999999999999998, 1.7, 0.5}, {4.7999999999999998, 3.3999999999999999, 1.8999999999999999, 0.20000000000000001}, {5.0, 3.0, 1.6000000000000001, 0.20000000000000001}, {5.0, 3.3999999999999999, 1.6000000000000001, 0.40000000000000002}, {5.2000000000000002, 3.5, 1.5, 0.20000000000000001}, {4.7000000000000002, 3.2000000000000002, 1.6000000000000001, 0.20000000000000001}, {4.7999999999999998, 3.1000000000000001, 1.6000000000000001, 0.20000000000000001}, {5.4000000000000004, 3.3999999999999999, 1.5, 0.40000000000000002}, {4.9000000000000004, 3.1000000000000001, 1.5, 0.10000000000000001}, {4.9000000000000004, 3.1000000000000001, 1.5, 0.10000000000000001}, {5.0999999999999996, 3.3999999999999999, 1.5, 0.20000000000000001}, {4.5, 2.2999999999999998, 1.3, 0.29999999999999999}, {5.0, 3.5, 1.6000000000000001, 0.59999999999999998}, {5.0999999999999996, 3.7999999999999998, 1.8999999999999999, 0.40000000000000002}, {4.7999999999999998, 3.0, 1.3999999999999999, 0.29999999999999999}, {5.0999999999999996, 3.7999999999999998, 1.6000000000000001, 0.20000000000000001}, {5.2999999999999998, 3.7000000000000002, 1.5, 0.20000000000000001}, {7.0, 3.2000000000000002, 4.7000000000000002, 1.3999999999999999}, {6.4000000000000004, 3.2000000000000002, 4.5, 1.5}, {6.9000000000000004, 3.1000000000000001, 4.9000000000000004, 1.5}, {5.5, 2.2999999999999998, 4.0, 1.3}, {6.5, 2.7999999999999998, 4.5999999999999996, 1.5}, {5.7000000000000002, 2.7999999999999998, 4.5, 1.3}, {6.2999999999999998, 3.2999999999999998, 4.7000000000000002, 1.6000000000000001}, {4.9000000000000004, 2.3999999999999999, 3.2999999999999998, 1.0}, {6.5999999999999996, 2.8999999999999999, 4.5999999999999996, 1.3}, {5.2000000000000002, 2.7000000000000002, 3.8999999999999999, 1.3999999999999999}, {5.0, 2.0, 3.5, 1.0}, {5.9000000000000004, 3.0, 4.2000000000000002, 1.5}, {6.0, 2.2000000000000002, 4.0, 1.0}, {6.0999999999999996, 2.8999999999999999, 4.7000000000000002, 1.3999999999999999}, {5.5999999999999996, 2.8999999999999999, 3.6000000000000001, 1.3}, {6.7000000000000002, 3.1000000000000001, 4.4000000000000004, 1.3999999999999999}, {5.5999999999999996, 3.0, 4.5, 1.5}, {5.7999999999999998, 2.7000000000000002, 4.0999999999999996, 1.0}, {6.2000000000000002, 2.2000000000000002, 4.5, 1.5}, {5.5999999999999996, 2.5, 3.8999999999999999, 1.1000000000000001}, {5.9000000000000004, 3.2000000000000002, 4.7999999999999998, 1.8}, {6.0999999999999996, 2.7999999999999998, 4.0, 1.3}, {6.2999999999999998, 2.5, 4.9000000000000004, 1.5}, {6.0999999999999996, 2.7999999999999998, 4.7000000000000002, 1.2}, {6.5999999999999996, 3.0, 4.4000000000000004, 1.3999999999999999}, {6.7999999999999998, 2.7999999999999998, 4.7999999999999998, 1.3999999999999999}, {6.7000000000000002, 3.0, 5.0, 1.7}, {6.0, 2.8999999999999999, 4.5, 1.5}, {5.7000000000000002, 2.6000000000000001, 3.5, 1.0}, {5.5, 2.3999999999999999, 3.7999999999999998, 1.1000000000000001}, {5.5, 2.3999999999999999, 3.7000000000000002, 1.0}, {5.7999999999999998, 2.7000000000000002, 3.8999999999999999, 1.2}, {6.0, 2.7000000000000002, 5.0999999999999996, 1.6000000000000001}, {5.4000000000000004, 3.0, 4.5, 1.5}, {6.0, 3.3999999999999999, 4.5, 1.6000000000000001}, {6.7000000000000002, 3.1000000000000001, 4.7000000000000002, 1.5}, {6.2999999999999998, 2.2999999999999998, 4.4000000000000004, 1.3}, {5.5999999999999996, 3.0, 4.0999999999999996, 1.3}, {5.5, 2.5, 4.0, 1.3}, {5.5, 2.6000000000000001, 4.4000000000000004, 1.2}, {6.0999999999999996, 3.0, 4.5999999999999996, 1.3999999999999999}, {5.7999999999999998, 2.6000000000000001, 4.0, 1.2}, {5.0, 2.2999999999999998, 3.2999999999999998, 1.0}, {5.5999999999999996, 2.7000000000000002, 4.2000000000000002, 1.3}, {5.7000000000000002, 3.0, 4.2000000000000002, 1.2}, {5.7000000000000002, 2.8999999999999999, 4.2000000000000002, 1.3}, {6.2000000000000002, 2.8999999999999999, 4.2999999999999998, 1.3}, {5.0999999999999996, 2.5, 3.0, 1.1000000000000001}, {5.7000000000000002, 2.7999999999999998, 4.0999999999999996, 1.3}, {5.7999999999999998, 2.7000000000000002, 5.0999999999999996, 1.8999999999999999}, {6.2999999999999998, 2.8999999999999999, 5.5999999999999996, 1.8}, {4.9000000000000004, 2.5, 4.5, 1.7}, {6.5, 3.2000000000000002, 5.0999999999999996, 2.0}, {6.4000000000000004, 2.7000000000000002, 5.2999999999999998, 1.8999999999999999}, {5.7000000000000002, 2.5, 5.0, 2.0}, {5.7999999999999998, 2.7999999999999998, 5.0999999999999996, 2.3999999999999999}, {6.4000000000000004, 3.2000000000000002, 5.2999999999999998, 2.2999999999999998}, {6.5, 3.0, 5.5, 1.8}, {6.0, 2.2000000000000002, 5.0, 1.5}, {5.5999999999999996, 2.7999999999999998, 4.9000000000000004, 2.0}, {6.2999999999999998, 2.7000000000000002, 4.9000000000000004, 1.8}, {6.2000000000000002, 2.7999999999999998, 4.7999999999999998, 1.8}, {6.0999999999999996, 3.0, 4.9000000000000004, 1.8}, {7.2000000000000002, 3.0, 5.7999999999999998, 1.6000000000000001}, {6.2999999999999998, 2.7999999999999998, 5.0999999999999996, 1.5}, {6.0999999999999996, 2.6000000000000001, 5.5999999999999996, 1.3999999999999999}, {6.4000000000000004, 3.1000000000000001, 5.5, 1.8}, {6.0, 3.0, 4.7999999999999998, 1.8}, {6.9000000000000004, 3.1000000000000001, 5.4000000000000004, 2.1000000000000001}, {6.9000000000000004, 3.1000000000000001, 5.0999999999999996, 2.2999999999999998}, {5.7999999999999998, 2.7000000000000002, 5.0999999999999996, 1.8999999999999999}, {6.7000000000000002, 3.0, 5.2000000000000002, 2.2999999999999998}, {6.2999999999999998, 2.5, 5.0, 1.8999999999999999}, {6.5, 3.0, 5.2000000000000002, 2.0}, {6.2000000000000002, 3.3999999999999999, 5.4000000000000004, 2.2999999999999998}, {5.9000000000000004, 3.0, 5.0999999999999996, 1.8}};
            double[][] coefficients = {{4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 0.0, 4.6863813658892557, 0.0, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 4.6863813658892557, 0.0, 0.0, -0.0, -0.0, -0.0, -4.6863813658892557, -0.0, -0.0, -0.0, -4.6863813658892557, -0.0, -4.6863813658892557, -4.6863813658892557, -4.6863813658892557, -4.6863813658892557, -0.0, -4.6863813658892557, -0.0, -0.0, -4.6863813658892557, -0.0, -4.6863813658892557, -0.0, -4.6863813658892557, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -4.6863813658892557, -4.6863813658892557, -4.6863813658892557, -4.6863813658892557, -0.0, -0.0, -0.0, -0.0, -0.0, -4.6863813658892557, -4.6863813658892557, -4.6863813658892557, -0.0, -4.6863813658892557, -4.6863813658892557, -4.6863813658892557, -4.6863813658892557, -4.6863813658892557, -4.6863813658892557, -4.6863813658892557, -4.6863813658892557, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -0.0, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -0.0, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948, -2.1272220789292948}, {0.0, 0.0, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 2.1272220789292948, 0.0, 2.1272220789292948, 2.1272220789292948, 0.0, 2.1272220789292948, 2.1272220789292948, 47.529341773693893, 47.529341773693893, 47.529341773693893, 0.0, 47.529341773693893, 47.529341773693893, 47.529341773693893, 0.0, 47.529341773693893, 0.0, 0.0, 0.0, 0.0, 47.529341773693893, 0.0, 47.529341773693893, 47.529341773693893, 0.0, 47.529341773693893, 0.0, 47.529341773693893, 0.0, 47.529341773693893, 47.529341773693893, 47.529341773693893, 47.529341773693893, 47.529341773693893, 47.529341773693893, 0.0, 0.0, 0.0, 0.0, 47.529341773693893, 47.529341773693893, 47.529341773693893, 47.529341773693893, 47.529341773693893, 0.0, 0.0, 47.529341773693893, 47.529341773693893, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -0.0, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -47.529341773693893, -0.0, -47.529341773693893}};
            double[] intercepts = {0.10061840191760112, 0.051748160156319709, -0.084181689668018464};
            int[] weights = {29, 49, 27};

            // Prediction:
            NuSVC clf = new NuSVC(3, 3, vectors, coefficients, intercepts, weights, "rbf", 0.001, 0.0, 3);
            int estimation = clf.predict(features);
            System.out.println(estimation);

        }
    }
}
"""