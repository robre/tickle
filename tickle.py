#!/usr/bin/python3
import curses
import os
import sys
import subprocess
import shlex

# define commands here.
# The current line will repleace the {} placeholder:
commands = {
    'b': {
        'description': 'Open Current Line in Burp',
        'command': 'curl -k -x "http://127.0.0.1:8080" "{}"'
    },
    'g': {
        'description': 'Google current line',
        'command': 'open -g "https://www.google.com/search?q={}"'
    },
    'o': {
        'description': 'Open Current Line in Browser',
        'command': 'open -g "{}"'
    },
}


def main(stdscr):
    curses.curs_set(0)
    mystdin = open(mystdin_fd, 'r')
    data = [line for line in mystdin]
    mystdin.close()
    selected = 0  # currently selected line

    maxh, maxw = stdscr.getmaxyx()
    startline = 0
    endline = maxh-2
    
    while True:
        stdscr.clear()
        #stdscr.addstr(f"SEL: {selected}")
        for i,line in enumerate(data):
            if i < startline:
                continue
            if i > endline:
                break
            if i == selected:
                stdscr.addstr(line, curses.A_REVERSE)
            else:
                stdscr.addstr(line)
                #stdscr.chgat(selected,0,-1,curses.A_REVERSE)
        # Status Line:
        stdscr.addstr(maxh-1,0,f"[{selected}] start:{startline} end:{endline} maxh:{maxh}q:Exit j:up k:down b:send2Burp o:openInBrowser h:help")
        stdscr.refresh()
        key = stdscr.getkey()
        if key == 'q':
            curses.curs_set(1)
            sys.exit()
        elif key == 'j' or key == curses.KEY_DOWN:
            selected = min(selected+1,len(data))
            if selected > endline:
                endline += 1
                startline += 1
        elif key == 'k' or key == curses.KEY_UP:
            selected = max(selected-1,0)
            if selected < startline:
                startline -= 1
                endline -= 1
        elif key == 'h':
            print_help(stdscr)
        elif key in commands.keys():
            #stdscr.clear()
            #stdscr.addstr("running command:\n")
            cmd = shlex.split(commands[key]['command'].format(data[selected].strip()).strip())
            stdscr.addstr(' '.join(cmd))
            subprocess.run(cmd)
            #stdscr.refresh()
            #stdscr.getkey()

def print_help(stdscr):
    stdscr.clear()
    stdscr.addstr("Tickle HELP\n")
    stdscr.addstr("h: Show this help\n")
    stdscr.addstr("q: Quit\n")
    stdscr.addstr("j: Down\n")
    stdscr.addstr("k: Up\n")
    stdscr.addstr("o: Open current Line in Browser\n")
    stdscr.addstr("g: google current line in Browser\n")
    stdscr.addstr("b: open current line in Burp\n")
    stdscr.refresh()
    stdscr.getkey()

mystdin_fd = os.dup(0) # dup stdin
termin = open("/dev/tty")
os.dup2(termin.fileno(),0)
curses.wrapper(main)
