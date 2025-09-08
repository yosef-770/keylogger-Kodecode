import os

def print_welcome():
    # clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""\033[32m
▗▖ ▗▖▗▄▄▄▖▗▖  ▗▖▗▖    ▗▄▖  ▗▄▄▖ ▗▄▄▖▗▄▄▄▖▗▄▄▖ 
▐▌▗▞▘▐▌    ▝▚▞▘ ▐▌   ▐▌ ▐▌▐▌   ▐▌   ▐▌   ▐▌ ▐▌
▐▛▚▖ ▐▛▀▀▘  ▐▌  ▐▌   ▐▌ ▐▌▐▌▝▜▌▐▌▝▜▌▐▛▀▀▘▐▛▀▚▖
▐▌ ▐▌▐▙▄▄▖  ▐▌  ▐▙▄▄▖▝▚▄▞▘▝▚▄▞▘▝▚▄▞▘▐▙▄▄▖▐▌ ▐▌

           © 2025 - KodCode Cohort D
Yosef Avitan ＆ Elazar Kowler ＆ Yeuda Borodyanski
                                              
    \033[0m""")