import pytest

retcode = pytest.main()

print(retcode)
print(type(retcode))

from colorama import init
import colorama
from colorama import Fore, Back, Style

init()


print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')



from termcolor import colored
 
init()
 
print(colored('Hello, World!', 'green', 'on_red'))

from art import *
art_1=art("coffee") # return art as str in normal mode
print(art_1)

art_2=art("woman",number=2) # return multiple art as str
print(art_2)
art("random") # random 1-line art mode
art("rand")   # random 1-line art mode


Art=text2art("Code Analysis") # Return ASCII text (default font) and default chr_ignore=True 
print(Art)

from rich.console import Console
from rich.table import Table

table = Table(title="Star Wars Movies")

table.add_column("Released", justify="right", style="cyan", no_wrap=True)
table.add_column("Title", style="magenta")
table.add_column("Box Office", justify="right", style="green")

table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

console = Console()
console.print(table)

from rich.tree import Tree
from rich import print

tree = Tree("Rich Tree")
print(tree)
tree.add("foo")
tree.add("bar")
print(tree)

baz_tree = tree.add("baz")
baz_tree.add("[red]Red").add("[green]Green").add("[blue]Blue")
print(tree)

print(str(tree))

from rich import print
print(r"foo\[bar]")

console.rule(title="[bold red]Chapter 2", characters='=')
