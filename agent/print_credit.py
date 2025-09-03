import os

def print_welcome():
    # clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
▗▖ ▗▖▗▄▄▄▖▗▖  ▗▖▗▖    ▗▄▖  ▗▄▄▖ ▗▄▄▖▗▄▄▄▖▗▄▄▖ 
▐▌▗▞▘▐▌    ▝▚▞▘ ▐▌   ▐▌ ▐▌▐▌   ▐▌   ▐▌   ▐▌ ▐▌
▐▛▚▖ ▐▛▀▀▘  ▐▌  ▐▌   ▐▌ ▐▌▐▌▝▜▌▐▌▝▜▌▐▛▀▀▘▐▛▀▚▖
▐▌ ▐▌▐▙▄▄▖  ▐▌  ▐▙▄▄▖▝▚▄▞▘▝▚▄▞▘▝▚▄▞▘▐▙▄▄▖▐▌ ▐▌
                                              
    """)