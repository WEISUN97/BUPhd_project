import subprocess

command = [
    'java', 
    '-jar', 
    './CNSTNanolithographyToolboxV2016.10.01.jar', 
    'cnstscripting', 
    'result/bend_waveguide.cnst', 
    'Xiangyu2Wei/CNSTPython/result/bend_waveguide222222.gds'
]

result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
