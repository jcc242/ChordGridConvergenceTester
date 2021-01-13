from computeConvergance import *

def findFloatsInString(string):
    f = []
    for t in string.split():
        try:
            f.append(float(t))
        except ValueError:
            pass
    return f
                
def extractErrors_ChordExact(filename):
    with open(filename) as file:
        errorsReported=False
        componentNames = []
        errorNames = []
        errors = []
        for line in file:
            if "-> Error norms at time" in line:
                print("Found start of solution error at time " +
                      str(findFloatsInString(line)[0]) +
                      " from " + filename)
                errorsReported=True
            if "Component" in line and errorsReported:
                componentNames.append(line.split()[-1])
                errors.append([])
            if "(error)" in line and errorsReported:
                errorName = line.split()[0]
                compNum = len(componentNames)-1
                if errorName in errorNames:
                    errors[compNum].insert(errorNames.index(errorName),
                                           findFloatsInString(line)[0])
                else:
                    errorNames.append(errorName)
                    errors[compNum].append(findFloatsInString(line)[0])
        return [errors, componentNames, errorNames]

def convergenceFromChordOutput(files, gridSize, dim, output):
    errors=[]
    componentNames=''
    errorNames=''
    for f in files:
        [er, cn, en] = extractErrors_ChordExact(f)
        errors.append(er)
        if componentNames == '':
            componentNames = cn
            errorNames = en
        assert componentNames == cn
        assert errorNames == en
    output(errors, gridSize, dim, componentNames, errorNames)

files = ['error32.out', 'error64.out', 'error128.out', 'error256.out',
         'error512.out', 'error1024.out', 'error2048.out', 'error4096.out']
dim = 2
gridSize = [32**dim, 64**dim, 128**dim, 256**dim, 512**dim, 1024**dim, 2048**dim, 4096**dim]

# output type needs to be one of:
#   1. convergeReport
#         Write the convergence rate report to standard output
#   2. convergeReportFiles
#         Write the convergence rate report to files named
#         '<component-name>.dat'
#   3. convergeReportLatexTables
#         Write the convergence rate report in LaTeX format to
#         files named '<component-name>_latex.dat'
output_type = convergeReport
convergenceFromChordOutput(files, gridSize, dim, output_type)
