import sys
sys.path.append("..")
from installcobra.installers import ScriptInstaller

class TestProgram(ScriptInstaller):
    def prerequisite(self):
        print("PREREQ")

    def preinstall(self):
        print("PREINST")

    def install(self):
        print("INSTALL")

    def postinstall(self):
        print("POSTINST")


if __name__ == '__main__':
    TestProgram("testprogram", "1_0").run()
