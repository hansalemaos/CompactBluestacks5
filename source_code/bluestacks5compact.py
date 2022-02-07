# -*- coding: iso-8859-1 -*-
import sys
from farbprinter.farbprinter import Farbprinter
import re
from winregistry import WinRegistry
from winreg import REG_DWORD
from maximize_console import maximize_console
import os


class BlueStacksCompact:
    def __init__(self, name):
        self.drucker = Farbprinter()
        BlueStacksCompact.close_bluestacks()
        self.introduction(name)
        self.logo_auswahl = [
            self.drucker.f.brightred.black.bold,
            self.drucker.f.black.brightred.bold,
            self.drucker.f.yellow.black.bold,
            self.drucker.f.brightyellow.black.bold,
        ]
        self.REGEDITPATH = r"HKEY_CURRENT_USER\Console"
        self.regedit_success = "I think, it has worked out! Let's start"
        self.virtualterminalregedit = "VirtualTerminalLevel"
        self.able_to_see_col_text = "Everything is configured right! You should be able to see colored text! Please restart the app if you can't see colored text"
        self.regedit_is_zero = "HKEY_CURRENT_USER\Console\VirtualTerminalLevel is set to 0! I will try to change it to 1 so that you can read colored text!"
        self.regeditfail = """I was unable to change the Registry!\n Let\'s try it anyway!\n If you can\'t read the text in the terminal, add this to your Windows Registry:\n\n[HKEY_CURRENT_USER\Console]\n
        "VirtualTerminalLevel"=dword:00000001"""
        self.try_to_create_key = "HKEY_CURRENT_USER\Console\VirtualTerminalLevel not found! I will try to create it so that you can see colored text"
        self.bluestackspath = BlueStacksCompact.get_bluestacks_engine_path()
        self.allbluestacksinstances = self.get_all_nougat_folders()
        self.drucker.p_pandas_list_dict(self.allbluestacksinstances)
        userinput = ''
        while userinput !='ok':
            try:
                userinput = input(
                    self.drucker.f.black.brightyellow.normal(
                        "\nThose are all Bluestacks instances that I have found!\nMake a backup now, come back, write \"OK\"  and press RETURN to compact them!\n"
                    )
                )
                userinput = str(userinput).lower().strip().strip('''"\'''')
            except Exception as Fehler:
                print(Fehler)
        self.dict_to_compact = {
            k + "\\Data.vdi": k + "\\Data1.vdi" for k in self.allbluestacksinstances
        }

    @staticmethod
    def close_bluestacks():
        bluestacksplayer = "taskkill /f /im HD-Player.exe"
        bluestacksmanager = "taskkill /f /im HD-MultiInstanceManager.exe"
        try:
            os.system(bluestacksplayer)
        except:
            pass
        try:
            os.system(bluestacksmanager)
        except:
            pass

    def introduction(self, name):
        colorfunctionslogo = [
            self.drucker.f.black.red.normal,
            self.drucker.f.black.brightyellow.normal,
        ]
        self.drucker.p_ascii_front_on_flag_with_border(
            text=name,
            colorfunctions=colorfunctionslogo,
            bordercolorfunction=self.drucker.f.brightgreen.black.italic,
            font="slant",
            width=1000,
            offset_from_left_side=5,
            offset_from_text=15,
        )
        colorfunctionspage = [
            self.drucker.f.black.brightwhite.normal,
            self.drucker.f.black.brightgreen.normal,
        ]
        self.drucker.p_ascii_front_on_flag_with_border(
            text="www . queroestudaralemao . com . br",
            colorfunctions=colorfunctionspage,
            bordercolorfunction=self.drucker.f.brightgreen.black.negative,
            font="slant",
            width=1000,
            offset_from_left_side=1,
            offset_from_text=1,
        )

    def compact_bluestacks(self):
        def get_file_path(datei):
            pfad = sys.path
            pfad = [x.replace("/", "\\") + "\\" + datei for x in pfad]
            exists = []
            for p in pfad:
                if os.path.exists(p):
                    exists.append(p)
            return list(dict.fromkeys(exists))

        clonevdipath = get_file_path("CloneVDI.exe")[0]
        instancenumber = 1
        for bluestacks_old, bluestacks_new in self.dict_to_compact.items():
            try:
                execute_command = (
                    fr'''{clonevdipath} "{bluestacks_old}" -kc -o "{bluestacks_new}"'''
                )
                print(
                    self.drucker.f.black.brightmagenta.normal(
                        f"\nInstance: {instancenumber}\n"
                    ),
                    end="",
                )
                print(
                    self.drucker.f.black.brightblue.normal(
                        f"\nExecuting command: {execute_command}\n"
                    ),
                    end="",
                )
                os.system(execute_command)
                print(
                    self.drucker.f.black.brightgreen.normal(
                        f"\nDeleting {bluestacks_old}\n"
                    ),
                    end="",
                )
                os.remove(bluestacks_old)
                print(
                    self.drucker.f.black.brightyellow.normal(
                        f"\nRenaming {bluestacks_new}\n"
                    ),
                    end="",
                )
                os.rename(bluestacks_new, bluestacks_old)
                instancenumber = instancenumber + 1
            except Exception as Fehler:
                _ = input(
                    self.drucker.f.black.brightred.normal(
                        f"\nError! {Fehler}\nPress any key to continue\n"
                    )
                )

        _ = input(
            self.drucker.f.black.brightgreen.normal(
                "\nWork done! Press any key to exit\n"
            )
        )
        sys.exit()

    def get_all_nougat_folders(self):
        listOfFile = os.listdir(self.bluestackspath)
        allFiles = list()
        for entry in listOfFile:
            fullPath = os.path.join(self.bluestackspath, entry)
            allFiles.append(fullPath)
        allFiles = [x for x in allFiles if any(re.findall(r"Nougat\d\d_\d+", x))]
        return allFiles

    @staticmethod
    def get_bluestacks_engine_path():
        bluestackspath = "HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt"
        with WinRegistry() as client:
            regedit_entry = client.read_entry(bluestackspath, "DataDir")
        return regedit_entry.value.strip("\\")

    def add_color_print_to_regedit(self):
        try:
            with WinRegistry() as client:
                try:

                    regedit_entry = client.read_entry(
                        self.REGEDITPATH, self.virtualterminalregedit
                    )
                    if int(regedit_entry.value) == 1:
                        print(
                            self.drucker.f.black.green.negative(
                                self.able_to_see_col_text
                            )
                        )
                        return True
                    if int(regedit_entry.value) == 0:
                        print(
                            self.drucker.f.black.brightyellow.negative(
                                self.regedit_is_zero
                            )
                        )
                        try:
                            client.write_entry(
                                self.REGEDITPATH,
                                self.virtualterminalregedit,
                                value=1,
                                reg_type=REG_DWORD,
                            )
                            print(
                                self.drucker.f.black.green.negative(
                                    self.regedit_success
                                )
                            )
                        except:
                            print(
                                self.drucker.f.black.brightred.negative(
                                    self.regeditfail
                                )
                            )
                            return False
                except:
                    print(
                        self.drucker.f.black.brightyellow.negative(
                            self.try_to_create_key
                        )
                    )
                    try:
                        client.write_entry(
                            self.REGEDITPATH,
                            "VirtualTerminalLevel",
                            value=1,
                            reg_type=REG_DWORD,
                        )
                        print(self.drucker.f.black.green.negative(self.regedit_success))

                        return True
                    except:
                        print(self.drucker.f.black.brightred.negative(self.regeditfail))
                        return False
        except:
            print(
                self.drucker.f.black.brightred.negative(
                    "Error checking if VirtualTerminalLevel is set to 1"
                )
            )


if __name__ =='__main__':
    maximize_console()
    bs = BlueStacksCompact('CompactBluestacks5')
    bs.compact_bluestacks()
