import sys;
from os import listdir;
from os import listdir;
from os.path import isfile;
from os.path import isdir;
from os.path import dirname;
from os.path import islink;

USEAGE = """USEAGE : command PASE_PATH
"""

class DependPackageDetector:
        startPath = "";
        dependInfo = dict();

        def getDependPackages(self, file):
                file.seek(0,0)

                line = file.readline()
                while not line.startswith("import") and not line == "":
                        line = file.readline()

                packages = set();
                while line.startswith("import") and not line == "":
                        if line == "\n":
                                line = file.readline()
                                continue;
                        #print line;
                        packages.add(line.split()[-1].rpartition(".")[0]);
                        line = file.readline()

                #print "packages : %s" % packages
                return packages;

        def getFilePackage(self, file):
                file.seek(0,0)
                line = file.readline()
                while not line.startswith("package") and not line == "":
                        line = file.readline()
                package = line.split()[-1][:-1]
                #print "package : %s" % package
                return package;

        def analyzeFile(self, filePath):
                print filePath
                if filePath.endswith(".java"):
                        # open file
                        file = open(filePath, "r", -1)
                        if file:
                                # get this file package
                                package = self.getFilePackage(file)

                                # get depend package
                                dependPackages = self.getDependPackages(file)

                                # add depend package to depInfo
                                if package in self.dependInfo:
                                        self.dependInfo[package] = self.dependInfo[package] | (dependPackages)
                                else:
                                        self.dependInfo[package] = dependPackages
                                return True
                        else:
                                return False
                        file.close()
                else:
                        return False;

        def setStartPath(self, dir):
                if isdir(dir):
                        self.startPath = dir
                        return True
                else:
                        return False

        def startSearch(self):
                self.search(self.startPath)
                print self.dependInfo

        def search(self, dir):
                for file in listdir(dir):
                        filePath = dir + "/" + file
                        if isfile(filePath):
                                #print "%s is file." % filePath
                                self.analyzeFile(filePath)
                        elif isdir(filePath) and not islink(filePath):
                                #print "%s is dir, search in this directory." % filePath
                                self.search(filePath)

def main():
        args = sys.argv
        if len(args) != 2:
                print USEAGE
                quit()
        else:
                detector = DependPackageDetector()
                if detector.setStartPath(args[1]):
                        detector.startSearch()
                else:
                        print USEAGE
                        quit()


if __name__ == "__main__":
        main()

