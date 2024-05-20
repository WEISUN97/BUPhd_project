from io import StringIO
import os
import platform
import subprocess
import xml.etree.ElementTree as ET
import re
from geo import Geo
from typing import Union
import time

CNST_PATH = r"."


class CNSTGenerator:
    def __init__(self, gdsReso: float = 0.001, shapeReso: float = 0.01) -> None:
        self.string_io = StringIO()
        self.gdsReso = gdsReso
        self.shapeReso = shapeReso
        self.string_io.write(f"{gdsReso} gdsReso\n")
        self.string_io.write(f"{shapeReso} shapeReso\n")
        self.save_dir = self.init_config()
        self.jar_path = os.path.join(
            CNST_PATH, "CNSTNanolithographyToolboxV2016.10.01.jar"
        )

    def init_config(self) -> None:
        tree = ET.parse(os.path.join(CNST_PATH, "CNSTdefaultValues.xml"))
        root = tree.getroot()
        for elem in root.iter("SaveToDirectory"):
            return elem.text

    def generate(self, filename: str, save_path: str, show=False) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.string_io.getvalue())
        self.string_io.close()

        if not self.save_dir.endswith("\\"):
            path = "\\" + os.path.relpath(save_path, self.save_dir)
        if self._is_mac_os():
            path = os.path.relpath(save_path, self.save_dir)

        java_command = [
            "java",
            "-jar",
            os.path.join(CNST_PATH, "CNSTNanolithographyToolboxV2016.10.01.jar"),
            "cnstscripting",
            filename,
            path,
        ]
        start_time = time.time()
        if self._is_mac_os():
            result = subprocess.run(java_command, capture_output=True, text=True)
        else:
            result = subprocess.run(
                java_command,
                shell=True,
                capture_output=True,
                text=True,
                encoding="ISO-8859-1",
            )
        end_time = time.time()

        print("Runtime:", end_time - start_time, "seconds")
        print(result.stdout)
        if show and result.returncode == 0:
            if self._is_mac_os:
                # save_path = result.stdout.split(".gds")[0][11:] + ".gds"
                save_path = result.stdout[
                    result.stdout.find("/") : result.stdout.find(".gds") + 4
                ]
                print(save_path)
                os.system("open " + save_path)
            else:
                os.system(save_path)

    def add(self, item: Union[str, Geo]) -> None:
        if isinstance(item, Geo):
            self.string_io.write(f"{item.__str__()}\n")
        else:
            self.string_io.write(f"{item}\n")

    def read_cnst(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as f:
            self.string_io.write(f.read())

    @staticmethod
    def _is_mac_os():
        return platform.system() == "Darwin"
