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
    TestProgram(__file__, "testprogram", "1_0", copy_source_files=True).run()
